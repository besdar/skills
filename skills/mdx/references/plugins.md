# Plugins and Nonstandard Markdown

Use this reference when enabling GFM, frontmatter, math, syntax highlighting, embeds, code metadata, or custom MDX transforms.

Source-condensed from this repository's docs:
`docs/docs/extending-mdx.mdx`, `docs/guides/gfm.mdx`, `docs/guides/frontmatter.mdx`, `docs/guides/math.mdx`, `docs/guides/syntax-highlighting.mdx`, `docs/guides/embed.mdx`, and `packages/mdx/readme.md`.

## Extension Points

MDX can be extended in three places:

- Compiler options.
- Plugins in the unified pipeline:
  - `remarkPlugins` for markdown/mdast transforms.
  - `rehypePlugins` for HTML/hast transforms.
  - `recmaPlugins` for JavaScript/esast transforms.
- Runtime components passed, imported, or provided.

Plugin arrays accept plugins or `[plugin, options]` tuples:

```js
await compile(file, {
  remarkPlugins: [remarkGfm, [remarkFrontmatter, 'toml']],
  rehypePlugins: [[rehypeKatex, {strict: true}]],
  recmaPlugins: [recmaMdxDisplayname]
})
```

## GFM

MDX supports CommonMark by default, not GitHub Flavored Markdown. Add `remark-gfm` for:

- Autolink literals.
- Footnotes.
- Strikethrough.
- Tables.
- Task lists.

```js
import {compile} from '@mdx-js/mdx'
import remarkGfm from 'remark-gfm'

await compile(await fs.readFile('example.mdx'), {
  remarkPlugins: [remarkGfm]
})
```

Use the same `remarkPlugins` option in Rollup, Vite, webpack, Next, esbuild, or node-loader integrations.

## Frontmatter

MDX does not support frontmatter by default.

Use ESM exports when metadata belongs to the compiled module:

```mdx
export const title = 'Hi, World!'

# {title}
```

Use frontmatter when metadata must be extracted from files before compiling:

```mdx
---
title: Hi, World!
---

# Hi, World!
```

For compile support that ignores frontmatter as content:

```js
import remarkFrontmatter from 'remark-frontmatter'

await compile(file, {remarkPlugins: [remarkFrontmatter]})
```

To expose frontmatter values inside MDX as exports, add `remark-mdx-frontmatter` too:

```js
import remarkFrontmatter from 'remark-frontmatter'
import remarkMdxFrontmatter from 'remark-mdx-frontmatter'

await compile(file, {
  remarkPlugins: [remarkFrontmatter, remarkMdxFrontmatter]
})
```

If metadata is needed without compiling, use a file parser such as `vfile-matter` outside MDX compilation.

## Math

MDX does not support math by default. Add `remark-math` plus a rehype renderer:

```js
import {compile} from '@mdx-js/mdx'
import rehypeKatex from 'rehype-katex'
import remarkMath from 'remark-math'

await compile('# $$\\sqrt{a^2 + b^2}$$', {
  remarkPlugins: [remarkMath],
  rehypePlugins: [rehypeKatex]
})
```

If using `rehype-katex`, include KaTeX CSS in the rendered page. For MathJax, use `rehype-mathjax` instead.

## Syntax Highlighting

MDX does not highlight code by default.

Prefer compile-time highlighting for static content because it avoids sending highlighter code to the client:

```js
import {compile} from '@mdx-js/mdx'
import rehypeStarryNight from 'rehype-starry-night'

await compile('```js\nconsole.log(1)\n```', {
  rehypePlugins: [rehypeStarryNight]
})
```

Other compile-time options include `rehype-highlight` and `@mapbox/rehype-prism`.

Runtime highlighting is framework-specific. In React, pass a custom `code` or `pre` component:

```jsx
<Post components={{code: Code}} />
```

## Code Meta

Markdown code fences can include meta:

````mdx
```js filename="index.js"
console.log(1)
```
````

MDX ignores `meta` by default. Use `rehype-mdx-code-props` when code-fence metadata should become JSX props accessible to a `pre` component.

## Embeds

MDX does not support embeds by default.

Compile-time embeds use remark plugins such as `@remark-embedder/core`:

```js
await compile(code, {
  remarkPlugins: [[remarkEmbedder, {transformers: [oembedTransformer]}]]
})
```

Runtime embeds use framework components:

```mdx
import {CodePen} from 'mdx-embed'

<CodePen codePenId="PNaGbb" />
```

If imports should not appear in content, pass embed components through the `components` prop or a provider.

## Creating Plugins

Creating a plugin for MDX is mostly the same as creating a remark, rehype, or recma plugin.

Use the right tree stage:

- Authoring syntax and markdown nodes: remark/mdast.
- HTML semantics and rendered element transforms: rehype/hast.
- Generated JavaScript transforms: recma/esast.

For AST work involving MDX nodes, register MDX node types when using TypeScript:

```ts
/// <reference types="remark-mdx" />
```

When passing MDX nodes through `remark-rehype`, include:

```js
passThrough: [
  'mdxjsEsm',
  'mdxFlowExpression',
  'mdxJsxFlowElement',
  'mdxJsxTextElement',
  'mdxTextExpression'
]
```

## Plugin Selection Rule

Do not add plugin presets just in case. Add a plugin only when content or product requirements need the syntax or transform, then add a fixture MDX file that exercises it.
