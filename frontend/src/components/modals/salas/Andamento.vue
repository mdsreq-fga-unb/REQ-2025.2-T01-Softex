<!-- src/components/modals/salas/Andamento.vue -->
<script setup lang="ts">
import { ref, watch, computed } from 'vue'

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
  motivoReuniao?: string   // 👈 motivo que o solicitante escreveu
}

const props = defineProps<{
  open: boolean
  reserva: ReservaSala | null
}>()

const emit = defineEmits<{
  (e: 'close'): void
  (e: 'aprovar', payload: { id: number; salaEscolhida: string }): void
  (e: 'recusar', id: number): void
}>()

const salasDisponiveis = ref<string[]>([
  'Sala Alfa',
  'Sala Beta',
  'Sala Gama',
  'Sala Ômega'
])

const salaSelecionada = ref<string>('')

watch(
  () => props.open,
  (isOpen) => {
    if (isOpen && props.reserva) {
      salaSelecionada.value =
        props.reserva.sala || salasDisponiveis.value[0] || ''
    }
  },
  { immediate: true }
)

const podeAprovar = computed(
  () => !!props.reserva && !!salaSelecionada.value
)

const tipoReuniaoLabel = computed(() => {
  if (!props.reserva) return ''
  return props.reserva.tipoReuniao === 'interna'
    ? 'Reunião interna'
    : 'Reunião externa'
})

/**
 * Mock simples para indicar se a sala está ocupada
 * nesse mesmo dia/horário da reserva atual.
 * Depois você pode substituir por dados reais do backend.
 */
const salaOcupadaNaReserva = (salaNome: string): boolean => {
  if (!props.reserva) return false

  const conflitosMock = [
    {
      sala: 'Sala Alfa',
      dataInicio: '10/03/2026',
      dataFim: '10/03/2026',
      horaInicio: '09:00',
      horaFim: '10:00'
    }
  ]

  return conflitosMock.some((c) =>
    c.sala === salaNome &&
    c.dataInicio === props.reserva!.dataInicio &&
    c.dataFim === props.reserva!.dataFim &&
    c.horaInicio === props.reserva!.horaInicio &&
    c.horaFim === props.reserva!.horaFim
  )
}

const aprovar = () => {
  if (!props.reserva || !salaSelecionada.value) return
  emit('aprovar', {
    id: props.reserva.id,
    salaEscolhida: salaSelecionada.value
  })
}

const recusar = () => {
  if (!props.reserva) return
  emit('recusar', props.reserva.id)
}

const fechar = () => emit('close')
</script>

<template>
  <div v-if="open && reserva" class="overlay">
    <div class="card">
      <div class="header">
        <h2 class="title">Solicitação de sala de reunião</h2>
        <button class="close-btn" type="button" @click="fechar">×</button>
      </div>

      <div class="content">
        <p class="descricao">
          Revise os detalhes da solicitação antes de aprovar ou recusar o uso da sala.
        </p>

        <div class="linha-info">
          <span class="label">Solicitante:</span>
          <span class="valor">{{ reserva.solicitante }}</span>
        </div>

        <div class="linha-info">
          <span class="label">Sala solicitada:</span>
          <span class="valor">{{ reserva.sala }}</span>
        </div>

        <div class="linha-info">
          <span class="label">Período:</span>
          <span class="valor">
            {{ reserva.dataInicio }} → {{ reserva.dataFim }}
          </span>
        </div>

        <div class="linha-info">
          <span class="label">Horário:</span>
          <span class="valor">
            {{ reserva.horaInicio }} → {{ reserva.horaFim }}
          </span>
        </div>

        <div class="linha-info">
          <span class="label">Tipo de reunião:</span>
          <span class="valor">{{ tipoReuniaoLabel }}</span>
        </div>

        <div class="linha-info">
          <span class="label">Participantes:</span>
          <span class="valor">{{ reserva.participantes }} pessoas</span>
        </div>

        <!-- Motivo da reunião (somente leitura) -->
        <div v-if="reserva.motivoReuniao" class="motivo-box">
          <span class="motivo-label">Motivo da reunião:</span>
          <p class="motivo-text">
            {{ reserva.motivoReuniao }}
          </p>
        </div>

        <div class="divider" />

        <div class="field">
          <label class="label" for="sala-aprovada">
            Sala aprovada para a reserva:
          </label>
          <select
            id="sala-aprovada"
            v-model="salaSelecionada"
            class="select"
          >
            <option
              v-for="sala in salasDisponiveis"
              :key="sala"
              :value="sala"
            >
              {{ sala }}
              —
              {{ salaOcupadaNaReserva(sala) ? 'Ocupada' : 'Disponível' }}
            </option>
          </select>
          <p class="hint">
            Você pode manter a sala solicitada ou alterar para outra sala disponível.
          </p>
        </div>
      </div>

      <div class="actions">
        <button
          class="btn btn-ghost"
          type="button"
          @click="recusar"
        >
          Recusar
        </button>
        <button
          class="btn btn-primary"
          type="button"
          :disabled="!podeAprovar"
          @click="aprovar"
        >
          Aprovar reserva
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.45);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 90;
}

