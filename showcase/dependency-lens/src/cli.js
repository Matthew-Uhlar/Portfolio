#!/usr/bin/env node
import { analyze, format } from './analyze.js';

const help = `Usage: node src/cli.js [root] [--entry file] [--format text|json|mermaid] [--strict]

Inspect local JavaScript and TypeScript imports without executing source files.
Root defaults to the current directory. Entry is relative to root.
--strict returns exit code 1 for cycles or unresolved relative imports.
Exit codes: 0 success, 1 strict findings, 2 invalid input or read failure.
--help, -h shows this message.`;

try {
  const args = process.argv.slice(2);
  if (args.includes('--help') || args.includes('-h')) console.log(help);
  else {
    let root, entry, mode = 'text', strict = false;
    while (args.length) {
      const arg = args.shift();
      if (arg === '--strict') strict = true;
      else if (arg === '--entry' || arg === '--format') {
        const value = args.shift();
        if (!value || value.startsWith('--')) throw new Error(`Missing value for ${arg}`);
        if (arg === '--entry') entry = value; else mode = value;
      } else if (arg.startsWith('-')) throw new Error(`Unknown option: ${arg}`);
      else if (root !== undefined) throw new Error('Only one root directory is supported');
      else root = arg;
    }
    if (!['text', 'json', 'mermaid'].includes(mode)) throw new Error('Format must be text, json, or mermaid');
    const report = await analyze(root ?? '.', entry);
    console.log(format(report, mode));
    if (strict && (report.cycles.length || report.unresolved.length)) process.exitCode = 1;
  }
} catch (error) {
  console.error(`dependency-lens: ${error.message}`);
  process.exitCode = 2;
}
