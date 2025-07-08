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
