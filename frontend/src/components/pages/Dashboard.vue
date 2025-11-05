<script setup lang="ts">
import { computed, ref } from 'vue'
import { 
  Home, 
  LogOut, 
  Gauge, 
  MapPin, 
  Sofa, 
  Calendar, 
  Settings,
  FileText,
  Filter,
  Search,
  X
} from 'lucide-vue-next'
import { useAuth } from '@/composables/useAuth'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'

const { user, logout } = useAuth()

const isFilterModalOpen = ref(false)
const searchQuery = ref('')
const dateRange = ref('')
const startDate = ref<Date | null>(null)
const endDate = ref<Date | null>(null)
const currentMonth = ref(new Date())

const users = ref([
  'Claudio santana',
  'Maria Silva',
  'João Santos',
  'Ana Costa',
  'Pedro Oliveira',
  'Carla Ferreira',
  'Lucas Almeida'
])

const selectedUsers = ref<string[]>([])

const filteredUsers = computed(() => {
  if (!searchQuery.value.trim()) {
    return users.value
  }
  const query = searchQuery.value.toLowerCase().trim()
  return users.value.filter(user => 
    user.toLowerCase().includes(query)
  )
})

// Tooltip para gráfico de rosca
const tooltip = ref<{ show: boolean; label: string; percentage: string; x: number; y: number }>({
  show: false,
  label: '',
  percentage: '',
  x: 0,
  y: 0
})

const showTooltip = (event: Event, label: string, percentage: string) => {
  const mouseEvent = event as MouseEvent
  tooltip.value = {
    show: true,
    label,
    percentage,
    x: mouseEvent.clientX,
    y: mouseEvent.clientY
  }
}

const updateTooltipPosition = (event: Event) => {
  const mouseEvent = event as MouseEvent
  tooltip.value.x = mouseEvent.clientX
  tooltip.value.y = mouseEvent.clientY
}

const hideTooltip = () => {
  tooltip.value.show = false
}

const userInitials = computed(() => {
  if (!user.value) return 'U'
  const names = user.value.name.split(' ').filter(name => name.length > 0)
  if (names.length >= 2 && names[0] && names[1]) {
    return `${names[0][0]}${names[1][0]}`.toUpperCase()
  }
  return user.value.name.substring(0, 2).toUpperCase()
})

const handleLogout = () => {
  logout()
}

const openFilterModal = () => {
  isFilterModalOpen.value = true
}

const closeFilterModal = () => {
  isFilterModalOpen.value = false
}

const toggleUser = (userName: string) => {
  const index = selectedUsers.value.indexOf(userName)
  if (index > -1) {
    selectedUsers.value.splice(index, 1)
  } else {
    selectedUsers.value.push(userName)
  }
}

const getDaysInMonth = (date: Date) => {
  const year = date.getFullYear()
  const month = date.getMonth()
  const firstDay = new Date(year, month, 1)
  const lastDay = new Date(year, month + 1, 0)
  const daysInMonth = lastDay.getDate()
  const startingDayOfWeek = firstDay.getDay()
  
  const days: (Date | null)[] = []
  
  // Preencher dias do mês anterior
  for (let i = 0; i < startingDayOfWeek; i++) {
    days.push(null)
  }
  
  // Preencher dias do mês atual
  for (let day = 1; day <= daysInMonth; day++) {
    days.push(new Date(year, month, day))
  }
  
  return days
}

const selectDate = (date: Date) => {
  // Se não tem data inicial ou se já tem ambas, começa uma nova seleção
  if (!startDate.value || (startDate.value && endDate.value)) {
    startDate.value = date
    endDate.value = null
  } else {
    // Se já tem data inicial, define a data final
    if (date < startDate.value) {
      // Se a data selecionada é anterior à inicial, inverte
      endDate.value = startDate.value
      startDate.value = date
    } else {
      endDate.value = date
    }
  }
  
  // Atualiza o campo de data
  if (startDate.value && endDate.value) {
    const start = startDate.value.toLocaleDateString('pt-BR')
    const end = endDate.value.toLocaleDateString('pt-BR')
    dateRange.value = `${start} até ${end}`
  } else if (startDate.value) {
    dateRange.value = startDate.value.toLocaleDateString('pt-BR')
  }
}

