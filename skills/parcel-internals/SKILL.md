---
name: parcel-internals
description: Use when working on Parcel implementation internals or explaining Parcel's bundler, bundle graph, asset graph, scope hoisting, symbol propagation, deferring, SWC JS transformer visitors, manual shared bundles, AdjacencyList graph storage, or native binary CI. Use for code changes, debugging, reviews, and architecture explanations in the Parcel repo that touch packages/bundlers/default, packages/core/core graph and symbol logic, packages/core/graph, packages/transformers/js/core, packages/packagers/js, or related integration tests.
---

# Parcel Internals

## Workflow

Use this skill to orient implementation work against Parcel's internal design notes.

1. Start from the user request and identify the subsystem: bundling, graph storage, scope hoisting, symbol propagation, JS transformation, JS packaging, deferring, manual shared bundles, or native binary CI.
2. Read the smallest relevant reference listed below. Prefer the reference index first when the right document is not obvious.
3. Cross-check the copied docs against the live repository before editing. The docs explain intent and algorithms, but the code is the source of truth.
4. Search code with `rg` using the code path and symbol hints in the reference index.
5. For behavior changes, inspect nearby integration tests before adding new ones; many internals are covered under `packages/core/integration-tests/test/`.

## References

Read `references/index.md` first for a compact map of available docs, code locations, and search terms.

Use these topic references selectively:

- Bundler algorithm and bundle graph creation: `references/docs/DefaultBundler.md`
- Bundler examples, target handling, CSS merging, reused bundles, and manual bundle examples: `references/docs/BundlerExamples.md`
- Manual shared bundle implementation: `references/docs/ManualBundling.md`
- Scope hoisting concepts, tree shaking, skipping, symbols, runtime deduplication, and interop: `references/docs/Scopehoisting.md`
- Symbol propagation down/up traversal and circular reexports: `references/docs/Symbol Propagation.md`
- Deferring and undeferring asset graph nodes: `references/docs/Deferring.md`
- SWC visitor patterns used by Parcel's Rust JS transformer: `references/docs/swc Visitors.md`
- Scope-hoisting transformer implementation notes: `references/docs/Scopehoisting Transformer.md`
- Scope-hoisting packager implementation notes: `references/docs/Scopehoisting Packager.md`
- Shared graph storage internals: `references/docs/AdjacencyList.md`
- Native binary build CI notes: `references/docs/Continuous Integration/Native Binary Builds.md`

Bundler diagrams from the original docs are available under `references/docs/BundlerGraphs/`.

## Implementation Guidance

When changing `packages/bundlers/default/src/DefaultBundler.js`, keep the docs' distinction between the mutable asset graph and the local ideal bundle graph in mind. The algorithm intentionally computes most placement decisions in `createIdealGraph()` before `decorate()` mutates the `MutableBundleGraph`.

When changing scope hoisting, separate the phases:

- Transformer: rewrites import/export syntax, assigns symbol names, and records metadata in `packages/transformers/js/core/src/hoist.rs`.
- Symbol propagation: computes transitively used symbols in `packages/core/core/src/SymbolPropagation.js`.
- Packager: resolves transformed placeholders and inlines or wraps assets in `packages/packagers/js/src/ScopeHoistingPackager.js`.
- Bundle graph resolution: follows reexports in `packages/core/core/src/BundleGraph.js`.

When working on graph storage, read `AdjacencyList.md` before editing `packages/core/graph/src/AdjacencyList.js`. The implementation relies on SharedArrayBuffer-backed `Uint32Array` partitions and edge/node records, so apparent low-level layout details are part of the data model.

## Verification

Choose verification based on the touched subsystem:

- Bundler/manual bundle changes: run or add focused integration tests in `packages/core/integration-tests/test/bundler.js` and related fixture directories.
- Scope-hoisting changes: run or add focused tests in `packages/core/integration-tests/test/scope-hoisting.js`.
- Graph storage changes: run the graph package tests if available, and add small cases for edge ordering, removal, resizing, and typed edge behavior.
- CI/native binary doc or workflow changes: inspect `.github/workflows` and validate the specific job command locally only if the required toolchain is available.

Always report when the docs and live code disagree; treat that as either a code archaeology note or a docs update candidate.
