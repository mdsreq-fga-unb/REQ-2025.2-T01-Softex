<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { 
  Home, 
  LogOut, 
  Gauge, 
  MapPin, 
  Sofa, 
  Calendar, 
  Settings
} from 'lucide-vue-next'
import { useAuth } from '@/composables/useAuth'
import CadeiraModal from '@/components/modals/reservas/Cadeira.vue'
import SalaReuniaoModal from '@/components/modals/reservas/SalaReuniao.vue'

const { user, logout } = useAuth()
const router = useRouter()
const route = useRoute()

const userInitials = computed(() => {
  if (!user.value) return 'U'
  const firstName = user.value.first_name || ''
  const lastName = user.value.last_name || ''
  if (firstName && lastName) {
    return `${firstName[0]}${lastName[0]}`.toUpperCase()
  }
  if (firstName) {
    return firstName.substring(0, 2).toUpperCase()
  }
  return 'U'
})

const handleLogout = () => {
  logout()
  router.push('/login')
}

type ReservaStatus = 'andamento' | 'concluido'
type ResultadoSala = 'aprovado' | 'pendente' | 'negado'
type ResultadoEstacao = 'aprovado' | 'pendente'

type ReservaBase = {
  id: number
  titulo: string
  descricao: string
  status: ReservaStatus        // em andamento / concluído (aba)
  dataInicio: string
  dataFim: string
}

type ReservaSala = ReservaBase & {
  tipo: 'sala'
  resultado: ResultadoSala     // sala pode ser negada
}

type ReservaEstacao = ReservaBase & {
  tipo: 'estacao'
  resultado: ResultadoEstacao  // estação NÃO pode ser negada
}

type Reserva = ReservaSala | ReservaEstacao

const activeTab = ref<ReservaStatus>('andamento')

const reservas = ref<Reserva[]>([
  {
    id: 1,
    titulo: 'Sala de reunião — Andar 3',
    descricao: 'Reunião com equipe de produto',
    tipo: 'sala',
    status: 'andamento',
    resultado: 'aprovado',
    dataInicio: '10/03/2026',
    dataFim: '10/03/2026'
  },
  {
    id: 2,
    titulo: 'Estação 13 — Coworking',
    descricao: 'Reserva de estação de trabalho',
    tipo: 'estacao',
    status: 'andamento',
    resultado: 'pendente', 
    dataInicio: '11/03/2026',
    dataFim: '13/03/2026',
    horaInicio: '09:00',
    horaFim: '18:00'
  },
  {
    id: 3,
    titulo: 'Sala de reunião — Andar 1',
    descricao: 'Call com cliente externo',
    tipo: 'sala',
    status: 'concluido',
    resultado: 'aprovado',
    dataInicio: '02/03/2026',
    dataFim: '02/03/2026'
  },
  {
    id: 4,
    titulo: 'Estação 05 — Coworking',
    descricao: 'Trabalho presencial',
    tipo: 'estacao',
    status: 'concluido',
    resultado: 'aprovado',
    dataInicio: '25/02/2026',
    dataFim: '26/02/2026'
  }
])

const reservasFiltradas = computed(() =>
  reservas.value.filter(r => r.status === activeTab.value)
)

const selecionarTab = (tab: ReservaStatus) => {
  activeTab.value = tab
}

const showCadeiraModal = ref(false)
const showSalaModal = ref(false)

const reservaCadeiraSelecionada = ref<ReservaEstacao | null>(null)
const reservaSalaSelecionada = ref<ReservaSala | null>(null)

const handleClickReserva = (reserva: Reserva) => {
  console.log('Reserva clicada:', reserva)

  if (reserva.tipo === 'estacao') {
    reservaCadeiraSelecionada.value = reserva
    showCadeiraModal.value = true
  } else {
    reservaSalaSelecionada.value = reserva
    showSalaModal.value = true
  }
}

const labelResultado = (resultado: ResultadoSala | ResultadoEstacao): string => {
  if (resultado === 'aprovado') return 'Aprovada'
  if (resultado === 'pendente') return 'Pendente'
  return 'Negada'
}
</script>

