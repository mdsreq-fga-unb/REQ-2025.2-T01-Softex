<script setup lang="ts">
import { ref, watch, computed } from 'vue'
import { X } from 'lucide-vue-next'

const props = defineProps<{
  open: boolean
}>()

const emit = defineEmits<{
  (e: 'close'): void
  (e: 'confirm'): void
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

const podeExcluir = computed(() => {
  return confirmacao.value.trim().toLowerCase() === 'confirmar'
})

const excluir = () => {
  if (!podeExcluir.value) return
  emit('confirm')
}

const fechar = () => {
  emit('close')
}
</script>

<template>
  <div v-if="open" class="overlay" @click.self="fechar">
    <div class="card">
      <div class="header">
        <h2 class="title">Confirmar Exclusão</h2>
        <button class="close-btn" type="button" @click="fechar">
          <X class="close-icon" />
        </button>
      </div>

      <div class="content">
        <p class="mensagem">
          Para excluir definitivamente, digite <strong>"confirmar"</strong> no campo abaixo.
        </p>

        <div class="confirmacao-field">
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
          class="btn btn-fechar"
          @click="fechar"
        >
          Cancelar
        </button>
        <button
          type="button"
          class="btn btn-excluir"
          :disabled="!podeExcluir"
          @click="excluir"
        >
          Excluir
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
  max-width: 480px;
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

.mensagem {
  font-size: 0.95rem;
  color: #374151;
  line-height: 1.6;
  margin: 0 0 1.5rem 0;
  text-align: center;
}

.confirmacao-field {
  margin-top: 1rem;
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

.btn-fechar {
  background: #ffffff;
  color: #374151;
  border: 1.5px solid #e5e7eb;
}

.btn-fechar:hover {
  background: #f9fafb;
  border-color: #d1d5db;
}

.btn-excluir {
  background: linear-gradient(135deg, #EF4444 0%, #DC2626 100%);
  color: #ffffff;
  box-shadow: 0 4px 12px rgba(239, 68, 68, 0.3);
}

.btn-excluir:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  box-shadow: 0 2px 8px rgba(239, 68, 68, 0.2);
}

.btn-excluir:not(:disabled):hover {
  opacity: 0.95;
  transform: translateY(-1px);
  box-shadow: 0 6px 16px rgba(239, 68, 68, 0.4);
}
</style>

