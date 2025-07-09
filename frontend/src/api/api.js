import axios from 'axios';

const API_BASE = 'http://localhost:8000/api/';

// EVENTS
export function fetchEvents() {
  return axios.get(API_BASE + 'events/');
}
export function createEvent(data) {
  return axios.post(API_BASE + 'events/', data);
}

// ARENAS
export function fetchArenas() {
  return axios.get(API_BASE + 'arenas/');
}
export function createArena(data) {
  return axios.post(API_BASE + 'arenas/', data);
}

// POLES
export function fetchPoles() {
  return axios.get(API_BASE + 'poles/');
}

// WINGS
export function fetchWings() {
  return axios.get(API_BASE + 'wings/');
}

// POLE LOCATIONS
export function createPoleLocation(data) {
  return axios.post(API_BASE + 'pole-locations/', data);
}

// WING LOCATIONS
export function createWingLocation(data) {
  return axios.post(API_BASE + 'wing-locations/', data);
}

export function fetchPoleLocationsByArena(arenaId) {
  return axios.get(`http://localhost:8000/api/pole-locations/?arena=${arenaId}`);
}

export function fetchWingLocationsByArena(arenaId) {
  return axios.get(`http://localhost:8000/api/wing-locations/?arena=${arenaId}`);
}

export function fetchEventDetails(id) {
  return axios.get(API_BASE + `events/${id}/full_details/`);
}

export function fetchEvent(id) {
  return axios.get(API_BASE + 'events/' + id + '/');
}

export function deletePoleLocation(id) {
  return axios.delete(API_BASE + `pole-locations/${id}/`);
}
export function deleteWingsLocation(id) {
  return axios.delete(API_BASE + `wing-locations/${id}/`);
}

export function deleteEvent(eventId) {
  return axios.delete(API_BASE + 'events/' + eventId + '/');
}
export function updateEvent(eventId, data) {
  return axios.put(API_BASE + 'events/' + eventId + '/', data);
}
export function updateArena(arenaId, data) {
  return axios.patch( API_BASE + `arenas/${arenaId}/`, data);
}
export function createWishlist(data) {
  return axios.post(API_BASE + 'wishlist/', data);
}
export function archiveEvent(eventId) {
  return axios.post(API_BASE + `events/${eventId}/archive/`);
}
export function fetchArchivedEvents() {
  return axios.get(API_BASE + 'archived-events/');
}
export function fetchArchivedEventDetails(id) {
  return axios.get(API_BASE + 'archived-events/' + id + '/');
}