<template>
  <div class="reservas-container min-h-screen">
    <!-- Navbar -->
    <nav class="navbar">
      <!-- Top Section - Header -->
      <div class="navbar-header">
        <div class="header-left">
          <div class="logo-container">
            <img 
              src="../../assets/LOGO_SOFTEX_VERTICAL_BRANCO_OFFLINE.png" 
              alt="Softex" 
              class="logo-image"
            />
            <div class="logo-text">
              <div class="brand-top">
                <span class="brand-main">Coworking</span>
              </div>
              <span class="brand-desc">Sistema de gestão de Espaços</span>
            </div>
          </div>
        </div>
        
        <div class="header-right">
          <router-link to="/dashboard" class="header-icon-link">
            <Home class="header-icon" />
          </router-link>
          <div class="user-info">
            <span class="navbar-user-name">{{ user ? `${user.first_name} ${user.last_name}` : 'Usuário' }}</span>
            <span class="user-role">Administrador</span>
          </div>
          <div class="user-avatar">
            {{ userInitials }}
          </div>
          <button class="logout-button" @click="handleLogout">
            <LogOut class="logout-icon" />
          </button>
        </div>
      </div>
      
      <!-- Bottom Section - Navigation Links -->
      <div class="navbar-nav">
        <router-link to="/dashboard" class="nav-link" :class="{ active: route.path === '/dashboard' }">
          <Gauge class="nav-icon" />
          <span>Dashboard</span>
        </router-link>
        <router-link to="/coworking" class="nav-link" :class="{ active: route.path === '/coworking' }">
          <MapPin class="nav-icon" />
          <span>Coworking</span>
        </router-link>
        <router-link to="/salas" class="nav-link" :class="{ active: route.path === '/salas' }">
          <Sofa class="nav-icon" />
          <span>Salas de reunião</span>
        </router-link>
        <router-link to="/reservas" class="nav-link" :class="{ active: route.path === '/reservas' }">
          <Calendar class="nav-icon" />
          <span>Minhas Reservas</span>
        </router-link>
        <router-link to="/administracao" class="nav-link" :class="{ active: route.path === '/administracao' }">
          <Settings class="nav-icon" />
          <span>Administração</span>
        </router-link>
      </div>
    </nav>

    <div class="dashboard-content">
      <div class="dashboard-grid">
        <div class="tabs-row">
        <button
          type="button"
          class="tab-btn"
          :class="{ 'tab-active': activeTab === 'andamento' }"
          @click="selecionarTab('andamento')"
        >
          Em andamento
        </button>

        <span class="tab-separator">/</span>

        <button
          type="button"
          class="tab-btn"
          :class="{ 'tab-active': activeTab === 'concluido' }"
          @click="selecionarTab('concluido')"
        >
          Concluído
        </button>
      </div>

      <div class="card">
        <h2 class="card-title">Meu histórico</h2>

        <div v-if="reservasFiltradas.length === 0" class="empty-state">
          <p>
            Você ainda não possui reservas
            <span v-if="activeTab === 'andamento'">em andamento.</span>
            <span v-else>concluídas.</span>
          </p>
          <p class="empty-hint">
            Assim que você fizer uma reserva de sala ou estação, ela aparecerá aqui.
          </p>
        </div>

        <div v-else class="lista-reservas">
          <button
            v-for="reserva in reservasFiltradas"
            :key="reserva.id"
            type="button"
            class="reserva-item"
            @click="handleClickReserva(reserva)"
          >
            <div class="reserva-main">
              <p class="reserva-titulo">{{ reserva.titulo }}</p>
              <p class="reserva-desc">{{ reserva.descricao }}</p>
            </div>

            <div class="reserva-meta">
              <span
                class="badge status"
                :class="{
                  'status-ok': reserva.resultado === 'aprovado',
                  'status-wait': reserva.resultado === 'pendente',
                  'status-denied': reserva.resultado === 'negado'
                }"
              >
                {{ labelResultado(reserva.resultado) }}
              </span>

              <span class="badge tipo">
                {{ reserva.tipo === 'sala' ? 'Sala de reunião' : 'Estação' }}
              </span>
              <span class="badge periodo">
                {{ reserva.dataInicio }} — {{ reserva.dataFim }}
              </span>
            </div>
          </button>
        </div>
        </div>
      </div>
    </div>

    <CadeiraModal
      :open="showCadeiraModal"
      :reserva="reservaCadeiraSelecionada"
      @close="showCadeiraModal = false"
    />

    <SalaReuniaoModal
      :open="showSalaModal"
      :reserva="reservaSalaSelecionada"
      @close="showSalaModal = false"
    />
  </div>
</template>

