<script setup lang="ts">
import { ref } from 'vue'
import { Eye, EyeOff } from 'lucide-vue-next'
import { Button } from '@/components/ui/button'
import {
  Card,
  CardContent,
  CardFooter,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { useAuth } from '@/composables/useAuth'

const { login, isLoading, error } = useAuth()

const email = ref('')
const password = ref('')
const showPassword = ref(false)
const rememberMe = ref(false)

const handleSubmit = async (e: Event) => {
  e.preventDefault()
  
  if (!email.value || !password.value) {
    return
  }

  await login(email.value, password.value)
}

const togglePasswordVisibility = () => {
  showPassword.value = !showPassword.value
}

const handleGoogleLogin = () => {
  console.log('Login com Google')
}

const handleBack = () => {
  console.log('Voltar')
}
</script>

<template>
  <div class="auth-container">
    <!-- Cabeçalho com Logo -->
    <header class="header">
      <img class="header-logo" src="../../assets/LOGO_SOFTEX_VERTICAL_BRANCO_OFFLINE.png" alt="Softex">
    </header>

    <!-- Card de Login -->
    <Card class="login-card">
      <CardHeader class="text-center">
        <CardTitle>Acesse sua conta</CardTitle>
      </CardHeader>
      
      <CardContent>
        <form @submit="handleSubmit" class="space-y-8">
          <!-- Mensagem de erro -->
          <div 
            v-if="error" 
            class="bg-destructive/15 text-destructive text-sm p-3 rounded-md"
          >
            {{ error }}
          </div>
          
          <!-- Botão Google (primeiro) -->
          <Button 
            type="button" 
            variant="outline" 
            class="w-full google-button"
            :disabled="isLoading"
            @click="handleGoogleLogin"
          >
            <svg class="google-icon" viewBox="0 0 24 24" width="20" height="20">
              <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
              <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
              <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
              <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
            </svg>
            Entrar com Google
          </Button>

          <!-- Campos de entrada -->
          <div class="space-y-4">
            <div class="space-y-2">
              <Label for="email">E-mail</Label>
              <Input
                id="email"
                v-model="email"
                type="email"
                placeholder="E-mail"
                class="input-field"
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
                  class="input-field password-input"
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

          <!-- Lembrar-me e Esqueci a senha -->
          <div class="flex items-center justify-between">
            <div class="flex items-center space-x-2">
              <input
                id="remember-me"
                v-model="rememberMe"
                type="checkbox"
                class="checkbox"
              />
              <Label for="remember-me" class="cursor-pointer text-sm font-normal">
                Lembrar-me
              </Label>
            </div>
            <a
              href="#"
              class="text-sm text-muted-foreground underline-offset-4 hover:underline"
              @click.prevent
            >
              Esqueci a senha
            </a>
          </div>

          <!-- Botões de ação -->
          <div class="flex gap-3">
            <Button 
              type="submit" 
              class="flex-1 login-button"
              :disabled="isLoading"
            >
              {{ isLoading ? 'Entrando...' : 'Login' }}
            </Button>
            <Button 
              type="button" 
              variant="outline" 
              class="flex-1 back-button"
              :disabled="isLoading"
              @click="handleBack"
            >
              Voltar
            </Button>
          </div>
        </form>
      </CardContent>
    </Card>

    <!-- Rodapé -->
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

.google-button {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  border: 1px solid #e5e7eb;
  background: white;
  color: #1f2937;
  transition: all 0.2s;
}

.google-button:hover {
  background: #f9fafb;
  border-color: #d1d5db;
}

.google-icon {
  flex-shrink: 0;
}

.input-field {
  width: 100%;
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
  color: #6b7280;
}

.password-toggle:hover {
  color: #374151;
}

.checkbox {
  width: 1rem;
  height: 1rem;
  border: 1px solid #d1d5db;
  border-radius: 0.25rem;
  cursor: pointer;
  accent-color: #7C3AED;
}

.checkbox:checked {
  background-color: #7C3AED;
  border-color: #7C3AED;
}

.login-button {
  background: #2563eb;
  color: white;
  font-weight: 500;
}

.login-button:hover {
  background: #1d4ed8;
}

.back-button {
  border-color: #6b7280;
  color: #374151;
}

.back-button:hover {
  background: #f3f4f6;
  border-color: #9ca3af;
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
