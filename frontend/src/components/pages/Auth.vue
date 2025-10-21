<script setup lang="ts">
import { ref } from 'vue'
import { Button } from '@/components/ui/button'
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'

const email = ref('')
const password = ref('')

const handleSubmit = (e: Event) => {
  e.preventDefault()
  console.log('Login:', { email: email.value, password: password.value })
}
</script>

<template>
  <div class="container">
    <img class="logo" src="../../assets/LOGO_SOFTEX_VERTICAL_ROXO_OFFLINE.png" alt="logo">
    
    <Card class="w-full max-w-sm">
      <CardHeader>
        <CardTitle>Acesse sua conta</CardTitle>
        <CardDescription>
          Digite seu email abaixo para fazer login na sua conta
        </CardDescription>
      </CardHeader>
      
      <CardContent>
        <form @submit="handleSubmit">
          <div class="flex flex-col gap-6">
            <div class="grid gap-2">
              <Label for="email">Email</Label>
              <Input
                id="email"
                v-model="email"
                type="email"
                placeholder="seuemail@exemplo.com"
                required
              />
            </div>
            
            <div class="grid gap-2">
              <div class="flex items-center">
                <Label for="password">Senha</Label>
                <a
                  href="#"
                  class="ml-auto inline-block text-sm underline-offset-4 hover:underline"
                >
                  Esqueceu sua senha?
                </a>
              </div>
              <Input 
                id="password" 
                v-model="password"
                type="password" 
                required 
              />
            </div>
          </div>
        </form>
      </CardContent>
      
      <CardFooter class="flex-col gap-2">
        <Button type="submit" class="w-full" @click="handleSubmit">
          Login
        </Button>
        <Button variant="outline" class="w-full">
          Login com Google
        </Button>
        <div class="text-center text-sm text-muted-foreground">
          Não tem uma conta? 
          <a href="#" class="text-primary underline-offset-4 hover:underline">
            Cadastre-se
          </a>
        </div>
      </CardFooter>
    </Card>
  </div>
</template>

<style scoped>
.container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  gap: 2rem;
  padding: 1rem;
}

.logo {
  width: 120px;
  height: 120px;
  object-fit: contain;
}
</style>