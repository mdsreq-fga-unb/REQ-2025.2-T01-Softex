import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'

export interface User {
  id: number
  username: string
  email: string
  first_name: string
  last_name: string
  tipo_permissao: 'colaborador' | 'lider' | 'rh' | 'admin'
}

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const user = ref<User | null>(null)
const isLoading = ref(false)
const error = ref<string | null>(null)

const loadUserFromStorage = () => {
  const storedUser = localStorage.getItem('user')
  if (storedUser) {
    try {
      user.value = JSON.parse(storedUser)
    } catch {
      localStorage.removeItem('user')
    }
  }
}

loadUserFromStorage()

export function useAuth() {
  const router = useRouter()
  const isAuthenticated = computed(() => user.value !== null)

  const login = async (email: string, password: string) => {
    isLoading.value = true
    error.value = null
    try {
      const response = await fetch(`${API_URL}/api/login/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
      })
      const data = await response.json()
      if (!response.ok) {
        throw new Error(data.error || data.non_field_errors?.[0] || 'Email ou senha incorretos')
      }

      user.value = data.user
      localStorage.setItem('user', JSON.stringify(data.user))
      router.push('/dashboard')
      return true
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Erro ao fazer login'
      return false
    } finally {
      isLoading.value = false
    }
  }

  const googleLogin = async (googleToken: string) => {
    isLoading.value = true
    error.value = null
    try {
      const response = await fetch(`${API_URL}/api/auth/google/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ token: googleToken })
      })
      const data = await response.json()
      if (!response.ok) throw new Error(data.error || 'Erro ao fazer login com Google')

      user.value = data.user
      localStorage.setItem('user', JSON.stringify(data.user))
      router.push('/dashboard')
      return { success: true, isNewUser: data.is_new_user }
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Erro ao fazer login com Google'
      return { success: false, isNewUser: false }
    } finally {
      isLoading.value = false
    }
  }

  const logout = () => {
    user.value = null
    error.value = null
    localStorage.removeItem('user')
    router.push('/login')
  }

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
        headers: { 'Content-Type': 'application/json' },
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
      return await login(userData.email, userData.password)
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Erro ao criar conta'
      return false
    } finally {
      isLoading.value = false
    }
  }

  return { user, isAuthenticated, isLoading, error, login, googleLogin, logout, register }
}
