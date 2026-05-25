# `@mdx-js/mdx` API and On-Demand MDX

Use this reference when compiling MDX manually, evaluating strings, building server/client MDX flows, or using processor options directly.

Source-condensed from this repository's docs:
`packages/mdx/readme.md`, `docs/guides/mdx-on-demand.mdx`, and `docs/docs/getting-started.mdx`.

## Exports

`@mdx-js/mdx` exports:

- `compile`
- `compileSync`
- `createProcessor`
- `evaluate`
- `evaluateSync`
- `nodeTypes`
- `run`
- `runSync`

There is no default export.

## `compile(file, options?)`

Compile MDX to JavaScript and return a `VFile`.

```js
import {compile} from '@mdx-js/mdx'

const file = await compile('# Hello <Thing />', {
  jsxImportSource: 'react'
})

console.log(String(file))
```

`file` can be a string, UTF-8 `Uint8Array`, `VFile`, or object accepted by `new VFile`.

Use `compile` when:

- A bundler integration is not available.
- You want to write generated JS to disk.
- You want a lint/reporting pass through unified plugins.
- You need `outputFormat: 'function-body'` for later `run`.

Prefer async `compile` over `compileSync`.

## `createProcessor(options?)`

Create a unified processor to compile markdown or MDX to JavaScript.

Do not pass `format: 'detect'` to `createProcessor`; it supports only explicit `'md'` or `'mdx'`.

Use `compile` or an integration when format detection is needed.

## `evaluate(file, options)`

Compile and run MDX in one step.

```js
import {evaluate} from '@mdx-js/mdx'
import * as runtime from 'react/jsx-runtime'

const module = await evaluate('# Hi', {
  ...runtime,
  baseUrl: import.meta.url
})

const Content = module.default
```

Use `evaluate` only for trusted content. It evaluates JavaScript.

The result is an MDX module object with:

- `default`: the content component.
- named exports from the MDX file.

If using development mode, import from `react/jsx-dev-runtime` and pass `development: true`.

## `run(code, options)`

Run code produced by `compile(..., {outputFormat: 'function-body'})`.

Server:

```js
import {compile} from '@mdx-js/mdx'

const code = String(await compile('# hi', {
  outputFormat: 'function-body'
}))
```

Client:

```js
import {run} from '@mdx-js/mdx'
import * as runtime from 'react/jsx-runtime'

const {default: Content} = await run(code, {
  ...runtime,
  baseUrl: import.meta.url
})
```

Use this split when compiling on a server and rendering later in a client/runtime. MDX is not a bundler; imports inside MDX strings are not bundled into a self-contained asset.

## `baseUrl`

Pass `baseUrl` when using `evaluate`, `run`, or `outputFormat: 'function-body'` if MDX can contain:

- `import`
- `export ... from`
- `import.meta.url`

Usually:

```js
{baseUrl: import.meta.url}
```

Missing `baseUrl` is a common runtime error in MDX v3.

## Key Processor Options

- `format`: `'mdx'` or `'md'`; `compile` also supports `'detect'`.
- `jsxImportSource`: runtime package for automatic JSX, default `'react'`.
- `jsxRuntime`: `'automatic'` by default. Classic is deprecated.
- `jsx`: keep JSX in output instead of compiling it away.
- `outputFormat`: `'program'` by default; `'function-body'` for `run`.
- `providerImportSource`: module exporting `useMDXComponents`.
- `remarkPlugins`, `rehypePlugins`, `recmaPlugins`: unified plugin lists.
- `remarkRehypeOptions`: options passed through to `remark-rehype`.
- `development`: use dev runtime and better error source info.
- `baseUrl`: resolve imports/exports/import.meta.url.
- `elementAttributeNameCase`: `'react'` by default, or `'html'`.
- `stylePropertyNameCase`: `'dom'` by default, or `'css'`.
- `mdExtensions` and `mdxExtensions`: extension detection for integrations.

## Run Options

`run` and `evaluate` need JSX runtime functions.

Production:

```js
import * as runtime from 'react/jsx-runtime'

await evaluate('# hi', {...runtime, baseUrl: import.meta.url})
```

Development:

```js
import * as runtime from 'react/jsx-dev-runtime'

await evaluate('# hi', {
  development: true,
  ...runtime,
  baseUrl: import.meta.url
})
```

With provider support:

```js
import * as provider from '@mdx-js/react'
import * as runtime from 'react/jsx-runtime'

await evaluate('# hi', {
  ...provider,
  ...runtime,
  baseUrl: import.meta.url
})
```

## Performance Note

Repeatedly calling `evaluate` creates new component functions. For live-rendering frequently changing MDX, direct function invocation can be more diff-friendly than recreating elements:

```diff
 const {default: MDXContent} = await evaluate(source, options)
-<MDXContent {...props} />
+MDXContent(props)
```

Use this only when it fits the framework and rendering path.
