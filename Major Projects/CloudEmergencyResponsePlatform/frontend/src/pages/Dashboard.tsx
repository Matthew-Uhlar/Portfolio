import { useEffect, useState } from 'react'
import { api } from '../api'
import IncidentMap from '../components/IncidentMap'
import type { DashboardData } from '../types'

export default function Dashboard() {
  const [data, setData] = useState<DashboardData | null>(null)

  useEffect(() => {
    api<DashboardData>('/dashboard').then(setData)
  }, [])

  if (!data) return <p>Loading the response dashboard...</p>

  return (
    <>
      <header className="page-header">
        <div>
          <span className="eyebrow">Operational overview</span>
          <h2>Emergency Response Dashboard</h2>
          <p>See active incidents and available resources without switching between multiple systems.</p>
        </div>
      </header>

      <section className="metric-grid">
        <article className="metric-card">
          <span>Active incidents</span>
          <strong>{data.activeIncidents}</strong>
          <small>currently open</small>
        </article>
        <article className="metric-card">
          <span>Critical incidents</span>
          <strong>{data.criticalIncidents}</strong>
          <small>need immediate attention</small>
        </article>
        <article className="metric-card">
          <span>Available units</span>
          <strong>{data.availableUnits}</strong>
          <small>ready for assignment</small>
        </article>
        <article className="metric-card">
          <span>Assigned units</span>
          <strong>{data.assignedUnits}</strong>
          <small>currently responding</small>
        </article>
      </section>

      <section className="dashboard-grid">
        <IncidentMap incidents={data.recentlyReported} />
        <article className="panel">
          <span className="eyebrow">Recent reports</span>
          <h3>Latest incidents</h3>
          <div className="list-stack">
            {data.recentlyReported.map(incident => (
              <div className="compact-row" key={incident.id}>
                <div>
                  <strong>{incident.title}</strong>
                  <span>{incident.address}</span>
                </div>
                <span className={`severity ${incident.severity.toLowerCase()}`}>{incident.severity}</span>
              </div>
            ))}
          </div>
        </article>
      </section>
    </>
  )
}
