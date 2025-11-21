<script setup lang="ts">
import { ref, computed } from 'vue'

type ReservaSala = {
  id: number
  sala: string
  solicitante: string
  dataInicio: string   
  dataFim: string     
  horaInicio: string  
  horaFim: string      
}

const props = defineProps<{
  reservas: ReservaSala[]
}>()

const getTodayIso = () => {
  const now = new Date()
  const yyyy = String(now.getFullYear())
  const mm = String(now.getMonth() + 1).padStart(2, '0')
  const dd = String(now.getDate()).padStart(2, '0')
  return `${yyyy}-${mm}-${dd}`
}

const selectedDate = ref<string>(getTodayIso())

type TimeSlot = {
  start: string   
  end: string    
}

const timeSlots = computed<TimeSlot[]>(() => {
  const slots: TimeSlot[] = []
  let hour = 8
  let minute = 0

  while (hour < 18) {
    const startH = String(hour).padStart(2, '0')
    const startM = String(minute).padStart(2, '0')
    const start = `${startH}:${startM}`

    let h = hour
    let m = minute + 30
    if (m >= 60) {
      m -= 60
      h += 1
    }
    const endH = String(h).padStart(2, '0')
    const endM = String(m).padStart(2, '0')
    const end = `${endH}:${endM}`

    slots.push({ start, end })

    minute += 30
    if (minute >= 60) {
      minute = 0
      hour += 1
    }
  }
  return slots
})

const salas = computed(() => {
  const set = new Set<string>()
  props.reservas.forEach((r) => set.add(r.sala))
  return Array.from(set).sort()
})

const toIsoFromBr = (dateBr: string): string => {
  const [dia, mes, ano] = dateBr.split('/')
  return `${ano}-${mes.padStart(2, '0')}-${dia.padStart(2, '0')}`
}

const reservasDoDia = computed(() =>
  props.reservas.filter((r) => {
    const inicioIso = toIsoFromBr(r.dataInicio)
    const fimIso = toIsoFromBr(r.dataFim)
    return selectedDate.value >= inicioIso && selectedDate.value <= fimIso
  })
)


const getReservaForCell = (salaNome: string, slot: TimeSlot) => {
  return reservasDoDia.value.find((r) => {
    if (r.sala !== salaNome) return false
    return slot.start >= r.horaInicio && slot.start < r.horaFim
  })
}
</script>

<template>
  <div class="sala-grid-wrapper">
    <div class="grid-header">
      <div class="header-left">
        <h3 class="grid-title">Agenda das salas</h3>
        <p class="grid-subtitle">
          Veja os horários ocupados e livres das salas de reunião para o dia selecionado.
        </p>
      </div>

      <div class="header-right">
        <label class="date-label">
          Dia
          <input
            v-model="selectedDate"
            type="date"
            class="date-input"
          />
        </label>
      </div>
    </div>

    <div class="grid-container">
      <div class="grid-row grid-header-row">
        <div class="grid-cell time-col-header">Horário</div>
        <div
          v-for="sala in salas"
          :key="sala"
          class="grid-cell sala-col-header"
        >
          {{ sala }}
        </div>
      </div>

      <div
        v-for="slot in timeSlots"
        :key="slot.start"
        class="grid-row"
      >
        <div class="grid-cell time-col">
          {{ slot.start }} - {{ slot.end }}
        </div>

        <div
          v-for="sala in salas"
          :key="sala + '-' + slot.start"
          class="grid-cell sala-cell"
          :class="{ ocupado: !!getReservaForCell(sala, slot) }"
        >
          <template v-if="getReservaForCell(sala, slot)">
            <span class="ocupado-nome">
              {{ getReservaForCell(sala, slot)!.solicitante }}
            </span>
          </template>
          <template v-else>
            <span class="livre-label">Livre</span>
          </template>
        </div>
      </div>
    </div>

    <p class="legend">
      <span class="legend-box filled" /> Ocupado ·
      <span class="legend-box" /> Livre
    </p>
  </div>
</template>

<style scoped>
.sala-grid-wrapper {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.grid-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  gap: 1rem;
  margin-bottom: 0.5rem;
}

.grid-title {
  font-size: 0.98rem;
  font-weight: 700;
}

.grid-subtitle {
  font-size: 0.8rem;
  color: #6b7280;
  margin-top: 0.15rem;
}

.header-right {
  display: flex;
  align-items: center;
}

.date-label {
  display: flex;
  flex-direction: column;
  font-size: 0.75rem;
  font-weight: 600;
  color: #374151;
  gap: 0.25rem;
}

.date-input {
  border-radius: 999px;
  border: 1px solid #d1d5db;
  padding: 0.35rem 0.9rem;
  font-size: 0.85rem;
  outline: none;
}

.date-input:focus {
  border-color: #3b82f6;
  box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.25);
}

.grid-container {
  width: 100%;
  border-radius: 16px;
  border: 1px solid #e5e7eb;
  overflow: auto;
  background: #f9fafb;
}

.grid-row {
  display: grid;
  grid-template-columns: 130px repeat(auto-fit, minmax(120px, 1fr));
}

.grid-header-row {
  background: #eef2ff;
  border-bottom: 1px solid #e5e7eb;
}

.grid-cell {
  padding: 0.4rem 0.6rem;
  font-size: 0.78rem;
  border-bottom: 1px solid #e5e7eb;
  border-right: 1px solid #e5e7eb;
  min-height: 32px;
  display: flex;
  align-items: center;
}

.grid-cell:last-child {
  border-right: none;
}

.time-col-header {
  font-weight: 600;
  background: #e0e7ff;
}

.sala-col-header {
  font-weight: 600;
  text-align: center;
}

.time-col {
  font-weight: 500;
  background: #f3f4f6;
}

.sala-cell {
  justify-content: center;
  text-align: center;
}

.sala-cell.ocupado {
  background: #dbeafe;
  color: #1e3a8a;
  font-weight: 600;
}

.ocupado-nome {
  font-size: 0.78rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.livre-label {
  font-size: 0.72rem;
  color: #9ca3af;
}

.legend {
  font-size: 0.75rem;
  color: #6b7280;
  display: flex;
  align-items: center;
  gap: 0.4rem;
}

.legend-box {
  width: 12px;
  height: 12px;
  border-radius: 3px;
  border: 1px solid #d1d5db;
  display: inline-block;
}

.legend-box.filled {
  background: #dbeafe;
  border-color: #93c5fd;
}

@media (max-width: 700px) {
  .grid-row {
    grid-template-columns: 110px repeat(auto-fit, minmax(110px, 1fr));
  }

  .grid-title {
    font-size: 0.9rem;
  }

  .grid-subtitle {
    font-size: 0.76rem;
  }
}
</style>
