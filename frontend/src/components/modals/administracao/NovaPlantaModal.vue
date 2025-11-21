<script setup lang="ts">
import { ref, computed } from 'vue'
import plantaImg from '@/assets/planta.png'
import ModalUploadImagem from '@/components/modals/administracao/ModalUploadImagem.vue'
import EditarPlanta from '@/components/modals/administracao/Editar_Planta.vue' 

// --------- TIPOS ---------
type Planta = {
  id: number
  nome: string
  escritorio: string
}

type NovaPlantaPayload = {
  nome: string
  escritorio: string
  arquivo?: File | null
  previewUrl?: string | null
}

type SeatPoint = {
  id: number
  x: number   // em %
  y: number   // em %
}

// --------- PROPS / EMITS ---------
const props = defineProps<{
  open: boolean
  escritorios: string[]
}>()

const emit = defineEmits<{
  (e: 'close'): void
  (e: 'save', payload: NovaPlantaPayload): void
  (e: 'edit-save', payload: { plantaId: number; nome: string; pontos: SeatPoint[] }): void
}>()

// --------- STATE PRINCIPAL ---------
const plantas = ref<Planta[]>([
  { id: 1, nome: 'Escritório 1º andar - Layout A', escritorio: 'Escritório 1º andar' },
  { id: 2, nome: 'Escritório 2º andar - Layout B', escritorio: 'Escritório 2º andar' }
])

const selectedPlantaId = ref<number>(plantas.value[0]?.id ?? 1)

const selectedPlanta = computed(() =>
  plantas.value.find(p => p.id === selectedPlantaId.value) ?? null
)

const pontos = ref<SeatPoint[]>([
  { id: 2, x: 40, y: 32 },
  { id: 3, x: 55, y: 35 },
  { id: 4, x: 0, y: 55 }
])

// --------- MODAIS INTERNOS ---------
const showUploadModal = ref(false)
const showEditarPlanta = ref(false)
const showConfirmExcluir = ref(false)

// --------- CAMPOS DA NOVA PLANTA / UPLOAD ---------
const novoNome = ref('')
const novoEscritorio = ref('')
const arquivo = ref<File | null>(null)
const previewUrl = ref<string | null>(null)

const handleArquivoChange = (event: Event) => {
  const target = event.target as HTMLInputElement
  const file = target.files?.[0]
  if (!file) {
    arquivo.value = null
    previewUrl.value = null
    return
  }
  arquivo.value = file
  previewUrl.value = URL.createObjectURL(file)
}

const abrirNovaPlanta = () => {
  novoNome.value = ''
  novoEscritorio.value = props.escritorios[0] ?? ''
  arquivo.value = null
  previewUrl.value = null
}

const salvarPlanta = () => {
  const nome = novoNome.value || `Planta ${plantas.value.length + 1}`
  const escritorio =
    novoEscritorio.value || props.escritorios[0] || 'Sem escritório'

  const payload: NovaPlantaPayload = {
    nome,
    escritorio,
    arquivo: arquivo.value,
    previewUrl: previewUrl.value
  }

  const novoId = plantas.value.length
    ? Math.max(...plantas.value.map(p => p.id)) + 1
    : 1

  plantas.value.push({
    id: novoId,
    nome,
    escritorio
  })

  selectedPlantaId.value = novoId
  emit('save', payload)
}

// --------- EXCLUIR PLANTA ---------
const confirmarExcluir = () => {
  if (!selectedPlanta.value) return
  const id = selectedPlanta.value.id
  plantas.value = plantas.value.filter(p => p.id !== id)
  selectedPlantaId.value = plantas.value[0]?.id ?? id
  console.log('Excluir planta ID:', id)
  showConfirmExcluir.value = false
}

// --------- FECHAR MODAL PRINCIPAL ---------
const fechar = () => {
  emit('close')
}

