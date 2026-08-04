import { useEffect, useState } from 'react'
import { api } from '../api'
import { useProject } from '../hooks'
import type { DashboardData } from '../types'

export default function Dashboard() {
  const { project, loading } = useProject()
  const [data, setData] = useState<DashboardData | null>(null)

  useEffect(() => {
    if (project) {
      api<DashboardData>(`/dashboard/${project.id}`).then(setData)
    }
  }, [project])

  if (loading || !data || !project) return <p>Loading the project...</p>

  return (
    <>
      <header className="page-header">
        <div>
          <span className="eyebrow">Project overview</span>
          <h2>{project.name}</h2>
          <p>{project.goal}</p>
        </div>
      </header>

      <section className="metric-grid">
        <article className="metric-card">
          <span>Total work</span>
          <strong>{data.totalItems}</strong>
          <small>items in this project</small>
        </article>
        <article className="metric-card">
          <span>Completed</span>
          <strong>{data.completedItems}</strong>
          <small>items finished</small>
        </article>
        <article className="metric-card">
          <span>In motion</span>
          <strong>{data.activeItems}</strong>
          <small>active or in review</small>
        </article>
        <article className="metric-card">
          <span>Backlog size</span>
          <strong>{data.backlogPoints}</strong>
          <small>story points waiting</small>
        </article>
      </section>

      <section className="two-column">
        <article className="panel">
          <span className="eyebrow">Active sprint</span>
          <h3>{data.activeSprint?.name ?? 'No active sprint'}</h3>
          <p>{data.activeSprint?.goal ?? 'Create a sprint to start tracking the current goal.'}</p>
          {data.activeSprint && (
            <div className="date-row">
              <span>{new Date(data.activeSprint.startDate).toLocaleDateString()}</span>
              <span>through</span>
              <span>{new Date(data.activeSprint.endDate).toLocaleDateString()}</span>
            </div>
          )}
        </article>

        <article className="panel">
          <span className="eyebrow">Needs attention</span>
          <h3>{data.criticalItems} critical items</h3>
          <p>
            {data.criticalItems > 0
              ? 'The project has critical work that still needs to be completed.'
              : 'Nothing is marked critical right now. Keep priorities updated as the project changes.'}
          </p>
        </article>
      </section>
    </>
  )
}
