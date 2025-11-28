<script setup lang="ts">
import { onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useErrorLogger } from '@/composables/useErrorLogger'
import { Home } from 'lucide-vue-next'

const route = useRoute()
const router = useRouter()
const { logError } = useErrorLogger()

onMounted(() => {
  logError(
    'Página não encontrada',
    { path: route.path, fullPath: route.fullPath },
    'NotFound.vue'
  )
})

const goHome = () => {
  router.push('/dashboard')
}
</script>

<template>
  <div class="not-found-container">
    <div class="not-found-content">
      <h1 class="error-code">404</h1>
      <h2 class="error-title">Página não encontrada</h2>
      <p class="error-message">
        A página que você está procurando não existe ou foi movida.
      </p>
      <button class="home-button" @click="goHome">
        <Home class="home-icon" />
        Voltar para o Dashboard
      </button>
    </div>
  </div>
</template>

<style scoped>
.not-found-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(to bottom, #1C2457 0%, #2F2365 40%, #4A2E70 70%, #6C5885 100%);
  padding: 2rem;
}

.not-found-content {
  text-align: center;
  color: white;
  max-width: 600px;
}

.error-code {
  font-size: 8rem;
  font-weight: 700;
  margin: 0;
  line-height: 1;
  background: linear-gradient(135deg, #ffffff 0%, rgba(255, 255, 255, 0.7) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.error-title {
  font-size: 2rem;
  font-weight: 600;
  margin: 1rem 0;
  color: white;
}

.error-message {
  font-size: 1.125rem;
  color: rgba(255, 255, 255, 0.8);
  margin-bottom: 2rem;
  line-height: 1.6;
}

.home-button {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 0.5rem;
  padding: 0.75rem 1.5rem;
  color: white;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.home-button:hover {
  background: rgba(255, 255, 255, 0.2);
  border-color: rgba(255, 255, 255, 0.3);
  transform: translateY(-2px);
}

.home-icon {
  width: 20px;
  height: 20px;
}
</style>

