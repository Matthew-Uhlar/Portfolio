const baseUrl = '/api'

export function getToken() {
  return localStorage.getItem('token')
}

export async function api<T>(path: string, options: RequestInit = {}): Promise<T> {
  const headers = new Headers(options.headers)
  headers.set('Content-Type', 'application/json')

  const token = getToken()
  if (token) {
    headers.set('Authorization', `Bearer ${token}`)
  }

  const response = await fetch(`${baseUrl}${path}`, { ...options, headers })

  if (response.status === 401) {
    localStorage.clear()
    window.location.href = '/login'
    throw new Error('Your session ended. Please sign in again.')
  }

  if (!response.ok) {
    const error = await response.json().catch(() => ({ message: 'Something went wrong.' }))
    throw new Error(error.message ?? 'Something went wrong.')
  }

  if (response.status === 204) {
    return undefined as T
  }

  return response.json()
}
