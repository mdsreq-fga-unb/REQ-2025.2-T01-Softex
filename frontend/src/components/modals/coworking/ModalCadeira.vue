<script setup lang="ts">
import { ref, watch, computed } from 'vue'
import { Clock, Calendar, X } from 'lucide-vue-next'

type SeatStatus = 'disponivel' | 'ocupado' | 'reservado' 

type SeatInfo = {
  id: number
  status: SeatStatus
}

type ReservaCadeiraPayload = {
  seatId: number
  dataInicio: string
  dataFim: string
  horaInicio: string
  horaFim: string
}

const props = defineProps<{
  open: boolean
  seat: SeatInfo | null
}>()

const emit = defineEmits<{
  (e: 'close'): void
  (e: 'reserve', payload: ReservaCadeiraPayload): void
}>()

const dataInicio = ref('')
const dataFim = ref('')
const horaInicio = ref('')
const horaFim = ref('')

const labelFromStatus = (status: SeatStatus): string => {
  switch (status) {
    case 'disponivel': return 'disponível'
    case 'ocupado': return 'ocupado'
    case 'reservado': return 'reservado'
  }
}

const bloqueado = computed(() => {
  if (!props.seat) return true
  return props.seat.status === 'ocupado' || props.seat.status === 'reservado'
})

const diffDias = computed(() => {
  if (!dataInicio.value || !dataFim.value) return null
  const d1 = new Date(dataInicio.value)
  const d2 = new Date(dataFim.value)
  const diffMs = d2.getTime() - d1.getTime()
  return diffMs / (1000 * 60 * 60 * 24)
})

const dataValida = computed(() => {
  if (!dataInicio.value || !dataFim.value) return false
  const d1 = new Date(dataInicio.value)
  const d2 = new Date(dataFim.value)
  if (d2 < d1) return false
  const d = diffDias.value
  if (d === null) return false
  return d <= 2
})

const horasValidas = computed(() => {
  if (!horaInicio.value || !horaFim.value) return false
  return horaFim.value > horaInicio.value
})

const podeSalvar = computed(() => {
  if (bloqueado.value || !props.seat) return false
  return dataValida.value && horasValidas.value
})

watch(
  () => [props.open, props.seat?.id],
  () => {
    if (!props.open) return
    dataInicio.value = ''
    dataFim.value = ''
    horaInicio.value = ''
    horaFim.value = ''
  }
)

const fechar = () => {
  emit('close')
}

const salvar = () => {
  if (!podeSalvar.value || !props.seat) return

  emit('reserve', {
    seatId: props.seat.id,
    dataInicio: dataInicio.value,
    dataFim: dataFim.value,
    horaInicio: horaInicio.value,
    horaFim: horaFim.value
  })
}
</script>

<template>
  <div v-if="open" class="overlay">
    <div class="card">
      <div class="header">
        <div class="header-content">
          <h2 class="title">Reservar estação de trabalho</h2>
          <p class="subtitle">
            Para que reserve essa estação, precisaremos que declare
            o horário que deseja utilizar e a data, sendo possível
            reservar até <strong>3 dias consecutivos</strong>.
          </p>
        </div>
        <button class="close-btn" type="button" @click="fechar">
          <X class="close-icon" />
        </button>
      </div>

      <div v-if="seat && bloqueado" class="alert">
        Esta estação está <strong>{{ labelFromStatus(seat.status) }}</strong>
        e não pode ser reservada.
      </div>

      <div class="form" :class="{ disabled: bloqueado }">
        <div class="time-row">
          <div class="input-wrapper">
            <Clock class="input-icon" />
            <input
              v-model="horaInicio"
              type="time"
              class="input-time"
              :disabled="bloqueado"
            />
          </div>
          <span class="ate">até</span>
          <div class="input-wrapper">
            <input
              v-model="horaFim"
              type="time"
              class="input-time"
              :disabled="bloqueado"
            />
            <span class="asterisk">*</span>
          </div>
        </div>

        <div class="date-row">
          <div class="input-wrapper">
            <Calendar class="input-icon" />
            <input
              v-model="dataInicio"
              type="date"
              class="input-date"
              :disabled="bloqueado"
            />
          </div>
          <span class="ate">até</span>
          <div class="input-wrapper">
            <input
              v-model="dataFim"
              type="date"
              class="input-date"
              :disabled="bloqueado"
            />
            <span class="asterisk">*</span>
          </div>
        </div>

        <p v-if="!bloqueado && diffDias !== null && !dataValida" class="error">
          A reserva deve ter no máximo 3 dias consecutivos e a data final
          não pode ser anterior à data inicial.
        </p>
      </div>

      <p v-if="seat" class="info">
        Você está reservando a estação de trabalho de número
        <strong> {{ seat.id }} </strong>.
      </p>

      <button
        type="button"
        class="btn-submit"
        :disabled="!podeSalvar"
        @click="salvar"
      >
        Reservar agora
      </button>
    </div>
  </div>