.card {
  width: 100%;
  max-width: 480px;
  background: #ffffff;
  border-radius: 18px;
  box-shadow: 0 18px 40px rgba(0, 0, 0, 0.35);
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.8rem 1.4rem;
  border-bottom: 1px solid #e5e7eb;
}

.title {
  font-size: 1rem;
  font-weight: 700;
}

.close-btn {
  border: none;
  background: transparent;
  font-size: 1.4rem;
  line-height: 1;
  cursor: pointer;
}

.content {
  padding: 1.1rem 1.4rem 0.5rem;
}

.descricao {
  font-size: 0.8rem;
  color: #4b5563;
  margin-bottom: 0.9rem;
}

.linha-info {
  display: flex;
  justify-content: space-between;
  gap: 0.75rem;
  font-size: 0.85rem;
  margin-bottom: 0.4rem;
}

.label {
  font-weight: 600;
  color: #111827;
}

.valor {
  color: #111827;
}

.motivo-box {
  margin-top: 0.7rem;
  padding: 0.6rem 0.8rem;
  border-radius: 0.75rem;
  background: #f9fafb;
  border: 1px dashed #e5e7eb;
}

.motivo-label {
  font-size: 0.8rem;
  font-weight: 600;
  color: #111827;
}

.motivo-text {
  margin-top: 0.25rem;
  font-size: 0.8rem;
  color: #4b5563;
  white-space: pre-line;
}

.divider {
  margin: 0.9rem 0 0.7rem;
  border-top: 1px solid #e5e7eb;
}

.field {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  font-size: 0.85rem;
  margin-top: 0.5rem;
}

.select {
  border-radius: 999px;
  border: 1px solid #d1d5db;
  padding: 0.45rem 0.9rem;
  font-size: 0.9rem;
  outline: none;
  background: #ffffff;
}

.select:focus {
  border-color: #3b82f6;
  box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.25);
}

.hint {
  font-size: 0.78rem;
  color: #6b7280;
}

/* ações */
.actions {
  padding: 0.8rem 1.4rem 1rem;
  display: flex;
  justify-content: flex-end;
  gap: 0.5rem;
}

.btn {
  border-radius: 999px;
  padding: 0.4rem 1.2rem;
  font-size: 0.85rem;
  font-weight: 600;
  border: none;
  cursor: pointer;
  transition: opacity 0.15s ease, transform 0.1s ease, box-shadow 0.1s ease;
}

.btn-ghost {
  background: #e5e7eb;
  color: #111827;
}

.btn-primary {
  background: #16a34a;
  color: #ffffff;
  box-shadow: 0 4px 12px rgba(22, 163, 74, 0.35);
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  box-shadow: none;
}

.btn-primary:not(:disabled):hover,
.btn-ghost:hover {
  opacity: 0.95;
  transform: translateY(-1px);
}
</style>
