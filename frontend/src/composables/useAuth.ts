import { ref, computed } from 'vue'

export interface User {
  id: number
  email: string
  name: string
}

export function useAuth() {
  const user = ref<User | null>(null)
  const isLoading = ref(false)
  const error = ref<string | null>(null)

  const isAuthenticated = computed(() => user.value !== null)

  const login = async (email: string, password: string) => {
    isLoading.value = true
    error.value = null

    try {
      // Simulação de chamada para API
      await new Promise(resolve => setTimeout(resolve, 1000))

      // Mock de usuário (em um projeto real, isso viria da API)
      if (email === 'admin@softex.com' && password === '123456') {
        user.value = {
          id: 1,
          email,
          name: 'Administrador Softex'
        }
        return true
      } else {
        throw new Error('Credenciais inválidas')
      }
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
