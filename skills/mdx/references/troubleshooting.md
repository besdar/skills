# MDX Troubleshooting

Use this reference when an MDX compile, parser, runtime, bundler, or component error appears.

Source-condensed from this repository's docs:
`docs/docs/troubleshooting-mdx.mdx`, `docs/docs/what-is-mdx.mdx`, `docs/docs/using-mdx.mdx`, and migration docs.

## Fast Triage

1. Read the full error and line/column location.
2. Classify it:
   - Integration/tooling: ESM, bundler config, package versions.
   - API misuse: `format`, runtime options, `baseUrl`, deprecated options.
   - Authoring syntax: unescaped `<` or `{`, invalid JSX, invalid expression, invalid ESM.
   - Runtime components: missing component, wrong component map, provider not wired.
3. Reproduce with the smallest MDX snippet.
4. Fix syntax/config rather than adding string preprocessing.
5. Re-run compile/build and render the affected page.

## ESM Problems

Current `@mdx-js/*` packages are ESM-only. If CommonJS config fails:

- Convert config to ESM.
- Use `import` instead of `require`.
- For tools that cannot load ESM, bundle MDX tooling to CJS as a short-term workaround.

## `options.renderer` Is No Longer Supported

This was removed in MDX v2. Use:

- `jsxImportSource` for non-React runtimes.
- `recmaPlugins` when arbitrary generated JavaScript transforms are needed.

## `format: 'detect'` Errors

`createProcessor` cannot detect format. It expects explicit `'md'` or `'mdx'`.

Use `compile` or an integration for detection, or pass:

```js
createProcessor({format: 'mdx'})
```

## Classic Runtime Warnings or Errors

If using `jsxRuntime: 'classic'`, missing or inconsistent `pragma`, `pragmaFrag`, and `pragmaImportSource` can fail. Prefer the automatic JSX runtime unless maintaining legacy behavior.

## `Expected Fragment/jsx/jsxs given to evaluate`

`evaluate` needs runtime exports.

Production:

```js
import * as runtime from 'react/jsx-runtime'
await evaluate(source, {...runtime, baseUrl: import.meta.url})
```

Development:

```js
import * as runtime from 'react/jsx-dev-runtime'
await evaluate(source, {
  development: true,
  ...runtime,
  baseUrl: import.meta.url
})
```

## Missing `options.baseUrl`

When using `evaluate`, `run`, or `outputFormat: 'function-body'`, pass `baseUrl` if MDX may contain `import`, `export ... from`, or `import.meta.url`.

```js
await run(code, {...runtime, baseUrl: import.meta.url})
```

## `Could not parse import/exports with acorn`

Cause: a line starts with `import` or `export` but is not valid JavaScript.

Fix:

- Make the import/export valid.
- If it is prose, do not start the line with `import` or `export`.

## `Unexpected ... in code: only import/exports are supported`

Cause: top-level JavaScript that is not `import` or `export`.

Bad:

```mdx
export const a = 1
const b = 2
```

Good:

```mdx
export const a = 1
export const b = 2
```

## Unclosed or Invalid Expressions

Common messages:

- `Unexpected end of file in expression`
- `Could not parse expression with acorn`
- `Unexpected content after expression`
- `Unexpected empty expression`

Fixes:

- Escape literal braces: `\{`.
- Close every expression with `}`.
- Use a single JavaScript expression, not statements.
- Move complex logic to imports/helpers.
- Keep multiline expression braces clear, with no stray markdown interruption.

Bad:

```mdx
{const b = 'c'}
```

Good:

```mdx
{items.map((item) => <Item key={item.id} item={item} />)}
```

## JSX Tag Grammar Errors

Common messages:

- `Unexpected end of file ... expected`
- `Unexpected character ... expected`
- `Unexpected closing slash`
- `Unexpected attribute in closing tag`
- `Unexpected self-closing slash in closing tag`
- `Unexpected closing tag ... expected corresponding closing tag`

Fixes:

- Ensure every JSX tag is syntactically valid.
- Match opening and closing tags exactly.
- Put attributes on opening tags only.
- Self-close opening void tags: `<img />`, not `<img>`.
- Do not write closing tags as self-closing: `</h1>`, not `</h1/>`.

## Lazy Lines in Containers

Errors involving "lazy line" in lists or blockquotes usually mean a multiline expression or JSX tag is not explicitly continued.

Bad:

```mdx
* {1 +
2}

> <x
y />
```

Good:

```mdx
* {1 +
  2}

> <x
> y />
```

## Cannot Close Document or Token Still Open

Cause: markdown and JSX are interleaved incorrectly, often with JSX opened inside a markdown container that ends first.

Fix:

- Keep JSX tags inside the same markdown block/container.
- Close JSX before the markdown container ends.
- Restructure into explicit JSX blocks or separate markdown blocks.

## Missing Component Runtime Errors

Example: `Expected component Alert to be defined`.

Fix by one of:

- `import {Alert} from './alert.jsx'` in MDX.
- Define `function Alert()` in MDX.
- Pass `<Post components={{Alert}} />`.
- Provide through `providerImportSource` or framework component injection.

Use `development: true` when evaluating to get better source locations.

## Component Map Does Not Apply

If `components={{a: Link}}` does not affect `<a>`, remember:

- Markdown links use `components.a`.
- Literal JSX `<a>` is a lowercase literal tag and is not replaced by `components.a`.
- Use markdown link syntax or `<Link>` if you want a component.

## Next.js Component Injection Not Working

Check:

- `mdx-components.tsx` exists in root or `src/`.
- It exports `useMDXComponents`.
- `@next/mdx` is configured.
- You are not relying on `@mdx-js/react` provider behavior for Next-specific injection.
