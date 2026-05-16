#!/usr/bin/env python3
"""Summarize a Flatpak manifest and flag common review items.

This is a lightweight triage helper. It intentionally avoids external
dependencies and does not replace flatpak-builder-lint.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


TOP_LEVEL_KEYS = [
    "id",
    "app-id",
    "runtime",
    "runtime-version",
    "sdk",
    "command",
    "branch",
    "base",
    "base-version",
]

REQUIRED_APP_KEYS = ["runtime", "runtime-version", "sdk", "command"]

BROAD_PERMISSION_PATTERNS = [
    (re.compile(r"--filesystem=(host|home|host-root|host-os|host-etc)(:|$)"), "broad filesystem access"),
    (re.compile(r"--filesystem=(xdg-[^:]+|~/[^:]+|/[^:]+)$"), "writeable filesystem access; consider :ro or portals"),
    (re.compile(r"--device=(all|kvm|input|usb)(:|$)"), "sensitive device access"),
    (re.compile(r"--socket=(session-bus|system-bus|ssh-auth|gpg-agent|pcsc|inherit-wayland-socket)(:|$)"), "sensitive socket access"),
    (re.compile(r"--(system-)?talk-name=.*\*"), "broad D-Bus talk permission"),
    (re.compile(r"--(system-)?own-name=.*\*"), "broad D-Bus ownership permission"),
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", help="Flatpak manifest path, or '-' for stdin")
    parser.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    return parser.parse_args()


def read_manifest(path_arg: str) -> tuple[str, str]:
    if path_arg == "-":
        return "<stdin>", sys.stdin.read()
    path = Path(path_arg)
    return str(path), path.read_text(encoding="utf-8")


def load_json_if_possible(path: str, text: str) -> dict[str, Any] | None:
    if not path.endswith(".json") and not text.lstrip().startswith("{"):
        return None
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        return None
    return data if isinstance(data, dict) else None


def strip_quotes(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        return value[1:-1]
    return value


def top_level_scalar(text: str, key: str) -> str | None:
    pattern = re.compile(rf"^(?:{re.escape(key)}):\s*(.+?)\s*$", re.MULTILINE)
    match = pattern.search(text)
    if not match:
        return None
    value = match.group(1).split(" #", 1)[0].strip()
    if value in {"", "|", ">"}:
        return None
    return strip_quotes(value)


def yaml_block_items(text: str, key: str) -> list[str]:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        match = re.match(rf"^(\s*){re.escape(key)}:\s*$", line)
        if not match:
            continue
        base_indent = len(match.group(1))
        items: list[str] = []
        for child in lines[index + 1 :]:
            if not child.strip() or child.lstrip().startswith("#"):
                continue
            indent = len(child) - len(child.lstrip(" "))
            if indent <= base_indent:
                break
            item = re.match(r"^\s*-\s*(.+?)\s*$", child)
            if item:
                items.append(strip_quotes(item.group(1).split(" #", 1)[0]))
        return items
    return []


def collect_values(data: dict[str, Any] | None, text: str) -> dict[str, Any]:
    if data is not None:
        values: dict[str, Any] = {key: data.get(key) for key in TOP_LEVEL_KEYS if data.get(key) is not None}
        values["finish-args"] = data.get("finish-args", []) if isinstance(data.get("finish-args", []), list) else []
        values["sdk-extensions"] = data.get("sdk-extensions", []) if isinstance(data.get("sdk-extensions", []), list) else []
        modules = data.get("modules", [])
        values["modules"] = modules if isinstance(modules, list) else []
        return values

    values = {key: top_level_scalar(text, key) for key in TOP_LEVEL_KEYS}
    values = {key: value for key, value in values.items() if value is not None}
    values["finish-args"] = yaml_block_items(text, "finish-args")
    values["sdk-extensions"] = yaml_block_items(text, "sdk-extensions")
    values["modules"] = re.findall(r"^\s*-\s*(?:name:\s*)?([A-Za-z0-9_.+/@-]+)\s*$", text, re.MULTILINE)
    return values


def module_names(values: dict[str, Any], text: str) -> list[str]:
    modules = values.get("modules", [])
    names: list[str] = []
    if isinstance(modules, list) and modules and isinstance(modules[0], dict):
        for module in modules:
            name = module.get("name")
            if isinstance(name, str):
                names.append(name)
        return names
    names.extend(re.findall(r"^\s*-\s*name:\s*([A-Za-z0-9_.+/@-]+)\s*$", text, re.MULTILINE))
    names.extend(re.findall(r'^\s*-\s*"([^"]+\.(?:json|yml|yaml))"\s*$', text, re.MULTILINE))
    names.extend(re.findall(r"^\s*-\s*'([^']+\.(?:json|yml|yaml))'\s*$", text, re.MULTILINE))
    return sorted(set(names))


def source_types(data: dict[str, Any] | None, text: str) -> list[str]:
    types: list[str] = []

    def walk(value: Any) -> None:
        if isinstance(value, dict):
            if isinstance(value.get("type"), str):
                types.append(value["type"])
            for child in value.values():
                walk(child)
        elif isinstance(value, list):
            for child in value:
                walk(child)

    if data is not None:
        walk(data.get("modules", []))
    else:
        types.extend(re.findall(r"^\s*(?:-\s*)?type:\s*([A-Za-z0-9_.+/@-]+)\s*$", text, re.MULTILINE))
    return sorted(set(types))


def source_pin_warnings(data: dict[str, Any] | None, text: str) -> list[str]:
    warnings: list[str] = []
    if data is None:
        if re.search(r"^\s*url:\s*https?://", text, re.MULTILINE) and not re.search(r"^\s*sha(256|512):", text, re.MULTILINE):
            warnings.append("URLs found but no sha256/sha512 lines were detected; archive/file sources usually need checksums.")
        git_blocks = [m.start() for m in re.finditer(r"^\s*(?:-\s*)?type:\s*git\s*$", text, re.MULTILINE)]
        if git_blocks and not re.search(r"^\s*commit:\s*", text, re.MULTILINE):
            warnings.append("git source detected without a commit line; pin commits for reproducibility.")
        return warnings

    def walk_sources(value: Any) -> None:
        if isinstance(value, dict):
            source_type = value.get("type")
            if source_type in {"archive", "file"} and value.get("url") and not (value.get("sha256") or value.get("sha512")):
                warnings.append(f"{source_type} source with url lacks sha256/sha512.")
            if source_type == "git" and not value.get("commit"):
                warnings.append("git source lacks commit.")
            for child in value.values():
                walk_sources(child)
        elif isinstance(value, list):
            for child in value:
                walk_sources(child)

    walk_sources(data.get("modules", []))
    return sorted(set(warnings))


def app_id_warnings(app_id: str | None) -> list[str]:
    if not app_id:
        return ["missing id/app-id"]
    warnings: list[str] = []
    parts = app_id.split(".")
    if len(app_id) > 255:
        warnings.append("app ID exceeds 255 characters")
    if len(parts) < 3:
        warnings.append("app ID has fewer than 3 components")
    if len(parts) > 5:
        warnings.append("app ID has more than 5 components; Flathub applications should avoid this")
    if app_id.endswith((".desktop", ".app", ".linux")):
        warnings.append("app ID ends with a generic suffix")
    for index, part in enumerate(parts):
        allowed = r"^[A-Za-z0-9_]+$" if index < len(parts) - 1 else r"^[A-Za-z0-9_-]+$"
        if not re.match(allowed, part):
            warnings.append(f"app ID component has disallowed characters: {part}")
        if index < len(parts) - 1 and part.lower() != part:
            warnings.append("domain portion should be lowercase")
        if part and part[0].isdigit():
            warnings.append(f"component starts with a digit and should be prefixed with underscore: {part}")
    hosting_prefixes = {
        "github": "io.github.",
        "gitlab": "io.gitlab.",
        "codeberg": "page.codeberg.",
        "framagit": "io.frama.",
    }
    for host, prefix in hosting_prefixes.items():
        if host in app_id and not app_id.startswith(prefix):
            warnings.append(f"code-hosting ID for {host} should use prefix {prefix}")
    if app_id.startswith(("io.github.", "io.gitlab.", "page.codeberg.", "io.frama.")) and len(parts) < 4:
        warnings.append("code-hosting IDs need at least 4 components")
    return sorted(set(warnings))


def permission_warnings(finish_args: list[str]) -> list[str]:
    warnings: list[str] = []
    for arg in finish_args:
        for pattern, message in BROAD_PERMISSION_PATTERNS:
            if pattern.search(arg):
                warnings.append(f"{arg}: {message}")
    return warnings


def build_report(path: str, text: str) -> dict[str, Any]:
    data = load_json_if_possible(path, text)
    values = collect_values(data, text)
    app_id = values.get("id") or values.get("app-id")
    finish_args = values.get("finish-args") if isinstance(values.get("finish-args"), list) else []

    warnings: list[str] = []
    missing = [key for key in REQUIRED_APP_KEYS if not values.get(key)]
    if not app_id:
        warnings.append("missing id/app-id")
    if missing:
        warnings.append("missing common application keys: " + ", ".join(missing))
    if app_id and path != "<stdin>":
        filename = Path(path).name
        expected = {f"{app_id}.json", f"{app_id}.yml", f"{app_id}.yaml"}
        if filename not in expected:
            warnings.append(f"manifest filename does not match app ID: expected one of {', '.join(sorted(expected))}")
    runtime = values.get("runtime")
    if runtime and not str(runtime).startswith(("org.freedesktop.", "org.gnome.", "org.kde.")):
        warnings.append("runtime is not one of the common Flathub-hosted runtime families; verify it is hosted on Flathub")
    if "build-args" in text and "--share=network" in text:
        warnings.append("build args request network; Flathub builds have no network access during build")
    warnings.extend(app_id_warnings(str(app_id) if app_id else None))
    warnings.extend(permission_warnings([str(arg) for arg in finish_args]))
    warnings.extend(source_pin_warnings(data, text))

    return {
        "path": path,
        "format": "json" if data is not None else "text-yaml",
        "app_id": app_id,
        "runtime": values.get("runtime"),
        "runtime_version": values.get("runtime-version"),
        "sdk": values.get("sdk"),
        "command": values.get("command"),
        "base": values.get("base"),
        "base_version": values.get("base-version"),
        "sdk_extensions": values.get("sdk-extensions", []),
        "finish_args": finish_args,
        "module_names": module_names(values, text),
        "source_types": source_types(data, text),
        "warnings": sorted(set(warnings)),
    }


def emit_text(report: dict[str, Any]) -> None:
    print(f"Manifest: {report['path']}")
    print(f"Format: {report['format']}")
    print(f"App ID: {report.get('app_id') or '(missing)'}")
    print(f"Runtime: {report.get('runtime') or '(missing)'} // {report.get('runtime_version') or '(missing)'}")
    print(f"SDK: {report.get('sdk') or '(missing)'}")
    print(f"Command: {report.get('command') or '(missing)'}")
    if report.get("base"):
        print(f"BaseApp: {report['base']} // {report.get('base_version') or '(missing)'}")
    if report.get("sdk_extensions"):
        print("SDK extensions: " + ", ".join(map(str, report["sdk_extensions"])))
    print(f"Finish args ({len(report['finish_args'])}):")
    for arg in report["finish_args"]:
        print(f"  - {arg}")
    print(f"Modules ({len(report['module_names'])}):")
    for name in report["module_names"][:40]:
        print(f"  - {name}")
    if len(report["module_names"]) > 40:
        print(f"  ... {len(report['module_names']) - 40} more")
    print("Source types: " + (", ".join(report["source_types"]) if report["source_types"] else "(none detected)"))
    print("Review warnings:")
    if report["warnings"]:
        for warning in report["warnings"]:
            print(f"  - {warning}")
    else:
        print("  - none from lightweight checks")


def main() -> int:
    args = parse_args()
    path, text = read_manifest(args.manifest)
    report = build_report(path, text)
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        emit_text(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