// --------- EDITAR PLANTA (ABRIR MODAL EDITOR) ---------
const abrirEditarPlanta = () => {
  if (!selectedPlanta.value) return
  showEditarPlanta.value = true
}

// recebe nome + pontos do Editar_Planta
const handleSalvarEdicao = (payload: { nome: string; pontos: SeatPoint[] }) => {
  if (!selectedPlanta.value) return

  selectedPlanta.value.nome = payload.nome
  pontos.value = payload.pontos
  showEditarPlanta.value = false

  emit('edit-save', {
    plantaId: selectedPlanta.value.id,
    nome: payload.nome,
    pontos: payload.pontos
  })
}

// --------- UPLOAD MODAL (CONFIRM) ---------
const handleUploadConfirm = (data: { file: File | null; previewUrl: string | null; nome: string }) => {
  arquivo.value = data.file
  previewUrl.value = data.previewUrl
  novoNome.value = data.nome
  showUploadModal.value = false
}
</script>

<template>
  <!-- Overlay do modal -->
  <div v-if="open" class="planta-overlay">
    <div class="card">
      <div class="modal-header">
        <h1 class="title">Gerenciar plantas</h1>
        <button class="close-btn" @click="fechar">×</button>
      </div>

      <p class="text">
        Nesta tela, você poderá visualizar as plantas cadastradas do seu escritório.
      </p>
      <p class="text">
        Todas as plantas adicionadas serão disponibilizadas automaticamente para os usuários
        e a numeração dos lugares será gerada de forma automática.
      </p>

      <p class="text text-small">
        <strong>Recomendação:</strong>
        para melhor experiência e evitar erros de carregamento, recomenda-se realizar este
        procedimento em um computador (desktop).
      </p>

      <p class="text text-small">
        <strong>Obs.:</strong> a imagem deve ter tamanho mínimo de
        <span class="tag-dim">1400 × 1400 px</span>.
      </p>

      <!-- Ações -->
      <div class="actions-row">
        <button
          class="btn editar"
          @click="abrirEditarPlanta"
          :disabled="!selectedPlanta"
        >
          Editar planta
        </button>

        <button
          class="btn excluir"
          @click="showConfirmExcluir = true"
          :disabled="!selectedPlanta"
        >
          Excluir planta
        </button>

        <button class="btn salvar" @click="showUploadModal = true">
          Escolher imagem da planta
        </button>

        <div class="select-wrapper">
          <select v-model.number="selectedPlantaId" class="select">
            <option
              v-for="planta in plantas"
              :key="planta.id"
              :value="planta.id"
            >
              {{ planta.nome }}
            </option>
          </select>
        </div>
      </div>

      <!-- Preview da planta -->
      <div class="planta-container" v-if="selectedPlanta">
        <img
          :src="previewUrl || plantaImg"
          alt="Planta do escritório"
          class="planta-img"
        />

        <div
          v-for="p in pontos"
          :key="p.id"
          class="seat-dot"
          :style="{ left: p.x + '%', top: p.y + '%' }"
        />
      </div>

      <!-- Mini modal confirmar exclusão -->
      <div v-if="showConfirmExcluir" class="mini-overlay">
        <div class="mini-modal">
          <h3 class="mini-title">Excluir planta</h3>
          <p class="mini-text">
            Tem certeza que deseja excluir a planta selecionada?
            Esta ação não poderá ser desfeita.
          </p>
          <div class="mini-actions">
            <button class="mini-btn ghost" @click="showConfirmExcluir = false">
              Cancelar
            </button>
            <button class="mini-btn danger" @click="confirmarExcluir">
              Excluir
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- Modal de upload de imagem -->
  <ModalUploadImagem
    :open="showUploadModal"
    :initial-preview-url="previewUrl"
    :initial-nome="novoNome"
    @close="showUploadModal = false"
    @confirm="handleUploadConfirm"
  />

  <!-- Modal de edição de planta (pontos verdes) -->
  <EditarPlanta
    :open="showEditarPlanta"
    :nome-inicial="selectedPlanta?.nome || ''"
    :planta-url="previewUrl || plantaImg"
    :pontos-iniciais="pontos"
    @close="showEditarPlanta = false"
    @save="handleSalvarEdicao"
  />
