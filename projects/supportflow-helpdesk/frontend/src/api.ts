import type { Session } from './types'

const sessionKey = 'supportflow-session'

export function getSession(): Session | null {
  const raw = localStorage.getItem(sessionKey)
  if (!raw) return null

  const session = JSON.parse(raw) as Session
  if (isExpired(session.token)) {
    // Spring Security answers expired tokens with 403, so check the expiry here instead.
    clearSession()
    return null
  }
  return session
}

function isExpired(token: string) {
  try {
    const payload = JSON.parse(atob(token.split('.')[1].replace(/-/g, '+').replace(/_/g, '/')))
    return typeof payload.exp === 'number' && payload.exp * 1000 < Date.now()
  } catch {
    return true
  }
}

export function saveSession(session: Session) {
  localStorage.setItem(sessionKey, JSON.stringify(session))
}

export function clearSession() {
  localStorage.removeItem(sessionKey)
}

export async function api<T>(path: string, options: RequestInit = {}): Promise<T> {
  const headers = new Headers(options.headers)
  headers.set('Content-Type', 'application/json')

  const session = getSession()
  if (session) {
    headers.set('Authorization', `Bearer ${session.token}`)
  }

  const response = await fetch(`/api${path}`, { ...options, headers })

  if (response.status === 401 && session) {
    clearSession()
    window.location.href = '/login'
    throw new Error('Your session ended. Please sign in again.')
  }

  if (!response.ok) {
    const body = await response.json().catch(() => null)
    throw new Error(body?.message ?? (response.status === 403
      ? 'You do not have permission to do that.'
      : 'Something went wrong. Please try again.'))
  }

  return response.status === 204 ? (undefined as T) : response.json()
}
