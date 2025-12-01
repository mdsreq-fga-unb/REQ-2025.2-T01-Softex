<script setup lang="ts">
import { useAuth } from '@/composables/useAuth'
import { useRouter } from 'vue-router'

const { user, logout } = useAuth()
const router = useRouter()

const handleLogout = () => {
  logout()
  router.push('/login')   // navegação correta
}
</script>


<template>
  <header class="header">
    <div class="header-content">

      <!-- LOGO -->
      <div class="logo-section">
        <img
          src="@/assets/LOGO_SOFTEX_VERTICAL_BRANCO_OFFLINE.png"
          alt="Softex"
          class="logo"
        />

        <div class="logo-text">
          <h1 class="logo-title">Softex</h1>
          <p class="logo-subtitle">Sistema de gestão de Espaços</p>
        </div>
      </div>

      <!-- USER -->
      <div class="user-section">
        <span class="user-name">{{ user?.first_name }} {{ user?.last_name }}</span>
        <span class="user-role">{{ user?.tipo_funcao }}</span>

        <div class="user-avatar">
          {{ user?.first_name?.charAt(0) }}{{ user?.last_name?.charAt(0) }}
        </div>

        <button @click="handleLogout" class="logout-btn" title="Sair">
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20"
            fill="none" stroke="currentColor" stroke-width="2">
            <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path>
            <polyline points="16 17 21 12 16 7"></polyline>
            <line x1="21" y1="12" x2="9" y2="12"></line>
          </svg>
        </button>
      </div>
    </div>

  <nav class="navigation">
    <router-link to="/dashboard" class="nav-item" active-class="active">
      Dashboard
    </router-link>

    <router-link to="/coworking" class="nav-item" active-class="active">
      Coworking
    </router-link>

    <router-link to="/salas" class="nav-item" active-class="active">
      Salas de reunião
    </router-link>

    <router-link to="/reservas" class="nav-item" active-class="active">
      Minhas Reservas
    </router-link>

    <router-link to="/administracao" class="nav-item" active-class="active">
      Administração
    </router-link>
  </nav>

  </header>
</template>

<style scoped>
/* Header */
.header {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 2rem;
}

.logo-section {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.logo {
  height: 40px;
  width: auto;
}

.logo-text {
  display: flex;
  flex-direction: column;
}

.logo-title {
  color: white;
  font-size: 1.25rem;
  font-weight: 600;
}

.logo-subtitle {
  color: rgba(255, 255, 255, 0.7);
  font-size: 0.875rem;
}

.user-section {
  display: flex;
  align-items: center;
  gap: 1rem;
  color: white;
}

.user-name {
  font-weight: 500;
}

.user-role {
  color: rgba(255, 255, 255, 0.7);
  font-size: 0.875rem;
  text-transform: capitalize;
}

.user-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 0.875rem;
  color: white;
}

.logout-btn {
  background: rgba(255, 255, 255, 0.1);
  border: none;
  padding: 0.5rem;
  border-radius: 0.5rem;
  cursor: pointer;
  color: white;
  transition: background 0.2s;
}

.logout-btn:hover {
  background: rgba(255, 255, 255, 0.2);
}

/* Navigation */
.navigation {
  display: flex;
  gap: 2rem;
  padding: 0 2rem;
  overflow-x: auto;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 1rem 0;
  color: rgba(255, 255, 255, 0.7);
  text-decoration: none;
  border-bottom: 2px solid transparent;
  transition: all 0.2s;
  white-space: nowrap;
}

.nav-item:hover {
  color: white;
}

.nav-item.active {
  color: white;
  border-bottom-color: white;
}
</style>