</template>

<style scoped>
.overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.55);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 95;
}

.card {
  width: 100%;
  max-width: 480px;
  background: #ffffff;
  border-radius: 20px;
  padding: 1.75rem 2rem 2rem;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.3), 0 10px 10px -5px rgba(0, 0, 0, 0.2);
  font-size: 0.9rem;
  position: relative;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 1rem;
  margin-bottom: 1.25rem;
}

.header-content {
  flex: 1;
}

.title {
  font-size: 1.25rem;
  font-weight: 700;
  color: #111827;
  margin: 0 0 0.5rem 0;
}

.subtitle {
  font-size: 0.875rem;
  color: #6b7280;
  line-height: 1.5;
  margin: 0;
}

.close-btn {
  border: none;
  background: transparent;
  cursor: pointer;
  padding: 0.25rem;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #6b7280;
  transition: color 0.2s;
  flex-shrink: 0;
}

.close-btn:hover {
  color: #111827;
}

.close-icon {
  width: 20px;
  height: 20px;
}

.alert {
  background: #fee2e2;
  color: #991b1b;
  border-radius: 10px;
  padding: 0.4rem 0.6rem;
  font-size: 0.76rem;
  margin-bottom: 0.7rem;
}

.form {
  margin-bottom: 1.25rem;
}

.form.disabled {
  opacity: 0.6;
  pointer-events: none;
}

.time-row,
.date-row {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1rem;
}

.input-wrapper {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  flex: 1;
  position: relative;
}

.input-icon {
  width: 18px;
  height: 18px;
  color: #6b7280;
  flex-shrink: 0;
}

.input-time,
.input-date {
  flex: 1;
  border-radius: 10px;
  border: 1.5px solid #e5e7eb;
  padding: 0.625rem 0.75rem;
  font-size: 0.875rem;
  background: #ffffff;
  color: #111827;
  transition: border-color 0.2s, box-shadow 0.2s;
  min-width: 0;
}

.input-time:focus,
.input-date:focus {
  outline: none;
  border-color: #8b5cf6;
  box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.1);
}

.input-time:disabled,
.input-date:disabled {
  background: #f3f4f6;
  color: #9ca3af;
  cursor: not-allowed;
}

.ate {
  font-size: 0.875rem;
  color: #6b7280;
  font-weight: 500;
  flex-shrink: 0;
}

.asterisk {
  font-size: 1rem;
  color: #ef4444;
  font-weight: 600;
  margin-left: 0.25rem;
}

.error {
  font-size: 0.75rem;
  color: #b91c1c;
  margin-top: 0.2rem;
}

.info {
  font-size: 0.875rem;
  color: #6b7280;
  text-align: center;
  margin-bottom: 1.25rem;
  line-height: 1.5;
}

.btn-submit {
  width: 100%;
  border: none;
  border-radius: 12px;
  padding: 0.75rem 1.5rem;
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  color: #ffffff;
  background: linear-gradient(135deg, #ec4899, #8b5cf6);
  box-shadow: 0 10px 25px rgba(139, 92, 246, 0.4);
  transition: opacity 0.2s ease, transform 0.15s ease, box-shadow 0.2s ease;
}

.btn-submit:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  box-shadow: 0 4px 12px rgba(139, 92, 246, 0.2);
}

.btn-submit:not(:disabled):hover {
  opacity: 0.95;
  transform: translateY(-2px);
  box-shadow: 0 12px 30px rgba(139, 92, 246, 0.5);
}
</style>