<style scoped>
.reservas-container {
  min-height: 100vh;
  background: linear-gradient(to bottom, #1C2457 0%, #2F2365 40%, #4A2E70 70%, #6C5885 100%);
  display: flex;
  flex-direction: column;
  width: 100%;
}

.navbar {
  background: #1C2457;
  width: 100%;
  z-index: 100;
}

.navbar-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 2rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.header-left {
  display: flex;
  align-items: center;
}

.logo-container {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.logo-image {
  height: 48px;
  width: auto;
  object-fit: contain;
}

.logo-text {
  display: flex;
  flex-direction: column;
}

.brand-top {
  display: flex;
  align-items: baseline;
  gap: 0.5rem;
}

.brand-main {
  color: white;
  font-size: 1.25rem;
  font-weight: 600;
}

.brand-desc {
  color: rgba(255, 255, 255, 0.6);
  font-size: 0.875rem;
  font-weight: 400;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.header-icon-link {
  display: flex;
  align-items: center;
  justify-content: center;
  text-decoration: none;
  cursor: pointer;
}

.header-icon {
  width: 24px;
  height: 24px;
  color: white;
  cursor: pointer;
}

.user-info {
  display: flex;
  flex-direction: column;
  text-align: right;
}

.navbar-user-name {
  color: #ffffff;
  font-size: 0.875rem;
  font-weight: 500;
}

.user-role {
  color: rgba(255, 255, 255, 0.6);
  font-size: 0.75rem;
}

.user-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: #7C3AED;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 0.875rem;
}

.logout-button {
  background: none;
  border: none;
  cursor: pointer;
  padding: 0.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  transition: opacity 0.2s;
}

.logout-button:hover {
  opacity: 0.7;
}

.logout-icon {
  width: 20px;
  height: 20px;
}

.navbar-nav {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 2rem;
  padding: 0.75rem 2rem;
  background: rgba(28, 36, 87, 0.8);
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: white;
  text-decoration: none;
  font-size: 0.875rem;
  padding: 0.5rem 0;
  position: relative;
  transition: opacity 0.2s;
}

.nav-link:hover {
  opacity: 0.8;
}

.nav-link.active {
  font-weight: 500;
}

.nav-link.active::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: white;
}

.nav-icon {
  width: 18px;
  height: 18px;
}

.dashboard-content {
  flex: 1;
  padding: 2rem;
  width: 100%;
}

.dashboard-grid {
  max-width: 1600px;
  margin: 0 auto;
  width: 100%;
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  gap: 2rem;
}

.tabs-row {
  grid-column: 1 / -1;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 0;
}

.tab-btn {
  background: transparent;
  border: none;
  color: rgba(255, 255, 255, 0.6);
  font-size: 0.9rem;
  font-weight: 500;
  cursor: pointer;
  padding: 0.2rem 0.4rem;
  transition: color 0.12s ease;
}

.tab-btn:hover {
  color: rgba(255, 255, 255, 0.9);
}

.tab-active {
  color: #ffffff;
  font-weight: 700;
}

.tab-separator {
  color: rgba(255, 255, 255, 0.6);
  font-size: 1.1rem;
}

.card {
  grid-column: 1 / -1;
  background: #ffffff;
  border-radius: 24px;
  padding: 2rem 2.5rem 2.3rem;
  box-shadow: 0 18px 40px rgba(0, 0, 0, 0.35);
}

.card-title {
  text-align: center;
  font-size: 1rem;
  font-weight: 700;
  margin-bottom: 1.4rem;
}

.empty-state {
  text-align: center;
  padding: 2rem 1rem;
  color: #4b5563;
  font-size: 0.88rem;
}

.empty-hint {
  margin-top: 0.4rem;
  font-size: 0.8rem;
  color: #9ca3af;
}

.lista-reservas {
  display: flex;
  flex-direction: column;
  gap: 0.7rem;
}

.reserva-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
  width: 100%;
  border: none;
  border-radius: 999px;
  background: #e5e7eb;
  padding: 0.8rem 1.4rem;
  cursor: pointer;
  text-align: left;
  transition: box-shadow 0.12s ease, transform 0.1s ease, background 0.12s ease;
}

.reserva-item:hover {
  background: #e5e7eb;
  box-shadow: 0 6px 14px rgba(15, 23, 42, 0.18);
  transform: translateY(-1px);
}

.reserva-main {
  display: flex;
  flex-direction: column;
  gap: 0.1rem;
}

.reserva-titulo {
  font-weight: 600;
  font-size: 0.9rem;
  color: #111827;
}

.reserva-desc {
  font-size: 0.8rem;
  color: #6b7280;
}

.reserva-meta {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 0.25rem;
}

.badge {
  border-radius: 999px;
  padding: 0.15rem 0.7rem;
  font-size: 0.75rem;
  font-weight: 500;
}

.badge.tipo {
  background: #312e81;
  color: #e5e7eb;
}

.badge.periodo {
  background: #d1d5db;
  color: #111827;
}

.badge.status {
  font-weight: 600;
}

.status-ok {
  background: #dcfce7;
  color: #166534;
}

.status-wait {
  background: #fef9c3;
  color: #854d0e;
}

.status-denied {
  background: #fee2e2;
  color: #b91c1c;
}

@media (max-width: 700px) {
  .card {
    padding: 1.5rem 1.2rem 1.8rem;
  }

  .reserva-item {
    flex-direction: column;
    align-items: flex-start;
  }

  .reserva-meta {
    align-items: flex-start;
  }
}
</style>
