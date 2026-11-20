
import { useEffect, useState } from 'react'
import AuthContext from './authContext'
import api from '../services/api'
import {
  loginUser,
  getCurrentUser,
} from '../services/authService'

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)

  const [loading, setLoading] = useState(
    () => Boolean(sessionStorage.getItem('access'))
  )

  // Restore an existing session
  useEffect(() => {
    const accessToken = sessionStorage.getItem('access')

    if (!accessToken) return

    api.defaults.headers.common.Authorization = `Bearer ${accessToken}`

    getCurrentUser()
      .then((userData) => {
        setUser(userData)
      })
      .catch(() => {
        sessionStorage.removeItem('access')
        sessionStorage.removeItem('refresh')
        delete api.defaults.headers.common.Authorization
        setUser(null)
      })
      .finally(() => {
        setLoading(false)
      })
  }, [])

  // Login
  const login = async (credentials) => {
  console.log('1. AuthContext login started')

  const tokens = await loginUser(credentials)
  console.log('2. Login API response received')

  sessionStorage.setItem('access', tokens.access)
  sessionStorage.setItem('refresh', tokens.refresh)

  api.defaults.headers.common.Authorization = `Bearer ${tokens.access}`

  console.log('3. Access token configured')

  const userData = await getCurrentUser()
  console.log('4. Current user received:', userData)

  setUser(userData)

  return userData
}
  // Logout
  const logout = () => {
    sessionStorage.removeItem('access')
    sessionStorage.removeItem('refresh')

    delete api.defaults.headers.common.Authorization

    setUser(null)
  }

  return (
    <AuthContext.Provider value={{ user, loading, login, logout }}>
      {children}
    </AuthContext.Provider>
  )
}
