<script setup lang="ts">
import { ref, watch, computed } from "vue";
import { X } from "lucide-vue-next";
import { useAuth } from "@/composables/useAuth";

type ReservaSala = {
  id: number;
  titulo: string;
  solicitante: string;
  sala: string;
  dataInicio: string;
  dataFim: string;
  horaInicio: string;
  horaFim: string;
  status?: string;
};

const props = defineProps<{
  open: boolean;
  reserva: ReservaSala | null;
}>();

const emit = defineEmits<{
  (e: "close"): void;
  (e: "cancelar", id: number): void;
}>();

// Verificar se o usuário é administrador
const { user } = useAuth();
const isAdmin = computed(() => user.value?.tipo_funcao === "Administrativo");

const confirmacao = ref("");

watch(
  () => props.open,
  (isOpen) => {
    if (isOpen) {
      confirmacao.value = "";
    }
  }
);

const podeCancelar = computed(() => {
  return confirmacao.value.trim().toLowerCase() === "confirmar";
});

const cancelar = () => {
  if (!props.reserva || !podeCancelar.value) return;
  emit("cancelar", props.reserva.id);
};

const fechar = () => {
  emit("close");
};
</script>

<template>
  <div v-if="open && reserva" class="overlay" @click.self="fechar">
    <div class="card-container">
      <!-- Conteúdo principal -->
      <div class="card-main">
        <div class="header">
          <h2 class="title">Cancelar Reunião</h2>
          <button class="close-btn" type="button" @click="fechar">×</button>
        </div>

        <div class="content">
          <p class="pergunta">Tem certeza que deseja cancelar essa reunião?</p>

          <div class="reserva-info">
            <div class="info-row">
              <span class="info-label">Reunião:</span>
              <span class="info-value">{{ reserva.titulo }}</span>
            </div>
            <div class="info-row">
              <span class="info-label">Solicitante:</span>
              <span class="info-value">{{ reserva.solicitante }}</span>
            </div>
            <div class="info-row">
              <span class="info-label">Sala:</span>
              <span class="info-value">{{ reserva.sala }}</span>
            </div>
            <div class="info-row">
              <span class="info-label">Data:</span>
              <span class="info-value"
                >{{ reserva.dataInicio }} – {{ reserva.dataFim }}</span
              >
            </div>
            <div class="info-row">
              <span class="info-label">Horário:</span>
              <span class="info-value"
                >{{ reserva.horaInicio }} → {{ reserva.horaFim }}</span
              >
            </div>
          </div>

          <div class="confirmacao-field">
            <label class="confirmacao-label" for="confirmacao">
              Digite <strong>"confirmar"</strong> para cancelar:
            </label>
            <input
              id="confirmacao"
              v-model="confirmacao"
              type="text"
              class="confirmacao-input"
              placeholder="confirmar"
              autocomplete="off"
            />
          </div>

          <!-- Botões de ação para não-admins (fallback) -->
          <div v-if="!isAdmin" class="actions">
            <button type="button" class="btn btn-fechar" @click="fechar">
              Fechar
            </button>
            <button
              type="button"
              class="btn btn-cancelar"
              :disabled="!podeCancelar"
              @click="cancelar"
            >
              Cancelar Reunião
            </button>
          </div>
        </div>
      </div>

      <!-- Sidebar para administradores -->
      <div v-if="isAdmin" class="sidebar">
        <div class="sidebar-header">
          <h3 class="sidebar-title">Ações do Administrador</h3>
        </div>
        <div class="sidebar-content">
          <div class="sidebar-section">
            <p class="sidebar-description">
              Como administrador, você pode cancelar esta reserva. Esta ação não
              pode ser desfeita.
            </p>
          </div>

          <div class="sidebar-actions">
            <button
              class="sidebar-btn sidebar-btn-danger"
              type="button"
              :disabled="!podeCancelar"
              @click="cancelar"
            >
              <span class="btn-icon">⚠</span>
              <span>Cancelar Reunião</span>
            </button>

            <button
              class="sidebar-btn sidebar-btn-secondary"
              type="button"
              @click="fechar"
            >
              <span class="btn-icon">✕</span>
              <span>Fechar</span>
            </button>
          </div>

          <div class="sidebar-info">
            <div class="info-item">
              <span class="info-label">Status atual:</span>
              <span
                class="info-value"
                :class="`status-${reserva.status || 'pendente'}`"
              >
                {{
                  reserva.status === "aprovado"
                    ? "Aprovada"
                    : reserva.status === "negado"
                    ? "Negada"
                    : "Pendente"
                }}
              </span>
            </div>
            <div class="info-item">
              <span class="info-label">Confirmação:</span>
              <span class="info-value">
                {{
                  podeCancelar ? "✓ Pronto para cancelar" : 'Digite "confirmar"'
                }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  backdrop-filter: blur(4px);
}

.card-container {
  width: 100%;
  max-width: 900px;
  max-height: 90vh;
  background: #ffffff;
  border-radius: 24px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
  overflow: hidden;
  display: flex;
  margin: 1rem;
}

.card-main {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow-y: auto;
  /* Scrollbar customizada */
  scrollbar-width: thin;
  scrollbar-color: #8b5cf6 #f1f1f1;
}

.card-main::-webkit-scrollbar {
  width: 8px;
}

.card-main::-webkit-scrollbar-track {
  background: #f9fafb;
  border-radius: 10px;
  margin: 8px 0;
}

