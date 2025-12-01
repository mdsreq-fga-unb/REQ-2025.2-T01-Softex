<script setup lang="ts">
import { ref, watch } from 'vue'

type PerfilPermissao = {
  id: number
  nome: string
  descricao?: string
  acessoBasico: boolean
  dashboards: boolean
  salasReuniao: boolean
  administracao: boolean
}

const props = defineProps<{
  open: boolean
  perfis: PerfilPermissao[]
}>()

const emit = defineEmits<{
  (e: 'close'): void
  (e: 'save', perfis: PerfilPermissao[]): void
}>()

// cópia local para edição
const perfisLocais = ref<PerfilPermissao[]>([])

// mini modal de novo perfil
const showNovoPerfil = ref(false)
const novoNome = ref('')
const novoDescricao = ref('')

const resetNovoPerfil = () => {
  novoNome.value = ''
  novoDescricao.value = ''
}

// sempre que abrir o modal principal, sincroniza a lista local
watch(
  () => props.open,
  (isOpen) => {
    if (isOpen) {
      perfisLocais.value = props.perfis.map(
        p => ({ ...p } as PerfilPermissao)
      )
      resetNovoPerfil()
      showNovoPerfil.value = false
    }
  },
  { immediate: true }
)

const toggleCampo = (
  perfilId: number | undefined,
  campo: 'acessoBasico' | 'dashboards' | 'salasReuniao' | 'administracao'
) => {
  if (perfilId == null) return

  const perfil = perfisLocais.value.find(p => p.id === perfilId)
  if (!perfil) return

  perfil[campo] = !perfil[campo]
}


const abrirNovoPerfil = () => {
  showNovoPerfil.value = true
}

const salvarNovoPerfil = () => {
  if (!novoNome.value.trim()) return

  const novoId = perfisLocais.value.length
    ? Math.max(...perfisLocais.value.map(p => p.id)) + 1
    : 1

  perfisLocais.value.push({
    id: novoId,
    nome: novoNome.value.trim(),
    descricao: novoDescricao.value.trim() || undefined,
    acessoBasico: true,
    dashboards: false,
    salasReuniao: false,
    administracao: false
  })

  resetNovoPerfil()
  showNovoPerfil.value = false
}

const salvar = () => {
  emit('save', perfisLocais.value)
  emit('close')
}

const fechar = () => {
  emit('close')
}
</script>

