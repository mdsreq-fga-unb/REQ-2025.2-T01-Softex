<script setup lang="ts">
import { ref, watch, computed } from 'vue'

type Usuario = {
  id: number
  nome: string
  email: string
  funcao: string
  status?: string
}

const props = defineProps<{
  open: boolean
  usuario: Usuario | null
  funcoes: string[]
}>()

const emit = defineEmits<{
  (e: 'close'): void
  (e: 'save', payload: Usuario): void
  (e: 'delete', id: number): void
  (e: 'resend-password', id: number): void
}>()

const nome = ref('')
const email = ref('')
const funcao = ref('')

const showConfirmDelete = ref(false)

watch(
  () => props.open,
  (isOpen) => {
    if (isOpen && props.usuario) {
      nome.value = props.usuario.nome
      email.value = props.usuario.email
      funcao.value = props.usuario.funcao
      showConfirmDelete.value = false
    }
  },
  { immediate: true }
)

const formValido = computed(() =>
  nome.value.trim().length > 0 &&
  email.value.trim().length > 0 &&
  funcao.value.trim().length > 0
)

const fechar = () => {
  emit('close')
}

const salvar = () => {
  if (!props.usuario || !formValido.value) return

  emit('save', {
    ...props.usuario,
    nome: nome.value.trim(),
    email: email.value.trim(),
    funcao: funcao.value
  })
}

const pedirConfirmacaoExclusao = () => {
  showConfirmDelete.value = true
}

const cancelarExclusao = () => {
  showConfirmDelete.value = false
}

const confirmarExclusao = () => {
  if (!props.usuario) return
  emit('delete', props.usuario.id)
  showConfirmDelete.value = false
}

// NOVO: reenviar senha
const reenviarSenha = () => {
  if (!props.usuario) return
  emit('resend-password', props.usuario.id)
}
</script>

<template>
  <div v-if="open" class="overlay">
    <div class="card">
      <!-- header -->
      <div class="header">
        <h2 class="title">Editar usuário</h2>
        <button class="close-btn" type="button" @click="fechar">×</button>
      </div>

      <!-- conteúdo -->
      <div class="content" v-if="usuario">
        <p class="hint">
          Altere os dados do usuário. As mudanças serão refletidas nas permissões
          e notificações do sistema.
        </p>

        <div class="field">
          <label class="label" for="nome">Nome</label>
          <input
            id="nome"
            v-model="nome"
            type="text"
            class="input"
            placeholder="Nome completo"
          />
        </div>

        <div class="field">
          <label class="label" for="email">E-mail</label>
          <input
            id="email"
            v-model="email"
            type="email"
            class="input"
            placeholder="email@exemplo.com"
          />
        </div>

        <div class="field">
          <label class="label" for="funcao">Função</label>
          <select
            id="funcao"
            v-model="funcao"
            class="select"
          >
            <option value="" disabled>Selecione uma função</option>
            <option v-for="f in funcoes" :key="f" :value="f">
              {{ f }}
            </option>
          </select>
        </div>

        <!-- NOVO: botão roxo, pequeno, logo abaixo de função -->
        <button
          class="btn-resend"
          type="button"
          :disabled="!usuario"
          @click="reenviarSenha"
        >
          Reenviar senha para este usuário
        </button>
      </div>

      <!-- ações -->
      <div class="actions">
        <button
          class="btn btn-danger-outline"
          type="button"
          @click="pedirConfirmacaoExclusao"
          :disabled="!usuario"
        >
          Excluir usuário
        </button>

        <div class="actions-right">
          <button class="btn btn-ghost" type="button" @click="fechar">
            Cancelar
          </button>
          <button
            class="btn btn-primary"
            type="button"
            :disabled="!formValido || !usuario"
            @click="salvar"
          >
            Salvar
          </button>
        </div>
      </div>
    </div>

    <!-- mini modal confirmar exclusão -->
    <div v-if="showConfirmDelete" class="mini-overlay">
      <div class="mini-modal">
        <h3 class="mini-title">Excluir usuário</h3>
        <p class="mini-text">
          Tem certeza que deseja excluir
          <strong v-if="usuario">"{{ usuario.nome }}"</strong>?
          Esta ação não poderá ser desfeita.
        </p>
        <div class="mini-actions">
          <button class="mini-btn ghost" type="button" @click="cancelarExclusao">
            Cancelar
          </button>
          <button class="mini-btn danger" type="button" @click="confirmarExclusao">
            Excluir
          </button>
        </div>
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
  max-width: 520px;
  background: #ffffff;
  border-radius: 18px;
  box-shadow: 0 18px 40px rgba(0, 0, 0, 0.35);
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

