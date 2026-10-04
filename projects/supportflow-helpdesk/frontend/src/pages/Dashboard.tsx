import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { api, getSession } from '../api'
import { PriorityBadge, StatusBadge, formatDate } from '../components/Badges'
import type { Dashboard as DashboardData, Ticket } from '../types'

export default function Dashboard() {
  const session = getSession()
  const isEmployee = session?.role === 'EMPLOYEE'
  const [stats, setStats] = useState<DashboardData | null>(null)
  const [tickets, setTickets] = useState<Ticket[]>([])
  const [error, setError] = useState('')

  useEffect(() => {
    api<Ticket[]>('/tickets').then(setTickets).catch(err => setError(err.message))
    if (!isEmployee) {
      api<DashboardData>('/dashboard').then(setStats).catch(err => setError(err.message))
    }
  }, [isEmployee])

  const open = tickets.filter(ticket => ticket.status !== 'CLOSED' && ticket.status !== 'RESOLVED')
  const cards = isEmployee
    ? [
        { label: 'My open tickets', value: open.length },
        { label: 'Waiting on me', value: tickets.filter(ticket => ticket.status === 'WAITING_ON_USER').length },
        { label: 'Resolved', value: tickets.filter(ticket => ticket.status === 'RESOLVED').length },
        { label: 'All my tickets', value: tickets.length }
      ]
    : [
        { label: 'Open tickets', value: stats?.openTickets ?? 0 },
        { label: 'Critical and open', value: stats?.criticalTickets ?? 0 },
        { label: 'Resolved', value: stats?.resolvedTickets ?? 0 },
        { label: 'Total tickets', value: stats?.totalTickets ?? 0 }
      ]

  const queue = isEmployee
    ? open
    : open.filter(ticket => !ticket.assignedTo || ticket.priority === 'CRITICAL')

  return (
    <>
      <header className="page-header">
        <div>
          <span className="eyebrow">Welcome back, {session?.name}</span>
          <h1>Dashboard</h1>
        </div>
        <Link className="primary-button" to="/tickets/new">New ticket</Link>
      </header>

      {error && <p className="error-message" role="alert">{error}</p>}

      <section className="stat-grid">
        {cards.map(card => (
          <article className="stat-card" key={card.label}>
            <span>{card.label}</span>
            <strong>{card.value}</strong>
          </article>
        ))}
      </section>

      <section className="panel">
        <h2>{isEmployee ? 'Your open tickets' : 'Needs attention: unassigned or critical'}</h2>
        {queue.length === 0 ? (
          <p className="muted">Nothing here right now.</p>
        ) : (
          <ul className="ticket-list">
            {queue.map(ticket => (
              <li key={ticket.id}>
                <Link to={`/tickets/${ticket.id}`}>
                  <span className="ticket-id">#{ticket.id}</span>
                  <span className="ticket-title">{ticket.title}</span>
                  <PriorityBadge priority={ticket.priority} />
                  <StatusBadge status={ticket.status} />
                  <small className="muted">{formatDate(ticket.createdAt)}</small>
                </Link>
              </li>
            ))}
          </ul>
        )}
      </section>
    </>
  )
}
