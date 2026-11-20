
import api from './api'

// Login with username and password
export const loginUser = async (credentials) => {
  const response = await api.post('/auth/login/', credentials)
  return response.data
}

// Register a new account
export const registerUser = async (userData) => {
  const response = await api.post('/auth/register/', userData)
  return response.data
}

// Get currently authenticated user
export const getCurrentUser = async () => {
  const response = await api.get('/auth/me/')
  return response.data
}

// Refresh access token
export const refreshAccessToken = async (refresh) => {
  const response = await api.post('/auth/refresh/', { refresh })
  return response.data
}
