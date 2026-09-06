# Dependency Lens

A dependency-free command-line tool that maps local JavaScript and TypeScript imports. It reports circular dependency groups and unresolved relative imports, and can export a graph as JSON or Mermaid.

I wanted a small tool that makes a project's structure easier to inspect before changing it. The implementation is intentionally readable: directory traversal, import extraction, resolution, graph analysis, and presentation are separate steps. It reads source files as text and never executes them.

## Run it

Requires Node.js 24 or later. There are no packages to install.

```sh
node src/cli.js examples/healthy
node src/cli.js examples/cycle --strict
node src/cli.js examples/healthy --format json
node src/cli.js examples/healthy --format mermaid
node src/cli.js /path/to/project --entry src/main.ts
npm test
```

The healthy example has two files and one edge. The cycle example has `a.js` and `b.js` importing each other; these appear as one strongly connected group. Group members are sorted filenames, not a suggested traversal order. A cycle is a reason to inspect the design, not proof that the program fails at runtime.

The root defaults to the current directory. `--entry` selects the reachable graph from one exact source filename relative to that root. The tool still reads the root's source files before filtering the report. `--help` lists options.

Exit codes are `0` for a completed report, `1` for cycles or unresolved imports when `--strict` is enabled, and `2` for invalid arguments or file errors. This makes strict mode useful in CI while allowing exploratory reports to succeed.

## How it works

- Scan `.js`, `.mjs`, `.cjs`, `.jsx`, `.ts`, `.tsx`, `.mts`, and `.cts` files. Skip `node_modules`, `.git`, `dist`, `build`, `coverage`, and symbolic links.
- Extract common static imports, side-effect imports, re-exports, and literal `require()` / `import()` calls. Ignore line and block comments.
- Resolve relative paths against scanned files, known extensions, and directory `index` files. Also try TypeScript source replacements for `.js`, `.mjs`, and `.cjs` imports.
- Use Tarjan's algorithm to find strongly connected components, including self imports. Each distinct resolved file pair counts as one edge.

JSON includes `files`, `edges`, `cycles`, `unresolved`, `externalImports`, and a count `summary`. Mermaid uses generated node IDs so filenames do not become graph identifiers. Text output highlights findings and totals.

## Tradeoffs and limits

This is a lightweight text-based analyzer, not a JavaScript parser or a replacement for the TypeScript compiler. Import-looking text inside strings, templates, or regular expressions can produce false positives; unusual syntax can be missed. Computed imports, template-literal paths, aliases, `tsconfig` paths, package exports, and bundler resolution are unsupported. Type-only imports count as edges. Bare imports (including packages and Node built-ins) are listed as external and are not checked for installation. Relative references outside the chosen root or to non-source assets are reported unresolved.

Resolution uses a documented fixed extension order rather than recreating every runtime's behavior. The recursive traversal and cycle algorithm are intended for small to medium repositories, and very deep graphs can hit JavaScript's call-stack limit. A next improvement would be swapping extraction for a real parser while keeping the graph/report interfaces.

## Checks

`npm test` covers import forms, comment removal, TypeScript and index resolution, excluded directories, reachable entry filtering, a diamond-shaped acyclic graph, multi-file cycles, self imports, output escaping, and CLI exit codes. CI runs the same tests on Node 24. The examples are small enough to verify by hand.

MIT licensed.
