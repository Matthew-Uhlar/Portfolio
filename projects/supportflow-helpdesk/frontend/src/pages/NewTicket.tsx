import { FormEvent, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { api } from '../api'
import { label, priorities, type Ticket, type TicketPriority } from '../types'

export default function NewTicket() {
  const navigate = useNavigate()
  const [title, setTitle] = useState('')
  const [description, setDescription] = useState('')
  const [priority, setPriority] = useState<TicketPriority>('MEDIUM')
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState('')

  async function submit(event: FormEvent) {
    event.preventDefault()
    setBusy(true)
    setError('')
    try {
      const ticket = await api<Ticket>('/tickets', {
        method: 'POST',
        body: JSON.stringify({ title, description, priority })
      })
      navigate(`/tickets/${ticket.id}`)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'The ticket could not be created.')
      setBusy(false)
    }
  }

  return (
    <>
      <header className="page-header">
        <div>
          <span className="eyebrow">Get help from IT</span>
          <h1>New ticket</h1>
        </div>
      </header>

      <form className="panel form-stack narrow" onSubmit={submit}>
        <label>
          What do you need help with?
          <input value={title} onChange={event => setTitle(event.target.value)} placeholder="Example: Laptop will not connect to Wi-Fi" maxLength={200} required />
        </label>
        <label>
          Details
          <textarea rows={6} value={description} onChange={event => setDescription(event.target.value)} placeholder="What happened, when it started and anything you already tried" maxLength={4000} required />
        </label>
        <label>
          Priority
          <select value={priority} onChange={event => setPriority(event.target.value as TicketPriority)}>
            {priorities.map(value => <option key={value} value={value}>{label(value)}</option>)}
          </select>
        </label>
        <p className="muted">Use Critical only when work is stopped for several people.</p>
        {error && <p className="error-message" role="alert">{error}</p>}
        <div className="button-row">
          <button className="primary-button" disabled={busy}>{busy ? 'Submitting...' : 'Submit ticket'}</button>
          <button type="button" className="secondary-button" onClick={() => navigate(-1)}>Cancel</button>
        </div>
      </form>
    </>
  )
}
