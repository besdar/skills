---
name: flatpak-flathub
description: Use when Codex needs to package, build, debug, review, submit, or maintain Flatpak applications or Flathub submissions; work with flatpak-builder manifests in JSON/YAML, finish-args sandbox permissions, runtimes and SDKs, modules and sources, MetaInfo/AppStream XML, desktop files, icons, flathub.json, flatpak-builder-lint, external-data-checker, Flathub verification, or Flatpak install/update/downgrade/bisect/rebuild troubleshooting.
---

# Flatpak & Flathub

## Workflow

First classify the request:

- **Package or fix an app**: inspect the manifest, app metadata, build system, dependency strategy, and sandbox permissions. Read `references/flatpak-packaging.md`.
- **Prepare or review a Flathub submission**: check Flathub policy, app ID, source/build rules, required files, linter expectations, and submission workflow. Read `references/flathub-submission.md`.
- **Fix store metadata**: review MetaInfo/AppStream, desktop file, icon, screenshots, release notes, OARS, and quality guidance. Read `references/metainfo-appstream.md`.
- **Help a user operate Flatpak**: use install, permissions, downgrade, bisect, uninstall, source rebuild, slow connection, or debug commands. Read `references/commands-troubleshooting.md`.
- **Need the original docs**: use `references/source-doc-map.md` to locate the source Flatpak and Flathub documentation files.

For manifest review, run the helper first when a manifest path is available:

```bash
python3 /path/to/flatpak-flathub/scripts/inspect_manifest.py <manifest.yml>
```

Treat the helper as a triage tool. It does not replace `flatpak-builder`, `flatpak-builder-lint`, AppStream validation, or a real local build.

## Core Checks

When editing or reviewing a Flatpak app:

1. Confirm the manifest filename matches the application ID and uses `.json`, `.yml`, or `.yaml`.
2. Confirm `id` or `app-id`, `runtime`, `runtime-version`, `sdk`, `command`, and `modules` are present for applications.
3. Choose the runtime by app dependencies: Freedesktop for minimal/general apps, GNOME for GNOME/GTK stack, KDE for Qt/KDE stack. Verify live docs before asserting current runtime support or EOL status.
4. Keep bundled modules minimal, ordered from low-level dependencies to the main app, with the main app usually last.
5. Pin sources reproducibly: archives need checksums; git sources should include `commit`; avoid branch-only sources for Flathub review.
6. Keep static permissions minimal. Prefer XDG portals. Flag broad filesystem, device, and D-Bus grants for justification.
7. Remember Flathub builds have no network access during build. Dependency manifests for npm, cargo, pip, yarn, etc. must be generated and committed.
8. Ensure the MetaInfo file, desktop file, and icons are installed by the upstream build when possible, not copied into the Flathub submission.
9. Run the real validation commands before calling work complete.

## Validation Commands

Prefer the Flathub-provided builder when preparing Flathub submissions:

```bash
flatpak install -y flathub org.flatpak.Builder
flatpak run --command=flathub-build org.flatpak.Builder --install <manifest>
flatpak run <app-id>
flatpak run --command=flatpak-builder-lint org.flatpak.Builder manifest <manifest>
flatpak run --command=flatpak-builder-lint org.flatpak.Builder repo repo
flatpak run --command=flatpak-builder-lint org.flatpak.Builder appstream <app-id>.metainfo.xml
```

Use standard `flatpak-builder` directly for non-Flathub builds:

```bash
flatpak-builder --force-clean --user --install --install-deps-from=flathub build-dir <manifest>
```

## Live Policy

Flatpak and Flathub policies, runtime support windows, linter behavior, and submission rules change. For public submission guidance or anything that depends on the current rule, verify against the official docs before giving a final answer:

- `https://docs.flatpak.org/`
- `https://docs.flathub.org/`
