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
import plantaImg from '@/assets/planta.png'
import ModalSalaReuniao from '@/components/modals/coworking/ModalSalaReuniao.vue'
import ModalCadeira from '@/components/modals/coworking/ModalCadeira.vue'

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

type SeatStatus = 'disponivel' | 'ocupado' | 'reservado' | 'favorito'

type SeatPoint = {
  id: number
  x: number  
  y: number  
  status: SeatStatus
}

type PlantaOption = {
  id: number
  nome: string
  img: string
}

type ReservaPayload = {
  pessoas: number
  tipo: 'interna' | 'externa'
  motivo: string
  data: string
  horaInicio: string
  horaFim: string
}

type ReservaCadeiraPayload = ReservaPayload & {
  seatId: number
}

const plantas = ref<PlantaOption[]>([
  { id: 1, nome: 'Pavimento baixo - Coworking', img: plantaImg },
  { id: 2, nome: 'Pavimento superior - Coworking', img: plantaImg }
])

const selectedPlantaId = ref<number>(plantas.value[0].id)

const selectedPlantaImg = computed(() => {
  const p = plantas.value.find(p => p.id === selectedPlantaId.value)
  return p ? p.img : plantaImg
})

const seats = ref<SeatPoint[]>([
  { id: 1, x: 25, y: 30, status: 'disponivel' },
  { id: 2, x: 40, y: 32, status: 'ocupado' },
  { id: 3, x: 55, y: 35, status: 'reservado' },
  { id: 4, x: 30, y: 55, status: 'disponivel' },
  { id: 5, x: 45, y: 57, status: 'favorito' },
  { id: 6, x: 60, y: 59, status: 'disponivel' },
  { id: 7, x: 28, y: 75, status: 'disponivel' }
])

const selectedSeat = ref<SeatPoint | null>(null)

const showReservaModal = ref(false)

const showCadeiraModal = ref(false)

const handleSeatClick = (id: number) => {
  const seat = seats.value.find(s => s.id === id)
  if (!seat) return
  selectedSeat.value = seat
  showCadeiraModal.value = true
  console.log('Assento clicado:', seat)
}

const labelFromStatus = (status: SeatStatus): string => {
  switch (status) {
    case 'disponivel': return 'Disponível'
    case 'ocupado': return 'Ocupado'
    case 'reservado': return 'Reservado'
    case 'favorito': return 'Seu favorito'
  }
}

const handleSalvarReserva = (payload: ReservaPayload) => {
  console.log('Reserva de sala salva:', payload)
  showReservaModal.value = false
}

const handleReservaCadeira = (payload: ReservaCadeiraPayload) => {
  console.log('Reserva de cadeira:', payload)
  const seat = seats.value.find(s => s.id === payload.seatId)
  if (seat) {
    seat.status = 'reservado'
  }
  showCadeiraModal.value = false
}
</script>



<template>
  <div class="coworking-container min-h-screen">
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
        <div class="top-row">
          <div class="legend-card">
            <p class="legend-title">Legenda</p>
            <div class="legend-items">
              <div class="legend-item">
                <span class="legend-dot legend-disponivel" />
                <span>Disponível</span>
              </div>
              <div class="legend-item">
                <span class="legend-dot legend-ocupado" />
                <span>Ocupado</span>
              </div>
              <div class="legend-item">
                <span class="legend-dot legend-reservado" />
                <span>Reservado</span>
              </div>
            </div>
          </div>

          <button
          class="reserve-card"
          type="button"
          @click="showReservaModal = true"
          >
          <span class="reserve-plus">+</span>
          <span class="reserve-text">Reservar sala de reunião</span>
          </button>
        </div>

        <div class="planta-card">
        <div class="planta-header">
          <p class="planta-title">Espaço Coworking</p>

          <select
            v-model.number="selectedPlantaId"
            class="planta-select"
          >
            <option
              v-for="planta in plantas"
              :key="planta.id"
              :value="planta.id"
            >
              {{ planta.nome }}
            </option>
          </select>
        </div>

        <div class="planta-wrapper">
          <img
            :src="selectedPlantaImg"
            alt="Planta do coworking"
            class="planta-img"
          />

          <button
            v-for="seat in seats"
            :key="seat.id"
            type="button"
            class="seat-dot"
            :class="[
              seat.status === 'disponivel' ? 'seat-disponivel' : '',
              seat.status === 'ocupado' ? 'seat-ocupado' : '',
              seat.status === 'reservado' ? 'seat-reservado' : '',
            ]"
            :style="{ left: seat.x + '%', top: seat.y + '%'}"
            @click.stop="handleSeatClick(seat.id)"
          />
        </div>

        <p class="seat-info" v-if="selectedSeat">
          Assento {{ selectedSeat.id }} – Status:
          <strong>{{ labelFromStatus(selectedSeat.status) }}</strong>
          (em breve, aqui você pode abrir um modal de detalhes)
        </p>
        <p class="seat-info muted" v-else>
          Clique em um ponto da planta para ver os detalhes do assento.
        </p>
        </div>
      </div>
    </div>
    <ModalSalaReuniao
    :open="showReservaModal"
    @close="showReservaModal = false"
    @save="handleSalvarReserva"
    />

    <ModalCadeira
    :open="showCadeiraModal"
    :seat="selectedSeat"
    @close="showCadeiraModal = false"
    @reserve="handleReservaCadeira"
    />


  </div>
