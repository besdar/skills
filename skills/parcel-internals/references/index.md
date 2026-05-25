# Parcel Internals Reference Index

Use this index to pick a narrow reference before loading full docs.

## Bundling

- Read `docs/DefaultBundler.md` for the default bundler pipeline: target maps, entry bundles, explicit code split points, type-change bundles, reachability, availability, internalization, inserting or sharing assets, merging shared bundles, and decorating the mutable bundle graph.
- Read `docs/BundlerExamples.md` for worked examples: multiple targets, CSS bundle merging, reused bundles, manual bundles, and debugging notes.
- Read `docs/ManualBundling.md` for manual shared bundle implementation details: `manualAssetToConfig`, parent/root lookup, overriding code split bundles, internalized async assets, and overriding traditional shared bundles.
- Live code usually starts in `packages/bundlers/default/src/DefaultBundler.js`.
- Useful search terms: `createIdealGraph`, `decorate`, `reachableRoots`, `reachableAssets`, `manualSharedBundles`, `manualSharedBundle`, `bundleRootGraph`, `bundleGroupBundleIds`, `internalizedAssets`.

## Scope Hoisting And Symbols

- Read `docs/Scopehoisting.md` for concepts: tree shaking, scope hoisting, skipped assets, asset and dependency symbol maps, CJS namespace fallback, runtime deduplication, and interop.
- Read `docs/Symbol Propagation.md` for the down/up propagation passes, `export *` handling, circular reexports, dirty flags, and missing-export errors.
- Read `docs/Deferring.md` for deferring unused reexport asset groups during asset graph building and later undeferring when new dependencies make them used.
- Live code usually starts in `packages/core/core/src/SymbolPropagation.js`, `packages/core/core/src/BundleGraph.js`, and `packages/core/core/src/AssetGraph.js`.
- Useful search terms: `propagateSymbolsDown`, `propagateSymbolsUp`, `usedSymbolsDown`, `usedSymbolsUp`, `usedSymbolsUpDirtyDown`, `usedSymbolsUpDirtyUp`, `shouldDeferDependency`, `hasDeferred`, `getSymbolResolution`.

## JS Transformer And Packager

- Read `docs/swc Visitors.md` before transformer work that involves SWC traversal, node replacement, identifier handling, scopes, or ancestor-sensitive logic.
- Read `docs/Scopehoisting Transformer.md` for hoist transformer behavior: static ESM and CJS analysis, self references, generated identifier formats, dynamic import `promiseSymbol`, the `Collect` analysis pass, and the `Hoist` transform pass.
- Read `docs/Scopehoisting Packager.md` for package-time behavior: `buildAsset()`, `buildReplacements()`, asset prelude generation, replacement regex handling, wrapping, and `getSymbolResolution()`.
- Live code usually starts in `packages/transformers/js/core/src/hoist.rs` and `packages/packagers/js/src/ScopeHoistingPackager.js`.
- Useful search terms: `struct Hoist`, `Collect`, `promiseSymbol`, `fold_module`, `fold_expr`, `buildAsset`, `buildReplacements`, `buildAssetPrelude`, `REPLACEMENT_RE`, `hoistedRequires`.

## Graph Storage

- Read `docs/AdjacencyList.md` for the shared graph storage model: adjacency as linked edge lists, `SharedTypeMap`, coalesced hashing, `EdgeTypeMap`, `NodeTypeMap`, resizing, edge records, node records, and reverse traversal.
- Live code usually starts in `packages/core/graph/src/AdjacencyList.js`.
- Useful search terms: `SharedTypeMap`, `EdgeTypeMap`, `NodeTypeMap`, `incomingReverse`, `outgoingReverse`, `resize`, `deleteEdge`, `getAllEdges`.

## Native Binary CI

- Read `docs/Continuous Integration/Native Binary Builds.md` for the native artifact build matrix and local `gh act` testing command.
- Live workflow code may be under `.github/workflows`; confirm with `rg` because CI layout changes over time.
- Useful search terms: `napi`, `build-linux-gnu-x64`, `profile=release`, `macos-latest`, `windows-latest`, `musl`.

## Diagrams

The original bundler diagrams are copied under `docs/BundlerGraphs/` inside this references folder. They are useful when explaining bundle graph states, but inspect the matching markdown first to understand the scenario.
