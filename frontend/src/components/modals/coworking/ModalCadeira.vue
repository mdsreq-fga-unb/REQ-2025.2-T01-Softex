<script setup lang="ts">
import { ref, watch, computed } from 'vue'

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
        <div>
          <h2 class="title">Reservar estação de trabalho</h2>
          <p class="subtitle">
            Para que reserve essa estação, precisaremos que declare
            o horário que deseja utilizar e a data, sendo possível
            reservar até <strong>3 dias consecutivos</strong>.
          </p>
        </div>
        <button class="close-btn" type="button" @click="fechar">×</button>
      </div>

      <div v-if="seat && bloqueado" class="alert">
        Esta estação está <strong>{{ labelFromStatus(seat.status) }}</strong>
        e não pode ser reservada.
      </div>

      <div class="form" :class="{ disabled: bloqueado }">
        <div class="row">
          <span class="icon"><i class="fa-solid fa-clock"></i></span>
          <input
            v-model="horaInicio"
            type="time"
            class="input-time"
            :disabled="bloqueado"
          />
          <span class="ate">até</span>
          <input
            v-model="horaFim"
            type="time"
            class="input-time"
            :disabled="bloqueado"
          />
          <span class="asterisk">*</span>
        </div>

        <div class="row">
          <span class="icon"><i class="fa-solid fa-calendar"></i></span>
          <input
            v-model="dataInicio"
            type="date"
            class="input-date"
            :disabled="bloqueado"
          />
          <span class="ate">até</span>
          <input
            v-model="dataFim"
            type="date"
            class="input-date"
            :disabled="bloqueado"
          />
          <span class="asterisk">*</span>
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
  max-width: 360px;
  background: #f9fafb;
  border-radius: 22px;
  padding: 1.2rem 1.4rem 1.4rem;
  box-shadow: 0 18px 40px rgba(0, 0, 0, 0.45);
  font-size: 0.9rem;
}

.header {
  display: flex;
  justify-content: space-between;
  gap: 0.75rem;
  margin-bottom: 0.6rem;
}

.title {
  font-size: 0.95rem;
  font-weight: 700;
}

.subtitle {
  font-size: 0.75rem;
  color: #4b5563;
  margin-top: 0.15rem;
}

.close-btn {
  border: none;
  background: transparent;
  font-size: 1.4rem;
  line-height: 1;
  cursor: pointer;
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
  margin-bottom: 0.8rem;
}

.form.disabled {
  opacity: 0.6;
}

.row {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  margin-bottom: 0.4rem;
}

.icon {
  font-size: 0.9rem;
}

.input-time,
.input-date {
  border-radius: 8px;
  border: 1px solid #d1d5db;
  padding: 0.3rem 0.5rem;
  font-size: 0.8rem;
}

.ate {
  font-size: 0.8rem;
  color: #4b5563;
}

.asterisk {
  font-size: 0.85rem;
  color: #111827;
}

.error {
  font-size: 0.75rem;
  color: #b91c1c;
  margin-top: 0.2rem;
}

/* info final */
.info {
  font-size: 0.78rem;
  color: #4b5563;
  text-align: center;
  margin-bottom: 0.9rem;
}

.btn-submit {
  width: 100%;
  border: none;
  border-radius: 999px;
  padding: 0.55rem 1rem;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  color: #ffffff;
  background: linear-gradient(135deg, #ec4899, #8b5cf6);
  box-shadow: 0 8px 20px rgba(168, 85, 247, 0.6);
  transition: opacity 0.12s ease, transform 0.1s ease, box-shadow 0.12s ease;
}

.btn-submit:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  box-shadow: none;
}

.btn-submit:not(:disabled):hover {
  opacity: 0.95;
  transform: translateY(-1px);
}
</style>