<template>
  <div v-if="open" class="overlay">
    <div class="card">
      <div class="header">
        <div>
          <h2 class="title">Perfis de permissão</h2>
          <p class="subtitle">
            Defina quais áreas do sistema cada perfil pode acessar.
          </p>
        </div>

        <button type="button" class="btn-fechar" @click="fechar">
          ✕
        </button>
      </div>

      <div class="content">
        <div class="content-header">
          <h3 class="section-title">Perfis existentes</h3>
          <button type="button" class="btn-novo-perfil" @click="abrirNovoPerfil">
            + Novo perfil
          </button>
        </div>

        <!-- tabela de perfis -->
        <div class="table-wrapper">
          <table class="permissoes-table">
            <thead>
              <tr>
                <th class="th nome-col">Perfil</th>
                <th class="th">Acesso básico<br /><span class="th-hint">(Coworking + Minhas Reservas)</span></th>
                <th class="th">Dashboards</th>
                <th class="th">Salas de reunião</th>
                <th class="th">Administração</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="perfil in perfisLocais" :key="perfil.id" class="tr">
                <td class="td perfil-info">
                  <div class="perfil-nome">{{ perfil.nome }}</div>
                  <div v-if="perfil.descricao" class="perfil-desc">
                    {{ perfil.descricao }}
                  </div>
                </td>

                <td class="td">
                  <button
                    type="button"
                    class="toggle"
                    :class="{ on: perfil.acessoBasico }"
                    @click="toggleCampo(perfil.id, 'acessoBasico')"
                  >
                    <span class="toggle-knob" />
                    <span class="toggle-label">
                      {{ perfil.acessoBasico ? 'On' : 'Off' }}
                    </span>
                  </button>
                </td>

                <td class="td">
                  <button
                    type="button"
                    class="toggle"
                    :class="{ on: perfil.dashboards }"
                    @click="toggleCampo(perfil.id, 'dashboards')"
                  >
                    <span class="toggle-knob" />
                    <span class="toggle-label">
                      {{ perfil.dashboards ? 'On' : 'Off' }}
                    </span>
                  </button>
                </td>

                <td class="td">
                  <button
                    type="button"
                    class="toggle"
                    :class="{ on: perfil.salasReuniao }"
                    @click="toggleCampo(perfil.id, 'salasReuniao')"
                  >
                    <span class="toggle-knob" />
                    <span class="toggle-label">
                      {{ perfil.salasReuniao ? 'On' : 'Off' }}
                    </span>
                  </button>
                </td>

                <td class="td">
                  <button
                    type="button"
                    class="toggle"
                    :class="{ on: perfil.administracao }"
                    @click="toggleCampo(perfil.id, 'administracao')"
                  >
                    <span class="toggle-knob" />
                    <span class="toggle-label">
                      {{ perfil.administracao ? 'On' : 'Off' }}
                    </span>
                  </button>
                </td>
              </tr>

              <tr v-if="perfisLocais.length === 0">
                <td class="td empty" colspan="5">
                  Nenhum perfil cadastrado ainda.
                  Clique em <strong>“Novo perfil”</strong> para criar o primeiro.
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <div class="footer">
        <button type="button" class="btn-secondary" @click="fechar">
          Cancelar
        </button>
        <button type="button" class="btn-primary" @click="salvar">
          Salvar alterações
        </button>
      </div>
    </div>

    <!-- Mini modal: novo perfil -->
    <div v-if="showNovoPerfil" class="mini-overlay">
      <div class="mini-card">
        <div class="mini-header">
          <h3 class="mini-title">Novo perfil</h3>
          <button type="button" class="mini-close" @click="showNovoPerfil = false">
            ✕
          </button>
        </div>

        <div class="mini-body">
          <label class="mini-label">
            Nome do perfil
            <input
              v-model="novoNome"
              type="text"
              class="mini-input"
              placeholder="Ex.: Colaboradores, Gestores, Estagiários..."
            />
          </label>

          <label class="mini-label">
            Descrição (opcional)
            <textarea
              v-model="novoDescricao"
              class="mini-textarea"
              rows="2"
              placeholder="Ex.: Acesso apenas ao coworking e suas próprias reservas."
            />
          </label>

          <p class="mini-hint">
            Este perfil começará com <strong>Acesso básico</strong> ligado
            e as demais permissões desligadas. Você pode ajustá-las depois na tabela.
          </p>
        </div>

        <div class="mini-footer">
          <button type="button" class="btn-secondary" @click="showNovoPerfil = false">
            Cancelar
          </button>
          <button type="button" class="btn-primary" @click="salvarNovoPerfil">
            Criar perfil
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
  background: rgba(15, 23, 42, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 90;
}

.card {
  width: 100%;
  max-width: 860px;
  background: #ffffff;
  border-radius: 20px;
  box-shadow: 0 25px 60px rgba(15, 23, 42, 0.55);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.header {
  padding: 1rem 1.5rem;
  border-bottom: 1px solid #e5e7eb;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 1rem;
}

.title {
  font-size: 1.1rem;
  font-weight: 700;
  color: #111827;
}

.subtitle {
  font-size: 0.8rem;
  color: #6b7280;
  margin-top: 0.2rem;
}

.btn-fechar {
  border: none;
  background: transparent;
  font-size: 1.3rem;
  cursor: pointer;
  color: #6b7280;
}

.content {
  padding: 1rem 1.5rem 0.75rem;
}

.content-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.75rem;
}

