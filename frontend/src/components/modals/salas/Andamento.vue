<!-- src/components/modals/salas/Andamento.vue -->
<script setup lang="ts">
import { ref, watch, computed, onMounted } from "vue";
import api from "@/services/api";
import { useAuth } from "@/composables/useAuth";

type FluxoStatus = "andamento" | "concluido";
type ResultadoStatus = "aprovado" | "pendente" | "negado";

type ReservaSala = {
  id: number;
  titulo: string;
  solicitante: string;
  sala: string;
  fluxo: FluxoStatus;
  status: ResultadoStatus;
  data: string;
  horaInicio: string;
  horaFim: string;
  participantes: number;
  tipoReuniao: "interna" | "externa";
  motivoReuniao?: string;
};

type SalaFisica = {
  id: number;
  nome: string;
};

const props = defineProps<{
  open: boolean;
  reserva: ReservaSala | null;
}>();

const emit = defineEmits<{
  (e: "close"): void;
  (
    e: "aprovar",
    payload: { id: number; salaEscolhida: string; codigoSala: string }
  ): void;
  (e: "recusar", id: number): void;
  (e: "cancelar", id: number): void;
}>();

const salasDisponiveis = ref<SalaFisica[]>([]);
const isLoadingSalas = ref(false);
const salaSelecionada = ref<string>("");
const codigoSala = ref<string>("");

// Verificar se o usuário é administrador
const { user } = useAuth();
const isAdmin = computed(() => user.value?.tipo_funcao === "Administrativo");

// Carregar salas do backend
const carregarSalas = async () => {
  isLoadingSalas.value = true;
  try {
    const resSalas = await api.get("/salas-reuniao/");
    salasDisponiveis.value = Array.isArray(resSalas.data)
      ? resSalas.data.map((s: any) => ({
          id: s.id,
          nome: s.nome,
        }))
      : [];
    console.log(
      "✅ Salas carregadas no modal de aprovação:",
      salasDisponiveis.value
    );
  } catch (error: any) {
    console.error("❌ Erro ao carregar salas:", error);
  } finally {
    isLoadingSalas.value = false;
  }
};

watch(
  () => props.open,
  async (isOpen) => {
    if (isOpen) {
      // Recarregar salas ao abrir o modal para ter as mais recentes
      await carregarSalas();
      if (props.reserva) {
        // Definir a sala selecionada após carregar
        salaSelecionada.value =
          props.reserva.sala || salasDisponiveis.value[0]?.nome || "";
        codigoSala.value = ""; // limpa código ao abrir
      }
    }
  }
);

// Watch para atualizar sala selecionada quando as salas forem carregadas
watch(
  () => salasDisponiveis.value,
  () => {
    if (props.open && props.reserva && salasDisponiveis.value.length > 0) {
      // Se não houver sala selecionada, usar a primeira disponível ou a sala da reserva
      if (!salaSelecionada.value) {
        salaSelecionada.value =
          props.reserva.sala || salasDisponiveis.value[0]?.nome || "";
      }
    }
  }
);

onMounted(() => {
  carregarSalas();
});

const podeAprovar = computed(
  () => !!props.reserva && !!salaSelecionada.value
  // se quiser obrigar código, troca por:
  // () => !!props.reserva && !!salaSelecionada.value && !!codigoSala.value
);

const tipoReuniaoLabel = computed(() => {
  if (!props.reserva) return "";
  return props.reserva.tipoReuniao === "interna"
    ? "Reunião interna"
    : "Reunião externa";
});

const aprovar = () => {
  if (!props.reserva || !salaSelecionada.value) return;
  emit("aprovar", {
    id: props.reserva.id,
    salaEscolhida: salaSelecionada.value,
    codigoSala: codigoSala.value.trim(),
  });
};

const recusar = () => {
  if (!props.reserva) return;
  emit("recusar", props.reserva.id);
};

const cancelar = () => {
  if (!props.reserva) return;
  emit("cancelar", props.reserva.id);
};

const fechar = () => emit("close");
</script>

