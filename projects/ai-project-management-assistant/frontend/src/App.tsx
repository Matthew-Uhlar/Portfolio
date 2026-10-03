import { Navigate, Route, Routes } from 'react-router-dom'
import Layout from './components/Layout'
import Login from './pages/Login'
import Dashboard from './pages/Dashboard'
import Board from './pages/Board'
import Assistant from './pages/Assistant'
import Backlog from './pages/Backlog'

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
        <Route path="board" element={<Board />} />
        <Route path="backlog" element={<Backlog />} />
        <Route path="assistant" element={<Assistant />} />
      </Route>
    </Routes>
  )
}
