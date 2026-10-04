import { FormEvent, useCallback, useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import { api, getSession } from '../api'
import { PriorityBadge, StatusBadge, formatDate } from '../components/Badges'
import { label, priorities, statuses, type AssignableUser, type Ticket, type TicketPriority, type TicketStatus } from '../types'

export default function TicketDetail() {
  const { id } = useParams()
  const session = getSession()
  const isStaff = session?.role === 'TECHNICIAN' || session?.role === 'ADMIN'
  const [ticket, setTicket] = useState<Ticket | null>(null)
  const [people, setPeople] = useState<AssignableUser[]>([])
  const [message, setMessage] = useState('')
  const [internal, setInternal] = useState(false)
  const [busy, setBusy] = useState('')
  const [error, setError] = useState('')

  const load = useCallback(() => {
    return api<Ticket>(`/tickets/${id}`).then(setTicket).catch(err => setError(err.message))
  }, [id])

  useEffect(() => {
    load()
    if (isStaff) {
      api<AssignableUser[]>('/users/assignable').then(setPeople).catch(() => setPeople([]))
    }
  }, [load, isStaff])

  async function update(change: { status?: TicketStatus; priority?: TicketPriority; assignedToUserId?: number }) {
    setBusy('update')
    setError('')
    try {
      await api<Ticket>(`/tickets/${id}`, { method: 'PATCH', body: JSON.stringify(change) })
      await load()
    } catch (err) {
      setError(err instanceof Error ? err.message : 'The ticket could not be updated.')
    } finally {
      setBusy('')
    }
  }

  async function addComment(event: FormEvent) {
    event.preventDefault()
    setBusy('comment')
    setError('')
    try {
      await api(`/tickets/${id}/comments`, { method: 'POST', body: JSON.stringify({ message, internal }) })
      setMessage('')
      setInternal(false)
      await load()
    } catch (err) {
      setError(err instanceof Error ? err.message : 'The comment could not be added.')
    } finally {
      setBusy('')
    }
  }

  if (!ticket) {
    return (
      <section className="panel">
        {error ? <p className="error-message" role="alert">{error}</p> : <p className="muted">Loading ticket...</p>}
        <Link to="/tickets">Back to tickets</Link>
      </section>
    )
  }

  return (
    <>
      <header className="page-header">
        <div>
          <Link className="eyebrow" to="/tickets">Tickets</Link>
          <h1>#{ticket.id} {ticket.title}</h1>
          <div className="badge-row">
            <StatusBadge status={ticket.status} />
            <PriorityBadge priority={ticket.priority} />
          </div>
        </div>
      </header>

      {error && <p className="error-message" role="alert">{error}</p>}

      <div className="detail-grid">
        <div className="detail-main">
          <section className="panel">
            <h2>Description</h2>
            <p className="description">{ticket.description}</p>
            <p className="muted">Opened by {ticket.createdBy.name} on {formatDate(ticket.createdAt)}</p>
          </section>

          <section className="panel">
            <h2>Conversation</h2>
            {ticket.comments.length === 0 && <p className="muted">No comments yet.</p>}
            <ul className="comments">
              {[...ticket.comments].reverse().map(comment => (
                <li key={comment.id} className={comment.internal ? 'internal' : ''}>
                  <div className="comment-meta">
                    <strong>{comment.author.name}</strong>
                    {comment.internal && <span className="badge internal-badge">Internal note</span>}
                    <small className="muted">{formatDate(comment.createdAt)}</small>
                  </div>
                  <p>{comment.message}</p>
                </li>
              ))}
            </ul>
            <form className="form-stack" onSubmit={addComment}>
              <textarea rows={3} value={message} onChange={event => setMessage(event.target.value)} placeholder={isStaff ? 'Reply to the requester or add a note' : 'Add more detail or reply to IT'} required aria-label="Comment" />
              <div className="button-row">
                {isStaff && (
                  <label className="checkbox">
                    <input type="checkbox" checked={internal} onChange={event => setInternal(event.target.checked)} />
                    Internal note (hidden from the requester)
                  </label>
                )}
                <button className="primary-button" disabled={busy === 'comment'}>{busy === 'comment' ? 'Posting...' : 'Post'}</button>
              </div>
            </form>
          </section>
        </div>

        <aside className="detail-side">
          <section className="panel">
            <h2>Details</h2>
            <dl>
              <dt>Requester</dt>
              <dd>{ticket.createdBy.name}</dd>
              <dt>Assigned to</dt>
              <dd>{ticket.assignedTo?.name ?? 'Unassigned'}</dd>
              <dt>Last updated</dt>
              <dd>{formatDate(ticket.updatedAt)}</dd>
              {ticket.resolvedAt && (
                <>
                  <dt>Resolved</dt>
                  <dd>{formatDate(ticket.resolvedAt)}</dd>
                </>
              )}
            </dl>
          </section>

          {isStaff && (
            <section className="panel form-stack">
              <h2>Work this ticket</h2>
              <label>
                Status
                <select value={ticket.status} disabled={busy === 'update'} onChange={event => update({ status: event.target.value as TicketStatus })}>
                  {statuses.map(value => <option key={value} value={value}>{label(value)}</option>)}
                </select>
              </label>
              <label>
                Priority
                <select value={ticket.priority} disabled={busy === 'update'} onChange={event => update({ priority: event.target.value as TicketPriority })}>
                  {priorities.map(value => <option key={value} value={value}>{label(value)}</option>)}
                </select>
              </label>
              <label>
                Assign to
                <select value={ticket.assignedTo?.id ?? ''} disabled={busy === 'update'} onChange={event => event.target.value && update({ assignedToUserId: Number(event.target.value) })}>
                  <option value="">Choose a person</option>
                  {people.map(person => <option key={person.id} value={person.id}>{person.name} ({label(person.role)})</option>)}
                </select>
              </label>
            </section>
          )}

          <section className="panel">
            <h2>History</h2>
            <ol className="timeline">
              {ticket.history.map(entry => (
                <li key={entry.id}>
                  <span>{entry.changeDescription}</span>
                  <small className="muted">{entry.changedBy.name} · {formatDate(entry.createdAt)}</small>
                </li>
              ))}
            </ol>
          </section>
        </aside>
      </div>
    </>
  )
}