<template>
  <div v-if="open && reserva" class="overlay">
    <div class="card-container">
      <!-- Conteúdo principal -->
      <div class="card-main">
        <div class="header">
          <h2 class="title">Solicitação de sala de reunião</h2>
          <button class="close-btn" type="button" @click="fechar">×</button>
        </div>

        <div class="content">
          <p class="descricao">
            Revise os detalhes da solicitação antes de aprovar ou recusar o uso
            da sala.
          </p>

          <div class="linha-info">
            <span class="label">Solicitante:</span>
            <span class="valor">{{ reserva.solicitante }}</span>
          </div>

          <div class="linha-info">
            <span class="label">Data:</span>
            <span class="valor">
              {{ reserva.data }}
            </span>
          </div>

          <div class="linha-info">
            <span class="label">Horário:</span>
            <span class="valor">
              {{ reserva.horaInicio }} → {{ reserva.horaFim }}
            </span>
          </div>

          <div class="linha-info">
            <span class="label">Tipo de reunião:</span>
            <span class="valor">{{ tipoReuniaoLabel }}</span>
          </div>

          <div class="linha-info">
            <span class="label">Participantes:</span>
            <span class="valor">{{ reserva.participantes }} pessoas</span>
          </div>

          <!-- Motivo da reunião (somente leitura) -->
          <div v-if="reserva.motivoReuniao" class="motivo-box">
            <span class="motivo-label">Motivo da reunião:</span>
            <p class="motivo-text">
              {{ reserva.motivoReuniao }}
            </p>
          </div>

          <div class="divider" />

          <div class="field">
            <label class="label" for="sala-aprovada">
              Sala aprovada para a reserva:
            </label>
            <select
              id="sala-aprovada"
              v-model="salaSelecionada"
              class="select"
              :disabled="isLoadingSalas"
            >
              <option :value="null">Selecione uma sala</option>
              <option
                v-for="sala in salasDisponiveis"
                :key="sala.id"
                :value="sala.nome"
              >
                {{ sala.nome }}
              </option>
            </select>
            <p class="hint">
              Você pode manter a sala solicitada ou alterar para outra sala
              disponível.
            </p>
          </div>

          <!-- Caixa de texto para código da sala -->
          <div class="field">
            <label class="label" for="codigo-sala">
              Código da sala (para envio ao solicitante)
            </label>
            <input
              id="codigo-sala"
              v-model="codigoSala"
              type="text"
              class="input"
              placeholder="Ex: SALA-ALFA-3ANDAR"
            />
            <p class="hint">
              Este código poderá ser enviado ao solicitante junto com a
              confirmação da reserva.
            </p>
          </div>

          <!-- Botões de ação para não-admins (fallback) -->
          <div v-if="!isAdmin" class="actions">
            <button class="btn btn-cancelar" type="button" @click="cancelar">
              Cancelar Reunião
            </button>
            <button class="btn btn-ghost" type="button" @click="recusar">
              Recusar
            </button>
            <button
              class="btn btn-primary"
              type="button"
              :disabled="!podeAprovar"
              @click="aprovar"
            >
              Aprovar reserva
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
              Como administrador, você pode aprovar, recusar ou cancelar esta
              solicitação.
            </p>
          </div>

          <div class="sidebar-actions">
            <button
              class="sidebar-btn sidebar-btn-primary"
              type="button"
              :disabled="!podeAprovar || isLoadingSalas"
              @click="aprovar"
            >
              <span class="btn-icon">✓</span>
              <span>Aprovar Reserva</span>
            </button>

            <button
              class="sidebar-btn sidebar-btn-danger"
              type="button"
              @click="recusar"
            >
              <span class="btn-icon">✕</span>
              <span>Recusar</span>
            </button>

            <button
              class="sidebar-btn sidebar-btn-cancel"
              type="button"
              @click="cancelar"
            >
              <span class="btn-icon">⚠</span>
              <span>Cancelar Reunião</span>
            </button>
          </div>

          <div class="sidebar-info">
            <div class="info-item">
              <span class="info-label">Status:</span>
              <span class="info-value" :class="`status-${reserva.status}`">
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
              <span class="info-label">Sala selecionada:</span>
              <span class="info-value">{{
                salaSelecionada || "Não selecionada"
              }}</span>
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
}