const previousMonth = () => {
  currentMonth.value = new Date(
    currentMonth.value.getFullYear(),
    currentMonth.value.getMonth() - 1,
    1
  )
}

const nextMonth = () => {
  currentMonth.value = new Date(
    currentMonth.value.getFullYear(),
    currentMonth.value.getMonth() + 1,
    1
  )
}

const isToday = (date: Date) => {
  const today = new Date()
  return (
    date.getDate() === today.getDate() &&
    date.getMonth() === today.getMonth() &&
    date.getFullYear() === today.getFullYear()
  )
}

const isSelected = (date: Date) => {
  if (!startDate.value) return false
  
  const dateTime = date.getTime()
  const startTime = startDate.value.getTime()
  
  // Se só tem data inicial
  if (!endDate.value) {
    return dateTime === startTime
  }
  
  // Se tem intervalo, verifica se está dentro do range
  const endTime = endDate.value.getTime()
  return dateTime >= startTime && dateTime <= endTime
}

const isRangeStart = (date: Date) => {
  if (!startDate.value) return false
  return (
    date.getDate() === startDate.value.getDate() &&
    date.getMonth() === startDate.value.getMonth() &&
    date.getFullYear() === startDate.value.getFullYear()
  )
}

const isRangeEnd = (date: Date) => {
  if (!endDate.value) return false
  return (
    date.getDate() === endDate.value.getDate() &&
    date.getMonth() === endDate.value.getMonth() &&
    date.getFullYear() === endDate.value.getFullYear()
  )
}

const isInRange = (date: Date) => {
  if (!startDate.value || !endDate.value) return false
  const dateTime = date.getTime()
  const startTime = startDate.value.getTime()
  const endTime = endDate.value.getTime()
  return dateTime > startTime && dateTime < endTime
}

const monthNames = [
  'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
  'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'
]

const weekDays = ['Dom', 'Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb']
</script>

