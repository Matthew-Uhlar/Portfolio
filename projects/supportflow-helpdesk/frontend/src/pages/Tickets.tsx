import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { api, getSession } from '../api'
import { PriorityBadge, StatusBadge, formatDate } from '../components/Badges'
import { label, priorities, statuses, type Ticket } from '../types'

export default function Tickets() {
  const isEmployee = getSession()?.role === 'EMPLOYEE'
  const [tickets, setTickets] = useState<Ticket[]>([])
  const [status, setStatus] = useState('')
  const [priority, setPriority] = useState('')
  const [search, setSearch] = useState('')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    // The API filters by one field at a time, so load everything once and filter here.
    api<Ticket[]>('/tickets')
      .then(values => setTickets([...values].sort((a, b) => b.createdAt.localeCompare(a.createdAt))))
      .catch(err => setError(err.message))
      .finally(() => setLoading(false))
  }, [])

  const term = search.trim().toLowerCase()
  const visible = tickets.filter(ticket =>
    (!status || ticket.status === status) &&
    (!priority || ticket.priority === priority) &&
    (!term || ticket.title.toLowerCase().includes(term) || String(ticket.id) === term.replace('#', '')))

  return (
    <>
      <header className="page-header">
        <div>
          <span className="eyebrow">{isEmployee ? 'Requests you opened' : 'Every request in the queue'}</span>
          <h1>{isEmployee ? 'My tickets' : 'All tickets'}</h1>
        </div>
        <Link className="primary-button" to="/tickets/new">New ticket</Link>
      </header>

      <section className="filters">
        <input placeholder="Search by title or #id" value={search} onChange={event => setSearch(event.target.value)} aria-label="Search tickets" />
        <select value={status} onChange={event => setStatus(event.target.value)} aria-label="Filter by status">
          <option value="">Any status</option>
          {statuses.map(value => <option key={value} value={value}>{label(value)}</option>)}
        </select>
        <select value={priority} onChange={event => setPriority(event.target.value)} aria-label="Filter by priority">
          <option value="">Any priority</option>
          {priorities.map(value => <option key={value} value={value}>{label(value)}</option>)}
        </select>
      </section>

      {error && <p className="error-message" role="alert">{error}</p>}

      <section className="panel table-panel">
        {loading ? (
          <p className="muted">Loading tickets...</p>
        ) : visible.length === 0 ? (
          <p className="muted">No tickets match these filters.</p>
        ) : (
          <table>
            <thead>
              <tr>
                <th>#</th>
                <th>Title</th>
                <th>Priority</th>
                <th>Status</th>
                <th>Requester</th>
                <th>Assigned to</th>
                <th>Opened</th>
              </tr>
            </thead>
            <tbody>
              {visible.map(ticket => (
                <tr key={ticket.id}>
                  <td>{ticket.id}</td>
                  <td><Link to={`/tickets/${ticket.id}`}>{ticket.title}</Link></td>
                  <td><PriorityBadge priority={ticket.priority} /></td>
                  <td><StatusBadge status={ticket.status} /></td>
                  <td>{ticket.createdBy.name}</td>
                  <td>{ticket.assignedTo?.name ?? <span className="muted">Unassigned</span>}</td>
                  <td>{formatDate(ticket.createdAt)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </section>
    </>
  )
}
