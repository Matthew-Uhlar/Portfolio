import { NavLink, Outlet, useNavigate } from 'react-router-dom'

export default function Layout() {
  const navigate = useNavigate()
  const name = localStorage.getItem('name') ?? 'Team member'

  function signOut() {
    localStorage.clear()
    navigate('/login')
  }

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div>
          <div className="brand-mark">PP</div>
          <h1>Project Pilot</h1>
          <p className="muted sidebar-copy">Planning tools that help the team spend less time on busywork.</p>
        </div>

        <nav>
          <NavLink to="/" end>Overview</NavLink>
          <NavLink to="/board">Sprint Board</NavLink>
          <NavLink to="/backlog">Backlog</NavLink>
          <NavLink to="/assistant">AI Assistant</NavLink>
        </nav>

        <div className="profile">
          <strong>{name}</strong>
          <button className="link-button" onClick={signOut}>Sign out</button>
        </div>
      </aside>

      <main className="main-content">
        <Outlet />
      </main>
    </div>
  )
}
