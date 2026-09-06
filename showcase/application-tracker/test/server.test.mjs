import { test } from 'node:test';
import assert from 'node:assert/strict';
import { createServer } from '../server.mjs';

test('serves browser assets and compiled domain while blocking other paths', async () => {
  const server = createServer();
  await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
  const base = `http://127.0.0.1:${server.address().port}`;
  try {
    for (const path of ['/', '/app.js', '/style.css', '/domain.js']) {
      const response = await fetch(base + path);
      assert.equal(response.status, 200);
      assert.equal(response.headers.get('x-content-type-options'), 'nosniff');
      assert.ok((await response.text()).length > 0);
    }
    const domain = await (await fetch(base + '/domain.js')).text();
    const module = await import(`data:text/javascript,${encodeURIComponent(domain)}`);
    assert.deepEqual(module.summarize([]), { Saved: 0, Applied: 0, Interview: 0, Offer: 0, Closed: 0 });
    for (const path of ['/package.json', '/.git/config', '/src/applications.ts', '/%2e%2e/server.mjs']) assert.equal((await fetch(base + path)).status, 404);
    assert.equal((await fetch(base, { method: 'POST' })).status, 405);
    const head = await fetch(base, { method: 'HEAD' }); assert.equal(head.status, 200); assert.equal(await head.text(), '');
  } finally { await new Promise(resolve => server.close(resolve)); }
});
