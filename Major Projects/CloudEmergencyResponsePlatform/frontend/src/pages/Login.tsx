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
  const [email, setEmail] = useState('dispatcher@example.com')
  const [password, setPassword] = useState('Dispatch123!')
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
        <div className="brand-mark large">RG</div>
        <h1>Response Grid</h1>
        <p>Keep incidents, resources and response updates in one place.</p>
      </section>

      <form className="login-card" onSubmit={submit}>
        <h2>Sign in</h2>
        <p className="muted">Use the demo dispatcher account to explore the full application.</p>

        <label>
          Email
          <input type="email" value={email} onChange={event => setEmail(event.target.value)} required />
        </label>

        <label>
          Password
          <input type="password" value={password} onChange={event => setPassword(event.target.value)} required />
        </label>

        {error && <div className="error-message">{error}</div>}
        <button className="primary-button" disabled={loading}>
          {loading ? 'Signing in...' : 'Sign in'}
        </button>
      </form>
    </div>
  )
}