</template>

<style scoped>
.planta-overlay {
  position: fixed;
  inset: 0;
  background: rgba(15, 23, 42, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 50;
}

.card {
  background: #f9fafb;
  border-radius: 18px;
  padding: 1.75rem 2rem 2.25rem;
  box-shadow: 0 18px 40px rgba(0, 0, 0, 0.35);
  max-width: 960px;
  width: 100%;
  max-height: 90vh;
  overflow: auto;
}

.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  margin-bottom: 0.75rem;
}

.close-btn {
  border: none;
  background: transparent;
  font-size: 1.4rem;
  line-height: 1;
  cursor: pointer;
  padding: 0.2rem 0.4rem;
}

.title {
  text-align: left;
  font-size: 1.4rem;
  font-weight: 700;
}

.text {
  font-size: 0.92rem;
  color: #111827;
  line-height: 1.4;
}
.text + .text {
  margin-top: 0.3rem;
}
.text-small {
  font-size: 0.85rem;
  margin-top: 0.5rem;
}
.tag-dim {
  background: #fee2e2;
  color: #991b1b;
  padding: 0.05rem 0.45rem;
  border-radius: 999px;
  font-size: 0.8rem;
}

.actions-row {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin: 1.4rem 0 1.3rem;
  align-items: center;
  justify-content: center;
}

.btn {
  border: none;
  border-radius: 999px;
  padding: 0.45rem 1.2rem;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.08s ease, box-shadow 0.12s ease, opacity 0.12s ease;
  color: #ffffff;
}
.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  box-shadow: none;
}
.btn:not(:disabled):hover {
  transform: translateY(-1px);
  box-shadow: 0 8px 18px rgba(15, 23, 42, 0.2);
}

.editar {
  background: #0ea5e9;
}
.excluir {
  background: #ef4444;
}
.adicionar {
  background: #22c55e;
}
.salvar {
  background: #4f46e5;
}

.select-wrapper {
  min-width: 200px;
}
.select {
  width: 100%;
  border: 1px solid #d1d5db;
  padding: 0.45rem 0.9rem;
  font-size: 0.9rem;
}

.planta-container {
  margin-top: 0.5rem;
  border-radius: 18px;
  overflow: hidden;
  position: relative;
  background: #111827;
  max-width: 800px;
  width: 100%;
  aspect-ratio: 1 / 1;
  margin-left: auto;
  margin-right: auto;
}

.planta-img {
  width: 100%;
  height: 100%;
  display: block;
  object-fit: contain;   
}

.seat-dot {
  position: absolute;
  width: 14px;
  height: 14px;
  border-radius: 999px;
  background: #22c55e;
  border: 2px solid #ffffff;
  box-shadow: 0 0 0 2px rgba(22, 163, 74, 0.4);
  transform: translate(-50%, -50%);
}

.mini-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.45);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 60;
}
.mini-modal {
  background: #ffffff;
  border-radius: 14px;
  padding: 1.25rem 1.5rem 1.1rem;
  width: 100%;
  max-width: 360px;
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.3);
}
.mini-title {
  font-size: 1rem;
  font-weight: 700;
  margin-bottom: 0.4rem;
}
.mini-text {
  font-size: 0.9rem;
  color: #374151;
}
.mini-actions {
  display: flex;
  justify-content: flex-end;
  gap: 0.5rem;
  margin-top: 1rem;
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
.mini-btn.primary {
  background: #0ea5e9;
  color: #ffffff;
}
.mini-btn.danger {
  background: #dc2626;
  color: #ffffff;
}
</style>
