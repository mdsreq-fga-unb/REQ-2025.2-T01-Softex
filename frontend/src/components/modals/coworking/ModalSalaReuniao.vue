<script setup lang="ts">
import { ref, watch, computed } from "vue";

type TipoReuniao = "interna" | "externa";

type ReservaPayload = {
  pessoas: number;
  tipo: TipoReuniao;
  motivo: string;
  data: string;
  horaInicio: string;
  horaFim: string;
};

const props = defineProps<{
  open: boolean;
}>();

const emit = defineEmits<{
  (e: "close"): void;
  (e: "save", payload: ReservaPayload): void;
}>();

const pessoas = ref<string>("");
const tipo = ref<TipoReuniao>("interna");
const motivo = ref<string>("");
const data = ref<string>("");
const horaInicio = ref<string>("");
const horaFim = ref<string>("");

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
    }
  }
);

const podeSalvar = computed(() => {
  const qtd = Number(pessoas.value || 0);
  return (
    qtd > 0 &&
    motivo.value.trim().length > 0 &&
    data.value !== "" &&
    horaInicio.value !== "" &&
    horaFim.value !== ""
  );
});

const fechar = () => {
  emit("close");
};

const salvar = () => {
  if (!podeSalvar.value) return;

  emit("save", {
    pessoas: Number(pessoas.value),
    tipo: tipo.value,
    motivo: motivo.value.trim(),
    data: data.value,
    horaInicio: horaInicio.value,
    horaFim: horaFim.value,
  });
};
</script>

<template>
  <div v-if="open" class="overlay">
    <div class="card">
      <div class="header">
        <h2 class="title">Reservar Sala de reunião</h2>
        <button class="close-btn" type="button" @click="fechar">×</button>
      </div>

      <p class="intro">
        Para que se reserve uma sala de reunião é necessário informar o motivo,
        a quantidade de participantes, se a reunião é interna ou externa,
        horário e dia.
      </p>

      <div class="field-row">
        <label class="label" for="pessoas">Pessoas:</label>
        <input
          id="pessoas"
          v-model="pessoas"
          type="number"
          min="1"
          class="input-sm"
          placeholder="Qtd."
        />
      </div>

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
        <label class="label" for="motivo">Motivo</label>
        <textarea
          id="motivo"
          v-model="motivo"
          rows="3"
          class="textarea"
          placeholder="Descreva rapidamente o objetivo da reunião"
        />
      </div>

      <div class="date-time-block">
        <div class="date-row">
          <span class="icon"><i class="fa-solid fa-calendar"></i></span>
          <input v-model="data" type="date" class="input-date" />
        </div>

        <div class="time-row">
          <span class="icon"> <i class="fa-solid fa-clock"></i></span>
          <input v-model="horaInicio" type="time" class="input-time" />
          <span class="time-separator">até</span>
          <input v-model="horaFim" type="time" class="input-time" />
        </div>
      </div>

      <p class="info-text">
        Quando uma sala de reunião estiver reservada para você, você receberá um
        aviso no Slack e também poderá consultar em
        <strong>"Minhas reservas".</strong>
      </p>

      <button
        type="button"
        class="btn-submit"
        :disabled="!podeSalvar"
        @click="salvar"
      >
        Reservar agora
      </button>
    </div>
  </div>
</template>

<style scoped>
.overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.55);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 90;
}

.card {
  width: 100%;
  max-width: 380px;
  background: #f9fafb;
  border-radius: 22px;
  padding: 1.2rem 1.4rem 1.4rem;
  box-shadow: 0 18px 40px rgba(0, 0, 0, 0.45);
  font-size: 0.9rem;
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
  align-items: center;
  gap: 0.4rem;
  margin-bottom: 0.35rem;
}

.icon {
  font-size: 0.9rem;
}

.input-date,
.input-time {
  border-radius: 8px;
  border: 1px solid #d1d5db;
  padding: 0.3rem 0.5rem;
  font-size: 0.8rem;
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
