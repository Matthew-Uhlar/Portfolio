import { FormEvent, useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import { api } from '../api'
import { createIncidentConnection } from '../realtime'
import type { Incident, IncidentStatus, ResponseUnit } from '../types'

export default function IncidentDetails() {
  const { id } = useParams()
  const incidentId = Number(id)
  const [incident, setIncident] = useState<Incident | null>(null)
  const [units, setUnits] = useState<ResponseUnit[]>([])
  const [selectedUnit, setSelectedUnit] = useState(0)
  const [status, setStatus] = useState<IncidentStatus>('Reported')
  const [note, setNote] = useState('')
  const [activityNote, setActivityNote] = useState('')
  const role = localStorage.getItem('role')

  function load() {
    api<Incident>(`/incidents/${incidentId}`).then(value => {
      setIncident(value)
      setStatus(value.status)
    })
    api<ResponseUnit[]>('/units').then(values => {
      setUnits(values)
      const available = values.find(value => value.status === 'Available')
      if (available) setSelectedUnit(available.id)
    })
  }

  useEffect(() => {
    load()
    const connection = createIncidentConnection()

    connection.on('IncidentUpdated', load)
    connection.on('ActivityAdded', load)
    connection.on('AssignmentCreated', load)
    connection.on('AssignmentCleared', load)

    connection.start()
      .then(() => connection.invoke('JoinIncidentGroup', incidentId))
      .catch(() => undefined)

    return () => {
      connection.stop()
    }
  }, [incidentId])

  async function updateStatus(event: FormEvent) {
    event.preventDefault()
    await api(`/incidents/${incidentId}/status`, {
      method: 'PATCH',
      body: JSON.stringify({ status, note })
    })
    setNote('')
    load()
  }

  async function assignUnit() {
    if (!selectedUnit) return

    await api('/assignments', {
      method: 'POST',
      body: JSON.stringify({ incidentId, responseUnitId: selectedUnit })
    })
    load()
  }

  async function addActivity(event: FormEvent) {
    event.preventDefault()

    await api(`/incidents/${incidentId}/activity`, {
      method: 'POST',
      body: JSON.stringify({ message: activityNote })
    })

    setActivityNote('')
    load()
  }

  if (!incident) return <p>Loading incident details...</p>

  return (
    <>
      <header className="page-header">
        <div>
          <span className="eyebrow">Incident #{incident.id}</span>
          <h2>{incident.title}</h2>
          <p>{incident.address}</p>
        </div>
        <div className="header-badges">
          <span className={`severity ${incident.severity.toLowerCase()}`}>{incident.severity}</span>
          <span className="status-pill">{incident.status}</span>
        </div>
      </header>

      <section className="details-grid">
        <article className="panel">
          <h3>Incident information</h3>
          <p>{incident.description}</p>
          <dl>
            <div><dt>Reported</dt><dd>{new Date(incident.reportedAt).toLocaleString()}</dd></div>
            <div><dt>Latitude</dt><dd>{incident.latitude}</dd></div>
            <div><dt>Longitude</dt><dd>{incident.longitude}</dd></div>
          </dl>
        </article>

        <article className="panel">
          <h3>Assigned units</h3>
          <div className="list-stack">
            {incident.assignments?.filter(item => !item.clearedAt).map(assignment => (
              <div className="compact-row" key={assignment.id}>
                <div>
                  <strong>{assignment.responseUnit?.unitName ?? `Unit ${assignment.responseUnitId}`}</strong>
                  <span>{assignment.responseUnit?.unitType}</span>
                </div>
                <span>{assignment.responseUnit?.status}</span>
              </div>
            ))}

            {incident.assignments?.filter(item => !item.clearedAt).length === 0 && (
              <p className="muted">No response units are assigned yet.</p>
            )}
          </div>

          {role === 'Dispatcher' && (
            <div className="assign-row">
              <select value={selectedUnit} onChange={event => setSelectedUnit(Number(event.target.value))}>
                <option value={0}>Select an available unit</option>
                {units.filter(unit => unit.status === 'Available').map(unit => (
                  <option value={unit.id} key={unit.id}>{unit.unitName} - {unit.unitType}</option>
                ))}
              </select>
              <button className="secondary-button" onClick={assignUnit}>Assign</button>
            </div>
          )}
        </article>

        <form className="panel form-stack" onSubmit={updateStatus}>
          <h3>Update response status</h3>
          <label>
            Status
            <select value={status} onChange={event => setStatus(event.target.value as IncidentStatus)}>
              <option>Reported</option>
              <option>Dispatched</option>
              <option>OnScene</option>
              <option>Contained</option>
              <option>Closed</option>
            </select>
          </label>
          <label>
            Note
            <textarea rows={3} value={note} onChange={event => setNote(event.target.value)} placeholder="Add context for this status change" />
          </label>
          <button className="primary-button">Save update</button>
        </form>

        <article className="panel">
          <h3>Activity timeline</h3>

          <form className="activity-form" onSubmit={addActivity}>
            <input value={activityNote} onChange={event => setActivityNote(event.target.value)} placeholder="Add an operational note" required />
            <button className="secondary-button">Add</button>
          </form>

          <div className="timeline">
            {incident.activity?.map(activity => (
              <div className="timeline-item" key={activity.id}>
                <div className="timeline-dot" />
                <div>
                  <strong>{activity.message}</strong>
                  <span>{activity.createdBy} · {new Date(activity.createdAt).toLocaleString()}</span>
                </div>
              </div>
            ))}
          </div>
        </article>
      </section>
    </>
  )
}
