import { NavLink, Outlet, useNavigate } from 'react-router-dom'

export default function Layout() {
  const navigate = useNavigate()
  const name = localStorage.getItem('name') ?? 'Response team'

  function signOut() {
    localStorage.clear()
    navigate('/login')
  }

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div>
          <div className="brand-mark">RG</div>
          <h1>Response Grid</h1>
          <p className="sidebar-copy">A shared view of incidents, resources and response activity.</p>
        </div>

        <nav>
          <NavLink to="/" end>Overview</NavLink>
          <NavLink to="/incidents">Incidents</NavLink>
          <NavLink to="/units">Response Units</NavLink>
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
