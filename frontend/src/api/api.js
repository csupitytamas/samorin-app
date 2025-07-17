import axios from 'axios'

// TOKEN INTERCEPTORS
axios.interceptors.request.use(config => {
  const token = localStorage.getItem('access_token') || sessionStorage.getItem('access_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

axios.interceptors.response.use(
  response => response,
  async error => {
    const originalRequest = error.config
    if (error.response && error.response.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true
      const refreshToken = localStorage.getItem('refresh_token') || sessionStorage.getItem('refresh_token')
      if (refreshToken) {
        try {
          const res = await axios.post('/api/token/refresh/', { refresh: refreshToken })
          const newAccess = res.data.access
          if (localStorage.getItem('refresh_token')) {
            localStorage.setItem('access_token', newAccess)
          } else {
            sessionStorage.setItem('access_token', newAccess)
          }
          originalRequest.headers['Authorization'] = `Bearer ${newAccess}`
          return axios(originalRequest)
        } catch {
          localStorage.removeItem('access_token')
          localStorage.removeItem('refresh_token')
          sessionStorage.removeItem('access_token')
          sessionStorage.removeItem('refresh_token')
          window.location.href = '/login'
        }
      } else {
        window.location.href = '/login'
      }
    }
    return Promise.reject(error)
  }
)

const API_BASE = process.env.NODE_ENV === 'production'
  ? 'http://13.48.70.78:8000/api/'
  : '/api/';

// --- API FÜGGVÉNYEK ---
export function fetchEvents() {
  return axios.get(API_BASE + 'events/')
}
export function createEvent(data) {
  return axios.post(API_BASE + 'events/', data)
}
export function fetchArenas() {
  return axios.get(API_BASE + 'arenas/')
}
export function createArena(data) {
  return axios.post(API_BASE + 'arenas/', data)
}
export function fetchPoles() {
  return axios.get(API_BASE + 'poles/')
}
export function fetchWings() {
  return axios.get(API_BASE + 'wings/')
}
export function createPoleLocation(data) {
  return axios.post(API_BASE + 'pole-locations/', data)
}
export function createWingLocation(data) {
  return axios.post(API_BASE + 'wing-locations/', data)
}
export function fetchPoleLocationsByArena(arenaId) {
  return axios.get(API_BASE + `pole-locations/?arena=${arenaId}`)
}
export function fetchWingLocationsByArena(arenaId) {
  return axios.get(API_BASE + `wing-locations/?arena=${arenaId}`)
}
export function fetchEventDetails(id) {
  return axios.get(API_BASE + `events/${id}/full_details/`)
}
export function fetchEvent(id) {
  return axios.get(API_BASE + 'events/' + id + '/')
}
export function deletePoleLocation(id) {
  return axios.delete(API_BASE + `pole-locations/${id}/`)
}
export function deleteWingsLocation(id) {
  return axios.delete(API_BASE + `wing-locations/${id}/`)
}
export function deleteEvent(eventId) {
  return axios.delete(API_BASE + 'events/' + eventId + '/')
}
export function updateEvent(eventId, data) {
  return axios.put(API_BASE + 'events/' + eventId + '/', data)
}
export function updateArena(arenaId, data) {
  return axios.patch(API_BASE + `arenas/${arenaId}/`, data)
}
export function createWishlist(data) {
  return axios.post(API_BASE + 'wishlist/', data)
}
export function archiveEvent(eventId) {
  return axios.post(API_BASE + `events/${eventId}/archive/`)
}
export function fetchArchivedEvents() {
  return axios.get(API_BASE + 'archived-events/')
}
export function fetchArchivedEventDetails(id) {
  return axios.get(API_BASE + 'archived-events/' + id + '/')
}
export function registerUser(data) {
  return axios.post(API_BASE + 'users/register/', data)
}
export function loginUser(data) {
  return axios.post(API_BASE + 'token/', data)
}
export function fetchProfile() {
  return axios.get(API_BASE + 'users/me/').then(r => r.data)
}
export function fetchWishlists() {
  return axios.get(API_BASE + 'wishlist/').then(r => r.data)
}
export function logoutUser() {
  localStorage.removeItem('access_token')
  localStorage.removeItem('refresh_token')
  sessionStorage.removeItem('access_token')
  sessionStorage.removeItem('refresh_token')
}
export function fetchUsers() {
  return axios.get(API_BASE + 'users/userprofiles/').then(r => r.data)
}
export function updateUserRole(id, data) {
  return axios.patch(API_BASE + `users/userprofiles/${id}/`, data)
}
export function fetchWarehouses() {
  return axios.get(API_BASE + 'warehouses/').then(r => r.data)
}
export function createPole(data) {
  return axios.post(API_BASE + 'poles/', data)
}
export function createWings(data) {
  return axios.post(API_BASE + 'wings/', data)
}
export function wishList(data) {
  return axios.post(API_BASE + 'wishlist/', data)
}
export function fetchWishlist(id) {
  return axios.get(API_BASE + `wishlist/${id}/`)
}
export function updateWishlist(id, data) {
  return axios.patch(API_BASE + `wishlist/${id}/`, data)
}
export function fetchEventWishlists(eventId) {
  return axios.get(API_BASE + `events/${eventId}/all_wishlists/`)
}
export function fetchActiveArenas() {
  return axios.get(API_BASE + 'active-arenas/')
}
export function deleteWishlist(id) {
  return axios.delete(API_BASE + `wishlist/${id}/`);
}
