<script setup lang="ts">
import { ref, watch, computed, onMounted } from "vue";
import { Teleport } from "vue";
import { useAuth } from "@/composables/useAuth";

type TipoReuniao = "interna" | "externa";

type Sala = {
  id: number;
  nome: string;
};

type ReservaPayload = {
  pessoas: number;
  tipo: TipoReuniao;
  motivo: string;
  data: string;
  horaInicio: string;
  horaFim: string;
  salaId: number;
};

const props = defineProps<{
  open: boolean;
}>();

const emit = defineEmits<{
  (e: "close"): void;
  (e: "save", payload: ReservaPayload): void;
}>();

const { authenticatedFetch } = useAuth();
const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

const pessoas = ref<string>("");
const tipo = ref<TipoReuniao>("interna");
const motivo = ref<string>("");
const data = ref<string>("");
const horaInicio = ref<string>("");
const horaFim = ref<string>("");
const salaId = ref<number | null>(null);
const salas = ref<Sala[]>([]);
const isLoadingSalas = ref(false);
const errors = ref<Record<string, string>>({});

// Carregar salas disponíveis
const carregarSalas = async () => {
  isLoadingSalas.value = true;
  try {
    // Buscar apenas do endpoint de salas de reunião
    const response = await authenticatedFetch(`${API_URL}/api/salas-reuniao/`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    });

    if (response.ok) {
      const data = await response.json();
      salas.value = Array.isArray(data) ? data : [];
      console.log("✅ Salas de reunião carregadas:", salas.value);
    } else {
      console.error("❌ Erro ao carregar salas:", response.status);
      const errorText = await response.text();
      console.error("Detalhes do erro:", errorText);
    }
  } catch (e) {
    console.error("❌ Erro ao carregar salas:", e);
  } finally {
    isLoadingSalas.value = false;
  }
};

watch(
  () => props.open,
  (isOpen) => {
    if (isOpen) {
      pessoas.value = "";
      tipo.value = "interna";
      motivo.value = "";
      data.value = "";
      horaInicio.value = "";
      horaFim.value = "";
      salaId.value = null;
      errors.value = {};
      // Sempre recarregar salas ao abrir o modal para ter as mais recentes
      carregarSalas();
    }
  }
);

// Validações
const validar = (): boolean => {
  errors.value = {};

  const qtd = Number(pessoas.value || 0);
  if (qtd <= 0) {
    errors.value.pessoas = "Informe a quantidade de pessoas";
  }

  if (!motivo.value.trim()) {
    errors.value.motivo = "Informe o motivo da reunião";
  }

  if (!data.value) {
    errors.value.data = "Selecione uma data";
  } else {
    const hoje = new Date();
    hoje.setHours(0, 0, 0, 0);
    const dataSelecionada = new Date(data.value);
    if (dataSelecionada < hoje) {
      errors.value.data = "A data não pode ser no passado";
    }
  }

  if (!horaInicio.value) {
    errors.value.horaInicio = "Informe o horário de início";
  }

  if (!horaFim.value) {
    errors.value.horaFim = "Informe o horário de fim";
  }

  if (horaInicio.value && horaFim.value) {
    if (horaInicio.value >= horaFim.value) {
      errors.value.horaFim =
        "O horário de fim deve ser após o horário de início";
    }
  }

  if (!salaId.value) {
    errors.value.sala = "Selecione uma sala";
  }

  return Object.keys(errors.value).length === 0;
};

const podeSalvar = computed(() => {
  const qtd = Number(pessoas.value || 0);
  return (
    qtd > 0 &&
    motivo.value.trim().length > 0 &&
    data.value !== "" &&
    horaInicio.value !== "" &&
    horaFim.value !== "" &&
    salaId.value !== null
  );
});

const fechar = () => {
  emit("close");
};

