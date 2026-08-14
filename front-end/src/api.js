const API_URL = import.meta.env.VITE_API_URL
const API_KEY = import.meta.env.VITE_API_KEY

// Thin wrapper around fetch that attaches the API key header (X-API-Key).
// The backend (back-end/security.py) requires it (or a JWT) in production.
export function apiFetch(path, options = {}) {
  const headers = { ...(options.headers || {}) }
  if (API_KEY) headers['X-API-Key'] = API_KEY
  return fetch(`${API_URL}${path}`, { ...options, headers })
}
