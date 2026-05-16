# Flatpak Packaging

Use this reference for manifest authoring, `flatpak-builder`, runtimes, dependencies, sources, permissions, toolkit-specific packaging, and debugging.

## Contents

- Manifest Essentials
- Build Commands
- Runtimes and Dependencies
- Sources
- Build Systems
- Sandbox Permissions
- Toolkit and Language Notes
- Debugging

## Manifest Essentials

- The `flatpak-builder` input is a JSON or YAML manifest.
- Name the manifest after the application ID, for example `org.example.App.yml`.
- Application manifests normally start with `id`, `runtime`, `runtime-version`, `sdk`, and `command`.
- Exported files visible to the host, such as desktop files, icons, and MetaInfo, must be prefixed with the application ID.
- Prefer renaming exported files upstream. If that is not possible, use `rename-icon`, `rename-desktop-file`, or `rename-appdata-file`.
- Put sandbox permissions in `finish-args`.
- Use `cleanup` and `cleanup-commands` to remove build artifacts, headers, static libraries, docs, or helper tools that should not ship. Prefer disabling unnecessary build outputs when possible.
- The `modules` list builds in declaration order. When a module changes, it and following modules rebuild. Put the main app module last unless an independent frequently updated module should be last for cache efficiency.
- Modules can be nested or linear. Linear manifests are often easier to review; nested manifests can clarify dependency structure.

## Build Commands

For regular local builds:

```bash
flatpak-builder --force-clean --user --install --install-deps-from=flathub build-dir <manifest>
flatpak run <app-id>
```

To export to a local repository:

```bash
flatpak-builder --repo=repo build-dir <manifest>
flatpak install --user repo <app-id>
```

For Flathub-like local builds:

```bash
flatpak install -y flathub org.flatpak.Builder
flatpak run --command=flathub-build org.flatpak.Builder --install <manifest>
```

## Runtimes and Dependencies

- Every application needs a runtime and matching SDK.
- Choose the runtime by dependencies already provided there. Avoid bundling libraries that are available in the selected runtime unless a different or patched version is required.
- Keep bundled modules as low as practical; bundling increases maintenance burden.
- Main hosted runtime families:
  - `org.freedesktop.Platform` / `org.freedesktop.Sdk`: minimal/general base and base for GNOME/KDE runtimes.
  - `org.gnome.Platform` / `org.gnome.Sdk`: GNOME platform libraries and components.
  - `org.kde.Platform` / `org.kde.Sdk`: Qt and KDE Frameworks.
- Runtime support windows change. Check current runtime docs before asserting a branch is supported.
- BaseApps can avoid rebuilding large framework stacks. Electron apps commonly use an Electron BaseApp.
- Extensions mount optional content into runtimes or applications. Common suffixes are `.Debug`, `.Locale`, and `.Sources`.

Inspect runtime contents:

```bash
flatpak run --command=pkg-config <sdk-id>//<branch> --list-all
flatpak run --command=ldconfig <runtime-id>//<branch> -p
flatpak run --command=cat <runtime-id>//<branch> /usr/manifest.json
```

## Sources

- `archive` sources require `sha256` or `sha512`.
- `git` sources should include a pinned `commit`; for tags, pin the commit the tag points to. Avoid branch-only sources for reproducible builds.
- `file` sources copy a file into the source directory and are useful with `buildsystem: simple`.
- Use `dest` to place a source under a subdirectory.
- Use `only-arches` and `skip-arches` for architecture-specific sources.
- `mirror-urls`, `dest-filename`, `strip-components`, and `archive-type` are available for archive sources.
- `flatpak-builder` currently does not support git-lfs directly; workarounds require explicit build commands and suitable tooling.
- Use `extra-data` for non-redistributable sources that cannot be mirrored or redistributed.

## Build Systems

