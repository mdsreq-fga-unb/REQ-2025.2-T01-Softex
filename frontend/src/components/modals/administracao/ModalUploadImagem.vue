<script setup lang="ts">
import { ref, watch, onBeforeUnmount } from 'vue'

type UploadPayload = {
  file: File | null
  previewUrl: string | null
  nome: string
}

const props = defineProps<{
  open: boolean
  initialPreviewUrl?: string | null
  initialNome?: string | null
}>()

const emit = defineEmits<{
  (e: 'close'): void
  (e: 'confirm', payload: UploadPayload): void
}>()

const file = ref<File | null>(null)
const previewUrl = ref<string | null>(props.initialPreviewUrl ?? null)
const nome = ref<string>(props.initialNome ?? '')

const fileInput = ref<HTMLInputElement | null>(null)

const revokePreview = () => {
  if (previewUrl.value && previewUrl.value.startsWith('blob:')) {
    URL.revokeObjectURL(previewUrl.value)
  }
}

watch(
  () => file.value,
  (newFile) => {
    revokePreview()
    if (newFile) {
      previewUrl.value = URL.createObjectURL(newFile)
    } else if (!props.initialPreviewUrl) {
      previewUrl.value = null
    }
  }
)

onBeforeUnmount(() => {
  revokePreview()
})

const handleFiles = (files: FileList | null) => {
  if (!files || !files[0]) return
  const f = files[0]
  file.value = f
}

const onDrop = (event: DragEvent) => {
  event.preventDefault()
  if (!event.dataTransfer) return
  handleFiles(event.dataTransfer.files)
}

const onDragOver = (event: DragEvent) => {
  event.preventDefault()
}

const abrirFilePicker = () => {
  fileInput.value?.click()
}

const confirmar = () => {
  emit('confirm', {
    file: file.value,
    previewUrl: previewUrl.value,
    nome: nome.value.trim()
  })
}

const cancelar = () => {
  emit('close')
}
</script>

<template>
  <div v-if="open" class="upload-overlay">
    <div class="upload-card">
      <h2 class="upload-title">Adicionar planta</h2>
      <p class="upload-subtitle">
        Obs: A imagem deve ser de proporção <strong>1400 × 1400</strong>.
      </p>

      <!-- Área de drop / clique -->
      <div
        class="drop-area"
        @dragover="onDragOver"
        @drop="onDrop"
        @click="abrirFilePicker"
      >
        <!-- Quando ainda não tem imagem -->
        <template v-if="!previewUrl">
          <div class="drop-circle">
            <svg
              class="drop-icon"
              viewBox="0 0 24 24"
              aria-hidden="true"
            >
              <path
                fill="currentColor"
                d="M12 3l4 4h-3v6h-2V7H8l4-4zm-7 14h14v2H5v-2z"
              />
            </svg>
          </div>
          <p class="drop-text">Arraste a imagem</p>
          <p class="drop-hint">ou clique aqui para selecionar</p>
        </template>

        <!-- Quando já tem preview -->
        <template v-else>
          <img
            :src="previewUrl"
            alt="Prévia da planta"
            class="drop-preview-img"
          />
          <p class="drop-change">Clique para trocar a imagem</p>
        </template>

        <input
          ref="fileInput"
          type="file"
          accept="image/*"
          class="hidden-input"
          @change="(e: Event) => handleFiles((e.target as HTMLInputElement).files)"
        />
      </div>

      <!-- Campo nome da planta -->
      <div class="name-wrapper">
        <label class="name-label" for="nomePlanta">
          Nome da planta
        </label>
        <input
          id="nomePlanta"
          v-model="nome"
          type="text"
          class="name-input"
          placeholder="Ex: Escritório 1º andar - Layout A"
        />
      </div>

      <p class="confirm-text">Gostaria de adicionar essa planta?</p>

      <div class="actions-row">
        <button class="btn-confirm" @click="confirmar">
          Sim
        </button>
        <button class="btn-cancel" @click="cancelar">
          Não
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.upload-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.45);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1100;
}

.upload-card {
  width: 100%;
  max-width: 420px;
  background: #ffffff;
  border-radius: 18px;
  padding: 1.5rem 1.75rem 1.25rem;
  box-shadow: 0 18px 40px rgba(0, 0, 0, 0.35);
  text-align: center;
}

.upload-title {
  font-size: 1.15rem;
  font-weight: 700;
  margin-bottom: 0.3rem;
}

.upload-subtitle {
  font-size: 0.85rem;
  color: #4b5563;
  margin-bottom: 1rem;
}

.drop-area {
  border-radius: 16px;
  border: 2px dashed #9ca3af;
  padding: 1.75rem 1rem;
  cursor: pointer;
  background: #f9fafb;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.4rem;
  transition: border-color 0.15s ease, background 0.15s ease;
  min-height: 170px;
}

.drop-area:hover {
  border-color: #4f46e5;
  background: #eef2ff;
}

.drop-circle {
  width: 56px;
  height: 56px;
  border-radius: 999px;
  border: 2px solid #9ca3af;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 0.25rem;
}

.drop-icon {
  width: 26px;
  height: 26px;
  color: #6b7280;
}

.drop-text {
  font-size: 0.9rem;
  color: #374151;
}

.drop-hint {
  font-size: 0.75rem;
  color: #6b7280;
}

.hidden-input {
  display: none;
}

/* preview dentro da área */
.drop-preview-img {
  max-width: 100%;
  max-height: 140px;
  border-radius: 12px;
  object-fit: contain;
}

.drop-change {
  font-size: 0.75rem;
  color: #6b7280;
  margin-top: 0.4rem;
}

/* nome da planta */
.name-wrapper {
  margin-top: 1rem;
  text-align: left;
}

.name-label {
  display: block;
  font-size: 0.8rem;
  color: #4b5563;
  margin-bottom: 0.2rem;
}

.name-input {
  width: 100%;
  border-radius: 999px;
  border: 1px solid #d1d5db;
  padding: 0.4rem 0.9rem;
  font-size: 0.9rem;
  outline: none;
}

.name-input:focus {
  border-color: #4f46e5;
  box-shadow: 0 0 0 2px rgba(79, 70, 229, 0.25);
}

/* texto da confirmação */
.confirm-text {
  margin-top: 1.25rem;
  font-size: 0.9rem;
  color: #111827;
}

/* botões */
.actions-row {
  margin-top: 0.75rem;
  display: flex;
  justify-content: center;
  gap: 1rem;
}

.btn-confirm,
.btn-cancel {
  min-width: 90px;
  padding: 0.4rem 1.1rem;
  border-radius: 999px;
  border: none;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  color: #ffffff;
  transition: opacity 0.15s ease, transform 0.1s ease;
}

.btn-confirm {
  background: #10b981;
}

.btn-cancel {
  background: #ef4444;
}

.btn-confirm:hover,
.btn-cancel:hover {
  opacity: 0.9;
  transform: translateY(-1px);
}
</style>
