import http from 'node:http';
import { readFile } from 'node:fs/promises';
import { stripTypeScriptTypes } from 'node:module';
import { fileURLToPath } from 'node:url';

const routes = new Map([
  ['/', ['public/index.html', 'text/html']],
  ['/app.js', ['public/app.js', 'text/javascript']],
  ['/style.css', ['public/style.css', 'text/css']],
  ['/domain.js', ['src/applications.ts', 'text/javascript']],
]);

export function createServer() {
  return http.createServer(async (request, response) => {
    const headers = { 'X-Content-Type-Options': 'nosniff', 'Cache-Control': 'no-store', 'Content-Security-Policy': "default-src 'self'; object-src 'none'; base-uri 'none'; frame-ancestors 'none'" };
    if (request.method !== 'GET' && request.method !== 'HEAD') { response.writeHead(405, { ...headers, Allow: 'GET, HEAD' }); response.end(); return; }
    const route = routes.get((request.url || '/').split('?')[0]);
    if (!route) { response.writeHead(404, headers); response.end('Not found'); return; }
    try {
      let body = await readFile(new URL(route[0], import.meta.url), 'utf8');
      if (route[0].endsWith('.ts')) body = stripTypeScriptTypes(body);
      response.writeHead(200, { ...headers, 'Content-Type': `${route[1]}; charset=utf-8` });
      response.end(request.method === 'HEAD' ? undefined : body);
    } catch {
      response.writeHead(500, headers); response.end('Unable to load this resource.');
    }
  });
}

if (process.argv[1] && fileURLToPath(import.meta.url) === process.argv[1]) {
  const port = Number(process.env.PORT || 3000);
  const server = createServer();
  server.on('error', error => { console.error(`Unable to start: ${error.message}`); process.exitCode = 1; });
  server.listen(port, '127.0.0.1', () => console.log(`Application Tracker: http://127.0.0.1:${port}`));
}