<template>
  <div class="dashboard-container">
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
          <Home class="header-icon" />
          <div class="user-info">
            <span class="navbar-user-name">{{ user?.name || 'Usuário' }}</span>
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
        <a href="#" class="nav-link active">
          <Gauge class="nav-icon" />
          <span>Dashboard</span>
        </a>
        <a href="#" class="nav-link">
          <MapPin class="nav-icon" />
          <span>Coworking</span>
        </a>
        <a href="#" class="nav-link">
          <Sofa class="nav-icon" />
          <span>Salas de reunião</span>
        </a>
        <a href="#" class="nav-link">
          <Calendar class="nav-icon" />
          <span>Minhas Reservas</span>
        </a>
        <a href="#" class="nav-link">
          <Settings class="nav-icon" />
          <span>Administração</span>
        </a>
      </div>
    </nav>
    
    <!-- Conteúdo principal -->
    <main class="dashboard-content">
      <!-- Grid Container -->
      <div class="dashboard-grid">
        <!-- Header do Dashboard -->
        <div class="dashboard-header">
          <div class="header-left-section">
            <h1 class="dashboard-title">Dashboard</h1>
            <p class="dashboard-subtitle">Visão Geral do co-working da Softex</p>
          </div>
          <div class="header-right-section">
            <Button class="report-button">
              Gerar Relatórios
            </Button>
            <Filter class="filter-icon" @click="openFilterModal" />
          </div>
        </div>

        <!-- Cards de Estatísticas -->
        <div class="stats-cards">
        <!-- Card 1: Posições Ocupadas -->
        <div class="stat-card card-blue">
          <div class="card-icon-wrapper icon-blue">
            <FileText class="card-icon" />
          </div>
          <div class="card-content">
            <h3 class="card-title">Posições Ocupadas</h3>
            <p class="card-value">32</p>
            <p class="card-detail">de 58 totais</p>
          </div>
        </div>

        <!-- Card 2: Salas em uso -->
        <div class="stat-card card-purple">
          <div class="card-icon-wrapper icon-purple">
            <FileText class="card-icon" />
          </div>
          <div class="card-content">
            <h3 class="card-title">Salas em uso</h3>
            <p class="card-value">4</p>
            <p class="card-detail">de 6 Salas disponíveis</p>
          </div>
        </div>

        <!-- Card 3: Reservas hoje -->
        <div class="stat-card card-pink">
          <div class="card-icon-wrapper icon-pink">
            <Calendar class="card-icon" />
          </div>
          <div class="card-content">
            <h3 class="card-title">Reservas hoje</h3>
            <p class="card-value">18</p>
            <p class="card-detail">de 30 reservas ativas</p>
          </div>
        </div>

        <!-- Card 4: Taxa de Ocupação -->
        <div class="stat-card card-gray">
          <div class="card-icon-wrapper icon-gray">
            <span class="percent-icon">%</span>
          </div>
          <div class="card-content">
            <h3 class="card-title">Taxa de Ocupação</h3>
            <p class="card-value">75%</p>
            <p class="card-detail">média semanal</p>
          </div>
        </div>
        </div>

        <!-- Gráficos -->
        <div class="charts-section">
          <!-- Gráfico de Barras: Ocupação por Horário -->
          <div class="chart-card">
            <h3 class="chart-title">Ocupação por Horário</h3>
            <div class="bar-chart-container">
              <div class="bars-container">
                <div class="bar bar-blue" style="height: 50%;">
                  <span class="bar-value">50%</span>
                </div>
                <div class="bar bar-light-blue" style="height: 78%;">
                  <span class="bar-value">78%</span>
                </div>
                <div class="bar bar-magenta" style="height: 98%;">
                  <span class="bar-value">98%</span>
                </div>
                <div class="bar bar-dark-blue" style="height: 70%;">
                  <span class="bar-value">70%</span>
                </div>
                <div class="bar bar-green" style="height: 55%;">
                  <span class="bar-value">55%</span>
                </div>
                <div class="bar bar-orange" style="height: 40%;">
                  <span class="bar-value">40%</span>
                </div>
              </div>
              <div class="bar-labels">
                <span class="bar-label">8h</span>
                <span class="bar-label">10h</span>
                <span class="bar-label">12h</span>
                <span class="bar-label">14h</span>
                <span class="bar-label">16h</span>
                <span class="bar-label">18h</span>
              </div>
            </div>
          </div>

          <!-- Gráfico de Rosca: Distribuição de uso -->
          <div class="chart-card">
            <h3 class="chart-title">Distribuição de uso</h3>
            <div class="donut-chart-container">
              <svg class="donut-chart" viewBox="0 0 200 200">
                <!-- Segmento Coworking (50%) -->
                <circle
                  cx="100"
                  cy="100"
                  r="70"
                  fill="none"
                  stroke="#1E3A8A"
                  stroke-width="30"
                  stroke-dasharray="219.91 439.82"
                  stroke-dashoffset="0"
                  transform="rotate(-90 100 100)"
                  class="donut-segment"
                  @mouseenter="(e) => showTooltip(e, 'Coworking', '50%')"
                  @mouseleave="hideTooltip"
                  @mousemove="updateTooltipPosition"
                />
                <!-- Segmento Salas (30%) -->
                <circle
                  cx="100"
                  cy="100"
                  r="70"
                  fill="none"
                  stroke="#3B82F6"
                  stroke-width="30"
                  stroke-dasharray="131.95 439.82"
                  stroke-dashoffset="-219.91"
                  transform="rotate(-90 100 100)"
                  class="donut-segment"
                  @mouseenter="(e) => showTooltip(e, 'Salas', '30%')"
                  @mouseleave="hideTooltip"
                  @mousemove="updateTooltipPosition"
                />
                <!-- Segmento Livre (20%) -->
                <circle
                  cx="100"
                  cy="100"
                  r="70"
                  fill="none"
                  stroke="#EC4899"
                  stroke-width="30"
                  stroke-dasharray="87.96 439.82"
                  stroke-dashoffset="-351.86"
                  transform="rotate(-90 100 100)"
                  class="donut-segment"
                  @mouseenter="(e) => showTooltip(e, 'Livre', '20%')"
                  @mouseleave="hideTooltip"
                  @mousemove="updateTooltipPosition"
                />
                <!-- Texto central -->
                <text x="100" y="95" text-anchor="middle" class="donut-center-text">
                  80%
                </text>
                <text x="100" y="110" text-anchor="middle" class="donut-center-subtext">
                  Ocupação
                </text>
              </svg>
              <!-- Tooltip -->
              <div 
                v-if="tooltip.show" 
                class="donut-tooltip"
                :style="{ left: tooltip.x + 'px', top: tooltip.y + 'px' }"
              >
                <div class="tooltip-label">{{ tooltip.label }}</div>
                <div class="tooltip-percentage">{{ tooltip.percentage }}</div>
              </div>
              <div class="donut-legend">
                <div class="legend-item">
                  <div class="legend-dot dot-dark-blue"></div>
                  <span>Coworking (50%)</span>
                </div>
                <div class="legend-item">
                  <div class="legend-dot dot-light-blue"></div>
                  <span>Salas (30%)</span>
                </div>
                <div class="legend-item">
                  <div class="legend-dot dot-magenta"></div>
                  <span>Livre (20%)</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Atividade Recente e Próximas Reservas -->
        <div class="activity-section">
          <!-- Card: Atividade Recente -->
          <div class="activity-card">
            <h3 class="activity-card-title">Atividade Recente</h3>
            <div class="activity-list">
              <div class="activity-item activity-green">
                <div class="activity-dot dot-green"></div>
                <div class="activity-content">
                  <p class="activity-text">Maria santos reservou sala Zeus</p>
                  <p class="activity-time">14:30-16:00 hoje</p>
                </div>
              </div>
              <div class="activity-item activity-blue">
                <div class="activity-dot dot-blue"></div>
                <div class="activity-content">
                  <p class="activity-text">Pedro Lima ocupou Posição A-15</p>
                  <p class="activity-time">13:45 hoje</p>
                </div>
              </div>
              <div class="activity-item activity-orange">
                <div class="activity-dot dot-orange"></div>
                <div class="activity-content">
                  <p class="activity-text">Sala Apolo liberada</p>
                  <p class="activity-time">14:30-16:00 hoje</p>
                </div>
              </div>
            </div>
          </div>

          <!-- Card: Próximas Reservas -->
          <div class="reservations-card">
            <h3 class="activity-card-title">Próximas Reservas</h3>
            <div class="reservations-list">
              <div class="reservation-item">
                <div class="reservation-content">
                  <p class="reservation-title">Reunião de Projeto</p>
                  <p class="reservation-subtitle">Sala Hermes - 15:00-16:30</p>
                </div>
                <span class="reservation-tag tag-purple">Em 30 min</span>
              </div>
              <div class="reservation-item">
                <div class="reservation-content">
                  <p class="reservation-title">Apresentação Cliente</p>
                  <p class="reservation-subtitle">Sala Zeus - 16:00-17:00</p>
                </div>
                <span class="reservation-tag tag-green">Em 1h30</span>
              </div>
              <div class="reservation-item">
                <div class="reservation-content">
                  <p class="reservation-title">Workshop Técnico</p>
                  <p class="reservation-subtitle">Sala Apolo - 17:30-19:00</p>
                </div>
                <span class="reservation-tag tag-orange">Em 3h</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Rodapé -->
      <footer class="dashboard-footer">
        <div class="footer-content">
          <span class="footer-text">© 2025 - Softex</span>
          <span class="footer-text">All rights reserved</span>
        </div>
      </footer>

      <!-- Modal de Filtros -->
      <div v-if="isFilterModalOpen" class="modal-overlay" @click="closeFilterModal">
        <div class="modal-content" @click.stop>
          <div class="modal-header">
            <h2 class="modal-title">Filtros</h2>
            <button class="modal-close" @click="closeFilterModal">
              <X class="close-icon" />
            </button>
          </div>
          
          <div class="modal-body">
            <div class="modal-top-row">
              <div class="search-input-wrapper">
                <Search class="search-icon" />
                <Input
                  v-model="searchQuery"
                  placeholder="Buscar..."
                  class="search-input"
                />
              </div>
              
              <div class="date-input-wrapper">
                <Label class="date-label">calendário</Label>
                <div class="date-input-container">
                  <Calendar class="calendar-icon" />
                  <Input
                    v-model="dateRange"
                    placeholder="até"
                    class="date-input"
                  />
                </div>
              </div>
            </div>

            <div class="modal-bottom-row">
              <div class="users-list">
                <div
                  v-for="userName in filteredUsers"
                  :key="userName"
                  class="user-checkbox-item"
                  @click="toggleUser(userName)"
                >
                  <input
                    type="checkbox"
                    :checked="selectedUsers.includes(userName)"
                    class="checkbox-input"
                    @click.stop
                    @change="toggleUser(userName)"
                  />
                  <span class="user-name">{{ userName }}</span>
                </div>
                <div v-if="filteredUsers.length === 0" class="no-results">
                  Nenhum usuário encontrado
                </div>
              </div>

              <div class="calendar-container">
                <div class="calendar-header">
                  <button class="calendar-nav-button" @click="previousMonth">
                    <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                      <path d="M10 12L6 8L10 4" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                  </button>
                  <h3 class="calendar-month-title">
                    {{ monthNames[currentMonth.getMonth()] }} {{ currentMonth.getFullYear() }}
                  </h3>
                  <button class="calendar-nav-button" @click="nextMonth">
                    <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                      <path d="M6 4L10 8L6 12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                  </button>
                </div>
                
                <div class="calendar-weekdays">
                  <div v-for="day in weekDays" :key="day" class="weekday">
                    {{ day }}
                  </div>
                </div>
                
                <div class="calendar-days">
                  <div
                    v-for="(date, index) in getDaysInMonth(currentMonth)"
                    :key="index"
                    class="calendar-day"
                    :class="{
                      'empty': date === null,
                      'today': date && isToday(date),
                      'selected': date && isSelected(date),
                      'range-start': date && isRangeStart(date),
                      'range-end': date && isRangeEnd(date),
                      'in-range': date && isInRange(date)
                    }"
                    @click="date && selectDate(date)"
                  >
                    {{ date ? date.getDate() : '' }}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<style scoped>