.section-title {
  font-size: 0.9rem;
  font-weight: 600;
  color: #111827;
}

.btn-novo-perfil {
  border-radius: 999px;
  padding: 0.35rem 0.9rem;
  border: none;
  font-size: 0.8rem;
  font-weight: 600;
  cursor: pointer;
  background: #4f46e5;
  color: white;
}

.table-wrapper {
  border-radius: 12px;
  border: 1px solid #e5e7eb;
  overflow: auto;
}

.permissoes-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.8rem;
}

.th {
  padding: 0.6rem 0.75rem;
  background: #f9fafb;
  border-bottom: 1px solid #e5e7eb;
  text-align: left;
  font-weight: 600;
  color: #4b5563;
  white-space: nowrap;
}

.th-hint {
  font-weight: 400;
  font-size: 0.68rem;
  color: #9ca3af;
}

.nome-col {
  min-width: 160px;
}

.tr:nth-child(even) {
  background: #f9fafb;
}

.td {
  padding: 0.55rem 0.75rem;
  border-bottom: 1px solid #e5e7eb;
  vertical-align: middle;
}

.td.empty {
  text-align: center;
  color: #6b7280;
}

.perfil-info {
  max-width: 260px;
}

.perfil-nome {
  font-weight: 600;
  color: #111827;
}

.perfil-desc {
  font-size: 0.72rem;
  color: #6b7280;
  margin-top: 0.1rem;
}

/* toggle */
.toggle {
  position: relative;
  border-radius: 999px;
  padding: 0.1rem 0.5rem 0.1rem 0.1rem;
  border: 1px solid #d1d5db;
  background: #f9fafb;
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  cursor: pointer;
  transition: all 0.12s ease;
  min-width: 70px;
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
  font-size: 0.7rem;
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

/* footer */
.footer {
  padding: 0.75rem 1.5rem 1rem;
  border-top: 1px solid #e5e7eb;
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
}

.btn-secondary {
  border-radius: 999px;
  padding: 0.4rem 1rem;
  font-size: 0.82rem;
  border: 1px solid #d1d5db;
  background: white;
  cursor: pointer;
}

.btn-primary {
  border-radius: 999px;
  padding: 0.4rem 1.2rem;
  font-size: 0.82rem;
  border: none;
  background: #4f46e5;
  color: white;
  cursor: pointer;
}

/* mini modal */
.mini-overlay {
  position: fixed;
  inset: 0;
  background: transparent;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 95;
}

.mini-card {
  width: 100%;
  max-width: 420px;
  background: #ffffff;
  border-radius: 16px;
  box-shadow: 0 20px 50px rgba(15, 23, 42, 0.45);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.mini-header {
  padding: 0.7rem 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #e5e7eb;
}

.mini-title {
  font-size: 0.95rem;
  font-weight: 700;
}

.mini-close {
  border: none;
  background: transparent;
  cursor: pointer;
  font-size: 1.2rem;
}

.mini-body {
  padding: 0.8rem 1rem;
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
}

.mini-label {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  font-size: 0.75rem;
  font-weight: 600;
  color: #374151;
}

.mini-input,
.mini-textarea {
  border-radius: 10px;
  border: 1px solid #d1d5db;
  padding: 0.4rem 0.6rem;
  font-size: 0.8rem;
  outline: none;
}

.mini-input:focus,
.mini-textarea:focus {
  border-color: #4f46e5;
  box-shadow: 0 0 0 2px rgba(79, 70, 229, 0.25);
}

.mini-hint {
  font-size: 0.75rem;
  color: #6b7280;
}

.mini-footer {
  padding: 0.7rem 1rem 0.9rem;
  border-top: 1px solid #e5e7eb;
  display: flex;
  justify-content: flex-end;
  gap: 0.6rem;
}
</style>