</template>

<style scoped>
.coworking-container {
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

.top-row {
  grid-column: 1 / -1;
  display: flex;
  justify-content: space-between;
  gap: 1.5rem;
  align-items: flex-start;
  margin-bottom: 0;
}

.legend-card {
  background: #ffffff;
  border-radius: 16px;
  padding: 0.9rem 1.1rem;
  box-shadow: 0 12px 30px rgba(0, 0, 0, 0.25);
  min-width: 240px;
}

.legend-title {
  font-size: 0.9rem;
  font-weight: 700;
  margin-bottom: 0.4rem;
}

.legend-items {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem 1rem;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 0.35rem;
  font-size: 0.8rem;
  color: #374151;
}

.legend-dot {
  width: 10px;
  height: 10px;
  border-radius: 999px;
  border: 2px solid #ffffff;
  box-shadow: 0 0 0 2px rgba(148, 163, 184, 0.5);
}

.legend-disponivel {
  background: #22c55e;
  box-shadow: 0 0 0 2px rgba(34, 197, 94, 0.4);
}
.legend-ocupado {
  background: #ef4444;
  box-shadow: 0 0 0 2px rgba(248, 113, 113, 0.5);
}
.legend-reservado {
  background: #eab308;
  box-shadow: 0 0 0 2px rgba(234, 179, 8, 0.5);
}
.legend-favorito {
  background: #3b82f6;
  box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.5);
}

.reserve-card {
  border: none;
  background: linear-gradient(135deg, #8b5cf6, #ec4899);
  color: #ffffff;
  border-radius: 18px;
  padding: 0.9rem 1.8rem;
  display: inline-flex;
  align-items: center;
  gap: 0.6rem;
  box-shadow: 0 18px 40px rgba(0, 0, 0, 0.45);
  cursor: pointer;
  font-weight: 600;
  font-size: 0.98rem;
  transition: transform 0.1s ease, box-shadow 0.12s ease, opacity 0.12s ease;
}

.reserve-card:hover {
  transform: translateY(-2px);
  opacity: 0.96;
  box-shadow: 0 22px 48px rgba(0, 0, 0, 0.6);
}

.reserve-plus {
  font-size: 1.4rem;
  font-weight: 700;
}

.reserve-text {
  white-space: nowrap;
}

.planta-card {
  grid-column: 1 / -1;
  background: #f9fafb;
  border-radius: 18px;
  padding: 1.5rem 1.7rem 1.8rem;
  box-shadow: 0 18px 40px rgba(0, 0, 0, 0.35);
}

.planta-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
}

.planta-title {
  font-weight: 600;
  font-size: 0.95rem;
}

.planta-select {
  min-width: 220px;
  border: 1px solid #d1d5db;
  padding: 0.35rem 0.8rem;
  font-size: 0.9rem;
  background: #ffffff;
}

.planta-wrapper {
  margin-top: 0.8rem;
  border-radius: 18px;
  overflow: hidden;
  position: relative;
  background: #111827;

  width: 100%;
  max-width: 1000px;
  margin-left: auto;
  margin-right: auto;

  aspect-ratio: 1 / 1;
}

.planta-img {
  width: 100%;
  height: 100%;
  display: block;
  object-fit: fill;
}

.seat-dot {
  position: absolute;
  width: 14px;
  height: 14px;
  border-radius: 999px;
  border: 2px solid #ffffff;
  transform: translate(-50%, -50%);
  cursor: pointer;
}

.seat-disponivel {
  background: #22c55e;
  box-shadow: 0 0 0 2px rgba(34, 197, 94, 0.4);
}

.seat-ocupado {
  background: #ef4444;
  box-shadow: 0 0 0 2px rgba(248, 113, 113, 0.5);
}

.seat-reservado {
  background: #eab308;
  box-shadow: 0 0 0 2px rgba(234, 179, 8, 0.5);
}

.seat-favorito {
  background: #3b82f6;
  box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.5);
}

.seat-info {
  margin-top: 0.75rem;
  font-size: 0.86rem;
  color: #111827;
}

.seat-info.muted {
  color: #6b7280;
}

@media (max-width: 800px) {
  .top-row {
    flex-direction: column;
    align-items: stretch;
  }

  .reserve-card {
    align-self: flex-end;
  }

  .planta-select {
    min-width: 0;
    width: 50%;
  }
}
</style>
