import { test } from 'node:test';
import assert from 'node:assert/strict';
import { validateApplication, parseBackup, filterApplications, summarize } from '../src/applications.ts';
const row = (overrides = {}) => ({ id: 'one', company: ' Acme ', role: 'Developer', status: 'Applied', url: '', notes: '', updatedAt: '2026-01-01T00:00:00.000Z', ...overrides });
test('normalizes text and strips unknown fields', () => {
  const result = validateApplication(row({ extra: true }));
  assert.equal(result.company, 'Acme'); assert.equal('extra' in result, false);
});
test('rejects invalid fields and executable links', () => {
  for (const invalid of [null, [], row({ company: ' ' }), row({ status: 'Hired' }), row({ url: 'javascript:alert(1)' }), row({ notes: 'a'.repeat(5001) }), row({ updatedAt: 'yesterday' })]) {
    assert.throws(() => validateApplication(invalid));
  }
});
test('backup validation is all-or-nothing and rejects duplicate IDs', () => {
  const backup = applications => JSON.stringify({ version: 1, applications });
  assert.equal(parseBackup(backup([row()])).length, 1);
  assert.throws(() => parseBackup(backup([row(), row()])));
  assert.throws(() => parseBackup(backup([row(), row({ id: 'two', status: 'invalid' })])));
  assert.throws(() => parseBackup('{'));
  assert.throws(() => parseBackup(JSON.stringify({ version: 2, applications: [] })));
  assert.throws(() => parseBackup(backup(Array.from({ length: 1001 }, (_, id) => row({ id: String(id) })))));
});
test('filters across notes, status, and sorts without mutating input', () => {
  const applications = [row(), row({ id: 'two', company: 'Beta', notes: 'REMOTE', status: 'Interview', updatedAt: '2026-02-01T00:00:00Z' })];
  assert.deepEqual(filterApplications(applications, 'remote', 'Interview').map(a => a.id), ['two']);
  assert.equal(filterApplications(applications)[0].id, 'two'); assert.equal(applications[0].id, 'one');
  assert.equal(filterApplications(applications, 'remote', 'Applied').length, 0);
});
test('summary includes zero counts', () => assert.deepEqual(summarize([row()]), { Saved: 0, Applied: 1, Interview: 0, Offer: 0, Closed: 0 }));
test('dates reject calendar rollover and accept canonical UTC timestamps', () => {
  for (const updatedAt of ['2026-02-30T00:00:00.000Z', '2026-01-01T24:00:00Z', '2026-01-01T00:00:00+02:00', '2026-01-01T00:00:00.1Z']) {
    assert.throws(() => validateApplication(row({ updatedAt })));
  }
  for (const updatedAt of ['2024-02-29T12:30:01Z', '2026-01-01T00:00:00.123Z']) {
    assert.equal(validateApplication(row({ updatedAt })).updatedAt, updatedAt);
  }
});
