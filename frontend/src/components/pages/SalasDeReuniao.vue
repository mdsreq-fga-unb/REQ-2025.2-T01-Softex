<script setup lang="ts">
import { ref, computed } from 'vue'
import Header from '@/components/Layout/Header.vue'
import AndamentoModal from '@/components/modals/salas/Andamento.vue'
import ConcluidasModal from '@/components/modals/salas/Concluidas.vue'
import SalaDeReuniao from '@/components/modals/salas/SalaDeReuniao.vue'

type FluxoStatus = 'andamento' | 'concluido'
type ResultadoStatus = 'aprovado' | 'pendente' | 'negado'

type ReservaSala = {
  id: number
  titulo: string       
  solicitante: string  
  sala: string         
  fluxo: FluxoStatus
  status: ResultadoStatus
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

const reservaAndamentoSelecionada = ref<ReservaSala | null>(null)
const reservaConcluidaSelecionada = ref<ReservaSala | null>(null)

const handleClickReserva = (reserva: ReservaSala) => {
  if (activeTab.value === 'solicitacoes') {
    reservaAndamentoSelecionada.value = reserva
    showAndamentoModal.value = true
  } else if (activeTab.value === 'concluidas') {
    reservaConcluidaSelecionada.value = reserva
    showConcluidasModal.value = true
  } else {
    
  }
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
  const [dia, mes, ano] = dateBr.split('/')
  return `${ano}-${mes.padStart(2, '0')}-${dia.padStart(2, '0')}`
}

const filtroDataInicio = ref<string>('')
const filtroDataFim = ref<string>('')    
const ordenacao = ref<'recentes' | 'antigas'>('recentes')

const reservasConcluidasFiltradas = computed(() => {
  let lista = reservasConcluidas.value.slice()

  if (filtroDataInicio.value) {
    const inicioFiltroIso = filtroDataInicio.value
    lista = lista.filter(r => {
      const dataIso = toIsoFromBr(r.dataInicio)
      return dataIso >= inicioFiltroIso
    })
  }

  if (filtroDataFim.value) {
    const fimFiltroIso = filtroDataFim.value
    lista = lista.filter(r => {
      const dataIso = toIsoFromBr(r.dataInicio)
      return dataIso <= fimFiltroIso
    })
  }

  lista.sort((a, b) => {
    const aKey = `${toIsoFromBr(a.dataInicio)}T${a.horaInicio}`
    const bKey = `${toIsoFromBr(b.dataInicio)}T${b.horaInicio}`

    if (ordenacao.value === 'recentes') {
      if (aKey < bKey) return 1
      if (aKey > bKey) return -1
      return 0
    } else {
      if (aKey < bKey) return -1
      if (aKey > bKey) return 1
      return 0
    }
  })

  return lista
})
</script>

<template>
  <div class="salas-bg min-h-screen">
    <Header />

    <div class="wrapper">
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
                  {{ reserva.dataInicio }} – {{ reserva.dataFim }}
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
                  {{ reserva.dataInicio }} – {{ reserva.dataFim }}
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

    <AndamentoModal
      :open="showAndamentoModal"
      :reserva="reservaAndamentoSelecionada"
      @close="showAndamentoModal = false"
      @aprovar="payload => console.log('Aprovar reserva sala:', payload)"
      @recusar="payload => console.log('Recusar reserva sala:', payload)"
    />

    <ConcluidasModal
      :open="showConcluidasModal"
      :reserva="reservaConcluidaSelecionada"
      @close="showConcluidasModal = false"
    />
  </div>
</template>

<style scoped>
.salas-bg {
  background: linear-gradient(
    to bottom right,
    #00107b,
    #320d73,
    #746388
  );
  padding-bottom: 3rem;
}

.wrapper {
  max-width: 1100px;
  margin: 0 auto;
  padding: 2.5rem 1rem 0;
}

.tabs-row {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1.8rem;
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
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>
