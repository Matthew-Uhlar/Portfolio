import { FormEvent, useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { api } from '../api'
import { createIncidentConnection } from '../realtime'
import type { Incident, IncidentSeverity } from '../types'

export default function Incidents() {
  const [incidents, setIncidents] = useState<Incident[]>([])
  const [title, setTitle] = useState('')
  const [description, setDescription] = useState('')
  const [address, setAddress] = useState('')
  const [latitude, setLatitude] = useState(30.2672)
  const [longitude, setLongitude] = useState(-97.7431)
  const [severity, setSeverity] = useState<IncidentSeverity>('Moderate')
  const role = localStorage.getItem('role')

  function load() {
    api<Incident[]>('/incidents').then(setIncidents)
  }

  useEffect(() => {
    load()
    const connection = createIncidentConnection()

    connection.on('IncidentCreated', load)
    connection.on('IncidentUpdated', load)
    connection.on('AssignmentCreated', load)
    connection.on('AssignmentCleared', load)
    connection.start().catch(() => undefined)

    return () => {
      connection.stop()
    }
  }, [])

  async function create(event: FormEvent) {
    event.preventDefault()

    await api<Incident>('/incidents', {
      method: 'POST',
      body: JSON.stringify({ title, description, address, latitude, longitude, severity })
    })

    setTitle('')
    setDescription('')
    setAddress('')
    load()
  }

  return (
    <>
      <header className="page-header">
        <div>
          <span className="eyebrow">Incident management</span>
          <h2>Incidents</h2>
          <p>Create new reports and keep the response status current.</p>
        </div>
      </header>

      <section className="incident-layout">
        {role === 'Dispatcher' && (
          <form className="panel form-stack" onSubmit={create}>
            <h3>Create an incident</h3>

            <label>
              Title
              <input value={title} onChange={event => setTitle(event.target.value)} required />
            </label>

            <label>
              Description
              <textarea value={description} onChange={event => setDescription(event.target.value)} rows={4} required />
            </label>

            <label>
              Address
              <input value={address} onChange={event => setAddress(event.target.value)} required />
            </label>

            <div className="form-row">
              <label>
                Latitude
                <input type="number" step="any" value={latitude} onChange={event => setLatitude(Number(event.target.value))} />
              </label>

              <label>
                Longitude
                <input type="number" step="any" value={longitude} onChange={event => setLongitude(Number(event.target.value))} />
              </label>
            </div>

            <label>
              Severity
              <select value={severity} onChange={event => setSeverity(event.target.value as IncidentSeverity)}>
                <option>Low</option>
                <option>Moderate</option>
                <option>High</option>
                <option>Critical</option>
              </select>
            </label>

            <button className="primary-button">Create incident</button>
          </form>
        )}

        <div className="list-stack">
          {incidents.map(incident => (
            <Link to={`/incidents/${incident.id}`} className="incident-card" key={incident.id}>
              <div>
                <div className="card-topline">
                  <span className={`severity ${incident.severity.toLowerCase()}`}>{incident.severity}</span>
                  <span className="status-pill">{incident.status}</span>
                </div>
                <h3>{incident.title}</h3>
                <p>{incident.description}</p>
                <small>{incident.address}</small>
              </div>

              <div className="incident-meta">
                <strong>{incident.assignments?.filter(item => !item.clearedAt).length ?? 0}</strong>
                <span>assigned units</span>
              </div>
            </Link>
          ))}
        </div>
      </section>
    </>
  )
}