.title {
  font-size: 1rem;
  font-weight: 700;
  text-align: center;
}

.close-btn {
  position: absolute;
  right: 1.8rem;
  top: 1.3rem;
  border: none;
  background: transparent;
  font-size: 1.4rem;
  line-height: 1;
  cursor: pointer;
  color: #111827;
}

.content {
  padding: 1.1rem 1.8rem 0.5rem;
  font-size: 0.9rem;
}

.descricao {
  font-size: 0.78rem;
  color: #4b5563;
  text-align: left;
  margin-bottom: 0.8rem;
}

.linha-info {
  display: flex;
  justify-content: space-between;
  gap: 0.75rem;
  font-size: 0.85rem;
  margin-bottom: 0.4rem;
}

.label {
  font-weight: 600;
  color: #111827;
}

.valor {
  color: #111827;
}

.motivo-box {
  margin-top: 0.7rem;
  padding: 0.6rem 0.8rem;
  border-radius: 0.75rem;
  background: #f9fafb;
  border: 1px dashed #e5e7eb;
}

.motivo-label {
  font-size: 0.8rem;
  font-weight: 600;
  color: #111827;
}

.motivo-text {
  margin-top: 0.25rem;
  font-size: 0.8rem;
  color: #4b5563;
  white-space: pre-line;
}

.divider {
  margin: 0.9rem 0 0.7rem;
  border-top: 1px solid #e5e7eb;
}

.field {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  font-size: 0.85rem;
  margin-top: 0.5rem;
}

.select {
  border-radius: 999px;
  border: 1px solid #d1d5db;
  padding: 0.4rem 0.9rem;
  font-size: 0.85rem;
  outline: none;
  background: #ffffff;
  width: 100%;
  cursor: pointer;
}

.select:focus {
  border-color: #3b82f6;
  box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.25);
}

.select:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.input {
  border-radius: 8px;
  border: 1px solid #d1d5db;
  padding: 0.45rem 0.75rem;
  font-size: 0.85rem;
  outline: none;
  background: #ffffff;
  width: 100%;
}

.input:focus {
  border-color: #3b82f6;
  box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.25);
}

.hint {
  font-size: 0.78rem;
  color: #6b7280;
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
  background: #ffffff;
}

.sidebar-title {
  font-size: 0.95rem;
  font-weight: 700;
  color: #111827;
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

.sidebar-btn-primary {
  background: linear-gradient(135deg, #16a34a 0%, #15803d 100%);
  color: #ffffff;
}

.sidebar-btn-primary:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(22, 163, 74, 0.3);
}

.sidebar-btn-danger {
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
  color: #ffffff;
}

.sidebar-btn-danger:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(239, 68, 68, 0.3);
}

.sidebar-btn-cancel {
  background: #f3f4f6;
  color: #111827;
  border: 1px solid #d1d5db;
}

.sidebar-btn-cancel:hover {
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

.info-label {
  font-weight: 600;
  color: #6b7280;
}

.info-value {
  font-weight: 500;
  color: #111827;
}

.info-value.status-aprovado {
  color: #16a34a;
}

.info-value.status-negado {
  color: #ef4444;
}

.info-value.status-pendente {
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

.btn-ghost {
  background: #f3f4f6;
  color: #111827;
  border: 1px solid #d1d5db;
}

.btn-primary {
  background: linear-gradient(135deg, #16a34a 0%, #15803d 100%);
  color: #ffffff;
  box-shadow: 0 4px 12px rgba(22, 163, 74, 0.35);
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  box-shadow: none;
}

.btn-cancelar:hover,
.btn-primary:not(:disabled):hover,
.btn-ghost:hover {
  opacity: 0.95;
  transform: translateY(-1px);
}
</style>
