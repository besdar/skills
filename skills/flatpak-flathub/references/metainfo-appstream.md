# MetaInfo and AppStream

Use this reference for Flathub MetaInfo, AppStream validation, listing quality, desktop integration metadata, screenshots, releases, translations, and common linter issues.

## Contents

- Validation
- File Location and Header
- Required Tags
- Optional but Important Tags
- Screenshots
- Translation Rules
- Quality Guidance
- Generated Output
- Common Linter Issues

## Validation

Install the Flathub builder:

```bash
flatpak install -y flathub org.flatpak.Builder
```

Validate MetaInfo:

```bash
flatpak run --command=flatpak-builder-lint org.flatpak.Builder appstream <app-id>.metainfo.xml
```

This runs `appstreamcli validate` with Flathub-specific checks. Treat warnings and errors as fatal.

Preview metadata:

```bash
gnome-software --show-metainfo /path/to/<app-id>.metainfo.xml
appstreamcli get --details --datapath /path/to/<app-id>.metainfo.xml <app-id>
```

## File Location and Header

- Install MetaInfo to `/app/share/metainfo/<app-id>.metainfo.xml`.
- The filename, MetaInfo `<id>`, and manifest `id` must match exactly.
- `/app/share/appdata` and `<app-id>.appdata.xml` are legacy.

Typical header:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!-- Copyright [year] [name] -->
<component type="desktop-application">
```

Use `desktop-application` for graphical apps, `console-application` for console apps, `addon` for extensions, and `runtime` for SDK extensions or runtimes.

## Required Tags

ID:

```xml
<id>org.example.App</id>
```

Licenses:

```xml
<metadata_license>CC0-1.0</metadata_license>
<project_license>GPL-3.0-only</project_license>
```

- `metadata_license` is the license of the MetaInfo file itself.
- `project_license` is the application license and must be a valid SPDX identifier or expression.
- Proprietary licenses can use `LicenseRef-proprietary=https://example.org/legal/`.

Developer:

```xml
<developer id="org.example">
  <name>Developer name</name>
</developer>
```

Name and summary:

```xml
<name>App Name</name>
<summary>Short summary</summary>
```

Description:

```xml
<description>
  <p>Describe what the app does and why it is useful.</p>
  <ul>
    <li>Feature one</li>
    <li>Feature two</li>
  </ul>
</description>
```

Supported child tags are `p`, `ol`, `ul`, `li`, `em`, and inline `code`. The description needs at least one non-empty `p`, `ol`, or `ul`.

Launchable for graphical apps:

```xml
<launchable type="desktop-id">org.example.App.desktop</launchable>
```

OARS content rating:

```xml
<content_rating type="oars-1.1" />
```

At minimum include a homepage URL:

```xml
<url type="homepage">https://example.org/</url>
```

Recommended URLs include `bugtracker`, `donation`, `contact`, `faq`, `translate`, `contribute`, and `vcs-browser`.

Releases:

```xml
<releases>
  <release version="1.0.1" date="2024-01-18">
    <description>
      <p>Briefly describe user-visible changes.</p>
    </description>
  </release>
</releases>
```

Release dates must not be in the future and versions must be ordered correctly. Use `appstreamcli vercmp <a> <b>` when order is uncertain.

## Optional but Important Tags

Provides and replaces for renames:

```xml
<provides>
  <id>org.example.OldApp</id>
</provides>
<replaces>
  <id>org.example.OldApp</id>
</replaces>
```

Console apps should provide their main binary:

```xml
<provides>
  <binary>foo</binary>
</provides>
```

Categories and keywords:

```xml
<categories>
  <category>Development</category>
</categories>
<keywords>
  <keyword>IDE</keyword>
</keywords>
```

Avoid generic categories such as `GTK`, `Qt`, `KDE`, `GNOME`, `Motif`, `Java`, `GUI`, `Application`, `XFCE`, and `DDE`.

Brand colors:

```xml
<branding>
  <color type="primary" scheme_preference="light">#faa298</color>
  <color type="primary" scheme_preference="dark">#7f2c22</color>
</branding>
```

Device support for desktop-only apps:

```xml
<requires>
  <control>keyboard</control>
  <control>pointing</control>
  <display_length compare="ge">768</display_length>
</requires>
```

