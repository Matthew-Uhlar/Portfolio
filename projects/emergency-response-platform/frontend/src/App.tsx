import { Navigate, Route, Routes } from 'react-router-dom'
import Layout from './components/Layout'
import Login from './pages/Login'
import Dashboard from './pages/Dashboard'
import Incidents from './pages/Incidents'
import Units from './pages/Units'
import IncidentDetails from './pages/IncidentDetails'

function PrivatePage({ children }: { children: React.ReactNode }) {
  return localStorage.getItem('token') ? children : <Navigate to="/login" replace />
}

export default function App() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route
        path="/"
        element={
          <PrivatePage>
            <Layout />
          </PrivatePage>
        }
      >
        <Route index element={<Dashboard />} />
        <Route path="incidents" element={<Incidents />} />
        <Route path="incidents/:id" element={<IncidentDetails />} />
        <Route path="units" element={<Units />} />
      </Route>
    </Routes>
  )
}
