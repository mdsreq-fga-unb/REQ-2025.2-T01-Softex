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
import AndamentoModal from '@/components/modals/salas/Andamento.vue'
import ConcluidasModal from '@/components/modals/salas/Concluidas.vue'
import SalaDeReuniao from '@/components/modals/salas/SalaDeReuniao.vue'
import CancelarReuniaoModal from '@/components/modals/salas/CancelarReuniao.vue'

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

type FluxoStatus = 'andamento' | 'concluido'
type ResultadoStatus = 'aprovado' | 'pendente' | 'negado'

type ReservaSala = {
  id: number
  titulo: string       
  solicitante: string  
  sala: string         
  fluxo: FluxoStatus
  status: ResultadoStatus
  data: string                
  dataInicio: string          
  dataFim: string            
  horaInicio: string   
  horaFim: string      
  participantes: number
  tipoReuniao: 'interna' | 'externa'
  motivoReuniao?: string  
}


type Aba = 'solicitacoes' | 'salas' | 'concluidas'

const activeTab = ref<Aba>('solicitacoes')
const reservasSalas = ref<ReservaSala[]>([
  {
    id: 1,
    titulo: 'Sala Alfa - Andar 3',
    solicitante: 'Ana Souza',
    sala: 'Sala Alfa',
    fluxo: 'andamento',
    status: 'pendente',
    data: '10/03/2026',
    dataInicio: '10/03/2026',
    dataFim: '10/03/2026',
    horaInicio: '09:00',
    horaFim: '10:00',
    participantes: 6,
    tipoReuniao: 'interna',
    motivoReuniao: 'Alinhamento semanal com o time de produto.'
  },
  {
    id: 2,
    titulo: 'Sala Beta - Andar 2',
    solicitante: 'Carlos Lima',
    sala: 'Sala Beta',
    fluxo: 'andamento',
    status: 'aprovado',
    data: '11/03/2026',
    dataInicio: '11/03/2026',
    dataFim: '11/03/2026',
    horaInicio: '14:00',
    horaFim: '15:30',
    participantes: 4,
    tipoReuniao: 'externa',
    motivoReuniao: 'Reunião com cliente para apresentação de proposta.'
  },
  {
    id: 3,
    titulo: 'Sala Ômega - Andar 1',
    solicitante: 'Mariana Costa',
    sala: 'Sala Ômega',
    fluxo: 'concluido',
    status: 'aprovado',
    data: '02/03/2026',
    dataInicio: '02/03/2026',
    dataFim: '02/03/2026',
    horaInicio: '16:00',
    horaFim: '17:00',
    participantes: 8,
    tipoReuniao: 'interna',
    motivoReuniao: 'Retrospectiva do projeto e planejamento do próximo ciclo.'
  },
  {
    id: 4,
    titulo: 'Sala Gama - Andar 4',
    solicitante: 'João Pedro',
    sala: 'Sala Gama',
    fluxo: 'concluido',
    status: 'negado',
    data: '25/02/2026',
    dataInicio: '25/02/2026',
    dataFim: '25/02/2026',
    horaInicio: '11:00',
    horaFim: '12:00',
    participantes: 5,
    tipoReuniao: 'externa',
    motivoReuniao: 'Reunião extra com parceiro, fora do calendário padrão.'
  },
  {
    id: 5,
    titulo: 'Sala Alpha - Andar 4',
    solicitante: 'João Pedro',
    sala: 'Sala Alpha',
    fluxo: 'concluido',
    status: 'negado',
    data: '21/11/2025',
    dataInicio: '21/11/2025',
    dataFim: '21/11/2025',
    horaInicio: '11:00',
    horaFim: '12:00',
    participantes: 5,
    tipoReuniao: 'externa',
    motivoReuniao: 'Reunião extra com parceiro, fora do calendário padrão.'
  }
])

const solicitacoesEmAndamento = computed(() =>
  reservasSalas.value.filter(r => r.fluxo === 'andamento')
)

const reservasConcluidas = computed(() =>
  reservasSalas.value.filter(r => r.fluxo === 'concluido')
)

const selecionarTab = (tab: Aba) => {
  activeTab.value = tab
}

const showAndamentoModal = ref(false)
const showConcluidasModal = ref(false)
const showCancelarModal = ref(false)

