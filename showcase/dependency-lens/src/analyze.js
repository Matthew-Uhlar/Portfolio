import { readdir, readFile, stat } from 'node:fs/promises';
import path from 'node:path';

const extensions = ['.js', '.mjs', '.cjs', '.jsx', '.ts', '.tsx', '.mts', '.cts'];
const ignored = new Set(['node_modules', '.git', 'coverage', 'dist', 'build']);

// Keep strings intact while removing comments so commented imports stay out.
function withoutComments(source) {
  return source.replace(/("(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*'|`(?:\\.|[^`\\])*`)|\/\*[\s\S]*?\*\/|\/\/[^\n]*/g,
    (match, string) => string ?? ' '.repeat(match.length));
}

export function imports(source) {
  const cleaned = withoutComments(source);
  const pattern = /\b(?:import\s+(?:type\s+)?(?:[^;'"()]*?\s+from\s*)?|export\s+(?:type\s+)?[^;'"()]*?\s+from\s*|require\s*\(\s*|import\s*\(\s*)['"]([^'"\n]+)['"]/g;
  return [...new Set([...cleaned.matchAll(pattern)].map(match => match[1]))].sort();
}

async function collect(root) {
  const result = [];
  async function walk(directory) {
    for (const item of await readdir(directory, { withFileTypes: true })) {
      const filename = path.join(directory, item.name);
      // Symlinks are skipped to keep traversal bounded by the chosen root.
      if (item.isDirectory() && !ignored.has(item.name)) await walk(filename);
      else if (item.isFile() && extensions.includes(path.extname(item.name))) result.push(filename);
    }
  }
  await walk(root);
  return result.sort();
}

function resolveImport(filename, specifier, known) {
  const base = path.resolve(path.dirname(filename), specifier);
  const candidates = [base, ...extensions.map(ext => base + ext), ...extensions.map(ext => path.join(base, 'index' + ext))];
  // TS source commonly imports the .js filename that will exist after compilation.
  const replacement = { '.js': ['.ts', '.tsx'], '.mjs': ['.mts'], '.cjs': ['.cts'] }[path.extname(base)];
  if (replacement) candidates.push(...replacement.map(ext => base.slice(0, -path.extname(base).length) + ext));
  return candidates.find(candidate => known.has(candidate));
}

export function findCycles(nodes) {
  let nextIndex = 0;
  const indices = new Map(), low = new Map(), stack = [], active = new Set(), groups = [];
  function visit(id) {
    indices.set(id, nextIndex); low.set(id, nextIndex++); stack.push(id); active.add(id);
    for (const target of nodes.get(id)) {
      if (!indices.has(target)) { visit(target); low.set(id, Math.min(low.get(id), low.get(target))); }
      else if (active.has(target)) low.set(id, Math.min(low.get(id), indices.get(target)));
    }
    if (low.get(id) === indices.get(id)) {
      const group = [];
      let member;
      do { member = stack.pop(); active.delete(member); group.push(member); } while (member !== id);
      if (group.length > 1 || nodes.get(id).includes(id)) groups.push(group.sort());
    }
  }
  for (const id of nodes.keys()) if (!indices.has(id)) visit(id);
  return groups.sort((a, b) => a[0].localeCompare(b[0]));
}

export async function analyze(root, entry) {
  root = path.resolve(root);
  if (!(await stat(root)).isDirectory()) throw new Error('Root must be a directory');
  const files = await collect(root), known = new Set(files), graph = new Map(), missing = [], external = [];
  const relative = filename => path.relative(root, filename).split(path.sep).join('/');
  for (const filename of files) {
    const targets = [];
    for (const specifier of imports(await readFile(filename, 'utf8'))) {
      if (!specifier.startsWith('./') && !specifier.startsWith('../')) {
        external.push({ file: relative(filename), specifier }); continue;
      }
      const target = resolveImport(filename, specifier, known);
      if (target) targets.push(relative(target));
      else missing.push({ file: relative(filename), specifier });
    }
    graph.set(relative(filename), [...new Set(targets)].sort());
  }
  let included = new Set(graph.keys());
  if (entry) {
    const id = relative(path.resolve(root, entry));
    if (!graph.has(id)) throw new Error('Entry must be a scanned source file inside the root');
    included = new Set();
    const pending = [id];
    while (pending.length) {
      const current = pending.pop();
      if (included.has(current)) continue;
      included.add(current); pending.push(...graph.get(current));
    }
  }
  const selected = new Map([...graph].filter(([id]) => included.has(id)));
  const edges = [...selected].flatMap(([from, targets]) => targets.map(to => ({ from, to })));
  const unresolved = missing.filter(item => included.has(item.file));
  const externalImports = external.filter(item => included.has(item.file));
  const cycles = findCycles(selected);
  return { files: [...selected.keys()], edges, cycles, unresolved, externalImports,
    summary: { files: selected.size, edges: edges.length, cycles: cycles.length, unresolved: unresolved.length, externalImports: externalImports.length } };
}

export function format(report, mode) {
  if (mode === 'json') return JSON.stringify(report, null, 2);
  if (mode === 'mermaid') {
    const ids = new Map(report.files.map((file, i) => [file, `n${i}`]));
    const escape = value => value.replace(/&/g, '&amp;').replace(/"/g, '&quot;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
    return ['graph TD', ...report.files.map(file => `  ${ids.get(file)}["${escape(file)}"]`),
      ...report.edges.map(edge => `  ${ids.get(edge.from)} --> ${ids.get(edge.to)}`)].join('\n');
  }
  return [`Files: ${report.summary.files} | Edges: ${report.summary.edges} | Cycle groups: ${report.summary.cycles} | Unresolved: ${report.summary.unresolved}`,
    ...report.cycles.map(group => `Cycle group: ${group.join(', ')}`),
    ...report.unresolved.map(item => `Unresolved: ${item.file} -> ${item.specifier}`),
    `External imports (not resolved): ${report.summary.externalImports}`].join('\n');
}
