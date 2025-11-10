<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import Auth from '@/components/pages/Auth.vue'
import Dashboard from '@/components/pages/Dashboard.vue'
import { useAuth } from '@/composables/useAuth'

const { isAuthenticated } = useAuth()
const currentRoute = ref(window.location.pathname)

// Atualizar rota quando mudar
const updateRoute = () => {
  currentRoute.value = window.location.pathname
}

onMounted(() => {
  // Escutar mudanças na URL
  window.addEventListener('popstate', updateRoute)
  
  // Se está autenticado e na raiz, ir para dashboard
  if (isAuthenticated.value && currentRoute.value === '/') {
    window.history.replaceState({}, '', '/dashboard')
    currentRoute.value = '/dashboard'
  }
})

// Mostrar componente baseado na rota
const showDashboard = ref(false)

watch([isAuthenticated, currentRoute], ([auth, route]) => {
  showDashboard.value = auth && (route === '/dashboard' || route === '/')
}, { immediate: true })
</script>

<template>
  <Auth v-if="!showDashboard" />
  <Dashboard v-else />
</template>

<style scoped>

</style>