const reservaAndamentoSelecionada = ref<any | null>(null)
const reservaConcluidaSelecionada = ref<any | null>(null)
const reservaCancelarSelecionada = ref<any | null>(null)

const handleClickReserva = (reserva: ReservaSala) => {
  if (activeTab.value === 'solicitacoes') {
    reservaAndamentoSelecionada.value = reserva
    showAndamentoModal.value = true
  } else if (activeTab.value === 'concluidas') {
    reservaConcluidaSelecionada.value = reserva
    showConcluidasModal.value = true
  } else {
    // aba "salas" não abre modal aqui
  }
}

const handleAprovarReserva = (payload: { id: number; salaEscolhida: string; codigoSala: string }) => {
  const reserva = reservasSalas.value.find(r => r.id === payload.id)
  if (reserva) {
    reserva.status = 'aprovado'
    reserva.sala = payload.salaEscolhida
    console.log('Reserva aprovada:', payload)
  }
  showAndamentoModal.value = false
  reservaAndamentoSelecionada.value = null
}

const handleRecusarReserva = (id: number) => {
  const reserva = reservasSalas.value.find(r => r.id === id)
  if (reserva) {
    reserva.status = 'negado'
    reserva.fluxo = 'concluido'
    console.log('Reserva recusada:', id)
  }
  showAndamentoModal.value = false
  reservaAndamentoSelecionada.value = null
}

const handleCancelarClick = (id: number) => {
  const reserva = reservasSalas.value.find(r => r.id === id)
  if (reserva) {
    reservaCancelarSelecionada.value = reserva
    showCancelarModal.value = true
    showAndamentoModal.value = false
  }
}

const handleConfirmarCancelamento = (id: number) => {
  const reserva = reservasSalas.value.find(r => r.id === id)
  if (reserva) {
    reserva.status = 'negado'
    reserva.fluxo = 'concluido'
  }
  showCancelarModal.value = false
  reservaCancelarSelecionada.value = null
  console.log('Reunião cancelada:', id)
}

const labelResultado = (resultado: ResultadoStatus): string => {
  if (resultado === 'aprovado') return 'Aprovada'
  if (resultado === 'pendente') return 'Pendente'
  return 'Negada'
}

const resultadoClass = (resultado: ResultadoStatus): string => {
  if (resultado === 'aprovado') return 'status-ok'
  if (resultado === 'pendente') return 'status-wait'
  return 'status-denied'
}

const labelTipoReuniao = (tipo: 'interna' | 'externa'): string =>
  tipo === 'interna' ? 'Reunião interna' : 'Reunião externa'


const toIsoFromBr = (dateBr: string): string => {
  if (!dateBr) return ''

  const parts = dateBr.split('/')
  const dia = parts[0]
  const mes = parts[1]
  const ano = parts[2]

  if (!dia || !mes || !ano) return ''

  return `${ano}-${mes.padStart(2, '0')}-${dia.padStart(2, '0')}`
}



const filtroDataInicio = ref<string>('')   // yyyy-MM-dd (input type="date")
const filtroDataFim = ref<string>('')      // yyyy-MM-dd
const ordenacao = ref<'recentes' | 'antigas'>('recentes')
const filtroStatus = ref<'todos' | 'aprovado' | 'recusado' | 'cancelado'>('todos')

const reservaEstaNoIntervalo = (reserva: ReservaSala): boolean => {
  if (!filtroDataInicio.value && !filtroDataFim.value) {
    return true
  }

  const reservaIso = toIsoFromBr(reserva.data)
  if (!reservaIso) return false

  // Só data início
  if (filtroDataInicio.value && !filtroDataFim.value) {
    return reservaIso >= filtroDataInicio.value
  }

  // Só data fim
  if (!filtroDataInicio.value && filtroDataFim.value) {
    return reservaIso <= filtroDataFim.value
  }

  // Ambos os filtros
  if (filtroDataInicio.value && filtroDataFim.value) {
    return reservaIso >= filtroDataInicio.value && reservaIso <= filtroDataFim.value
  }

  return true
}

const mapearStatusFiltro = (statusFiltro: string): ResultadoStatus | null => {
  switch (statusFiltro) {
    case 'aprovado':
      return 'aprovado'
    case 'recusado':
      return 'negado'
    case 'cancelado':
      return 'negado'
    default:
      return null
  }
}

