<script setup lang="ts">
import { ref, watch } from 'vue'

type NovoUsuario = {
  nome: string
  email: string
  funcao: string
}

const props = defineProps<{
  open: boolean
  funcoes: string[]
}>()

const emit = defineEmits<{
  (e: 'close'): void
  (e: 'save', payload: NovoUsuario): void
}>()

// Estado interno do formulário
const form = ref<NovoUsuario>({
  nome: '',
  email: '',
  funcao: ''
})

// Sempre que abrir o modal, limpa o formulário
watch(
  () => props.open,
  (val) => {
    if (val) {
      form.value = { nome: '', email: '', funcao: '' }
    }
  }
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
    <div class="modal-body">
      <h2 class="modal-title">Novo usuário</h2>

      <form class="space-y-4" @submit.prevent="salvar">
        <div>
          <label class="label">Nome</label>
          <input class="input" type="text" v-model="form.nome" />
        </div>

        <div>
          <label class="label">Email</label>
          <input class="input" type="email" v-model="form.email" />
        </div>

        <div>
          <label class="label">Função</label>
          <select class="input" v-model="form.funcao">
            <option disabled value="">Selecione uma função</option>
            <option v-for="f in funcoes" :key="f" :value="f">{{ f }}</option>
          </select>
        </div>
      </form>

      <div class="modal-footer">
        <button class="btn-cancelar" type="button" @click="fechar">Cancelar</button>
        <button class="btn-salvar" type="button" @click="salvar">Salvar</button>
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

.modal-body {
  background: white;
  padding: 1.5rem;
  border-radius: 12px;
  width: 100%;
  max-width: 420px;
  box-shadow: 0 6px 20px rgba(0,0,0,0.15);
}

.modal-title {
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: 1rem;
}

.label {
  font-size: 0.875rem;
  font-weight: 500;
}

.input {
  width: 100%;
  padding: 0.5rem 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  outline: none;
}

.input:focus {
  border-color: #3b82f6;
  box-shadow: 0 0 0 2px rgba(59,130,246,0.4);
}

.modal-footer {
  margin-top: 1.5rem;
  display: flex;
  justify-content: flex-end;
  gap: 0.5rem;
}

.btn-cancelar {
  background: #e5e7eb;
  padding: 0.5rem 1rem;
  border-radius: 8px;
}

.btn-cancelar:hover {
  background: #d1d5db;
}

.btn-salvar {
  background: #2563eb;
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 8px;
}

.btn-salvar:hover {
  background: #1e40af;
}
</style>
