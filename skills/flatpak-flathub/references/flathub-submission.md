# Flathub Submission and Maintenance

Use this reference for Flathub submission policy, app IDs, required files, source/build rules, linter workflow, verification, external-data-checker, and maintenance.

## Contents

- AI Policy
- Inclusion Policy
- Application ID Rules
- Legal and Source Rules
- Build Rules
- Required Files
- Submission Workflow
- Linter
- Verification
- External Data Checker
- Maintenance

## AI Policy

Flathub documentation says submission pull requests must not be generated, opened, or automated using AI tools or agents. It also disallows low-quality AI-generated or AI-assisted code and changes where most code is written by AI without meaningful human input, review, justification, or moderation.

Do not open a Flathub submission PR as an AI agent. Help the user prepare local changes, analyze errors, and build a checklist. The human maintainer must review, own, and submit the work.

## Inclusion Policy

Flathub targets curated, high-quality, sandboxed graphical desktop applications. Submissions can be rejected or removed if they violate policy.

Flag likely-ineligible submissions:

- Non-functional apps or apps with obvious visible issues.
- Console-only software, except Flatpak/Flathub-related tooling cases.
- Minimal scripts, thin launchers, and simple web wrappers without significant functionality or desktop integration.
- Shell/window-manager/desktop-environment extensions.
- Tray-only apps.
- Host-oriented system utilities.
- Apps locked to a narrow desktop/distro/environment without justification.
- Apps that rely on host components or complicated post-install setup for core functionality.
- Development tools, terminals, file managers, and IDEs with broad scope when sandbox tradeoffs severely harm the experience, unless officially submitted and supported upstream.
- Duplicate submissions, minimal forks, conflicting third-party submissions, misleading/malicious/illegal submissions, and certain Wine/emulation submissions.
- EOL main apps, EOL runtimes/extensions/baseapps, or high-risk EOL dependencies with invasive permissions.

## Application ID Rules

An app ID is a constant reverse-DNS identifier like `{tld}.{vendor}.{product}`.

Rules:

- Maximum 255 characters.
- At least 3 dot-separated components.
- Applications should not exceed 5 components.
- Components may contain `[A-Z][a-z][0-9]_`; a dash is allowed only in the last component.
- The domain portion must be lowercase and convert dashes to underscores. Components starting with digits need a leading underscore.
- Do not end with generic terms like `.desktop`, `.app`, or `.linux`.
- The ID must exactly match the MetaInfo `<id>`.
- Code hosting IDs must use the right prefixes:
  - GitHub: `io.github.`
  - GitLab: `io.gitlab.`
  - Codeberg: `page.codeberg.`
  - Framagit: `io.frama.`
  - SourceForge may use `io.sourceforge.` or `net.sourceforge.`
- Code hosting IDs need at least 4 components and a reachable calculated repository URL.
- Protected prefixes have project-specific rules: `org.gnome.`, `org.kde.`, `com.system76.`.
- BaseApps must end with `BaseApp`.
- Extensions must prefix their ID with the extension point ID.

Choose the ID carefully. Renames require resubmission and are reviewed conservatively.

## Legal and Source Rules

- All hosted content must allow legal redistribution.
- The app MetaInfo must declare the app license correctly with SPDX identifiers or expressions.
- Non-redistributable sources must use `extra-data`.
- Names and icons must avoid trademark violations and must not imply official affiliation incorrectly.
- Manifest repository licensing is optional, but permissive licenses such as MIT, 0BSD, or Unlicense are recommended for manifests and build metadata.
- License files for each module should be installed to `$FLATPAK_DEST/share/licenses/$FLATPAK_ID`.
- Source-available submissions must build the main app and runtime dependencies from source.
- Keep patches minimal, include them in the submission, and follow upstream closely.
- Stable Flathub is for stable software. Nightlies, development snapshots, daily-update software, and new beta-only submissions are not accepted.

## Build Rules

Flathub builds have no network access during build. All dependencies must be declared as manifest sources with publicly reachable URLs or included local sources. Do not rely on `build-options.build-args: --share=network`.

For ecosystem dependencies, commit generated dependency manifests from tools such as `flatpak-builder-tools` generators for npm, yarn, cargo, pip, and similar ecosystems.