.card-main::-webkit-scrollbar-thumb {
  background: linear-gradient(135deg, #8b5cf6 0%, #ec4899 100%);
  border-radius: 10px;
  border: 2px solid #f9fafb;
  transition: background 0.3s ease;
}

.card-main::-webkit-scrollbar-thumb:hover {
  background: linear-gradient(135deg, #7c3aed 0%, #db2777 100%);
}

.header {
  display: flex;
  justify-content: center;
  align-items: flex-start;
  position: relative;
  padding: 1.5rem 1.8rem 1rem;
  border-bottom: 1px solid #e5e7eb;
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
}

.title {
  font-size: 1rem;
  font-weight: 700;
  text-align: center;
  color: white;
  margin: 0;
}

.close-btn {
  position: absolute;
  right: 1.8rem;
  top: 1.3rem;
  border: none;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 8px;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: white;
  font-size: 1.4rem;
  line-height: 1;
  transition: background 0.2s;
}

.close-btn:hover {
  background: rgba(255, 255, 255, 0.3);
}

.content {
  padding: 1.1rem 1.8rem 0.5rem;
  font-size: 0.9rem;
}

.pergunta {
  font-size: 1rem;
  font-weight: 600;
  color: #111827;
  margin: 0 0 1.2rem 0;
  text-align: center;
}

.reserva-info {
  background: #f9fafb;
  border-radius: 12px;
  padding: 1rem 1.2rem;
  margin-bottom: 1.2rem;
  border: 1px solid #e5e7eb;
}

.info-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 0.75rem;
  font-size: 0.85rem;
  margin-bottom: 0.5rem;
}

.info-row:last-child {
  margin-bottom: 0;
}

.info-label {
  font-weight: 600;
  color: #6b7280;
}

.info-value {
  color: #111827;
  text-align: right;
}

.confirmacao-field {
  margin-top: 1.5rem;
}

.confirmacao-label {
  display: block;
  font-size: 0.875rem;
  font-weight: 600;
  color: #374151;
  margin-bottom: 0.5rem;
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
  border-color: #ef4444;
  box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.1);
}

.confirmacao-input::placeholder {
  color: #9ca3af;
}

/* Sidebar para administradores */
.sidebar {
  width: 320px;
  background: linear-gradient(135deg, #f9fafb 0%, #f3f4f6 100%);
  border-left: 1px solid #e5e7eb;
  display: flex;
  flex-direction: column;
  overflow-y: auto;
}

.sidebar-header {
  padding: 1.2rem 1.5rem;
  border-bottom: 1px solid #e5e7eb;
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
}

.sidebar-title {
  font-size: 0.95rem;
  font-weight: 700;
  color: white;
  margin: 0;
}

.sidebar-content {
  flex: 1;
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.sidebar-section {
  margin-bottom: 0.5rem;
}

.sidebar-description {
  font-size: 0.8rem;
  color: #6b7280;
  line-height: 1.5;
  margin: 0;
}

.sidebar-actions {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.sidebar-btn {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.75rem 1rem;
  border-radius: 12px;
  border: none;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.15s ease;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.sidebar-btn-danger {
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
  color: #ffffff;
}

.sidebar-btn-danger:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(239, 68, 68, 0.3);
}

.sidebar-btn-secondary {
  background: #f3f4f6;
  color: #111827;
  border: 1px solid #d1d5db;
}

.sidebar-btn-secondary:hover {
  background: #e5e7eb;
  transform: translateY(-1px);
}

.sidebar-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none;
}

.btn-icon {
  font-size: 1.1rem;
  font-weight: 700;
}

.sidebar-info {
  margin-top: auto;
  padding-top: 1.5rem;
  border-top: 1px solid #e5e7eb;
}

.info-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem 0;
  font-size: 0.85rem;
}

.info-item .info-label {
  font-weight: 600;
  color: #6b7280;
}

.info-item .info-value {
  font-weight: 500;
  color: #111827;
}

.info-item .info-value.status-aprovado {
  color: #16a34a;
}

.info-item .info-value.status-negado {
  color: #ef4444;
}

.info-item .info-value.status-pendente {
  color: #f59e0b;
}

/* Responsividade */
@media (max-width: 768px) {
  .card-container {
    flex-direction: column;
    max-width: 100%;
    max-height: 95vh;
  }

  .sidebar {
    width: 100%;
    border-left: none;
    border-top: 1px solid #e5e7eb;
    max-height: 40vh;
  }

  .sidebar-header {
    background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
  }

  .sidebar-content {
    padding: 1rem;
    gap: 1rem;
  }

  .sidebar-actions {
    gap: 0.5rem;
  }
}

/* ações para não-admins (fallback) */
.actions {
  padding: 1rem 1.8rem 1.8rem;
  display: flex;
  justify-content: flex-end;
  gap: 0.5rem;
  flex-wrap: wrap;
  border-top: 1px solid #e5e7eb;
  margin-top: 0.5rem;
}

.btn {
  border-radius: 999px;
  padding: 0.55rem 1.2rem;
  font-size: 0.9rem;
  font-weight: 600;
  border: none;
  cursor: pointer;
  transition: opacity 0.12s ease, transform 0.1s ease, box-shadow 0.12s ease;
}

.btn-cancelar {
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
  color: #ffffff;
  box-shadow: 0 4px 12px rgba(239, 68, 68, 0.3);
}

.btn-fechar {
  background: #f3f4f6;
  color: #111827;
  border: 1px solid #d1d5db;
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  box-shadow: none;
}

.btn-cancelar:not(:disabled):hover,
.btn-fechar:hover {
  opacity: 0.95;
  transform: translateY(-1px);
}
</style>