.dashboard-container {
  min-height: 100vh;
  background: linear-gradient(to bottom, #1C2457 0%, #2F2365 40%, #4A2E70 70%, #6C5885 100%);
  width: 100%;
  display: flex;
  flex-direction: column;
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

.brand-name {
  color: white;
  font-size: 1rem;
  font-weight: 500;
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

.dashboard-header {
  grid-column: 1 / -1;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 0;
}

.header-left-section {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.dashboard-title {
  color: white;
  font-size: 2rem;
  font-weight: 600;
  margin: 0;
}

.dashboard-subtitle {
  color: rgba(255, 255, 255, 0.7);
  font-size: 1rem;
  margin: 0;
}

.header-right-section {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.report-button {
  background: #374151;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 0.5rem;
  font-weight: 500;
  cursor: pointer;
  transition: background 0.2s;
}

.report-button:hover {
  background: #4B5563;
}

.filter-icon {
  width: 20px;
  height: 20px;
  color: rgba(255, 255, 255, 0.7);
  cursor: pointer;
}

.filter-icon:hover {
  color: white;
}

.stats-cards {
  grid-column: 1 / -1;
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  gap: 2rem;
  width: 100%;
}

.stat-card {
  grid-column: span 3;
  background: white;
  border-radius: 0.5rem;
  padding: 1rem;
  position: relative;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  min-height: 100px;
}

.stat-card::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 4px;
  border-radius: 0.75rem 0 0 0.75rem;
}

.card-blue::before {
  background: #3B82F6;
}

.card-purple::before {
  background: #7C3AED;
}

.card-pink::before {
  background: #EC4899;
}

.card-gray::before {
  background: #6B7280;
}

.card-icon-wrapper {
  position: absolute;
  top: 0.75rem;
  right: 0.75rem;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.icon-blue {
  background: #DBEAFE;
}

.icon-purple {
  background: #EDE9FE;
}

.icon-pink {
  background: #FCE7F3;
}

.icon-gray {
  background: #F3F4F6;
}

.card-icon {
  width: 16px;
  height: 16px;
}

.icon-blue .card-icon {
  color: #3B82F6;
}

.icon-purple .card-icon {
  color: #7C3AED;
}

.icon-pink .card-icon {
  color: #EC4899;
}

.percent-icon {
  font-size: 1rem;
  font-weight: 600;
  color: #6B7280;
}

.card-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  margin-top: 1.5rem;
}

.card-title {
  color: #6B7280;
  font-size: 0.75rem;
  font-weight: 500;
  margin: 0 0 0.375rem 0;
}

.card-value {
  color: #1F2937;
  font-size: 1.5rem;
  font-weight: 700;
  margin: 0 0 0.125rem 0;
}

.card-detail {
  color: #9CA3AF;
  font-size: 0.6875rem;
  margin: 0;
}

/* Charts Section */
.charts-section {
  grid-column: 1 / -1;
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  gap: 2rem;
  margin-top: 2rem;
}

.activity-section {
  grid-column: 1 / -1;
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  gap: 2rem;
  margin-top: 2rem;
}

.activity-card,
.reservations-card {
  grid-column: span 6;
  background: white;
  border-radius: 0.75rem;
  padding: 1.5rem;
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
}

.activity-card-title {
  color: #1F2937;
  font-size: 1rem;
  font-weight: 600;
  margin: 0 0 1.5rem 0;
}

.activity-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.activity-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem;
  border-radius: 0.5rem;
}

.activity-item.activity-green {
  background: #D1FAE5;
}

.activity-item.activity-blue {
  background: #DBEAFE;
}

.activity-item.activity-orange {
  background: #FED7AA;
}

.activity-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  flex-shrink: 0;
}

.dot-green {
  background: #10B981;
}

.dot-blue {
  background: #3B82F6;
}

.dot-orange {
  background: #F59E0B;
}

.activity-content {
  flex: 1;
}

.activity-text {
  color: #374151;
  font-size: 0.875rem;
  font-weight: 500;
  margin: 0 0 0.25rem 0;
}

.activity-time {
  color: #9CA3AF;
  font-size: 0.75rem;
  margin: 0;
}

.reservations-list {
  display: flex;
  flex-direction: column;
  gap: 0;
}

.reservation-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem 0;
  border-bottom: 1px solid #E5E7EB;
}

.reservation-item:last-child {
  border-bottom: none;
}

.reservation-content {
  flex: 1;
}

.reservation-title {
  color: #374151;
  font-size: 0.875rem;
  font-weight: 500;
  margin: 0 0 0.25rem 0;
}

.reservation-subtitle {
  color: #9CA3AF;
  font-size: 0.75rem;
  margin: 0;
}

.reservation-tag {
  padding: 0.25rem 0.75rem;
  border-radius: 0.375rem;
  font-size: 0.75rem;
  font-weight: 500;
  color: white;
  flex-shrink: 0;
}

.tag-purple {
  background: #A78BFA;
}

.tag-green {
  background: #10B981;
}

.tag-orange {
  background: #F59E0B;
}

.chart-card {
  grid-column: span 6;
  background: white;
  border-radius: 0.75rem;
  padding: 1.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.chart-title {
  color: #1F2937;
  font-size: 1rem;
  font-weight: 600;
  margin: 0 0 1.5rem 0;
}

/* Bar Chart Styles */
.bar-chart-container {
  display: flex;
  flex-direction: column;
  height: 300px;
}

.bars-container {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  width: 100%;
  flex: 1;
  gap: 0.75rem;
  min-height: 0;
}

.bar {
  flex: 1;
  max-width: 60px;
  border-radius: 0.5rem 0.5rem 0 0;
  position: relative;
  display: flex;
  align-items: flex-start;
  justify-content: center;
  transition: height 0.3s ease;
}

.bar-labels {
  display: flex;
  justify-content: space-between;
  width: 100%;
  gap: 0.75rem;
  margin-top: 0.5rem;
  flex-shrink: 0;
}

.bar-label {
  flex: 1;
  text-align: center;
  max-width: 60px;
}

.bar-value {
  color: white;
  font-size: 0.75rem;
  font-weight: 600;
  position: absolute;
  top: 0.5rem;
  left: 50%;
  transform: translateX(-50%);
}

.bar-blue {
  background: #3B82F6;
}

.bar-light-blue {
  background: #60A5FA;
}

.bar-magenta {
  background: #EC4899;
}

.bar-dark-blue {
  background: #1E3A8A;
}

.bar-green {
  background: #10B981;
}

.bar-orange {
  background: #F59E0B;
}

.bar-label {
  color: #6B7280;
  font-size: 0.75rem;
  font-weight: 500;
  margin-top: 0.5rem;
  flex-shrink: 0;
}

/* Donut Chart Styles */
.donut-chart-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1.5rem;
}

.donut-chart {
  width: 200px;
  height: 200px;
  position: relative;
}

.donut-segment {
  cursor: pointer;
  transition: opacity 0.2s ease;
}

.donut-segment:hover {
  opacity: 0.8;
}

.donut-tooltip {
  position: fixed;
  background: #1F2937;
  color: white;
  padding: 0.5rem 0.75rem;
  border-radius: 0.5rem;
  font-size: 0.875rem;
  pointer-events: none;
  z-index: 1000;
  transform: translate(-50%, -100%);
  margin-top: -0.5rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  white-space: nowrap;
}

.tooltip-label {
  font-weight: 600;
  margin-bottom: 0.25rem;
}

.tooltip-percentage {
  font-weight: 500;
  opacity: 0.9;
}

.donut-center-text {
  fill: #1F2937;
  font-size: 24px;
  font-weight: 700;
}

.donut-center-subtext {
  fill: #6B7280;
  font-size: 14px;
  font-weight: 500;
}

.donut-legend {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  width: 100%;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  color: #1F2937;
  font-size: 0.875rem;
}

.legend-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  flex-shrink: 0;
}

