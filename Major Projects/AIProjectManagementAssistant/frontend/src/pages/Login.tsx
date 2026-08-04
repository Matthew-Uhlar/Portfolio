import { FormEvent, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { api } from '../api'

type LoginResponse = {
  token: string
  name: string
  role: string
}

export default function Login() {
  const navigate = useNavigate()
  const [email, setEmail] = useState('admin@example.com')
  const [password, setPassword] = useState('Admin123!')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  async function submit(event: FormEvent) {
    event.preventDefault()
    setError('')
    setLoading(true)

    try {
      const result = await api<LoginResponse>('/auth/login', {
        method: 'POST',
        body: JSON.stringify({ email, password })
      })

      localStorage.setItem('token', result.token)
      localStorage.setItem('name', result.name)
      localStorage.setItem('role', result.role)
      navigate('/')
    } catch (problem) {
      setError(problem instanceof Error ? problem.message : 'I could not sign you in.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="login-page">
      <section className="login-intro">
        <div className="brand-mark large">PP</div>
        <h1>Project Pilot</h1>
        <p>Manage the work. Use AI where it actually saves time.</p>
      </section>

      <form className="login-card" onSubmit={submit}>
        <h2>Welcome back</h2>
        <p className="muted">Use the demo account or sign in with your own credentials.</p>

        <label>
          Email
          <input value={email} onChange={event => setEmail(event.target.value)} type="email" required />
        </label>

        <label>
          Password
          <input value={password} onChange={event => setPassword(event.target.value)} type="password" required />
        </label>

        {error && <div className="error-message">{error}</div>}
        <button className="primary-button" disabled={loading}>
          {loading ? 'Signing in...' : 'Sign in'}
        </button>
      </form>
    </div>
  )
}