const salvar = async () => {
  if (!validar() || !podeSalvar.value) return;

  if (!salaId.value) {
    errors.value.sala = "Selecione uma sala";
    return;
  }

  try {
    // Combinar data e hora para criar DateTime
    const dataInicioStr = `${data.value}T${horaInicio.value}:00`;
    const dataFimStr = `${data.value}T${horaFim.value}:00`;

    // Usar o endpoint de reserva na API de salas
    const url = `${API_URL}/api/salas-reuniao/reservar/`;
    const payloadData = {
      sala: salaId.value,
      data_inicio: dataInicioStr,
      data_fim: dataFimStr,
      descricao:
        motivo.value.trim() ||
        `Reunião ${tipo.value} - ${pessoas.value} pessoas`,
    };

    console.log("🔗 Criando reserva de sala em:", url);
    console.log("📦 Dados da reserva:", payloadData);

    const response = await authenticatedFetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payloadData),
    });

    console.log(
      "📡 Resposta do servidor:",
      response.status,
      response.statusText
    );

    if (!response.ok) {
      const errorText = await response.text();
      console.error("❌ Erro na resposta:", errorText);
      let errorData;
      try {
        errorData = JSON.parse(errorText);
      } catch {
        errorData = { error: errorText };
      }

      if (response.status === 401 || response.status === 403) {
        alert("Sua sessão expirou. Por favor, faça login novamente.");
        return;
      }

      if (response.status === 405) {
        alert(
          "Erro: Método POST não permitido neste endpoint. Verifique a configuração do servidor."
        );
        console.error("❌ Endpoint não aceita POST:", url);
        return;
      }

      if (response.status === 400) {
        const errorMessage =
          errorData.non_field_errors?.[0] ||
          errorData.detail ||
          errorData.sala?.[0] ||
          (typeof errorData === "string"
            ? errorData
            : errorData.error || errorData.message) ||
          "Erro ao criar reserva. Verifique os dados informados.";
        alert(errorMessage);
        return;
      }

      throw new Error(
        errorData.detail ||
          errorData.error ||
          errorData.message ||
          `Erro ao criar reserva: ${response.status} - ${errorText}`
      );
    }

    const reservaCriada = await response.json();
    console.log("✅ Reserva de sala criada com sucesso:", reservaCriada);

    // Emitir evento de sucesso para o componente pai
    emit("save", {
      pessoas: Number(pessoas.value),
      tipo: tipo.value,
      motivo: motivo.value.trim(),
      data: data.value,
      horaInicio: horaInicio.value,
      horaFim: horaFim.value,
      salaId: salaId.value,
    });

    // Fechar o modal
    emit("close");
    alert("Reserva de sala criada com sucesso!");
  } catch (e) {
    console.error("❌ Erro ao criar reserva de sala:", e);
    alert(
      e instanceof Error ? e.message : "Erro ao criar reserva. Tente novamente."
    );
  }
};

onMounted(() => {
  carregarSalas();
});
</script>

<template>
  <Teleport to="body">
    <div v-if="open" class="overlay" @click.self="fechar">
      <div class="card">
        <div class="header">
          <h2 class="title">Reservar Sala de reunião</h2>
          <button class="close-btn" type="button" @click="fechar">×</button>
        </div>

        <p class="intro">
          Para que se reserve uma sala de reunião é necessário informar o
          motivo, a quantidade de participantes, se a reunião é interna ou
          externa, horário e dia.
        </p>

        <div class="field-column">
          <label class="label" for="sala">Sala *</label>
          <select
            id="sala"
            v-model.number="salaId"
            class="input-select"
            :class="{ 'input-error': errors.sala }"
          >
            <option :value="null">Selecione uma sala</option>
            <option v-for="sala in salas" :key="sala.id" :value="sala.id">
              {{ sala.nome }}
            </option>
          </select>
          <span v-if="errors.sala" class="error-text">{{ errors.sala }}</span>
        </div>

        <div class="field-row">
          <label class="label" for="pessoas">Pessoas *</label>
          <input
            id="pessoas"
            v-model="pessoas"
            type="number"
            min="1"
            class="input-sm"
            :class="{ 'input-error': errors.pessoas }"
            placeholder="Qtd."
          />
        </div>
        <span v-if="errors.pessoas" class="error-text">{{
          errors.pessoas
        }}</span>

        <div class="toggle-row">
          <span class="label">Tipo:</span>
          <div class="toggle">
            <button
              type="button"
              class="toggle-btn"
              :class="{ active: tipo === 'interna' }"
              @click="tipo = 'interna'"
            >
              Interna
            </button>
            <button
              type="button"
              class="toggle-btn"
              :class="{ active: tipo === 'externa' }"
              @click="tipo = 'externa'"
            >
              Externa
            </button>
          </div>
        </div>

        <div class="field-column">
          <label class="label" for="motivo">Motivo *</label>
          <textarea
            id="motivo"
            v-model="motivo"
            rows="3"
            class="textarea"
            :class="{ 'input-error': errors.motivo }"
            placeholder="Descreva rapidamente o objetivo da reunião"
          />
          <span v-if="errors.motivo" class="error-text">{{
            errors.motivo
          }}</span>
        </div>

        <div class="date-time-block">
          <div class="field-column">
            <label class="label" for="data">Data *</label>
            <input
              id="data"
              v-model="data"
              type="date"
              class="input-date"
              :class="{ 'input-error': errors.data }"
            />
            <span v-if="errors.data" class="error-text">{{ errors.data }}</span>
          </div>

          <div class="time-row">
            <div class="field-column" style="flex: 1">
              <label class="label" for="horaInicio">Início *</label>
              <input
                id="horaInicio"
                v-model="horaInicio"
                type="time"
                class="input-time"
                :class="{ 'input-error': errors.horaInicio }"
              />
              <span v-if="errors.horaInicio" class="error-text">{{
                errors.horaInicio
              }}</span>
            </div>
            <span class="time-separator">até</span>
            <div class="field-column" style="flex: 1">
              <label class="label" for="horaFim">Fim *</label>
              <input
                id="horaFim"
                v-model="horaFim"
                type="time"
                class="input-time"
                :class="{ 'input-error': errors.horaFim }"
              />
              <span v-if="errors.horaFim" class="error-text">{{
                errors.horaFim
              }}</span>
            </div>
          </div>
        </div>

        <p class="info-text">
          Quando uma sala de reunião estiver reservada para você, você receberá
          um aviso no Slack e também poderá consultar em
          <strong>"Minhas reservas".</strong>
        </p>

        <button
          type="button"
          class="btn-submit"
          :disabled="!podeSalvar || isLoadingSalas"
          @click="salvar"
        >
          {{ isLoadingSalas ? "Carregando..." : "Reservar agora" }}
        </button>
      </div>
    </div>
  </Teleport>
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

