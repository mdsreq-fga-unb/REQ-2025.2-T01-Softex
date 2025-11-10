import { ref, computed } from 'vue'

export interface User {
  id: number
  username: string
  email: string
  first_name: string
  last_name: string
  tipo_permissao: 'colaborador' | 'lider' | 'rh' | 'admin'
}

// Configuração da API
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

// Estado global compartilhado (singleton)
const user = ref<User | null>(null)
const isLoading = ref(false)
const error = ref<string | null>(null)

// Carregar usuário do localStorage ao iniciar
const loadUserFromStorage = () => {
  const storedUser = localStorage.getItem('user')
  if (storedUser) {
    try {
      user.value = JSON.parse(storedUser)
    } catch (e) {
      localStorage.removeItem('user')
    }
  }
}

// Carregar usuário ao importar
loadUserFromStorage()

export function useAuth() {
  const isAuthenticated = computed(() => user.value !== null)

  /**
   * Login via Google SSO
   */
  const googleLogin = async (googleToken: string) => {
    isLoading.value = true
    error.value = null

    try {
      const response = await fetch(`${API_URL}/api/auth/google/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ token: googleToken })
      })

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.error || 'Erro ao fazer login com Google')
      }

      // Salvar usuário
      user.value = data.user
      localStorage.setItem('user', JSON.stringify(data.user))
      
      return { success: true, isNewUser: data.is_new_user }
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Erro ao fazer login com Google'
      return { success: false, isNewUser: false }
    } finally {
      isLoading.value = false
    }
  }

  /**
   * Login tradicional (email/senha)
   */
  const login = async (email: string, password: string) => {
    isLoading.value = true
    error.value = null

    try {
      const response = await fetch(`${API_URL}/api/login/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password })
      })

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.error || data.non_field_errors?.[0] || 'Email ou senha incorretos')
      }

      // Salvar usuário
      user.value = data.user
      localStorage.setItem('user', JSON.stringify(data.user))
      
      return true
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Erro ao fazer login'
      return false
    } finally {
      isLoading.value = false
    }
  }

  /**
   * Logout
   */
  const logout = () => {
    user.value = null
    error.value = null
    localStorage.removeItem('user')
  }

  /**
   * Cadastrar novo usuário
   */
  const register = async (userData: {
    username: string
    email: string
    first_name: string
    last_name: string
    password: string
    tipo_permissao?: string
  }) => {
    isLoading.value = true
    error.value = null

    try {
      const response = await fetch(`${API_URL}/api/cadastro/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          ...userData,
          tipo_permissao: userData.tipo_permissao || 'colaborador'
        })
      })

      const data = await response.json()

      if (!response.ok) {
        const errorMsg = Object.values(data).flat().join(', ')
        throw new Error(errorMsg || 'Erro ao criar conta')
      }

      // Fazer login automaticamente após cadastro
      return await login(userData.email, userData.password)
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Erro ao criar conta'
      return false
    } finally {
      isLoading.value = false
    }
  }

  return {
    user,
    isAuthenticated,
    isLoading,
    error,
    login,
    googleLogin,
    logout,
    register
  }
}
