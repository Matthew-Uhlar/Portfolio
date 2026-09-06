import { statuses, validateApplication, parseBackup, filterApplications, summarize } from '/domain.js';
const $ = selector => document.querySelector(selector);
const key = 'application-tracker-v1';
let applications = [];
let storageHealthy = true;
const backup = rows => JSON.stringify({ version: 1, applications: rows }, null, 2);
function announce(message) { $('#message').textContent = message; }
try { const saved = localStorage.getItem(key); if (saved) applications = parseBackup(saved); }
catch { storageHealthy = false; announce('Saved data could not be loaded. Export any existing browser data or fix storage before saving. This session will not overwrite it.'); }
function save(next) {
  if (!storageHealthy) throw new Error('Storage is unavailable or contains an invalid backup. Clear this site’s storage to start over, or use a different browser profile.');
  localStorage.setItem(key, backup(next));
  applications = next; render();
}
for (const status of statuses) {
  for (const selector of ['#filter', '#status']) { const option = document.createElement('option'); option.value = status; option.textContent = status; $(selector).append(option); }
}
function element(tag, text, className) { const node = document.createElement(tag); node.textContent = text; if (className) node.className = className; return node; }
function render() {
  $('#stats').replaceChildren(...Object.entries(summarize(applications)).map(([status, count]) => {
    const card = element('div', '', 'stat'); card.append(element('span', status), element('strong', String(count))); return card;
  }));
  const visible = filterApplications(applications, $('#search').value, $('#filter').value);
  $('#count').textContent = `${visible.length} of ${applications.length}`;
  $('#list').replaceChildren();
  if (!visible.length) { const empty = element('div', '', 'empty'); empty.append(element('h3', applications.length ? 'No matching applications' : 'Make room for your next opportunity'), element('p', applications.length ? 'Try a different search or status.' : 'Add the first role you want to keep track of.')); $('#list').append(empty); }
  for (const app of visible) {
    const card = element('article', '', 'application');
    const identity = element('div', '', 'identity'); identity.append(element('span', app.company.slice(0, 1).toUpperCase(), 'avatar'));
    const title = element('div', '', 'title'); title.append(element('h3', app.role), element('p', app.company)); identity.append(title);
    const details = element('div', '', 'details'); details.append(element('span', app.status, `badge ${app.status.toLowerCase()}`), element('span', `Updated ${new Date(app.updatedAt).toLocaleDateString()}`, 'date'));
    const edit = element('button', 'Edit'); edit.setAttribute('aria-label', `Edit ${app.role} at ${app.company}`); edit.addEventListener('click', () => openEditor(app)); details.append(edit);
    card.append(identity, details);
    if (app.notes) card.append(element('p', app.notes, 'note'));
    if (app.url) { const link = element('a', 'View job posting ↗', 'job-link'); link.href = app.url; link.target = '_blank'; link.rel = 'noopener noreferrer'; card.append(link); }
    $('#list').append(card);
  }
}
function openEditor(app) {
  $('#form').reset(); $('#form-error').textContent = '';
  $('#editor-title').textContent = app ? 'Edit application' : 'Add application';
  $('#delete').hidden = !app;
  if (app) for (const field of ['id', 'company', 'role', 'status', 'url', 'notes']) $('#form').elements.namedItem(field).value = app[field];
  $('#editor').showModal(); $('#company').focus();
}
$('#new').addEventListener('click', () => openEditor());
$('#close').addEventListener('click', () => $('#editor').close());
$('#search').addEventListener('input', render); $('#filter').addEventListener('change', render);
$('#form').addEventListener('submit', event => {
  event.preventDefault();
  try {
    const data = Object.fromEntries(new FormData($('#form')));
    const app = validateApplication({ ...data, id: data.id || crypto.randomUUID(), updatedAt: new Date().toISOString() });
    if (!data.id && applications.length >= 1000) throw new Error('The tracker supports up to 1,000 applications.');
    save([app, ...applications.filter(item => item.id !== app.id)]); $('#editor').close(); announce('Application saved.');
  } catch (error) { $('#form-error').textContent = error.message; }
});
$('#delete').addEventListener('click', () => {
  if (!confirm('Delete this application? This cannot be undone.')) return;
  try { save(applications.filter(app => app.id !== $('#form').elements.namedItem('id').value)); $('#editor').close(); announce('Application deleted.'); }
  catch (error) { $('#form-error').textContent = error.message; }
});
$('#export').addEventListener('click', () => {
  const url = URL.createObjectURL(new Blob([backup(applications)], { type: 'application/json' }));
  const link = document.createElement('a'); link.href = url; link.download = `applications-${new Date().toISOString().slice(0, 10)}.json`; link.click(); setTimeout(() => URL.revokeObjectURL(url), 1000);
});
$('#import').addEventListener('click', () => $('#file').click());
$('#file').addEventListener('change', async event => {
  const file = event.target.files[0]; if (!file) return;
  try {
    if (file.size > 10_000_000) throw new Error('Choose a backup smaller than 10 MB.');
    const next = parseBackup(await file.text());
    if (!confirm(`Replace ${applications.length} applications with ${next.length} from this backup? Export first if you need the current data.`)) return;
    save(next); announce(`Imported ${next.length} applications.`);
  } catch (error) { announce(`Import failed: ${error.message}`); }
  finally { event.target.value = ''; }
});
window.addEventListener('storage', event => {
  if (event.key !== key && event.key !== null) return;
  try { applications = event.newValue ? parseBackup(event.newValue) : []; render(); announce('Applications updated from another tab.'); }
  catch { storageHealthy = false; announce('Another tab saved invalid data. Reload after restoring storage.'); }
});
render();