const reservasConcluidasFiltradas = computed(() => {
  let lista = reservasConcluidas.value.slice()

  // Filtro por status
  if (filtroStatus.value !== 'todos') {
    const statusMapeado = mapearStatusFiltro(filtroStatus.value)
    if (statusMapeado) {
      lista = lista.filter(r => r.status === statusMapeado)
    }
  }

  // Filtro por intervalo de datas
  lista = lista.filter(r => reservaEstaNoIntervalo(r))

  // Ordenação
  lista.sort((a, b) => {
    const aKey = `${toIsoFromBr(a.data)}T${a.horaInicio}`
    const bKey = `${toIsoFromBr(b.data)}T${b.horaInicio}`

    if (ordenacao.value === 'recentes') {
      return aKey < bKey ? 1 : -1
    } else {
      return aKey < bKey ? -1 : 1
    }
  })

  return lista
})
</script>


<template>
  <div class="salas-container min-h-screen">
    <!-- Navbar -->
    <nav class="navbar">
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
          :class="{ 'tab-active': activeTab === 'solicitacoes' }"
          @click="selecionarTab('solicitacoes')"
        >
          Solicitações em andamento
        </button>

        <span class="tab-separator">/</span>

        <button
          type="button"
          class="tab-btn"
          :class="{ 'tab-active': activeTab === 'salas' }"
          @click="selecionarTab('salas')"
        >
          Salas de reunião
        </button>

        <span class="tab-separator">/</span>

        <button
          type="button"
          class="tab-btn"
          :class="{ 'tab-active': activeTab === 'concluidas' }"
          @click="selecionarTab('concluidas')"
        >
          Concluídas
        </button>
      </div>

      <div class="card">
        <h2 class="card-title">
          <span v-if="activeTab === 'solicitacoes'">Solicitações de salas</span>
          <span v-else-if="activeTab === 'salas'">Salas de reunião</span>
          <span v-else>Histórico de reservas</span>
        </h2>

        <template v-if="activeTab === 'solicitacoes'">
          <div v-if="solicitacoesEmAndamento.length === 0" class="empty-state">
            <p>Não há solicitações de salas em andamento no momento.</p>
            <p class="empty-hint">
              Assim que alguém solicitar uma sala de reunião, ela aparecerá aqui para análise.
            </p>
          </div>

          <div v-else class="lista-reservas">
            <button
              v-for="reserva in solicitacoesEmAndamento"
              :key="reserva.id"
              type="button"
              class="reserva-item"
              @click="handleClickReserva(reserva)"
            >
              <div class="reserva-main">
                <p class="reserva-titulo">{{ reserva.titulo }}</p>
                <p class="reserva-desc">
                  Solicitante: <strong>{{ reserva.solicitante }}</strong>
                </p>
                <p v-if="reserva.motivoReuniao" class="reserva-motivo">
                  Motivo: {{ reserva.motivoReuniao }}
                </p>
                <p class="reserva-sub">
                  {{ reserva.data }}
                  · {{ reserva.horaInicio }} → {{ reserva.horaFim }}
                </p>
              </div>

              <div class="reserva-meta">
                <span class="badge status" :class="resultadoClass(reserva.status)">
                  {{ labelResultado(reserva.status) }}
                </span>
                <span class="badge tipo">
                  {{ labelTipoReuniao(reserva.tipoReuniao) }}
                </span>
                <span class="badge sala">
                  {{ reserva.sala }}
                </span>
                <span class="badge pessoas">
                  {{ reserva.participantes }} pessoas
                </span>
              </div>
            </button>
          </div>
        </template>

        <template v-else-if="activeTab === 'salas'">
          <SalaDeReuniao :reservas="reservasSalas" />
        </template>

        <template v-else>
          <div class="filtros-concluidas">
            <div class="filtro-data-range">
              <label class="filtro-label">
                De
                <input
                  v-model="filtroDataInicio"
                  type="date"
                  class="filtro-date-input"
                />
              </label>
              <label class="filtro-label">
                Até
                <input
                  v-model="filtroDataFim"
                  type="date"
                  class="filtro-date-input"
                />
              </label>
            </div>

            <!-- 🔹 FILTRO DE STATUS -->
            <div class="filtro-status">
              <label class="filtro-label">
                Status
                <select v-model="filtroStatus" class="filtro-select">
                  <option value="todos">Todos</option>
                  <option value="aprovado">Aprovado</option>
                  <option value="recusado">Recusado</option>
                  <option value="cancelado">Cancelado</option>
                </select>
              </label>
            </div>

            <div class="filtro-ordenacao">
              <label class="filtro-label">
                Ordenar
                <select v-model="ordenacao" class="filtro-select">
                  <option value="recentes">Mais recentes primeiro</option>
                  <option value="antigas">Mais antigas primeiro</option>
                </select>
              </label>
            </div>
          </div>


          <div v-if="reservasConcluidasFiltradas.length === 0" class="empty-state">
            <p>Nenhuma reserva encontrada para os filtros selecionados.</p>
            <p class="empty-hint">
              Ajuste o período ou a ordenação para visualizar outras reservas concluídas.
            </p>
          </div>

          <div v-else class="lista-reservas">
            <button
              v-for="reserva in reservasConcluidasFiltradas"
              :key="reserva.id"
              type="button"
              class="reserva-item"
              @click="handleClickReserva(reserva)"
            >
              <div class="reserva-main">
                <p class="reserva-titulo">{{ reserva.titulo }}</p>
                <p class="reserva-desc">
                  Solicitante: <strong>{{ reserva.solicitante }}</strong>
                </p>
                <p v-if="reserva.motivoReuniao" class="reserva-motivo">
                  Motivo: {{ reserva.motivoReuniao }}
                </p>
                <p class="reserva-sub">
                  {{ reserva.data }}
                  · {{ reserva.horaInicio }} → {{ reserva.horaFim }}
                </p>
              </div>

              <div class="reserva-meta">
                <span class="badge status" :class="resultadoClass(reserva.status)">
                  {{ labelResultado(reserva.status) }}
                </span>
                <span class="badge tipo">
                  {{ labelTipoReuniao(reserva.tipoReuniao) }}
                </span>
                <span class="badge sala">
                  {{ reserva.sala }}
                </span>
                <span class="badge pessoas">
                  {{ reserva.participantes }} pessoas
                </span>
              </div>
            </button>
          </div>
        </template>
        </div>
      </div>
    </div>

    <AndamentoModal
      :open="showAndamentoModal"
      :reserva="reservaAndamentoSelecionada"
      @close="showAndamentoModal = false"
      @aprovar="handleAprovarReserva"
      @recusar="handleRecusarReserva"
      @cancelar="handleCancelarClick"
    />

    <ConcluidasModal
      :open="showConcluidasModal"
      :reserva="reservaConcluidaSelecionada"
      @close="showConcluidasModal = false"
    />

    <CancelarReuniaoModal
      :open="showCancelarModal"
      :reserva="reservaCancelarSelecionada"
      @close="showCancelarModal = false"
      @cancelar="handleConfirmarCancelamento"
    />
  </div>