/* header */
.header {
  padding: 0.9rem 1.5rem;
  border-bottom: 1px solid #e5e7eb;
  background: #f9fafb;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.title {
  font-size: 1.1rem;
  font-weight: 700;
}

.close-btn {
  border: none;
  background: transparent;
  font-size: 1.4rem;
  line-height: 1;
  cursor: pointer;
  padding: 0.2rem 0.4rem;
}

/* conteúdo */
.content {
  padding: 1.1rem 1.5rem 0.5rem;
}

.hint {
  font-size: 0.82rem;
  color: #6b7280;
  margin-bottom: 0.8rem;
}

.field {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  margin-bottom: 0.75rem;
}

.label {
  font-size: 0.85rem;
  font-weight: 600;
  color: #111827;
}

.input,
.select {
  border-radius: 10px;
  border: 1px solid #d1d5db;
  padding: 0.45rem 0.9rem;
  font-size: 0.9rem;
  outline: none;
}

.input:focus,
.select:focus {
  border-color: #3b82f6;
  box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.25);
}

/* botão roxo pequeno */
.btn-resend {
  margin-top: 0.2rem;
  align-self: flex-start;
  background: #7c3aed; /* roxo */
  color: #ffffff;
  border: none;
  border-radius: 999px;
  padding: 0.25rem 0.8rem;
  font-size: 0.75rem;
  font-weight: 600;
  cursor: pointer;
  transition: opacity 0.15s ease, transform 0.1s ease;
}

.btn-resend:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-resend:not(:disabled):hover {
  opacity: 0.95;
  transform: translateY(-1px);
}

/* ações */
.actions {
  padding: 0.9rem 1.5rem 1.1rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.75rem;
}

.actions-right {
  display: flex;
  gap: 0.5rem;
}

.btn {
  border-radius: 999px;
  padding: 0.4rem 1.1rem;
  font-size: 0.9rem;
  font-weight: 600;
  border: none;
  cursor: pointer;
  transition: opacity 0.15s ease, transform 0.1s ease;
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-ghost {
  background: #e5e7eb;
  color: #111827;
}

.btn-primary {
  background: #1d4ed8;
  color: #ffffff;
  box-shadow: 0 4px 12px rgba(37, 99, 235, 0.35);
}

.btn-danger-outline {
  background: #fee2e2;
  color: #b91c1c;
}

.btn-primary:not(:disabled):hover,
.btn-ghost:hover,
.btn-danger-outline:hover {
  opacity: 0.95;
  transform: translateY(-1px);
}

/* mini modal confirmação */
.mini-overlay {
  position: fixed;
  inset: 0;
  background: transparent;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 100;
}

.mini-modal {
  background: #ffffff;
  border-radius: 14px;
  padding: 1.1rem 1.3rem 1rem;
  width: 100%;
  max-width: 360px;
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.3);
}

.mini-title {
  font-size: 1rem;
  font-weight: 700;
  margin-bottom: 0.45rem;
}

.mini-text {
  font-size: 0.88rem;
  color: #374151;
}

.mini-actions {
  display: flex;
  justify-content: flex-end;
  gap: 0.5rem;
  margin-top: 0.9rem;
}

.mini-btn {
  border-radius: 999px;
  padding: 0.35rem 0.95rem;
  font-size: 0.85rem;
  font-weight: 600;
  border: none;
  cursor: pointer;
  transition: opacity 0.1s ease;
}

.mini-btn:hover {
  opacity: 0.9;
}

.mini-btn.ghost {
  background: #e5e7eb;
  color: #111827;
}

.mini-btn.danger {
  background: #dc2626;
  color: #ffffff;
}
</style>
