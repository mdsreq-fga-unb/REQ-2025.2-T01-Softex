<script setup lang="ts">
import { ref, watch } from 'vue'

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
</script>

<template>
  <div v-if="open" class="modal-overlay">
    <div class="slack-modal">
      <h2 class="slack-title">Slack</h2>

      <div class="slack-field">
        <p class="slack-label">Mensagem para reserva de estação</p>
        <input class="slack-input" v-model="form.reservaEstacao" />
      </div>

      <div class="slack-field">
        <p class="slack-label">Alerta de dia da reserva</p>
        <input class="slack-input" v-model="form.alertaDiaReserva" />
      </div>

      <div class="slack-field">
        <p class="slack-label">Mensagem espelho da reserva da sala</p>
        <input class="slack-input" v-model="form.espelhoSala" />
      </div>

      <div class="slack-field">
        <p class="slack-label">Mensagem para sala e seu código</p>
        <input class="slack-input" v-model="form.mensagemSalaCodigo" />
      </div>

      <p class="slack-question">Gostaria de salvar as mudanças?</p>

      <div class="slack-buttons">
        <button class="slack-yes" @click="salvar">Sim</button>
        <button class="slack-no" @click="fechar">Não</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.4);
  backdrop-filter: blur(6px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 50;
}

.slack-modal {
  width: 430px;
  background: white;
  padding: 2rem 2.2rem;
  border-radius: 12px;
  text-align: center;
  box-shadow: 0 6px 20px rgba(0,0,0,0.2);
}

.slack-title {
  font-size: 1.4rem;
  font-weight: 600;
  margin-bottom: 1.5rem;
}

.slack-field {
  margin-bottom: 1.4rem;
}

.slack-label {
  font-size: 0.95rem;
  font-weight: 500;
  margin-bottom: 0.4rem;
}

.slack-input {
  width: 100%;
  height: 38px;
  background: #dcdcdc;
  border: none;
  border-radius: 6px;
  padding: 0 10px;
  font-size: 0.95rem;
}

.slack-question {
  margin-top: 1rem;
  font-size: 0.9rem;
  font-weight: 500;
}

.slack-buttons {
  display: flex;
  justify-content: center;
  gap: 1rem;
  margin-top: 1.2rem;
}

.slack-yes {
  background: #00ff9c;
  color: black;
  padding: 0.45rem 2rem;
  border-radius: 8px;
  font-weight: bold;
  border: none;
  cursor: pointer;
}

.slack-no {
  background: #ff0000;
  color: white;
  padding: 0.45rem 2rem;
  border-radius: 8px;
  font-weight: bold;
  border: none;
  cursor: pointer;
}

.slack-yes:hover,
.slack-no:hover {
  opacity: 0.85;
}
</style>