</template>

<style scoped>
.salas-container {
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

.filtros-concluidas {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  gap: 1rem;
  margin-bottom: 1rem;
}

.filtro-data-range {
  display: flex;
  gap: 0.75rem;
}

.filtro-label {
  display: flex;
  flex-direction: column;
  font-size: 0.75rem;
  font-weight: 600;
  color: #374151;
  gap: 0.25rem;
}

.filtro-date-input,
.filtro-select {
  border-radius: 999px;
  border: 1px solid #d1d5db;
  padding: 0.35rem 0.9rem;
  font-size: 0.8rem;
  outline: none;
}

.filtro-date-input:focus,
.filtro-select:focus {
  border-color: #3b82f6;
  box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.25);
}

.filtro-ordenacao {
  display: flex;
  align-items: flex-end;
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
  border-radius: 16px;
  background: #e5e7eb;
  padding: 0.9rem 1.4rem;
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
  gap: 0.15rem;
}

.reserva-titulo {
  font-weight: 600;
  font-size: 0.9rem;
  color: #111827;
}

.reserva-desc {
  font-size: 0.8rem;
  color: #4b5563;
}

.reserva-motivo {
  font-size: 0.78rem;
  color: #6b7280;
}

.reserva-sub {
  font-size: 0.78rem;
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
  display: inline-block;
}

.badge.tipo {
  background: #312e81;
  color: #e5e7eb;
}

.badge.sala {
  background: #d1d5db;
  color: #111827;
}

.badge.pessoas {
  background: #e0f2fe;
  color: #075985;
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

.filtros-concluidas {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  gap: 1rem;
  margin-bottom: 1rem;
}


}
</style>