Binary or precompiled files must not be included in submission pull requests unless policy explicitly allows a case.

## Required Files

At the top level of a submission:

- Manifest named after the app ID with `.json`, `.yml`, or `.yaml`.
- `flathub.json` only when needed, for example architecture restrictions or EOL metadata.
- Dependency manifests for generated dependency sources.

Required metadata is normally installed by upstream, not copied into the Flathub submission:

- MetaInfo file that validates and appears under `/app/share/metainfo/<app-id>.metainfo.xml`.
- Desktop file for graphical apps.
- Icon, preferably SVG or at least 256x256 PNG, named and installed correctly.

## Submission Workflow

Before submission:

```bash
flatpak install -y flathub org.flatpak.Builder
flatpak remote-add --if-not-exists --user flathub https://dl.flathub.org/repo/flathub.flatpakrepo
flatpak run --command=flathub-build org.flatpak.Builder --install <manifest>
flatpak run <app-id>
flatpak run --command=flatpak-builder-lint org.flatpak.Builder manifest <manifest>
flatpak run --command=flatpak-builder-lint org.flatpak.Builder repo repo
```

For `extra-data`:

```bash
flatpak run --command=flathub-build org.flatpak.Builder <manifest>
flatpak install --user -y ./repo <app-id>
```

New app submission PRs target the `new-pr` base branch in `flathub/flathub`, not `master`. The PR title should be `Add org.example.App`.

Do not close a submission PR just to address review comments. Do not merge `master` into the submission branch.

Once comments are resolved, a test build can be started by commenting:

```text
bot, build
```

## Linter

Run manifest and repo checks locally:

```bash
flatpak run --command=flatpak-builder-lint org.flatpak.Builder manifest <manifest>
flatpak run --command=flatpak-builder-lint org.flatpak.Builder repo repo
```

Exceptions are case-by-case and should be explanatory. Check current exceptions:

```bash
curl -s https://flathub.org/api/v2/exceptions/<app-id>
```

Common linter families:

- App ID length, syntax, code-hosting prefix, URL reachability, and filename mismatch.
- AppStream validation failures.
- Missing launchable, releases, OARS content rating, metadata license, categories, screenshots, or desktop file.
- Invalid SPDX expressions or unknown licenses.
- External screenshot URLs in generated AppStream catalog data.

## Verification

Verification indicates that the app is managed by its author or project.

Typical verification methods:

- Website/domain verification based on the app ID domain, often using a well-known token.
- Source code hosting verification for supported code hosting IDs.

Because verification rules depend on current Flathub infrastructure, verify live docs before giving exact steps.

## External Data Checker

Use External Data Checker when maintainers want automated update PRs for sources that include `x-checker-data`.

Typical knobs include:

- Only create updates for important modules.
- Automatically merge selected update PRs.
- Disable checking.
- Run on multiple branches.

Review generated update PRs like any other maintenance change.

## Maintenance

Repository branch mapping:

- `master` maps to the stable Flatpak ref.
- `beta` maps to the beta Flatpak ref.
- Applications must only use `master` or `beta`.
- `branch/*` is reserved for BaseApps and extensions.

Maintenance expectations:

- Use pull requests for updates and changes.
- Test PR builds before merging.
- Keep runtimes current and avoid EOL runtimes.
- Stay responsive to issues and PRs.
- Mark apps EOL when development has ceased or the app is no longer functional.

Test builds:

- Start on every push to PRs.
- Can be manually started with `bot, build`.
- Produce temporary test refs ending in `/test`.

Official builds:

- Start on merge or push to protected branches.
- Publish usually within 1-2 hours unless held for moderation.
- Permission changes and critical AppStream field changes can trigger moderation.

`flathub.json` examples:

```json
{
  "skip-arches": ["aarch64"]
}
```

```json
{
  "only-arches": ["x86_64"]
}
```

```json
{
  "end-of-life": "This application is no longer maintained."
}
```

```json
{
  "end-of-life": "The application has been renamed to the.new.appid.",
  "end-of-life-rebase": "the.new.appid"
}
```

Dropping an already-published architecture leaves that architecture stuck on its last published version until removal is handled by Flathub admins.