- Prefer the upstream build system: `meson`, `cmake-ninja`, `autotools`, or equivalent.
- Use `buildsystem: simple` for manual install commands, custom scripts, or dependency modules with no standard build system.
- Install into `/app`, not `/usr`. For Python/pip, use `--prefix=/app`.
- Use generator tools for dependency ecosystems rather than manually transcribing large dependency graphs:
  - `flatpak-pip-generator`
  - npm/yarn/cargo generators from `flatpak-builder-tools`

## Sandbox Permissions

By default Flatpak apps have no host file access except their app data locations, no network, no devices, no access to other processes, limited D-Bus access, and no host services like X11 or PulseAudio.

Prefer portals when a suitable portal exists. Static permissions are not dynamic; variable expansion is not available in `finish-args`.

Common permissions:

```yaml
finish-args:
  - --share=ipc
  - --socket=wayland
  - --socket=fallback-x11
  - --device=dri
  - --share=network
```

Display guidance:

- Apps with native Wayland support should usually use `--socket=wayland` and `--socket=fallback-x11`.
- Apps without native Wayland support should use `--socket=x11`.

Review broad permissions carefully:

- `--filesystem=host`, `home`, `host-os`, `host-etc`, `host-root`
- Writeable XDG directories when `:ro` or a portal would work
- `--device=all`, `kvm`, `input`, `usb`
- `--socket=session-bus`, `--socket=system-bus`
- Broad `--talk-name=*`, `--system-talk-name=*`, or unrelated D-Bus names
- `--socket=ssh-auth`, `gpg-agent`, `pcsc`, `inherit-wayland-socket`

Filesystem guidance:

- Prefer XDG directories such as `xdg-documents`, `xdg-download`, `xdg-music`, `xdg-pictures`, with `:ro` when possible.
- Use `--persist=DIR` for hardcoded home-relative directories when avoiding full home access.
- Do not try to expose reserved paths like `/app`, `/usr`, `/etc`, `/proc`, `/run/flatpak`, or `/run/host`; Flatpak ignores or restricts them.

## Toolkit and Language Notes

Python:

- Standard build systems can be used normally.
- For pip-installed modules, use `buildsystem: simple` and install with `pip3 install --prefix=/app`.
- Use `flatpak-pip-generator <package>` or `flatpak-pip-generator --requirements-file=requirements.txt` for dependency manifests.

Electron:

- Use the Freedesktop runtime unless another stack is clearly needed.
- Use the Electron BaseApp when appropriate.
- Add Node.js SDK extensions at build time, for example `org.freedesktop.Sdk.Extension.node18`, and append the matching SDK path.
- Default to X11/Xwayland unless native Wayland support is intentionally tested and justified.
- Use `--env=ELECTRON_TRASH=gio` when needed.

Qt/KDE:

- Use `org.kde.Platform` and `org.kde.Sdk` for Qt/KDE applications when the runtime provides the needed modules.
- Use Freedesktop and bundle Qt only when the KDE runtime is a poor fit and the maintenance cost is justified.

## Debugging

Install debug material:

```bash
flatpak install --include-sdk --include-debug <app-id>
flatpak info --show-runtime <app-id>
flatpak install org.freedesktop.Platform.{GL,GL32}.Debug.default//<branch>
```

Open a debug shell:

```bash
flatpak run --command=sh --devel --filesystem=$(pwd) <app-id>
flatpak-builder --run build-dir <manifest> sh
```

Use debugging tools inside the sandbox:

```bash
gdb /app/bin/<binary>
valgrind --leak-check=full --track-origins=yes --show-leak-kinds=all /app/bin/<binary>
strace -e trace=openat,read -o strace.log -f /app/bin/<binary>
coredumpctl list
flatpak-coredumpctl -m <pid> <app-id>
```

Inspect permissions and portal state:

```bash
flatpak info --show-permissions <app-id>
flatpak permission-show <app-id>
flatpak permission-reset <app-id>
flatpak run --log-session-bus <app-id>
flatpak run --log-system-bus <app-id>
```
