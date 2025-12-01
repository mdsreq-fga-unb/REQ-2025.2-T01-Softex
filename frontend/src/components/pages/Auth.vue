<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { Eye, EyeOff } from 'lucide-vue-next'
import { Button } from '@/components/ui/button'
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { useAuth } from '@/composables/useAuth'

const { login, isLoading, error } = useAuth()

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const email = ref('')
const password = ref('')
const showPassword = ref(false)
const rememberMe = ref(false)
const successMessage = ref('')

const handleSubmit = async (e: Event) => {
  e.preventDefault()
  
  if (!email.value || !password.value) {
    return
  }

  const success = await login(email.value, password.value)
  if (success) {
    successMessage.value = 'Login realizado com sucesso!'
    console.log('Login bem-sucedido!')
  }
}

const togglePasswordVisibility = () => {
  showPassword.value = !showPassword.value
}

onMounted(() => {
  const urlParams = new URLSearchParams(window.location.search)
  
  if (urlParams.get('auth') === 'success') {
    const userData = urlParams.get('user')
    const isNewUser = urlParams.get('new_user') === 'true'
    
    if (userData) {
      try {
        const user = JSON.parse(userData)
        localStorage.setItem('user', JSON.stringify(user))
        successMessage.value = isNewUser 
          ? 'Conta criada com sucesso!' 
          : 'Login realizado com sucesso!'
        
        console.log('✅ Login bem-sucedido!', user)
        
        setTimeout(() => {
          window.location.href = '/dashboard'
        }, 1000)
      } catch (e) {
        console.error('Erro ao processar dados do usuário:', e)
      }
    }
  }
  
  if (urlParams.has('error')) {
    const errorMsg = urlParams.get('error')
    successMessage.value = ''
    console.error('❌ Erro no login Google:', errorMsg)
  }
})

const handleGoogleLogin = () => {
  window.location.href = `${API_URL}/api/auth/google/login/`
}

const handleBack = () => {
  console.log('Voltar')
}
</script>

<template>
  <div class="auth-container">
    <header class="header">
      <img class="header-logo" src="../../assets/LOGO_SOFTEX_VERTICAL_BRANCO_OFFLINE.png" alt="Softex">
    </header>

    <Card class="login-card">
      <CardHeader class="text-center">
        <CardTitle>Acesse sua conta</CardTitle>
      </CardHeader>
      
      <CardContent>
        <form @submit="handleSubmit" class="space-y-6">
          <div 
            v-if="successMessage" 
            class="rounded-lg border border-green-200 bg-green-50 p-3 text-sm text-green-700"
            role="alert"
          >
            {{ successMessage }}
          </div>
          
          <div 
            v-if="error" 
            class="rounded-lg border border-destructive/50 bg-destructive/10 p-3 text-sm text-destructive"
            role="alert"
          >
            {{ error }}
          </div>
          
          <Button 
            type="button" 
            variant="outline" 
            class="w-full"
            :disabled="isLoading"
            @click="handleGoogleLogin"
          >
            <svg class="mr-2 h-5 w-5" viewBox="0 0 24 24">
              <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
              <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
              <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
              <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
            </svg>
            Entrar com Google
          </Button>

          <div class="space-y-4">
            <div class="space-y-2">
              <Label for="email">E-mail</Label>
              <Input
                id="email"
                v-model="email"
                type="email"
                placeholder="E-mail"
                :disabled="isLoading"
                required
              />
            </div>
            
            <div class="space-y-2">
              <Label for="password">Senha</Label>
              <div class="password-input-wrapper">
                <Input 
                  id="password" 
                  v-model="password"
                  :type="showPassword ? 'text' : 'password'"
                  placeholder="Senha"
                  class="password-input"
                  :disabled="isLoading"
                  required 
                />
                <button
                  type="button"
                  class="password-toggle"
                  @click="togglePasswordVisibility"
                  tabindex="-1"
                >
                  <Eye v-if="!showPassword" class="h-5 w-5 text-muted-foreground" />
                  <EyeOff v-else class="h-5 w-5 text-muted-foreground" />
                </button>
              </div>
            </div>
          </div>

          <div class="flex items-center justify-between text-sm">
            <div class="flex items-center space-x-2">
              <input
                id="remember-me"
                v-model="rememberMe"
                type="checkbox"
                class="h-4 w-4 rounded border-input bg-background ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
              />
              <Label for="remember-me" class="cursor-pointer font-normal">
                Lembrar-me
              </Label>
            </div>
            <a
              href="#"
              class="text-muted-foreground underline-offset-4 hover:underline"
              @click.prevent
            >
              Esqueci a senha
            </a>
          </div>

          <div class="flex gap-3">
            <Button 
              type="submit" 
              class="flex-1"
              :disabled="isLoading"
            >
              {{ isLoading ? 'Entrando...' : 'Login' }}
            </Button>
            <Button 
              type="button" 
              variant="outline" 
              class="flex-1"
              :disabled="isLoading"
              @click="handleBack"
            >
              Voltar
            </Button>
          </div>
        </form>
      </CardContent>
    </Card>

    <footer class="footer">
      <div class="footer-content">
        <span class="footer-text">© 2025 - Softex</span>
        <span class="footer-text">All rights reserved</span>
      </div>
    </footer>
  </div>
</template>

<style scoped>
.auth-container {
  min-height: 100vh;
  background: linear-gradient(to bottom, #1C2457 0%, #2F2365 40%, #4A2E70 70%, #6C5885 100%);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: space-between;
  padding: 2rem 1rem;
  position: relative;
}

.header {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  margin-bottom: 2rem;
}

.header-logo {
  height: 100px;
  width: auto;
  object-fit: contain;
}

.login-card {
  width: 100%;
  max-width: 380px;
  background: white;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
}

.login-card :deep(.card-header) {
  padding: 2rem 1.5rem 1.5rem;
}

.login-card :deep(.card-content) {
  padding: 0 1.5rem 1.5rem;
}

.login-card :deep(.card-footer) {
  padding: 1.5rem;
}


.password-input-wrapper {
  position: relative;
}

.password-input {
  padding-right: 2.5rem;
}

.password-toggle {
  position: absolute;
  right: 0.75rem;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  cursor: pointer;
  padding: 0.25rem;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: color 0.2s;
}

.password-toggle:hover {
  color: hsl(var(--foreground));
}


.footer {
  width: 100%;
  margin-top: 2rem;
  display: flex;
  justify-content: center;
  align-items: center;
}

.footer-content {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 0.25rem;
}

.footer-text {
  color: rgba(255, 255, 255, 0.7);
  font-size: 0.875rem;
}

@media (max-width: 640px) {
  .footer-content {
    flex-direction: column;
    gap: 0.5rem;
    text-align: center;
  }
}
</style>