.dot-dark-blue {
  background: #1E3A8A;
}

.dot-light-blue {
  background: #3B82F6;
}

.dot-magenta {
  background: #EC4899;
}

.legend-dot-empty {
  background: transparent;
  border: 2px solid #E5E7EB;
}

/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 2rem;
}

.modal-content {
  background: white;
  border-radius: 1rem;
  width: 100%;
  max-width: 900px;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.3), 0 10px 10px -5px rgba(0, 0, 0, 0.2);
  overflow: hidden;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid #e5e7eb;
}

.modal-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #1F2937;
  margin: 0;
}

.modal-close {
  background: none;
  border: none;
  cursor: pointer;
  padding: 0.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #6B7280;
  transition: color 0.2s;
}

.modal-close:hover {
  color: #1F2937;
}

.close-icon {
  width: 20px;
  height: 20px;
}

.modal-body {
  padding: 1.5rem;
  flex: 1;
  overflow-y: auto;
}

.modal-top-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.search-input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.search-icon {
  position: absolute;
  left: 0.75rem;
  width: 20px;
  height: 20px;
  color: #6B7280;
  pointer-events: none;
}

.search-input {
  padding-left: 2.75rem;
}

.date-input-wrapper {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.date-label {
  font-size: 0.75rem;
  color: #3B82F6;
  font-weight: 500;
}

.date-input-container {
  position: relative;
  display: flex;
  align-items: center;
}

.calendar-icon {
  position: absolute;
  left: 0.75rem;
  width: 18px;
  height: 18px;
  color: #6B7280;
  pointer-events: none;
}

.date-input {
  padding-left: 2.75rem;
}

.modal-bottom-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
}

