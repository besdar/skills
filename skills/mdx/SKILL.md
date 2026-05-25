---
name: mdx
description: Build, migrate, refactor, debug, and review MDX projects and content. Use when Codex needs to integrate @mdx-js packages, convert Markdown/HTML/React content to .mdx, configure bundlers or frameworks such as Vite, Rollup, webpack, Next.js, esbuild, or Node loaders, wire MDX components/providers/layouts, add remark/rehype/recma plugins for GFM/frontmatter/math/highlighting/embeds, troubleshoot MDX parser or runtime errors, or migrate MDX v1/v2/v3 projects.
---

# MDX

## Overview

Use this skill to work from the official MDX documentation model: MDX is markdown plus JSX, JavaScript expressions, and ESM imports/exports compiled to JavaScript components. Treat MDX content as executable code, integrate it through the project's existing build stack, and validate with the same build, type, lint, and rendering checks the project already uses.

## Workflow

1. Inspect the project before changing it.
   Read `package.json`, lockfiles, framework config, bundler config, TypeScript config, routing/content conventions, and representative `.md`, `.mdx`, `.jsx`, `.tsx`, or content-loader files.

2. Identify the MDX mode.
   Decide whether the project needs file-based MDX imports at build time, dynamic on-demand compilation, direct Node imports, or simple authoring fixes. Keep plain `.md` files as markdown unless JSX, ESM exports, or expressions are needed.

3. Choose the integration conservatively.
   Prefer the official integration that matches the existing stack:
   - Vite or Rollup: `@mdx-js/rollup`
   - webpack or Rspack: `@mdx-js/loader`
   - esbuild or Bun plugin flows: `@mdx-js/esbuild`
   - Next.js: `@next/mdx` plus `mdx-components.tsx`
   - Node file imports: `@mdx-js/node-loader`
   - Manual compile/evaluate/run: `@mdx-js/mdx`

4. Configure runtime and components.
   React is the default JSX runtime. For other runtimes, set `jsxImportSource`. Prefer passing `components` directly. Use `@mdx-js/react`, `@mdx-js/preact`, or `@mdx-js/vue` providers only when nested MDX makes explicit passing too noisy. In Next.js, use `mdx-components.tsx` instead of `@mdx-js/react`.

5. Add only the plugins the content needs.
   MDX supports CommonMark by default. Add plugins for nonstandard markdown: `remark-gfm` for GFM, `remark-frontmatter` and often `remark-mdx-frontmatter` for frontmatter, `remark-math` plus `rehype-katex` or `rehype-mathjax` for math, and rehype plugins for syntax highlighting or code metadata.

6. Refactor content using MDX authoring rules.
   Replace HTML syntax with JSX, close JSX tags, use framework-appropriate attributes such as `className` in React, escape literal `<` and `{`, and move complex JavaScript out of expressions into imported helpers.

7. Verify behavior.
   Run the smallest useful project checks first: install/typecheck/build/lint/tests. Compile at least one changed MDX file. For frontend apps, open the relevant route and inspect console/rendering.

## Reference Selection

Load only the reference needed for the current task:

- `references/authoring.md`: read before editing `.mdx` content, converting Markdown/HTML/JSX to MDX, or fixing syntax.
- `references/integrations.md`: read before adding packages or editing Vite, Rollup, webpack, Next.js, esbuild, Bun, Node, TypeScript, or JSX runtime config.
- `references/components-runtime.md`: read when passing components, layouts, providers, `providerImportSource`, `useMDXComponents`, or Next `mdx-components.tsx`.
- `references/plugins.md`: read when enabling GFM, frontmatter, math, syntax highlighting, embeds, or writing remark/rehype/recma plugins.
- `references/api-on-demand.md`: read when using `@mdx-js/mdx` APIs such as `compile`, `evaluate`, `run`, `createProcessor`, or server/client on-demand MDX.
- `references/migration-refactor.md`: read when upgrading MDX major versions or refactoring an existing project to MDX.
- `references/troubleshooting.md`: read when an MDX parser, compiler, bundler, runtime, or component error appears.

## Quick Rules

- Use ESM `import` syntax with `@mdx-js/*` packages.
- Require or recommend Node.js 16 or later for the current documented `@mdx-js/*` release line.
- Do not evaluate untrusted MDX. MDX is code.
- Prefer the automatic JSX runtime. Treat classic runtime options as legacy.
- Do not use `providerImportSource` or `@mdx-js/react` in Next.js projects; use `mdx-components.tsx`.
- Use `baseUrl: import.meta.url` with `evaluate`, `run`, or `outputFormat: 'function-body'` when imports, exports, or `import.meta.url` can appear.
- Remember that passed components override markdown-generated elements such as `h1`, `a`, `pre`, and `code`, but locally imported or defined MDX components take precedence over passed components.
- Keep project style intact. Do not introduce a new site/content framework unless the existing stack cannot support the requested MDX workflow.

## Refactoring Checklist

When converting an existing project to MDX:

1. Add one representative MDX page or content file before mass conversion.
2. Wire the integration into the existing bundler/framework.
3. Add TypeScript declarations or `@types/mdx` if imports are typed.
4. Decide metadata strategy: ESM exports for dynamic metadata, frontmatter plugins for filesystem extraction.
5. Move repeated JSX into components and either import them from MDX or pass them through `components`.
6. Convert HTML to JSX and update attributes for the target runtime.
7. Add plugins only for syntax already used by the content.
8. Run build and inspect rendered output before broad mechanical conversion.
