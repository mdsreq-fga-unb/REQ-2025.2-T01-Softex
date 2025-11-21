<script setup lang="ts">
import { ref, computed } from 'vue'
import Header from '@/components/Layout/Header.vue'
import CadeiraModal from '@/components/modals/reservas/Cadeira.vue'
import SalaReuniaoModal from '@/components/modals/reservas/SalaReuniao.vue'

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
  <div class="reservas-bg min-h-screen">
    <Header />

    <div class="wrapper">
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
.reservas-bg {
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
