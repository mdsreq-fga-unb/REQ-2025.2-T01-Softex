<script setup lang="ts">
import { ref, watch, computed } from 'vue'
import { X } from 'lucide-vue-next'

type ReservaSala = {
  id: number
  titulo: string
  solicitante: string
  sala: string
  dataInicio: string
  dataFim: string
  horaInicio: string
  horaFim: string
}

const props = defineProps<{
  open: boolean
  reserva: ReservaSala | null
}>()

const emit = defineEmits<{
  (e: 'close'): void
  (e: 'cancelar', id: number): void
}>()

const confirmacao = ref('')

watch(
  () => props.open,
  (isOpen) => {
    if (isOpen) {
      confirmacao.value = ''
    }
  }
)

const podeCancelar = computed(() => {
  return confirmacao.value.trim().toLowerCase() === 'confirmar'
})

const cancelar = () => {
  if (!props.reserva || !podeCancelar.value) return
  emit('cancelar', props.reserva.id)
}

const fechar = () => {
  emit('close')
}
</script>

<template>
  <div v-if="open" class="overlay" @click.self="fechar">
    <div class="card">
      <div class="header">
        <h2 class="title">Cancelar Reunião</h2>
        <button class="close-btn" type="button" @click="fechar">
          <X class="close-icon" />
        </button>
      </div>

      <div class="content">
        <p class="pergunta">
          Tem certeza que deseja cancelar essa reunião?
        </p>

        <div class="reserva-info" v-if="reserva">
          <p class="info-label">Reunião:</p>
          <p class="info-value">{{ reserva.titulo }}</p>
          <p class="info-label">Sala:</p>
          <p class="info-value">{{ reserva.sala }}</p>
          <p class="info-label">Data:</p>
          <p class="info-value">{{ reserva.dataInicio }} – {{ reserva.dataFim }}</p>
          <p class="info-label">Horário:</p>
          <p class="info-value">{{ reserva.horaInicio }} → {{ reserva.horaFim }}</p>
        </div>

        <div class="confirmacao-field">
          <label class="confirmacao-label" for="confirmacao">
            Digite <strong>"confirmar"</strong> para cancelar:
          </label>
          <input
            id="confirmacao"
            v-model="confirmacao"
            type="text"
            class="confirmacao-input"
            placeholder="confirmar"
            autocomplete="off"
          />
        </div>
      </div>

      <div class="actions">
        <button
          type="button"
          class="btn btn-cancelar"
          :disabled="!podeCancelar"
          @click="cancelar"
        >
          Cancelar Reunião
        </button>
        <button
          type="button"
          class="btn btn-fechar"
          @click="fechar"
        >
          Fechar
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.55);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1200;
  padding: 1rem;
}

.card {
  background: #ffffff;
  border-radius: 20px;
  width: 100%;
  max-width: 500px;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.3), 0 10px 10px -5px rgba(0, 0, 0, 0.2);
  overflow: hidden;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem 2rem;
  background: linear-gradient(135deg, #EF4444 0%, #DC2626 100%);
  color: white;
}

.title {
  font-size: 1.25rem;
  font-weight: 700;
  margin: 0;
  color: white;
}

.close-btn {
  background: rgba(255, 255, 255, 0.1);
  border: none;
  border-radius: 8px;
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: white;
  transition: background 0.2s;
  flex-shrink: 0;
}

.close-btn:hover {
  background: rgba(255, 255, 255, 0.2);
}

.close-icon {
  width: 20px;
  height: 20px;
}

.content {
  padding: 2rem;
}

.pergunta {
  font-size: 1.1rem;
  font-weight: 600;
  color: #111827;
  margin: 0 0 1.5rem 0;
  text-align: center;
}

.reserva-info {
  background: #f9fafb;
  border-radius: 12px;
  padding: 1.25rem;
  margin-bottom: 1.5rem;
  border: 1px solid #e5e7eb;
}

.info-label {
  font-size: 0.875rem;
  font-weight: 600;
  color: #6b7280;
  margin: 0.5rem 0 0.25rem 0;
}

.info-label:first-child {
  margin-top: 0;
}

.info-value {
  font-size: 0.95rem;
  color: #111827;
  margin: 0 0 0.75rem 0;
}

.confirmacao-field {
  margin-top: 1.5rem;
}

.confirmacao-label {
  display: block;
  font-size: 0.875rem;
  font-weight: 600;
  color: #374151;
  margin-bottom: 0.5rem;
}

.confirmacao-input {
  width: 100%;
  border-radius: 10px;
  border: 1.5px solid #e5e7eb;
  padding: 0.75rem 1rem;
  font-size: 0.95rem;
  background: #ffffff;
  color: #111827;
  transition: border-color 0.2s, box-shadow 0.2s;
}

.confirmacao-input:focus {
  outline: none;
  border-color: #EF4444;
  box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.1);
}

.confirmacao-input::placeholder {
  color: #9ca3af;
}

.actions {
  display: flex;
  gap: 0.75rem;
  padding: 1.5rem 2rem;
  background: #f9fafb;
  border-top: 1px solid #e5e7eb;
}

.btn {
  flex: 1;
  border: none;
  border-radius: 12px;
  padding: 0.75rem 1.5rem;
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-cancelar {
  background: linear-gradient(135deg, #EF4444 0%, #DC2626 100%);
  color: #ffffff;
  box-shadow: 0 4px 12px rgba(239, 68, 68, 0.3);
}

.btn-cancelar:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  box-shadow: none;
}

.btn-cancelar:not(:disabled):hover {
  opacity: 0.9;
  transform: translateY(-1px);
  box-shadow: 0 6px 16px rgba(239, 68, 68, 0.4);
}

.btn-fechar {
  background: #ffffff;
  color: #374151;
  border: 1.5px solid #e5e7eb;
}

.btn-fechar:hover {
  background: #f9fafb;
  border-color: #d1d5db;
}
</style>