.card {
  width: 100%;
  max-width: 480px;
  max-height: 90vh;
  overflow-y: auto;
  background: #ffffff;
  border-radius: 24px;
  padding: 1.5rem 1.8rem 1.8rem;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
  font-size: 0.9rem;
  margin: 1rem;
  /* Scrollbar customizada */
  scrollbar-width: thin;
  scrollbar-color: #8b5cf6 #f1f1f1;
}

.card::-webkit-scrollbar {
  width: 8px;
}

.card::-webkit-scrollbar-track {
  background: #f9fafb;
  border-radius: 10px;
  margin: 8px 0;
}

.card::-webkit-scrollbar-thumb {
  background: linear-gradient(135deg, #8b5cf6 0%, #ec4899 100%);
  border-radius: 10px;
  border: 2px solid #f9fafb;
  transition: background 0.3s ease;
}

.card::-webkit-scrollbar-thumb:hover {
  background: linear-gradient(135deg, #7c3aed 0%, #db2777 100%);
}

.header {
  display: flex;
  justify-content: center;
  align-items: flex-start;
  position: relative;
  margin-bottom: 0.4rem;
}

.title {
  font-size: 1rem;
  font-weight: 700;
  text-align: center;
}

.close-btn {
  position: absolute;
  right: 0;
  top: -0.2rem;
  border: none;
  background: transparent;
  font-size: 1.4rem;
  line-height: 1;
  cursor: pointer;
}

.intro {
  font-size: 0.78rem;
  color: #4b5563;
  text-align: left;
  margin-bottom: 0.8rem;
}

.field-row {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.6rem;
}

.label {
  font-size: 0.8rem;
  font-weight: 600;
  color: #111827;
}

.input-sm {
  flex: 0 0 70px;
  border-radius: 8px;
  border: 1px solid #d1d5db;
  padding: 0.3rem 0.5rem;
  font-size: 0.8rem;
}

.toggle-row {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.7rem;
}

.toggle {
  display: inline-flex;
  border-radius: 999px;
  background: #e5e7eb;
  padding: 0.12rem;
}

.toggle-btn {
  border: none;
  background: transparent;
  padding: 0.25rem 0.8rem;
  border-radius: 999px;
  font-size: 0.78rem;
  cursor: pointer;
  color: #4b5563;
}

.toggle-btn.active {
  background: #111827;
  color: #f9fafb;
}

.field-column {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  margin-bottom: 0.7rem;
}

.textarea {
  border-radius: 10px;
  border: 1px solid #d1d5db;
  padding: 0.45rem 0.6rem;
  font-size: 0.8rem;
  resize: none;
}

.date-time-block {
  margin-bottom: 0.7rem;
}

.date-row,
.time-row {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
  margin-bottom: 0.5rem;
}

.time-row {
  align-items: flex-end;
}

.icon {
  font-size: 0.9rem;
}

.input-date,
.input-time,
.input-select {
  border-radius: 8px;
  border: 1px solid #d1d5db;
  padding: 0.4rem 0.6rem;
  font-size: 0.85rem;
  width: 100%;
  background: white;
}

.input-select {
  cursor: pointer;
}

.input-error {
  border-color: #ef4444;
  background-color: #fef2f2;
}

.error-text {
  color: #ef4444;
  font-size: 0.75rem;
  margin-top: 0.25rem;
  display: block;
}

.time-separator {
  font-size: 0.8rem;
  color: #4b5563;
}

.info-text {
  font-size: 0.75rem;
  color: #4b5563;
  margin: 0.7rem 0 0.9rem;
}

.btn-submit {
  width: 100%;
  border: none;
  border-radius: 999px;
  padding: 0.55rem 1rem;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  color: #ffffff;
  background: linear-gradient(135deg, #ec4899, #8b5cf6);
  box-shadow: 0 8px 20px rgba(168, 85, 247, 0.6);
  transition: opacity 0.12s ease, transform 0.1s ease, box-shadow 0.12s ease;
}

.btn-submit:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  box-shadow: none;
}

.btn-submit:not(:disabled):hover {
  opacity: 0.95;
  transform: translateY(-1px);
}
</style>
