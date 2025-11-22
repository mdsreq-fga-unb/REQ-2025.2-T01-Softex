<script setup lang="ts">
import { ref, computed } from 'vue'
import { X, MapPin } from 'lucide-vue-next'
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

const handleOverlayClick = (e: MouseEvent) => {
  if (e.target === e.currentTarget) {
    fechar()
  }
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
  <div v-if="open" class="planta-overlay" @click="handleOverlayClick">
    <div class="card" @click.stop>
      <div class="modal-header">
        <div class="header-content">
          <div class="icon-wrapper">
            <MapPin class="header-icon" />
          </div>
          <div>
            <h1 class="title">Gerenciar plantas</h1>
            <p class="subtitle">Visualize e gerencie as plantas cadastradas</p>
          </div>
        </div>
        <button class="close-btn" @click="fechar">
          <X class="close-icon" />
        </button>
      </div>

      <div class="modal-content-wrapper">
        <div class="info-section">
          <div class="info-card">
            <p class="info-text">
              Nesta tela, você poderá visualizar as plantas cadastradas do seu escritório.
              Todas as plantas adicionadas serão disponibilizadas automaticamente para os usuários
              e a numeração dos lugares será gerada de forma automática.
            </p>
          </div>
          
          <div class="info-cards-row">
            <div class="info-card-small">
              <strong>Recomendação:</strong>
              para melhor experiência e evitar erros de carregamento, recomenda-se realizar este
              procedimento em um computador (desktop).
            </div>
            <div class="info-card-small">
              <strong>Obs.:</strong> a imagem deve ter tamanho mínimo de
              <span class="tag-dim">1400 × 1400 px</span>.
            </div>
          </div>
        </div>

        <!-- Ações -->
        <div class="actions-row">
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
      </div>

      <!-- Mini modal confirmar exclusão -->
      <div v-if="showConfirmExcluir" class="mini-overlay" @click="showConfirmExcluir = false">
        <div class="mini-modal" @click.stop>
          <div class="mini-header">
            <h3 class="mini-title">Excluir planta</h3>
            <button class="mini-close-btn" @click="showConfirmExcluir = false">
              <X class="mini-close-icon" />
            </button>
          </div>
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
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 2rem 1rem;
  overflow-y: auto;
}

.card {
  background: white;
  border-radius: 16px;
  padding: 0;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.3), 0 10px 10px -5px rgba(0, 0, 0, 0.2);
  max-width: 900px;
  width: 100%;
  max-height: calc(100vh - 4rem);
  overflow: hidden;
  position: relative;
  margin: auto;
  display: flex;
  flex-direction: column;
}

.modal-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 1rem;
  padding: 1.5rem 2rem;
  background: linear-gradient(135deg, #1C2457 0%, #2F2365 100%);
  color: white;
  position: sticky;
  top: 0;
  z-index: 10;
}

.header-content {
  display: flex;
  align-items: center;
  gap: 1rem;
  flex: 1;
}

.icon-wrapper {
  width: 48px;
  height: 48px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.header-icon {
  width: 24px;
  height: 24px;
  color: white;
}

.title {
  font-size: 1.5rem;
  font-weight: 700;
  margin: 0;
  color: white;
}

.subtitle {
  font-size: 0.875rem;
  margin: 0.25rem 0 0 0;
  color: rgba(255, 255, 255, 0.8);
  font-weight: 400;
}

.close-btn {
  border: none;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  cursor: pointer;
  padding: 0.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  transition: background 0.2s;
  flex-shrink: 0;
  width: 36px;
  height: 36px;
}

.close-btn:hover {
  background: rgba(255, 255, 255, 0.2);
}

.close-icon {
  width: 20px;
  height: 20px;
}

.modal-content-wrapper {
  padding: 2rem;
  overflow-y: auto;
  flex: 1;
}

.info-section {
  margin-bottom: 1.5rem;
}

.info-card {
  background: #f0f9ff;
  border: 1px solid #bae6fd;
  border-radius: 12px;
  padding: 1rem 1.25rem;
  margin-bottom: 1rem;
}

.info-text {
  font-size: 0.875rem;
  color: #1e40af;
  line-height: 1.6;
  margin: 0;
}

.info-cards-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 0.75rem;
}

