<script setup lang="ts">
import { ref, watch } from 'vue'
import {api } from '@/services/api'

type NovoUsuario = {
  nome: string
  email: string
  funcao: string
  enviarSenha: boolean
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
  funcao: '',
  enviarSenha: true    // padrão: enviar senha
})

// Sempre que abrir o modal, limpa o formulário
watch(
  () => props.open,
  (val) => {
    if (val) {
      form.value = { 
        nome: '', 
        email: '', 
        funcao: '',
        enviarSenha: true
      }
    }
  }
)

const fechar = () => {
  emit('close')
}

const salvar = async () => {
  try {
    const payload = {
      first_name: form.value.nome,
      email: form.value.email,
      username: form.value.email,
      password:form.value.enviarSenha ? 'TrocarSenha': '',
      tipo_funcao: form.value.funcao,

    }

const response = await api.post('/cadastro/', payload)
    console.log('Usuário criado:', response.data)

    emit('save', { ...form.value })
    emit('close')
  } catch (err) {
    console.error('Erro ao criar usuário:', err.response?.status, err.response?.data)
    return
  }
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

        <!-- Toggle enviar senha -->
        <div class="toggle-row">
          <span class="label">Enviar senha por e-mail</span>
          <button
            type="button"
            class="toggle"
            :class="{ on: form.enviarSenha }"
            @click="form.enviarSenha = !form.enviarSenha"
          >
            <span class="toggle-knob" />
            <span class="toggle-label">
              {{ form.enviarSenha ? 'On' : 'Off' }}
            </span>
          </button>
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

/* Toggle enviar senha */
.toggle-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 0.5rem;
  gap: 0.75rem;
}

.toggle {
  position: relative;
  border-radius: 999px;
  padding: 0.1rem 0.6rem 0.1rem 0.15rem;
  border: 1px solid #d1d5db;
  background: #f9fafb;
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  cursor: pointer;
  transition: all 0.12s ease;
  min-width: 80px;
  justify-content: flex-start;
}

.toggle-knob {
  width: 18px;
  height: 18px;
  border-radius: 999px;
  background: #9ca3af;
  transition: all 0.12s ease;
}

.toggle-label {
  font-size: 0.75rem;
  color: #6b7280;
  font-weight: 500;
}

.toggle.on {
  background: #4f46e5;
  border-color: #4f46e5;
  justify-content: flex-end;
}

.toggle.on .toggle-knob {
  background: #ffffff;
}

.toggle.on .toggle-label {
  color: #e5e7eb;
}
</style>
