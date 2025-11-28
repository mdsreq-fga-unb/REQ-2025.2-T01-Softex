<!-- src/components/modals/ModalSala.vue -->
<script setup lang="ts">
import { ref, watch, computed } from 'vue'
import ConfirmarExclusao from '@/components/modals/ConfirmarExclusao.vue'

type SalaPayload = {
  nome: string
}

type SalaItem = {
  id: number
  nome: string
}

const props = defineProps<{
  open: boolean
  initialName?: string | null
  modo?: 'criar' | 'editar'
  salas?: SalaItem[]
}>()

const emit = defineEmits<{
  (e: 'close'): void
  (e: 'save', payload: SalaPayload): void
  (e: 'delete', salaId: number): void   // 👈 NOVO evento de exclusão
}>()

const nome = ref<string>('')

// estado do modal de confirmar exclusão
const showConfirmDelete = ref(false)
const salaParaExcluir = ref<SalaItem | null>(null)

watch(
  () => props.open,
  (isOpen) => {
    if (isOpen) {
      nome.value = props.initialName ?? ''
      showConfirmDelete.value = false
      salaParaExcluir.value = null
    }
  },
  { immediate: true }
)

const titulo = computed(() =>
  props.modo === 'editar' ? 'Editar sala' : 'Adicionar sala'
)

const botaoTexto = computed(() =>
  props.modo === 'editar' ? 'Salvar' : 'Adicionar'
)

const nomeEhValido = computed(() => nome.value.trim().length > 0)

const fechar = () => {
  emit('close')
}

const salvar = () => {
  if (!nomeEhValido.value) return
  emit('save', { nome: nome.value.trim() })
}

// abrir modal de confirmação
const pedirConfirmacaoExclusao = (sala: SalaItem) => {
  salaParaExcluir.value = sala
  showConfirmDelete.value = true
}

const cancelarExclusao = () => {
  showConfirmDelete.value = false
  salaParaExcluir.value = null
}

const confirmarExclusao = () => {
  if (!salaParaExcluir.value) return
  emit('delete', salaParaExcluir.value.id)
  showConfirmDelete.value = false
  salaParaExcluir.value = null
}
</script>

<template>
  <div v-if="open" class="overlay">
    <div class="card">
      <!-- HEADER COM TÍTULO + X -->
      <div class="header">
        <h2 class="title">{{ titulo }}</h2>
        <button class="close-btn" type="button" @click="fechar">×</button>
      </div>

      <div class="content">
        <p class="hint">
          Informe o nome da sala que será exibido para os usuários
          nas reservas de reunião.
        </p>

        <div class="field">
          <label class="label" for="nomeSala">Nome da sala:</label>
          <input
            id="nomeSala"
            v-model="nome"
            type="text"
            placeholder="Ex: Sala 01 - Reunião"
            class="input"
            @keyup.enter="salvar"
          />
        </div>

        <!-- LISTA DE SALAS -->
        <div class="lista-salas">
          <p class="lista-title">Salas cadastradas</p>

          <div
            v-if="salas && salas.length"
            class="lista-scroll"
          >
            <div
              v-for="sala in salas"
              :key="sala.id"
              class="sala-item"
            >
              <div class="sala-esq">
                <div class="sala-badge" />
                <span class="sala-nome">{{ sala.nome }}</span>
              </div>

              <!-- botão lixeira -->
              <button
                type="button"
                class="delete-btn"
                @click="pedirConfirmacaoExclusao(sala)"
              >
                <i class="fa-solid fa-trash"></i>
              </button>
            </div>
          </div>

          <p v-else class="lista-empty">
            Nenhuma sala cadastrada ainda.
          </p>
        </div>
      </div>

      <div class="actions">
        <button class="btn btn-ghost" type="button" @click="fechar">
          Cancelar
        </button>
        <button
          class="btn btn-primary"
          type="button"
          :disabled="!nomeEhValido"
          @click="salvar"
        >
          {{ botaoTexto }}
        </button>
      </div>
    </div>

    <!-- MODAL PADRÃO DE CONFIRMAÇÃO DE EXCLUSÃO -->
    <ConfirmarExclusao
      :open="showConfirmDelete"
      @close="cancelarExclusao"
      @confirm="confirmarExclusao"
    />
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
  z-index: 80;
}

.card {
  width: 100%;
  max-width: 460px;
  background: #ffffff;
  border-radius: 18px;
  box-shadow: 0 18px 40px rgba(0, 0, 0, 0.35);
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

/* HEADER */
.header {
  padding: 0.9rem 1.5rem;
  border-bottom: 1px solid #e5e7eb;
  background: #f9fafb;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.75rem;
}

.title {
  font-size: 1.1rem;
  font-weight: 700;
  text-align: left;
}

.close-btn {
  border: none;
  background: transparent;
  font-size: 1.4rem;
  line-height: 1;
  cursor: pointer;
  padding: 0.2rem 0.4rem;
}

/* CONTEÚDO */
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
  margin-bottom: 1rem;
}

.label {
  font-size: 0.85rem;
  font-weight: 600;
  color: #111827;
}

.input {
  border-radius: 999px;
  border: 1px solid #d1d5db;
  padding: 0.45rem 0.9rem;
  font-size: 0.9rem;
  outline: none;
}

.input:focus {
  border-color: #3b82f6;
  box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.25);
}

/* LISTA DE SALAS */
.lista-salas {
  margin-top: 0.5rem;
}

.lista-title {
  font-size: 0.85rem;
  font-weight: 600;
  color: #111827;
  margin-bottom: 0.4rem;
}

.lista-scroll {
  max-height: 180px;
  border-radius: 12px;
  background: #f3f4f6;
  padding: 0.5rem;
  overflow-y: auto;
}

.sala-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.5rem;
  background: #ffffff;
  border-radius: 10px;
  padding: 0.45rem 0.75rem;
  font-size: 0.9rem;
  margin-bottom: 0.4rem;
  box-shadow: 0 1px 3px rgba(0,0,0,0.06);
}

.sala-item:last-child {
  margin-bottom: 0;
}

.sala-esq {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.sala-badge {
  width: 12px;
  height: 12px;
  border-radius: 4px;
  background: #3b82f6;
}

.sala-nome {
  font-weight: 500;
  color: #111827;
}

.delete-btn {
  border: none;
  background: transparent;
  color: #ef4444;
  cursor: pointer;
  font-size: 0.9rem;
  padding: 0.15rem 0.3rem;
}

.delete-btn:hover {
  opacity: 0.8;
}

.lista-empty {
  font-size: 0.8rem;
  color: #9ca3af;
}

/* AÇÕES */
.actions {
  padding: 0.9rem 1.5rem 1.1rem;
  display: flex;
  justify-content: flex-end;
  gap: 0.5rem;
}

.btn {
  border-radius: 999px;
  padding: 0.4rem 1.1rem;
  font-size: 0.9rem;
  font-weight: 600;
  border: none;
  cursor: pointer;
  transition: opacity 0.15s ease, transform 0.1s ease, box-shadow 0.1s ease;
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  box-shadow: none;
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

.btn-primary:not(:disabled):hover,
.btn-ghost:hover {
  opacity: 0.95;
  transform: translateY(-1px);
}

</style>
