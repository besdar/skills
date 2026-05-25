# MDX Integrations

Use this reference before adding packages or editing bundler, framework, TypeScript, JSX runtime, or Node import configuration.

Source-condensed from this repository's docs and package readmes:
`docs/docs/getting-started.mdx`, `packages/mdx/readme.md`, `packages/rollup/readme.md`, `packages/loader/readme.md`, `packages/esbuild/readme.md`, `packages/node-loader/readme.md`, and `packages/react/readme.md`.

## Baseline Requirements

- Current documented `@mdx-js/*` packages are ESM-only.
- Use Node.js 16 or later for the documented release line.
- MDX relies on JSX. The integration compiles JSX to JavaScript, but the project still needs a JSX runtime such as React, Preact, Vue, Solid, Svelte JSX, Emotion, or Theme UI.
- MDX is executable code. Do not compile/evaluate untrusted author input without strong sandboxing.

## Integration Decision Table

| Project shape | Prefer | Notes |
| --- | --- | --- |
| Vite | `@mdx-js/rollup` | Add the MDX plugin before React if also using `@vitejs/plugin-react`. |
| Rollup | `@mdx-js/rollup` | Add Babel only if emitted JS must be transformed for older targets. |
| webpack or Rspack | `@mdx-js/loader` | Webpack loaders run right-to-left; place `@mdx-js/loader` after `babel-loader` in `use`. |
| Next.js | `@next/mdx` | Use `mdx-components.tsx`; do not use `providerImportSource` or `@mdx-js/react` for component injection. |
| esbuild | `@mdx-js/esbuild` | esbuild handles modern JS target transforms. |
| Bun plugin flow | `@mdx-js/esbuild` through Bun plugin API | Configure in `bunfig.toml` preload if needed. |
| Node imports from file system | `@mdx-js/node-loader` | Use Node loader/register flow. |
| Compile strings/files manually | `@mdx-js/mdx` | Use `compile`, `evaluate`, `run`, or `createProcessor`. |
| Astro, Docusaurus, Gatsby, Parcel | Their native MDX integration | Follow the framework integration unless the request needs lower-level MDX behavior. |

## Vite

Install:

```sh
npm install @mdx-js/rollup
```

Basic config:

```js
import mdx from '@mdx-js/rollup'
import {defineConfig} from 'vite'

export default defineConfig({
  plugins: [mdx({/* jsxImportSource, remarkPlugins, rehypePlugins */})]
})
```

With React:

```js
import mdx from '@mdx-js/rollup'
import react from '@vitejs/plugin-react'
import {defineConfig} from 'vite'

export default defineConfig({
  plugins: [
    {enforce: 'pre', ...mdx({/* options */})},
    react({include: /\.(jsx|js|mdx|md|tsx|ts)$/})
  ]
})
```

## Rollup

Install:

```sh
npm install @mdx-js/rollup
```

Config:

```js
import mdx from '@mdx-js/rollup'

export default {
  plugins: [mdx({/* jsxImportSource, remarkPlugins, rehypePlugins */})]
}
```

If using Babel after MDX, include MDX-originating extensions:

```js
babel({
  extensions: ['.js', '.jsx', '.cjs', '.mjs', '.md', '.mdx']
})
```

## Webpack

Install:

```sh
npm install @mdx-js/loader
```

Config:

```js
export default {
  module: {
    rules: [
      {
        test: /\.mdx?$/,
        use: [
          {
            loader: '@mdx-js/loader',
            options: {/* jsxImportSource, remarkPlugins, rehypePlugins */}
          }
        ]
      }
    ]
  }
}
```

With Babel:

```js
{
  test: /\.mdx?$/,
  use: [
    {loader: 'babel-loader', options: {}},
    {loader: '@mdx-js/loader', options: {}}
  ]
}
```

Webpack applies loaders right-to-left, so MDX compiles first, then Babel transforms the generated JavaScript.

## Next.js

Use `@next/mdx`:

```js
import nextMdx from '@next/mdx'

const withMdx = nextMdx({
  extension: /\.mdx?$/,
  options: {/* remarkPlugins, rehypePlugins */}
})

export default withMdx({
  pageExtensions: ['md', 'mdx', 'tsx', 'ts', 'jsx', 'js']
})
```

For components, add `mdx-components.tsx` in the project root or `src/`:

```tsx
import type {MDXComponents} from 'mdx/types'

export function useMDXComponents(components: MDXComponents): MDXComponents {
  return {
    ...components,
    h1: (props) => <h1 className="heading" {...props} />
  }
}
```

Do not configure `providerImportSource: '@mdx-js/react'` in Next.js for this purpose.

## esbuild

Install:

```sh
npm install @mdx-js/esbuild
```

Use:

```js
import mdx from '@mdx-js/esbuild'
import esbuild from 'esbuild'

await esbuild.build({
  entryPoints: ['index.js'],
  format: 'esm',
  outfile: 'output.js',
  plugins: [mdx({/* options */})]
})
```

## Node.js Loader

Install:

```sh
npm install @mdx-js/node-loader
```

Import MDX from Node:

```sh
node --loader=@mdx-js/node-loader example.js
```

For newer Node warnings about `--loader`, create a register file:

```js
import {register} from 'node:module'

register('@mdx-js/node-loader', import.meta.url)
```

Run:

```sh
node --import ./register.js example.js
```

## JSX Runtime Options

React is the default.

For other runtimes, set `jsxImportSource`:

```js
mdx({jsxImportSource: 'preact'})
mdx({jsxImportSource: 'vue'})
mdx({jsxImportSource: 'solid-js/h'})
mdx({jsxImportSource: 'svelte-jsx'})
mdx({jsxImportSource: '@emotion/react'})
```

Prefer the automatic JSX runtime. Classic runtime options still exist but are deprecated in the current docs and expected to be removed in a future major release.

## TypeScript

Install MDX import types:

```sh
npm install --save-dev @types/mdx
```

Ensure the framework `JSX` namespace is typed. For React, install React types and optionally augment `mdx/types.js`:

```ts
import * as React from 'react'

declare module 'mdx/types.js' {
  export import JSX = React.JSX
}
```

Useful imports:

```ts
import type {MDXComponents, MDXContent} from 'mdx/types.js'
```

## Security

MDX is a programming language. It can execute JavaScript. For untrusted content, avoid `evaluate` entirely when possible. If unavoidable, use isolation such as iframes with sandboxing, OS/process sandboxing, rate limits, and timeouts; do not rely on MDX alone for safety.
