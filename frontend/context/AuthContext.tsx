'use client'

import { createContext, useState, useEffect, ReactNode } from 'react'
import { User } from '@/types'
import { login as loginApi, register as registerApi, logout as logoutApi, getCurrentUser, setAuthToken } from '@/lib/auth'
import { LoginCredentials, RegisterData } from '@/types'

interface AuthContextType {
  user: User | null
  loading: boolean
  login: (credentials: LoginCredentials) => Promise<void>
  register: (data: RegisterData) => Promise<void>
  logout: () => Promise<void>
  isAuthenticated: boolean
}

export const AuthContext = createContext<AuthContextType>({
  user: null,
  loading: true,
  login: async () => {},
  register: async () => {},
  logout: async () => {},
  isAuthenticated: false,
})

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const initAuth = async () => {
      const token = typeof window !== 'undefined' ? localStorage.getItem('access_token') : null
      if (token) {
        setAuthToken(token)
        try {
          const currentUser = await getCurrentUser()
          setUser(currentUser)
        } catch (error) {
          console.error('Failed to get user:', error)
          setAuthToken(null)
        }
      }
      setLoading(false)
    }
    initAuth()
  }, [])

  const login = async (credentials: LoginCredentials) => {
    const response = await loginApi(credentials)
    setUser(response.user)
    setAuthToken(response.access)
  }

  const register = async (data: RegisterData) => {
    const response = await registerApi(data)
    setUser(response.user)
    setAuthToken(response.access)
  }

  const logout = async () => {
    await logoutApi()
    setUser(null)
    setAuthToken(null)
  }

  return (
    <AuthContext.Provider
      value={{
        user,
        loading,
        login,
        register,
        logout,
        isAuthenticated: !!user,
      }}
    >
      {children}
    </AuthContext.Provider>
  )
}

