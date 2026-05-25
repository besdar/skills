# Migration and Refactoring

Use this reference when upgrading MDX major versions or refactoring an existing Markdown/HTML/React content project to MDX.

Source-condensed from this repository's docs:
`docs/migrating/v1.mdx`, `docs/migrating/v2.mdx`, `docs/migrating/v3.mdx`, and the main docs/guides.

## Refactor Strategy

1. Inventory content and runtime.
   Identify file extensions, frontmatter use, embedded HTML, custom React components, code fences, GFM syntax, math, routes, and current rendering path.

2. Add integration first.
   Wire MDX support into the existing bundler/framework before mass file conversion.

3. Convert one representative file.
   Pick a file with normal markdown, metadata, code fences, and one component. Validate build and render.

4. Choose metadata semantics.
   Use ESM exports for metadata consumed after import. Use frontmatter plugins for metadata that must be scanned from the filesystem before compilation.

5. Convert HTML to JSX.
   Close void tags, replace comments with `{/* ... */}`, update attributes (`className` for React), and fix style objects.

6. Extract repeated UI to components.
   Import components in MDX for local use or pass them through `components` for site-wide markdown element replacement.

7. Add plugins for used syntax.
   Use `remark-gfm`, `remark-frontmatter`, `remark-mdx-frontmatter`, `remark-math`, `rehype-katex`, syntax highlighting, or embed plugins only when content requires them.

8. Add types.
   Install `@types/mdx` and framework JSX types when TypeScript imports `.mdx`.

9. Verify broadly after the pattern works.
   Run build/typecheck/lint/tests and inspect rendered pages. Use content fixtures for syntax added by plugins.

## Markdown to MDX Conversion Rules

- Keep plain `.md` as `.md` if no JSX/ESM/expressions are needed and the integration supports both.
- Convert to `.mdx` when content needs components, imports/exports, expressions, or local layouts.
- Replace indented code with fenced code.
- Replace autolinks with normal markdown links.
- Escape literal `<` and `{`.
- Convert raw HTML to JSX.
- Move JavaScript statements out of inline braces.

## React/JSX Content to MDX

When moving JSX-heavy documentation into MDX:

- Keep prose in markdown instead of wrapping everything in `<p>`.
- Use components for reusable UI blocks.
- Import components at top level.
- Prefer markdown headings/lists/links when component replacement is desired through `components`.
- Use explicit JSX tags when the element should not be replaced by markdown component mapping.

Example:

```mdx
import {Callout} from '../components/callout.jsx'

# Install

<Callout tone="info">
  This package is ESM-only.
</Callout>
```

## Migrating to MDX v3

Typical changes:

- Use Node.js 16 or later.
- Update remark/rehype plugins.
- Pass `baseUrl` to `evaluate`, `run`, or code compiled with `outputFormat: 'function-body'`.
- Prefer automatic JSX runtime; classic runtime now warns and is expected to be removed in a future major.
- Replace deprecated `MDXContext` and `withMDXComponents` with `useMDXComponents`.
- Replace deprecated `@mdx-js/register` with `@mdx-js/node-loader`.
- Remove old `useDynamicImport`; dynamic import behavior is now default where relevant.

## Migrating to MDX v2

Major themes:

- `@mdx-js/*` packages became ESM-only. Replace `require(...)` with `import`.
- GFM features were turned off by default. Add `remark-gfm` if needed.
- MDX syntax became stricter and better defined.
- Missing components throw errors instead of rendering children with warnings.
- `parent.child` component mappings such as `ol.li` were removed.
- `inlineCode` was removed; use `code` for inline code and `pre` for block wrappers.
- `MDXContent.isMDXContent` was removed.
- Locally defined/imported components take precedence over passed components.
- Passed `components.h1` affects markdown `# hi`, not literal JSX `<h1>hi</h1>`.
- Objects can be passed and referenced as member components such as `<theme.Box>`.

Syntax improvements in v2:

- Blank lines are no longer required between JSX and markdown.
- Indented markdown inside JSX can work as markdown rather than indented code.
- Expressions can include JavaScript values and JSX escape hatches.
- ESM component definitions can include blank lines.

## Migrating from MDX v0 to v1

Legacy migration highlights:

- Replace `@mdx-js/tag` with `@mdx-js/react`.
- React support in `@mdx-js/react` requires React 16.8 or later.
- Nested `MDXProvider` contexts merge by default; use the functional component mapping form to replace outer context behavior.

## Common Refactor Anti-Patterns

- Adding `@mdx-js/react` to every React project by default. React works without it.
- Using providers in Next.js instead of `mdx-components.tsx`.
- Enabling broad plugin presets before seeing content requirements.
- Converting all markdown files at once before a representative route builds and renders.
- Treating MDX as safe user content.
- Solving parser errors with string preprocessing instead of valid MDX syntax.

## Verification Checklist

- A changed MDX file compiles.
- A route importing MDX renders.
- Component maps affect markdown-generated elements as intended.
- Literal JSX elements intentionally do or do not use component maps.
- Metadata is available at the layer that needs it.
- Code fences, GFM, frontmatter, and math render only after the corresponding plugin is configured.
- TypeScript accepts `.mdx` imports.
- No runtime missing-component errors remain.
