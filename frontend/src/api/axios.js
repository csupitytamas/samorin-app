import axios from 'axios';

const instance = axios.create({
  baseURL: process.env.NODE_ENV === 'production'
    ? 'http://13.48.70.78:8000/api/'
    : 'http://localhost:8000/api/',
  timeout: 5000,
});

export default instance;