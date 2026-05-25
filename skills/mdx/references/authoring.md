# MDX Authoring

Use this reference when editing `.mdx`, converting Markdown/HTML/JSX to MDX, or diagnosing authoring mistakes.

Source-condensed from this repository's docs:
`docs/docs/what-is-mdx.mdx`, `docs/docs/using-mdx.mdx`, `docs/table-of-components.mdx`, and `docs/docs/troubleshooting-mdx.mdx`.

## Mental Model

MDX combines:

- CommonMark markdown.
- JSX tags and components.
- JavaScript expressions in `{...}`.
- ESM `import` and `export` declarations.

An MDX file compiles to a JavaScript module. The default export is the content component. Other ESM exports remain available as named exports.

```mdx
import {Chart} from './chart.jsx'
export const title = 'Quarterly revenue'

# {title}

<Chart />
```

## Markdown Differences

Standard CommonMark works by default, but several ambiguous markdown features do not:

- Indented code blocks do not work as code. Use fenced code blocks.
- Autolinks such as `<https://example.com>` do not work. Use `[text](https://example.com)`.
- HTML syntax is replaced by JSX. Use `<img />`, `className` in React, and JSX comments `{/* ... */}`.
- Literal `<` and `{` must be escaped as `\<` and `\{`, or written as expressions such as `{'<'}`.
- Nonstandard markdown such as GFM, frontmatter, math, and syntax highlighting needs plugins.

## JSX Rules

Use JSX for components and HTML-like markup:

```mdx
<Callout type="warning">
  This paragraph can contain *markdown*.
</Callout>
```

Rules to preserve:

- JSX tags must be well formed and matched.
- Void elements must self-close: `<img />`, `<br />`, `<input />`.
- Attribute syntax follows the target JSX runtime. In React, use `className`, `htmlFor`, camel-cased SVG/CSS properties, and object styles.
- Lowercase JSX names such as `<a>` are literal tags. Capitalized names such as `<Link>` are component references.
- Member expressions such as `<theme.Box>` reference object properties.
- Locally imported or defined components take precedence over passed components.

## Markdown and JSX Interleaving

MDX allows markdown inside JSX blocks:

```mdx
<article>
  # Heading

  A paragraph with **strong** text.
</article>
```

Inline markdown inside one-line JSX stays inline:

```mdx
<div># not a heading, but *emphasis* works</div>
```

Separate lines produce markdown blocks:

```mdx
<div>
  This becomes a paragraph.
</div>
```

Avoid opening JSX inside one markdown block and closing it in another. This often causes "Cannot close document" or mismatched tag errors.

## Expressions

Use `{...}` for JavaScript expressions that yield renderable values:

```mdx
export const name = 'Venus'

# Hello {name.toUpperCase()}
```

Expressions must be expressions, not statements:

```mdx
{/* Good */}
{items.map((item) => <Item key={item.id} item={item} />)}

{/* Bad */}
{const value = 1}
```

For complex logic, prefer one of these:

- Move logic to an imported helper.
- Export/define a component and render it.
- Use an IIFE only for small local logic.

```mdx
{(() => {
  const tone = score > 80 ? 'good' : 'needs-work'
  return <Badge tone={tone} />
})()}
```

## ESM

Top-level `import` and `export` statements are supported:

```mdx
import {Badge} from './badge.jsx'
export const metadata = {title: 'Launch notes'}

# {metadata.title}

<Badge />
```

Only `import` and `export` declarations are allowed as top-level JavaScript. If a variable or helper is needed in MDX, export it:

```mdx
export const status = 'stable'

# Status: {status}
```

## Components for Markdown Elements

Markdown syntax maps to element names that can be replaced through the `components` prop:

- `[text](url)` -> `a`
- `> quote` -> `blockquote`
- inline and fenced code -> `code`, with block code wrapped in `pre`
- `*emphasis*` -> `em`
- headings -> `h1` through `h6`
- images -> `img`
- lists -> `ul`, `ol`, `li`
- tables from GFM -> `table`, `thead`, `tbody`, `tr`, `th`, `td`

Example:

```jsx
<Post components={{a: FancyLink, h2: SectionHeading, pre: CodeFrame}} />
```

## Metadata

Prefer ESM exports when metadata can be part of the compiled module:

```mdx
export const title = 'Hi'

# {title}
```

Use frontmatter when metadata must be read from files before compiling. MDX does not support frontmatter by default; use plugins described in `plugins.md`.

## Authoring Pitfalls

- If text contains "import" or "export" at the start of a line, MDX may parse it as ESM. Reword, indent as text, or avoid starting the paragraph with those keywords.
- If text contains literal braces, escape only the opening brace: `\{`.
- If JSX spread attributes are needed, each spread must stand alone: `<Box {...a} {...b} />`.
- Empty JSX attribute expressions are invalid: use `<Box {...props} />`, not `<Box {} />`.
- Missing components are runtime errors. Import them in MDX or pass/provide them.
