<script setup lang="ts">
import { ref, watch } from 'vue'
import { X } from 'lucide-vue-next'

type SlackConfig = {
  reservaEstacao: string
  alertaDiaReserva: string
  espelhoSala: string
  mensagemSalaCodigo: string
}

const props = defineProps<{
  open: boolean
  initialConfig: SlackConfig
}>()

const emit = defineEmits<{
  (e: 'close'): void
  (e: 'save', payload: SlackConfig): void
}>()

const form = ref<SlackConfig>({
  reservaEstacao: '',
  alertaDiaReserva: '',
  espelhoSala: '',
  mensagemSalaCodigo: ''
})

// Quando abrir, carrega o estado vindo do pai
watch(
  () => props.open,
  (val) => {
    if (val) {
      form.value = { ...props.initialConfig }
    }
  },
  { immediate: true }
)

const fechar = () => {
  emit('close')
}

const salvar = () => {
  emit('save', { ...form.value })
  emit('close')
}

const handleOverlayClick = (e: MouseEvent) => {
  if (e.target === e.currentTarget) {
    fechar()
  }
}
</script>

<template>
  <div v-if="open" class="modal-overlay" @click="handleOverlayClick">
    <div class="slack-modal">
      <!-- Header -->
      <div class="modal-header">
        <div class="header-content">
          <div class="slack-icon-wrapper">
            <svg class="slack-icon" viewBox="0 0 24 24" fill="currentColor">
              <path d="M5.042 15.165a2.528 2.528 0 0 1-2.52 2.523A2.528 2.528 0 0 1 0 15.165a2.527 2.527 0 0 1 2.522-2.52h2.52v2.52zM6.313 15.165a2.527 2.527 0 0 1 2.521-2.52 2.527 2.527 0 0 1 2.521 2.52v6.313A2.528 2.528 0 0 1 8.834 24a2.528 2.528 0 0 1-2.521-2.522v-6.313zM8.834 5.042a2.528 2.528 0 0 1-2.521-2.52A2.528 2.528 0 0 1 8.834 0a2.528 2.528 0 0 1 2.521 2.522v2.52H8.834zM8.834 6.313a2.528 2.528 0 0 1 2.521 2.521 2.528 2.528 0 0 1-2.521 2.521H2.522A2.528 2.528 0 0 1 0 8.834a2.528 2.528 0 0 1 2.522-2.521h6.312zM18.956 5.042a2.528 2.528 0 0 1 2.522-2.52A2.528 2.528 0 0 1 24 5.042a2.528 2.528 0 0 1-2.522 2.52h-2.522V5.042zM17.688 5.042a2.528 2.528 0 0 1-2.523 2.52 2.527 2.527 0 0 1-2.52-2.52V2.522A2.527 2.527 0 0 1 15.165 0a2.528 2.528 0 0 1 2.523 2.522v2.52zM15.165 18.956a2.528 2.528 0 0 1 2.523 2.522A2.528 2.528 0 0 1 15.165 24a2.527 2.527 0 0 1-2.52-2.522v-2.522h2.52zM15.165 17.688a2.527 2.527 0 0 1-2.52-2.523 2.526 2.526 0 0 1 2.52-2.52h6.313A2.527 2.527 0 0 1 24 15.165a2.528 2.528 0 0 1-2.522 2.523h-6.313z"/>
            </svg>
          </div>
          <div>
            <h2 class="slack-title">Configurações do Slack</h2>
            <p class="slack-subtitle">Personalize as mensagens de notificação</p>
          </div>
        </div>
        <button class="close-button" @click="fechar">
          <X class="close-icon" />
        </button>
      </div>

      <!-- Content -->
      <div class="modal-content">
        <div class="slack-field">
          <label class="slack-label">
            Mensagem para reserva de estação
          </label>
          <textarea 
            class="slack-input slack-textarea" 
            v-model="form.reservaEstacao"
            placeholder="Digite a mensagem que será enviada quando uma estação for reservada..."
            rows="3"
          />
        </div>

        <div class="slack-field">
          <label class="slack-label">
            Alerta de dia da reserva
          </label>
          <input 
            class="slack-input" 
            v-model="form.alertaDiaReserva"
            placeholder="Digite a mensagem de alerta..."
          />
        </div>

        <div class="slack-field">
          <label class="slack-label">
            Mensagem espelho da reserva da sala
          </label>
          <textarea 
            class="slack-input slack-textarea" 
            v-model="form.espelhoSala"
            placeholder="Digite a mensagem espelho para reservas de sala..."
            rows="3"
          />
        </div>

        <div class="slack-field">
          <label class="slack-label">
            Mensagem para sala e seu código
          </label>
          <input 
            class="slack-input" 
            v-model="form.mensagemSalaCodigo"
            placeholder="Digite a mensagem com código da sala..."
          />
        </div>
      </div>

      <!-- Footer -->
      <div class="modal-footer">
        <button class="slack-button slack-button-secondary" @click="fechar">
          Cancelar
        </button>
        <button class="slack-button slack-button-primary" @click="salvar">
          Salvar configurações
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 1rem;
  animation: fadeIn 0.2s ease-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

