import api from './api'

// Get dashboard summary statistics
export const getDashboardStats = async () => {
  const response = await api.get('/dashboard/')
  return response.data
}

// Get dashboard analytics
export const getDashboardAnalytics = async () => {
  const response = await api.get('/dashboard/analytics/')
  return response.data
}