Device support for desktop and mobile apps:

```xml
<supports>
  <control>keyboard</control>
  <control>pointing</control>
  <control>touch</control>
</supports>
<requires>
  <display_length compare="ge">360</display_length>
</requires>
```

## Screenshots

Graphical apps need one or more screenshots:

```xml
<screenshots>
  <screenshot type="default">
    <image>https://example.org/example1.png</image>
    <caption>Main window</caption>
  </screenshot>
</screenshots>
```

Guidance:

- Use direct image URLs from immutable tags or commits, not branch URLs.
- Include one default screenshot.
- Tag localized screenshots with `xml:lang`.
- Use Linux screenshots of just the app window, with native shadows and rounded corners.
- Do not include a full desktop, wallpaper, marketing text, edits, or promotional graphics.
- Use default settings unless showing theme support intentionally.
- Keep window size around 1000x700 or smaller, 2000x1400 for HiDPI.
- Captions should be one sentence and should not end with a full stop.
- Show realistic content, not empty states.
- Keep screenshots current with the app UI.

## Translation Rules

English/default values must not use `xml:lang`.

Translatable tags include:

- `name`
- `developer/name`
- `summary`
- `keywords`
- `image`
- `caption`
- `description` children: translate individual `p` and `li`, not the `description` element itself

Use `translate="no"` for values that should not be translated, such as a developer name.

## Quality Guidance

Quality checks are not always submission blockers, but they affect presentation and promotion.

Name:

- Prefer 15 characters or fewer; must be under 20 for quality.
- Use just the app name, not a tagline.
- Avoid odd punctuation, all-lowercase, all-uppercase, or brand-breaking formatting unless established.

Summary:

- Prefer 10-25 characters, no more than 35 for quality.
- Explain user value, not toolkit or implementation details.
- Do not repeat the app name.
- Do not end with a period.
- Prefer direct verb phrases such as `Edit documents`.

Description:

- Do not repeat the summary.
- Aim for roughly 3-6 lines for most apps.
- Avoid huge feature lists.

Icon:

- Prefer SVG, or square PNG at least 256x256.
- Avoid icons that fill too much or too little of the canvas.
- Maintain contrast on light and dark backgrounds.
- Avoid tiny text/detail, overly simple glyphs, baked-in shadows, or outdated styles.

Brand colors:

- Provide light and dark primary colors.
- Avoid black/white/gray, colors too close to the icon, or identical light/dark colors.

Release notes:

- Include release notes for every release.
- Use concrete user-visible changes, not "bug fixes and performance improvements".

Age ratings:

- Include easily accessible external content when filling OARS data.

## Generated Output

After a build, `flatpak-builder` composes AppStream catalog data from the desktop file, icon, and MetaInfo.

Generated paths include:

- `<builddir>/files/share/app-info/xmls/<app-id>.xml.gz`
- `${FLATPAK_DEST}/share/app-info/xmls/<app-id>.xml.gz`
- `<builddir>/files/share/app-info/icons/flatpak/{64x64,128x128}/<app-id>.png`

Do not create or edit generated AppStream catalog XML manually.

## Common Linter Issues

- `appstream-id-mismatch-flatpak-id`: MetaInfo ID does not match manifest ID.
- `desktop-app-launchable-missing` or `desktop-app-launchable-omitted`: missing launchable tag.
- `content-rating-missing`: missing OARS data.
- `metadata-license-missing` or `metadata-license-invalid`: missing or invalid metadata license.
- `spdx-expression-invalid` or `spdx-license-unknown`: invalid project license.
- `releases-info-missing`, `releases-not-in-order`, `release-version-missing`, `release-time-missing`: release metadata issues.
- `screenshot-default-missing`, `screenshot-no-media`, `screenshot-image-source-duplicated`: screenshot metadata issues.
- `description-markup-invalid`, `description-para-markup-invalid`, `description-enum-item-invalid`: unsupported description markup.
- `category-invalid`, `all-categories-ignored`, `app-categories-missing`: category issues.
- `cid-rdns-contains-hyphen`, `cid-has-number-prefix`: app ID format problems.
- `unknown-tag`: invalid tags; custom non-standard tags need `x-` prefixes or `<custom>`.