.slack-modal {
  width: 100%;
  max-width: 600px;
  background: white;
  border-radius: 16px;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
  display: flex;
  flex-direction: column;
  max-height: 90vh;
  overflow: hidden;
  animation: slideUp 0.3s ease-out;
}

@keyframes slideUp {
  from {
    transform: translateY(20px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: 1.5rem 2rem;
  border-bottom: 1px solid #e5e7eb;
  background: linear-gradient(135deg, #4A154B 0%, #350D36 100%);
  color: white;
}

.header-content {
  display: flex;
  align-items: center;
  gap: 1rem;
  flex: 1;
}

.slack-icon-wrapper {
  width: 48px;
  height: 48px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.slack-icon {
  width: 28px;
  height: 28px;
  color: white;
}

.slack-title {
  font-size: 1.5rem;
  font-weight: 700;
  margin: 0;
  color: white;
}

.slack-subtitle {
  font-size: 0.875rem;
  margin: 0.25rem 0 0 0;
  color: rgba(255, 255, 255, 0.8);
  font-weight: 400;
}

.close-button {
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

.close-button:hover {
  background: rgba(255, 255, 255, 0.2);
}

.close-icon {
  width: 20px;
  height: 20px;
}

.modal-content {
  padding: 2rem;
  overflow-y: auto;
  flex: 1;
}

.slack-field {
  margin-bottom: 1.5rem;
}

.slack-field:last-of-type {
  margin-bottom: 0;
}

.slack-label {
  display: block;
  font-size: 0.875rem;
  font-weight: 600;
  color: #374151;
  margin-bottom: 0.5rem;
}

.slack-input {
  width: 100%;
  padding: 0.75rem 1rem;
  border: 1.5px solid #e5e7eb;
  border-radius: 8px;
  font-size: 0.875rem;
  color: #1f2937;
  background: #ffffff;
  transition: all 0.2s;
  font-family: inherit;
}

.slack-input:focus {
  outline: none;
  border-color: #4A154B;
  box-shadow: 0 0 0 3px rgba(74, 21, 75, 0.1);
}

.slack-input::placeholder {
  color: #9ca3af;
}

.slack-textarea {
  resize: vertical;
  min-height: 80px;
  font-family: inherit;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
  padding: 1.5rem 2rem;
  border-top: 1px solid #e5e7eb;
  background: #f9fafb;
}

.slack-button {
  padding: 0.625rem 1.5rem;
  border-radius: 8px;
  font-size: 0.875rem;
  font-weight: 600;
  border: none;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.slack-button-primary {
  background: linear-gradient(135deg, #4A154B 0%, #350D36 100%);
  color: white;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.slack-button-primary:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.slack-button-primary:active {
  transform: translateY(0);
}

.slack-button-secondary {
  background: white;
  color: #374151;
  border: 1.5px solid #e5e7eb;
}

.slack-button-secondary:hover {
  background: #f9fafb;
  border-color: #d1d5db;
}

@media (max-width: 640px) {
  .slack-modal {
    max-width: 100%;
    border-radius: 12px;
  }

  .modal-header {
    padding: 1.25rem 1.5rem;
  }

  .modal-content {
    padding: 1.5rem;
  }

  .modal-footer {
    padding: 1.25rem 1.5rem;
    flex-direction: column-reverse;
  }

  .slack-button {
    width: 100%;
  }

  .header-content {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.75rem;
  }

  .slack-icon-wrapper {
    width: 40px;
    height: 40px;
  }

  .slack-icon {
    width: 24px;
    height: 24px;
  }
}
</style>
