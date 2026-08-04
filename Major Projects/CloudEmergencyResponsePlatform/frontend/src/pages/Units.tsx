import { FormEvent, useEffect, useState } from 'react'
import { api } from '../api'
import { createIncidentConnection } from '../realtime'
import type { ResponseUnit, UnitStatus } from '../types'

export default function Units() {
  const [units, setUnits] = useState<ResponseUnit[]>([])
  const [name, setName] = useState('')
  const [type, setType] = useState('')
  const [code, setCode] = useState('')
  const [location, setLocation] = useState('')
  const role = localStorage.getItem('role')

  function load() {
    api<ResponseUnit[]>('/units').then(setUnits)
  }

  useEffect(() => {
    load()
    const connection = createIncidentConnection()
    connection.on('UnitUpdated', load)
    connection.start().catch(() => undefined)

    return () => {
      connection.stop()
    }
  }, [])

  async function create(event: FormEvent) {
    event.preventDefault()

    await api('/units', {
      method: 'POST',
      body: JSON.stringify({
        unitName: name,
        unitType: type,
        radioCode: code,
        currentLocation: location
      })
    })

    setName('')
    setType('')
    setCode('')
    setLocation('')
    load()
  }

  async function updateStatus(unit: ResponseUnit, status: UnitStatus) {
    await api(`/units/${unit.id}/status`, {
      method: 'PATCH',
      body: JSON.stringify({
        status,
        currentLocation: unit.currentLocation
      })
    })
    load()
  }

  return (
    <>
      <header className="page-header">
        <div>
          <span className="eyebrow">Resource management</span>
          <h2>Response Units</h2>
          <p>Keep vehicle and team availability current for dispatch decisions.</p>
        </div>
      </header>

      <section className="unit-layout">
        {role === 'Dispatcher' && (
          <form className="panel form-stack" onSubmit={create}>
            <h3>Add a response unit</h3>
            <label>
              Unit name
              <input value={name} onChange={event => setName(event.target.value)} required />
            </label>
            <label>
              Unit type
              <input value={type} onChange={event => setType(event.target.value)} required />
            </label>
            <label>
              Radio code
              <input value={code} onChange={event => setCode(event.target.value)} required />
            </label>
            <label>
              Current location
              <input value={location} onChange={event => setLocation(event.target.value)} required />
            </label>
            <button className="primary-button">Add unit</button>
          </form>
        )}

        <div className="unit-grid">
          {units.map(unit => (
            <article className="panel unit-card" key={unit.id}>
              <div className="card-topline">
                <span className="unit-code">{unit.radioCode}</span>
                <span className={`unit-status ${unit.status.toLowerCase()}`}>{unit.status}</span>
              </div>
              <h3>{unit.unitName}</h3>
              <p>{unit.unitType}</p>
              <small>{unit.currentLocation}</small>

              <select value={unit.status} onChange={event => updateStatus(unit, event.target.value as UnitStatus)}>
                <option>Available</option>
                <option>Assigned</option>
                <option>EnRoute</option>
                <option>OnScene</option>
                <option>Unavailable</option>
              </select>
            </article>
          ))}
        </div>
      </section>
    </>
  )
}
