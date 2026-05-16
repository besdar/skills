# Source Documentation Map

Use this file when the summarized references are not enough and the original local docs are present. Prefer English source files and ignore `po/` translations unless the user asks about localization.

## Flatpak Docs

Local root: `flatpak-docs/docs`

- `index.rst`: documentation overview.
- `basic-concepts.rst`: runtimes, bundled libraries, sandboxes.
- `getting-started.rst`: initial setup.
- `first-build.rst`: minimal first Flatpak tutorial.
- `building-introduction.rst`: build process overview.
- `manifests.rst`: manifest structure, top-level fields, file renaming, finish-args, cleanup, modules.
- `module-sources.rst`: archive, git, file, extra-data, script, patch, shell, bzr, svn, dir, inline sources.
- `flatpak-builder.rst`: builder usage, repo export, local install, signing.
- `flatpak-builder-command-reference.rst`: full flatpak-builder option reference.
- `dependencies.rst`: runtimes, bundling, BaseApps, extensions.
- `available-runtimes.rst`: Freedesktop, GNOME, KDE, elementary runtimes and support model.
- `sandbox-permissions.rst`: finish-args, portals, D-Bus, filesystem, devices, USB portal, dconf, gvfs, external drives, conditional permissions.
- `conventions.rst`: app IDs, MetaInfo, desktop files, icons, XDG base directories.
- `desktop-integration.rst`: portals, notifications, status icons, MIME, secrets, settings, search, wallpapers, autostart.
- `portals.rst` and `portal-api-reference.rst`: portal guidance and API.
- `python.rst`, `electron.rst`, `qt.rst`, `dotnet.rst`: ecosystem-specific packaging.
- `debugging.rst`: debug extensions, shells, GDB, coredumps, Valgrind, strace, perf, D-Bus audit.
- `publishing.rst`, `repositories.rst`, `hosting-a-repository.rst`, `single-file-bundles.rst`, `usb-drives.rst`: distribution outside or alongside Flathub.
- `using-flatpak.rst`, `tips-and-tricks.rst`: CLI, install, remotes, downgrade, masking, bisect.
- `extension.rst`: extension points and extension manifests.
- `multiarch.rst`: 32-bit and multilib support.
- `under-the-hood.rst`: OSTree, refs, deployments.

Useful searches:

```bash
rg -n "finish-args|--filesystem|--socket|--device|--talk-name" flatpak-docs/docs
rg -n "runtime-version|org.freedesktop|org.gnome|org.kde|EOL|end-of-life" flatpak-docs/docs
rg -n "type: archive|type: git|extra-data|sha256|commit" flatpak-docs/docs/module-sources.rst
rg -n "flatpak-builder|--install|--repo|--run|--force-clean" flatpak-docs/docs
```

## Flathub Docs

Local root: `documentation/docs`

For users:

- `01-for-users/01-why-flathub.md`: Flatpak and Flathub overview.
- `01-for-users/02-installation.md`: Flathub setup, beta repo, subsets.
- `01-for-users/03-user-vs-system-install.md`: per-user vs system installs.
- `01-for-users/010-permissions.md`: user permission overrides.
- `01-for-users/06-verification.md`: verified apps.
- `01-for-users/07-downgrading.md`: downgrade commands.
- `01-for-users/08-bisecting.md`: regression bisect workflow.
- `01-for-users/09-uninstallation.md`: uninstall apps, data, unused dependencies, remotes.
- `01-for-users/10-rebuilding.md`: rebuild from published sources.
- `01-for-users/11-slow-connection.md`: troubleshooting slow Flathub.
- `01-for-users/12-finding-sources.md`: source discovery.

For app authors:

- `02-for-app-authors/01-why-flathub.md`: Flathub benefits and submission overview.
- `02-for-app-authors/02-requirements.md`: inclusion policy, app ID, license, permissions, source/build rules, required files, metadata.
- `02-for-app-authors/03-metainfo-guidelines/index.md`: MetaInfo requirements and examples.
- `02-for-app-authors/03-metainfo-guidelines/01-quality-guidelines.md`: store listing quality guidance.
- `02-for-app-authors/04-runtimes.md`: Flathub-hosted runtimes.
- `02-for-app-authors/05-submission.md`: new app submission flow.
- `02-for-app-authors/06-maintenance.md`: repo branches, builds, moderation, flathub.json, EOL, access.
- `02-for-app-authors/07-updates.md`: update workflow.
- `02-for-app-authors/08-shared-modules.md`: shared modules.
- `02-for-app-authors/09-github-actions.md`: GitHub Actions.
- `02-for-app-authors/10-verification.md`: app verification.
- `02-for-app-authors/11-external-data-checker.md`: automated update checker.
- `02-for-app-authors/12-linter.md`: flatpak-builder-lint and error explanations.
- `02-for-app-authors/13-useful-links.md`: external resources.

For team members:

- `03-for-team-members/01-review.md`: review checklist and special app ID rules.

Useful searches:

```bash
rg -n "Generative AI|AI policy|must not|not be accepted|Required files|No network" documentation/docs/02-for-app-authors
rg -n "Application ID|code hosting|Protected ID|rename" documentation/docs/02-for-app-authors/02-requirements.md
rg -n "metadata_license|project_license|launchable|content_rating|screenshots|releases" documentation/docs/02-for-app-authors/03-metainfo-guidelines
rg -n "flatpak-builder-lint|linter-error|appstream" documentation/docs/02-for-app-authors/12-linter.md
```
