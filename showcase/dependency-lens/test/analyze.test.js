import test from 'node:test';
import assert from 'node:assert/strict';
import { mkdtemp, mkdir, writeFile, rm } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { analyze, imports, findCycles, format } from '../src/analyze.js';

const project = fileURLToPath(new URL('../', import.meta.url));
async function fixture(t, files) {
  const root = await mkdtemp(path.join(os.tmpdir(), 'dependency-lens-'));
  t.after(() => {
    const resolved = path.resolve(root);
    if (path.dirname(resolved) !== path.resolve(os.tmpdir()) || !path.basename(resolved).startsWith('dependency-lens-')) {
      throw new Error('Refusing to remove a directory outside the owned fixture location');
    }
    return rm(resolved, { recursive: true, force: true });
  });
  for (const [name, source] of Object.entries(files)) {
    await mkdir(path.dirname(path.join(root, name)), { recursive: true });
    await writeFile(path.join(root, name), source);
  }
  return root;
}

test('finds supported import forms and ignores commented imports', () => {
  assert.deepEqual(imports(`// import './ignored.js'
    /* require('./ignored2') */
    import './side.js'; import type { Thing } from './types';
    export { thing } from './export';
    const x = require('./common'); const y = import('./lazy');
    import './side.js';`), ['./common', './export', './lazy', './side.js', './types']);
});

test('resolves TypeScript replacements and indexes, separates external imports, never executes files', async t => {
  const root = await fixture(t, {
    'main.ts': `import './lib'; import './types.js'; import 'node:fs'; import './missing'; throw new Error('must not run');`,
    'lib/index.js': 'export const value = 1;', 'types.ts': 'export type Value = string;',
    'node_modules/vendor/a.js': `import './missing';`, 'dist/generated.js': `import './missing';`
  });
  const result = await analyze(root);
  assert.deepEqual(result.summary, { files: 3, edges: 2, cycles: 0, unresolved: 1, externalImports: 1 });
  assert.deepEqual(result.unresolved, [{ file: 'main.ts', specifier: './missing' }]);
  assert.deepEqual(result.edges, [{ from: 'main.ts', to: 'lib/index.js' }, { from: 'main.ts', to: 'types.ts' }]);
});

test('separates import syntax from strings, templates, regexes, and object methods', () => {
  const source = [
    `const message = "import './fake-string'";`,
    "const template = `require('./fake-template')`;",
    `const pattern = /import ['"]fake-regex['"]/;`,
    `object.require('./fake-method');`,
    `// import './fake-comment'`,
    `/* export { x } from './fake-block' */`,
    `import {`, `  thing,`, `  other`, `} from './real-static';`,
    `const lazy = import(/* load later */ './real-dynamic');`,
    `const computed = import('./prefix' + variable);`,
    `export { thing } from './real-export';`
  ].join('\n');
  assert.deepEqual(imports(source), ['./real-dynamic', './real-export', './real-static']);
});

test('entry limits findings to reachable files', async t => {
  const root = await fixture(t, { 'main.js': `import './a.js';`, 'a.js': '', 'unused.js': `import './missing';` });
  const result = await analyze(root, 'main.js');
  assert.deepEqual(result.files, ['a.js', 'main.js']);
  assert.equal(result.unresolved.length, 0);
  await assert.rejects(analyze(root, '../outside.js'), /Entry must/);
});

test('reports strongly connected groups and self loops without mistaking a diamond for a cycle', () => {
  const graph = new Map([['a', ['b', 'c']], ['b', ['d']], ['c', ['d']], ['d', []], ['x', ['y']], ['y', ['x']], ['z', ['z']]]);
  assert.deepEqual(findCycles(graph), [['x', 'y'], ['z']]);
});

test('formats deterministic graph output and escapes labels', () => {
  assert.equal(format({ files: ['a"<.js', 'b.js'], edges: [{ from: 'a"<.js', to: 'b.js' }] }, 'mermaid'),
    'graph TD\n  n0["a&quot;&lt;.js"]\n  n1["b.js"]\n  n0 --> n1');
});

function cli(...args) { return spawnSync(process.execPath, ['src/cli.js', ...args], { cwd: project, encoding: 'utf8' }); }
test('CLI produces valid JSON and healthy strict exit', () => {
  const result = cli('examples/healthy', '--format', 'json', '--strict');
  assert.equal(result.status, 0, result.stderr);
  assert.equal(JSON.parse(result.stdout).summary.edges, 1);
});
test('CLI uses strict findings exit only when requested', () => {
  assert.equal(cli('examples/cycle').status, 0);
  const result = cli('examples/cycle', '--strict');
  assert.equal(result.status, 1); assert.match(result.stdout, /Cycle group: a.js, b.js/);
});
test('CLI rejects invalid input and supports help', () => {
  for (const args of [['--format', 'xml'], ['--entry'], ['--unknown'], ['does-not-exist'], ['.', '.']]) {
    const result = cli(...args); assert.equal(result.status, 2, result.stdout); assert.match(result.stderr, /dependency-lens:/);
  }
  assert.equal(cli('--help').status, 0);
  assert.match(cli('--help').stdout, /Usage:/);
});
