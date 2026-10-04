import { NavLink, Outlet, useNavigate } from 'react-router-dom'
import { clearSession, getSession } from '../api'
import { label } from '../types'

export default function Layout() {
  const navigate = useNavigate()
  const session = getSession()

  function signOut() {
    clearSession()
    navigate('/login')
  }

  return (
    <div className="shell">
      <aside className="sidebar">
        <div className="brand">
          <span className="brand-mark">SF</span>
          <div>
            <strong>SupportFlow</strong>
            <small>Help desk</small>
          </div>
        </div>
        <nav>
          <NavLink to="/" end>Dashboard</NavLink>
          <NavLink to="/tickets" end>{session?.role === 'EMPLOYEE' ? 'My tickets' : 'All tickets'}</NavLink>
          <NavLink to="/tickets/new">New ticket</NavLink>
        </nav>
        <div className="sidebar-footer">
          <span>{session?.name}</span>
          <small>{session ? label(session.role) : ''}</small>
          <button className="link-button" onClick={signOut}>Sign out</button>
        </div>
      </aside>
      <main className="content">
        <Outlet />
      </main>
    </div>
  )
}
