import axios from 'axios'

export const api = axios.create({
  baseURL: 'http://localhost:8000/api', // ou a URL do seu backend
  headers: {
    'Content-Type': 'application/json',
  },
})