.info-card-small {
  background: #fef3c7;
  border: 1px solid #fde68a;
  border-radius: 12px;
  padding: 0.875rem 1rem;
  font-size: 0.8125rem;
  color: #92400e;
  line-height: 1.5;
}

.tag-dim {
  background: #fee2e2;
  color: #991b1b;
  padding: 0.15rem 0.5rem;
  border-radius: 6px;
  font-size: 0.75rem;
  font-weight: 600;
  display: inline-block;
  margin-left: 0.25rem;
}

.actions-row {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
  margin-bottom: 1.5rem;
  align-items: center;
  justify-content: flex-start;
}

.btn {
  border: none;
  border-radius: 8px;
  padding: 0.625rem 1.25rem;
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  color: #ffffff;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}
.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  box-shadow: none;
}
.btn:not(:disabled):hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.editar {
  background: linear-gradient(135deg, #3B82F6 0%, #2563EB 100%);
}
.excluir {
  background: linear-gradient(135deg, #EF4444 0%, #DC2626 100%);
}
.adicionar {
  background: linear-gradient(135deg, #22C55E 0%, #16A34A 100%);
}
.salvar {
  background: linear-gradient(135deg, #7C3AED 0%, #6D28D9 100%);
}

.select-wrapper {
  min-width: 220px;
  flex: 1;
}
.select {
  width: 100%;
  border: 1.5px solid #e5e7eb;
  border-radius: 8px;
  padding: 0.625rem 1rem;
  font-size: 0.875rem;
  background: white;
  color: #374151;
  transition: all 0.2s;
}
.select:focus {
  outline: none;
  border-color: #7C3AED;
  box-shadow: 0 0 0 3px rgba(124, 58, 237, 0.1);
}

.planta-container {
  margin-top: 1rem;
  border-radius: 12px;
  overflow: hidden;
  position: relative;
  background: #1f2937;
  border: 2px solid #374151;
  max-width: 700px;
  width: 100%;
  aspect-ratio: 1 / 1;
  margin-left: auto;
  margin-right: auto;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
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
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
  padding: 1rem;
  animation: fadeIn 0.2s ease-out;
}

.mini-modal {
  background: white;
  border-radius: 16px;
  padding: 0;
  width: 100%;
  max-width: 420px;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.3), 0 10px 10px -5px rgba(0, 0, 0, 0.2);
  overflow: hidden;
  animation: slideUp 0.3s ease-out;
}

.mini-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.25rem 1.5rem;
  border-bottom: 1px solid #e5e7eb;
  background: linear-gradient(135deg, #EF4444 0%, #DC2626 100%);
  color: white;
}

.mini-title {
  font-size: 1.125rem;
  font-weight: 700;
  margin: 0;
  color: white;
}

.mini-close-btn {
  background: rgba(255, 255, 255, 0.1);
  border: none;
  border-radius: 8px;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: white;
  transition: background 0.2s;
}

.mini-close-btn:hover {
  background: rgba(255, 255, 255, 0.2);
}

.mini-close-icon {
  width: 18px;
  height: 18px;
}

.mini-text {
  font-size: 0.875rem;
  color: #374151;
  line-height: 1.6;
  padding: 1.25rem 1.5rem;
  margin: 0;
}

.mini-actions {
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
  padding: 1rem 1.5rem 1.25rem;
  background: #f9fafb;
  border-top: 1px solid #e5e7eb;
}

.mini-btn {
  border-radius: 8px;
  padding: 0.625rem 1.25rem;
  font-size: 0.875rem;
  font-weight: 600;
  border: none;
  cursor: pointer;
  transition: all 0.2s;
}

.mini-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.mini-btn.ghost {
  background: white;
  color: #374151;
  border: 1.5px solid #e5e7eb;
}

.mini-btn.ghost:hover {
  background: #f9fafb;
  border-color: #d1d5db;
}

.mini-btn.primary {
  background: linear-gradient(135deg, #3B82F6 0%, #2563EB 100%);
  color: #ffffff;
}

.mini-btn.danger {
  background: linear-gradient(135deg, #EF4444 0%, #DC2626 100%);
  color: #ffffff;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
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
</style>
