import { ref, computed } from 'vue'

export interface User {
  id: number
  email: string
  name: string
}

// Estado global compartilhado (singleton)
const user = ref<User | null>(null)
const isLoading = ref(false)
const error = ref<string | null>(null)

export function useAuth() {
  const isAuthenticated = computed(() => user.value !== null)

  const login = async (email: string, password: string) => {
    isLoading.value = true
    error.value = null

    try {
      // Simulação de chamada para API
      await new Promise(resolve => setTimeout(resolve, 1000))

      // Aceita qualquer credencial por enquanto
      user.value = {
        id: 1,
        email,
        name: email.split('@')[0] || 'Usuário'
      }
      return true
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Erro ao fazer login'
      return false
    } finally {
      isLoading.value = false
    }
  }

  const logout = () => {
    user.value = null
    error.value = null
  }

  return {
    user,
    isAuthenticated,
    isLoading,
    error,
    login,
    logout
  }
}
