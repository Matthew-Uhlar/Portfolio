export const statuses = ['Saved', 'Applied', 'Interview', 'Offer', 'Closed'] as const;
export type Status = typeof statuses[number];
export type Application = {
  id: string; company: string; role: string; status: Status;
  url: string; notes: string; updatedAt: string;
};

function text(value: unknown, field: string, limit: number, required = false): string {
  if (typeof value !== 'string') throw new Error(`${field} must be text.`);
  const cleaned = value.trim();
  if ((required && !cleaned) || cleaned.length > limit) throw new Error(`${field} must contain ${required ? '1' : '0'}–${limit} characters.`);
  return cleaned;
}

export function validateApplication(value: unknown): Application {
  if (!value || typeof value !== 'object' || Array.isArray(value)) throw new Error('Each application must be an object.');
  const row = value as Record<string, unknown>;
  const id = text(row.id, 'ID', 100, true);
  const company = text(row.company, 'Company', 120, true);
  const role = text(row.role, 'Role', 160, true);
  if (!statuses.includes(row.status as Status)) throw new Error('Choose a valid status.');
  const url = text(row.url, 'URL', 2000);
  if (url) {
    let parsed: URL;
    try { parsed = new URL(url); } catch { throw new Error('Use a complete http or https URL.'); }
    if (!['http:', 'https:'].includes(parsed.protocol)) throw new Error('Use a complete http or https URL.');
  }
  const notes = text(row.notes, 'Notes', 5000);
  const updatedAt = text(row.updatedAt, 'Updated date', 40, true);
  const timestamp = Date.parse(updatedAt);
  if (!/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{3})?Z$/.test(updatedAt) ||
      !Number.isFinite(timestamp) || new Date(timestamp).toISOString() !== updatedAt.replace(/(?<=:\d{2})Z$/, '.000Z')) {
    throw new Error('Updated date must be a valid UTC ISO timestamp.');
  }
  return { id, company, role, status: row.status as Status, url, notes, updatedAt };
}

export function parseBackup(raw: string): Application[] {
  const data = JSON.parse(raw);
  if (data?.version !== 1 || !Array.isArray(data.applications)) throw new Error('Use a version 1 Application Tracker backup.');
  if (data.applications.length > 1000) throw new Error('A backup can contain at most 1,000 applications.');
  const applications = data.applications.map(validateApplication);
  if (new Set(applications.map((app: Application) => app.id)).size !== applications.length) throw new Error('Application IDs must be unique.');
  return applications;
}

export function filterApplications(applications: Application[], query = '', status = 'All'): Application[] {
  const needle = query.trim().toLocaleLowerCase();
  return applications.filter(app => (status === 'All' || app.status === status) &&
    `${app.company} ${app.role} ${app.notes}`.toLocaleLowerCase().includes(needle))
    .sort((a, b) => Date.parse(b.updatedAt) - Date.parse(a.updatedAt) || a.company.localeCompare(b.company));
}

export function summarize(applications: Application[]): Record<Status, number> {
  const totals = Object.fromEntries(statuses.map(status => [status, 0])) as Record<Status, number>;
  for (const app of applications) totals[app.status]++;
  return totals;
}
