import { FormEvent, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { api, saveSession } from '../api'
import type { Session } from '../types'

const demoAccounts = [
  { label: 'Employee', email: 'employee@example.com', password: 'Employee123!' },
  { label: 'Technician', email: 'tech@example.com', password: 'Tech123!' },
  { label: 'Admin', email: 'admin@example.com', password: 'Admin123!' }
]

export default function Login() {
  const navigate = useNavigate()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [busy, setBusy] = useState(false)

  async function signIn(event?: FormEvent, account?: { email: string; password: string }) {
    event?.preventDefault()
    setBusy(true)
    setError('')
    try {
      const session = await api<Session>('/auth/login', {
        method: 'POST',
        body: JSON.stringify(account ?? { email, password })
      })
      saveSession(session)
      navigate('/')
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Sign in failed.')
    } finally {
      setBusy(false)
    }
  }

  return (
    <div className="login-page">
      <section className="login-card">
        <div className="brand">
          <span className="brand-mark">SF</span>
          <div>
            <strong>SupportFlow</strong>
            <small>IT help desk and service requests</small>
          </div>
        </div>

        <form className="form-stack" onSubmit={signIn}>
          <label>
            Email
            <input type="email" value={email} onChange={event => setEmail(event.target.value)} required autoComplete="username" />
          </label>
          <label>
            Password
            <input type="password" value={password} onChange={event => setPassword(event.target.value)} required autoComplete="current-password" />
          </label>
          {error && <p className="error-message" role="alert">{error}</p>}
          <button className="primary-button" disabled={busy}>{busy ? 'Signing in...' : 'Sign in'}</button>
        </form>

        <div className="demo-accounts">
          <span>Try a demo account</span>
          <div>
            {demoAccounts.map(account => (
              <button key={account.label} className="secondary-button" disabled={busy} onClick={() => signIn(undefined, account)}>
                {account.label}
              </button>
            ))}
          </div>
        </div>
      </section>
    </div>
  )
}