.users-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  max-height: 400px;
  overflow-y: auto;
}

.user-checkbox-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.5rem;
  cursor: pointer;
  border-radius: 0.5rem;
  transition: background 0.2s;
}

.user-checkbox-item:hover {
  background: #F3F4F6;
}

.checkbox-input {
  width: 18px;
  height: 18px;
  cursor: pointer;
  accent-color: #7C3AED;
}

.user-name {
  color: #1F2937;
  font-size: 0.875rem;
}

.no-results {
  color: #9CA3AF;
  font-size: 0.875rem;
  text-align: center;
  padding: 2rem;
  font-style: italic;
}

.calendar-container {
  background: #1C2457;
  border-radius: 0.75rem;
  padding: 1.5rem;
  min-height: 400px;
  display: flex;
  flex-direction: column;
}

.calendar-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.calendar-nav-button {
  background: rgba(255, 255, 255, 0.1);
  border: none;
  border-radius: 0.5rem;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: white;
  transition: background 0.2s;
}

.calendar-nav-button:hover {
  background: rgba(255, 255, 255, 0.2);
}

.calendar-month-title {
  color: white;
  font-size: 1rem;
  font-weight: 600;
  margin: 0;
}

.calendar-weekdays {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.weekday {
  color: rgba(255, 255, 255, 0.7);
  font-size: 0.75rem;
  font-weight: 500;
  text-align: center;
  padding: 0.5rem 0;
}

.calendar-days {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 0.5rem;
  flex: 1;
}

.calendar-day {
  aspect-ratio: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  color: rgba(255, 255, 255, 0.8);
  font-size: 0.875rem;
  cursor: pointer;
  border-radius: 0.5rem;
  transition: all 0.2s;
}

.calendar-day.empty {
  cursor: default;
  color: transparent;
}

.calendar-day:not(.empty):hover {
  background: rgba(255, 255, 255, 0.15);
}

.calendar-day.today {
  background: rgba(255, 255, 255, 0.2);
  font-weight: 600;
}

.calendar-day.selected {
  background: #7C3AED;
  color: white;
  font-weight: 600;
}

.calendar-day.selected:hover {
  background: #8B5CF6;
}

.calendar-day.range-start {
  background: #7C3AED;
  color: white;
  font-weight: 600;
  border-radius: 0.5rem 0 0 0.5rem;
}

.calendar-day.range-end {
  background: #7C3AED;
  color: white;
  font-weight: 600;
  border-radius: 0 0.5rem 0.5rem 0;
}

.calendar-day.in-range {
  background: rgba(124, 58, 237, 0.3);
  color: white;
  border-radius: 0;
}

/* Footer */
.dashboard-footer {
  grid-column: 1 / -1;
  width: 100%;
  margin-top: 3rem;
  padding: 2rem 0;
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

.calendar-day.range-start.range-end {
  border-radius: 0.5rem;
}
</style>
