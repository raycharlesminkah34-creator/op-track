const BASE_URL = '/api/v1'

export async function request(path, options = {}) {
  const response = await fetch(`${BASE_URL}${path}`, {
    headers: { 'Content-Type': 'application/json', ...options.headers },
    ...options,
  })
  if (!response.ok) {
    const detail = await response.json().catch(() => ({}))
    throw new Error(detail?.detail ?? `HTTP ${response.status}`)
  }
  if (response.status === 204) return null
  return response.json()
}

export function fetchOpportunities(params = {}) {
  const query = new URLSearchParams(params).toString()
  return request(`/opportunities${query ? `?${query}` : ''}`)
}

export function fetchOpportunity(id) {
  return request(`/opportunities/${id}`)
}

export function createOpportunity(data) {
  return request('/opportunities', {
    method: 'POST',
    body: JSON.stringify(data),
  })
}

export function updateOpportunity(id, data) {
  return request(`/opportunities/${id}`, {
    method: 'PATCH',
    body: JSON.stringify(data),
  })
}

export function deleteOpportunity(id) {
  return request(`/opportunities/${id}`, {
    method: 'DELETE',
  })
}
