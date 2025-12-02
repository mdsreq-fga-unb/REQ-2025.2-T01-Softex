<script setup lang="ts">
import { ref, watch, computed } from "vue";
import { Teleport } from "vue";
import { Clock, Calendar, X } from "lucide-vue-next";

type SeatStatus = "disponivel" | "ocupado" | "reservado";

type SeatInfo = {
  id: number;
  status: SeatStatus;
};

type ReservaInfo = {
  usuario_nome: string;
  usuario_email?: string;
  data_inicio: string;
  data_fim: string;
  hora_inicio: string;
  hora_fim: string;
  status: string;
};

type ReservaCadeiraPayload = {
  seatId: number;
  dataInicio: string;
  dataFim: string;
  horaInicio: string;
  horaFim: string;
};

const props = defineProps<{
  open: boolean;
  seat: SeatInfo | null;
  reservaInfo?: ReservaInfo | null;
}>();

const emit = defineEmits<{
  (e: "close"): void;
  (e: "reserve", payload: ReservaCadeiraPayload): void;
}>();

const dataInicio = ref("");
const horaInicio = ref("");
const horaFim = ref("");

const labelFromStatus = (status: SeatStatus): string => {
  switch (status) {
    case "disponivel":
      return "disponível";
    case "ocupado":
      return "ocupado";
    case "reservado":
      return "reservado";
  }
};

const bloqueado = computed(() => {
  if (!props.seat) return true;
  return props.seat.status === "ocupado" || props.seat.status === "reservado";
});

const isReservado = computed(() => {
  return props.seat?.status === "reservado" && !!props.reservaInfo;
});

const formatarData = (data: string): string => {
  if (!data) return "";
  try {
    const date = new Date(data);
    if (isNaN(date.getTime())) {
      // Se não for uma data válida, tentar formato YYYY-MM-DD
      return data;
    }
    return date.toLocaleDateString("pt-BR");
  } catch {
    return data;
  }
};

const formatarHora = (hora: string): string => {
  if (!hora) return "";
  // Se já estiver no formato HH:MM, retornar como está
  if (hora.match(/^\d{2}:\d{2}$/)) {
    return hora;
  }
  // Se for um objeto Time do Django, pode vir como "HH:MM:SS"
  if (hora.match(/^\d{2}:\d{2}:\d{2}$/)) {
    return hora.substring(0, 5); // Retornar apenas HH:MM
  }
  return hora;
};

// Validação de data
const dataValida = computed(() => {
  if (!dataInicio.value) return false;

  const hoje = new Date();
  hoje.setHours(0, 0, 0, 0);

  const dataSelecionada = new Date(dataInicio.value);
  dataSelecionada.setHours(0, 0, 0, 0);

  // A data não pode ser no passado
  return dataSelecionada >= hoje;
});

// Validação de horários
const horasValidas = computed(() => {
  if (!horaInicio.value || !horaFim.value) return false;

  // Verificar se o horário de fim é maior que o de início
  if (horaFim.value <= horaInicio.value) return false;

  // Verificar se há pelo menos 30 minutos de diferença
  const partesInicio = horaInicio.value.split(":").map(Number);
  const partesFim = horaFim.value.split(":").map(Number);

  if (partesInicio.length !== 2 || partesFim.length !== 2) return false;

  const [horaInicioH, minutoInicioM] = partesInicio;
  const [horaFimH, minutoFimM] = partesFim;

  if (
    horaInicioH === undefined ||
    minutoInicioM === undefined ||
    horaFimH === undefined ||
    minutoFimM === undefined
  ) {
    return false;
  }

  const minutosInicio = horaInicioH * 60 + minutoInicioM;
  const minutosFim = horaFimH * 60 + minutoFimM;
  const diferencaMinutos = minutosFim - minutosInicio;

  if (diferencaMinutos < 30) return false;

  // Verificar se os horários estão dentro de um range válido (ex: 06:00 - 22:00)
  const horaMinima = 6 * 60; // 06:00 em minutos
  const horaMaxima = 22 * 60; // 22:00 em minutos

  if (minutosInicio < horaMinima || minutosFim > horaMaxima) return false;

  return true;
});

// Validação de data e hora combinadas (se a data for hoje, a hora não pode ser no passado)
const dataHoraValida = computed(() => {
  if (!dataValida.value || !horaInicio.value) return true;

  const hoje = new Date();
  hoje.setHours(0, 0, 0, 0);

  const dataSelecionada = new Date(dataInicio.value);
  dataSelecionada.setHours(0, 0, 0, 0);

  // Se a data selecionada for hoje, verificar se o horário não é no passado
  if (dataSelecionada.getTime() === hoje.getTime()) {
    const agora = new Date();
    const partes = horaInicio.value.split(":").map(Number);

    if (
      partes.length !== 2 ||
      partes[0] === undefined ||
      partes[1] === undefined
    ) {
      return false;
    }

    const [horaInicioH, minutoInicioM] = partes;
    const horarioInicio = new Date();
    horarioInicio.setHours(horaInicioH, minutoInicioM, 0, 0);

    // Permitir reservas com pelo menos 15 minutos de antecedência
    const agoraMais15Min = new Date(agora.getTime() + 15 * 60 * 1000);

    return horarioInicio >= agoraMais15Min;
  }

  return true;
});

// Mensagens de erro
const mensagemErro = computed(() => {
  if (!dataInicio.value) {
    return "Selecione uma data para a reserva.";
  }

  if (!dataValida.value) {
    return "A data selecionada não pode ser no passado.";
  }

  if (!horaInicio.value || !horaFim.value) {
    return "Preencha os horários de início e fim.";
  }

  if (!dataHoraValida.value) {
    return "O horário de início deve ser pelo menos 15 minutos a partir de agora.";
  }

  if (!horasValidas.value) {
    const partesInicio = horaInicio.value.split(":").map(Number);
    const partesFim = horaFim.value.split(":").map(Number);

    if (partesInicio.length !== 2 || partesFim.length !== 2) {
      return "Formato de horário inválido.";
    }

    const [horaInicioH, minutoInicioM] = partesInicio;
    const [horaFimH, minutoFimM] = partesFim;

    if (
      horaInicioH === undefined ||
      minutoInicioM === undefined ||
      horaFimH === undefined ||
      minutoFimM === undefined
    ) {
      return "Formato de horário inválido.";
    }

    const minutosInicio = horaInicioH * 60 + minutoInicioM;
    const minutosFim = horaFimH * 60 + minutoFimM;

    if (horaFim.value <= horaInicio.value) {
      return "O horário de fim deve ser maior que o horário de início.";
    }

    const diferencaMinutos = minutosFim - minutosInicio;
    if (diferencaMinutos < 30) {
      return "A reserva deve ter no mínimo 30 minutos de duração.";
    }

    const horaMinima = 6 * 60;
    const horaMaxima = 22 * 60;

    if (minutosInicio < horaMinima || minutosFim > horaMaxima) {
      return "Os horários devem estar entre 06:00 e 22:00.";
    }
  }

  return "";
});

const podeSalvar = computed(() => {
  if (bloqueado.value || !props.seat) return false;
  return (
    dataValida.value &&
    horasValidas.value &&
    dataHoraValida.value &&
    !mensagemErro.value
  );
});

watch(
  () => [props.open, props.seat?.id],
  () => {
    if (!props.open) return;
    dataInicio.value = "";
    horaInicio.value = "";
    horaFim.value = "";
  }
);

const fechar = () => {
  emit("close");
};

const salvar = () => {
  if (!podeSalvar.value || !props.seat) return;

  emit("reserve", {
    seatId: props.seat.id,
    dataInicio: dataInicio.value,
    // como agora é sempre 1 dia, mantemos dataFim igual à dataInicio
    dataFim: dataInicio.value,
    horaInicio: horaInicio.value,
    horaFim: horaFim.value,
  });
};
</script>

<template>
  <Teleport to="body">
    <div v-if="open" class="overlay" @click.self="fechar">
      <div class="card">
        <div class="header">
          <div class="header-content">
            <h2 class="title">
              {{
                isReservado
                  ? "Informações da Reserva"
                  : "Reservar estação de trabalho"
              }}
            </h2>
            <p v-if="!isReservado" class="subtitle">
              Para reservar essa estação, informe o horário e
              <strong> um único dia</strong> de uso.
            </p>
          </div>
          <button class="close-btn" type="button" @click="fechar">
            <X class="close-icon" />
          </button>
        </div>

        <!-- Modal de visualização quando reservado -->
        <div v-if="isReservado && reservaInfo" class="reserva-info-container">
          <div class="info-box">
            <div class="info-item">
              <span class="info-label">Estação:</span>
              <span class="info-value">{{ seat?.id }}</span>
            </div>

            <div class="info-item">
              <span class="info-label">Reservado por:</span>
              <span class="info-value highlight">{{
                reservaInfo.usuario_nome
              }}</span>
            </div>

            <div v-if="reservaInfo.usuario_email" class="info-item">
              <span class="info-label">Email:</span>
              <span class="info-value">{{ reservaInfo.usuario_email }}</span>
            </div>

            <div class="info-item">
              <span class="info-label">Data:</span>
              <span class="info-value">
                {{ formatarData(reservaInfo.data_inicio) }}
                <span v-if="reservaInfo.data_inicio !== reservaInfo.data_fim">
                  até {{ formatarData(reservaInfo.data_fim) }}
                </span>
              </span>
            </div>

            <div class="info-item">
              <span class="info-label">Horário:</span>
              <span class="info-value">
                {{ formatarHora(reservaInfo.hora_inicio) }} até
                {{ formatarHora(reservaInfo.hora_fim) }}
              </span>
            </div>

            <div class="info-item">
              <span class="info-label">Status:</span>
              <span class="status-badge status-confirmada">
                {{
                  reservaInfo.status === "confirmada"
                    ? "Confirmada"
                    : "Cancelada"
                }}
              </span>
            </div>
          </div>

          <button type="button" class="btn-close" @click="fechar">
            Fechar
          </button>
        </div>

        <!-- Modal de reserva quando disponível -->
        <template v-else>
          <div v-if="seat && bloqueado" class="alert">
            Esta estação está
            <strong>{{ labelFromStatus(seat.status) }}</strong>
            e não pode ser reservada.
          </div>

          <div class="form" :class="{ disabled: bloqueado }">
            <div class="time-row">
              <div class="input-wrapper">
                <Clock class="input-icon" />
                <input
                  v-model="horaInicio"
                  type="time"
                  class="input-time"
                  :disabled="bloqueado"
                />
              </div>
              <span class="ate">até</span>
              <div class="input-wrapper">
                <input
                  v-model="horaFim"
                  type="time"
                  class="input-time"
                  :disabled="bloqueado"
                />
                <span class="asterisk">*</span>
              </div>
            </div>

            <div class="date-row">
              <div class="input-wrapper">
                <Calendar class="input-icon" />
                <input
                  v-model="dataInicio"
                  type="date"
                  class="input-date"
                  :disabled="bloqueado"
                  :min="new Date().toISOString().split('T')[0]"
                />
                <span class="asterisk">*</span>
              </div>
            </div>

            <p v-if="!bloqueado && mensagemErro" class="error">
              {{ mensagemErro }}
            </p>
          </div>

          <p v-if="seat" class="info">
            Você está reservando a estação de trabalho de número
            <strong> {{ seat.id }} </strong>.
          </p>

          <button
            type="button"
            class="btn-submit"
            :disabled="!podeSalvar"
            @click="salvar"
          >
            Reservar agora
          </button>
        </template>
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
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.55);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 99999;
  overflow-y: auto;
  padding: 2rem 1rem;
  margin: 0;
  box-sizing: border-box;
}

.card {
  width: 100%;
  max-width: 480px;
  background: #ffffff;
  border-radius: 20px;
  padding: 1.75rem 2rem 2rem;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.3),
    0 10px 10px -5px rgba(0, 0, 0, 0.2);
  font-size: 0.9rem;
  position: relative;
  margin: auto;
  max-height: calc(100vh - 4rem);
  overflow-y: auto;
  z-index: 100000;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 1rem;
  margin-bottom: 1.25rem;
}

.header-content {
  flex: 1;
}

.title {
  font-size: 1.25rem;
  font-weight: 700;
  color: #111827;
  margin: 0 0 0.5rem 0;
}

.subtitle {
  font-size: 0.875rem;
  color: #6b7280;
  line-height: 1.5;
  margin: 0;
}

.close-btn {
  border: none;
  background: transparent;
  cursor: pointer;
  padding: 0.25rem;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #6b7280;
  transition: color 0.2s;
  flex-shrink: 0;
}

.close-btn:hover {
  color: #111827;
}

.close-icon {
  width: 20px;
  height: 20px;
}

.alert {
  background: #fee2e2;
  color: #991b1b;
  border-radius: 10px;
  padding: 0.4rem 0.6rem;
  font-size: 0.76rem;
  margin-bottom: 0.7rem;
}

.form {
  margin-bottom: 1.25rem;
}

.form.disabled {
  opacity: 0.6;
  pointer-events: none;
}

.time-row,
.date-row {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1rem;
}

.input-wrapper {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  flex: 1;
  position: relative;
}

.input-icon {
  width: 18px;
  height: 18px;
  color: #6b7280;
  flex-shrink: 0;
}

.input-time,
.input-date {
  flex: 1;
  border-radius: 10px;
  border: 1.5px solid #e5e7eb;
  padding: 0.625rem 0.75rem;
  font-size: 0.875rem;
  background: #ffffff;
  color: #111827;
  transition: border-color 0.2s, box-shadow 0.2s;
  min-width: 0;
}

.input-time:focus,
.input-date:focus {
  outline: none;
  border-color: #8b5cf6;
  box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.1);
}

.input-time:disabled,
.input-date:disabled {
  background: #f3f4f6;
  color: #9ca3af;
  cursor: not-allowed;
}

.ate {
  font-size: 0.875rem;
  color: #6b7280;
  font-weight: 500;
  flex-shrink: 0;
}

.asterisk {
  font-size: 1rem;
  color: #ef4444;
  font-weight: 600;
  margin-left: 0.25rem;
}

.error {
  font-size: 0.75rem;
  color: #b91c1c;
  margin-top: 0.2rem;
}

.info {
  font-size: 0.875rem;
  color: #6b7280;
  text-align: center;
  margin-bottom: 1.25rem;
  line-height: 1.5;
}

.btn-submit {
  width: 100%;
  border: none;
  border-radius: 12px;
  padding: 0.75rem 1.5rem;
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  color: #ffffff;
  background: linear-gradient(135deg, #ec4899, #8b5cf6);
  box-shadow: 0 10px 25px rgba(139, 92, 246, 0.4);
  transition: opacity 0.2s ease, transform 0.15s ease, box-shadow 0.2s ease;
}

.btn-submit:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  box-shadow: 0 4px 12px rgba(139, 92, 246, 0.2);
}

.btn-submit:not(:disabled):hover {
  opacity: 0.95;
  transform: translateY(-2px);
  box-shadow: 0 12px 30px rgba(139, 92, 246, 0.5);
}

/* Estilos para modal de visualização */
.reserva-info-container {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.info-box {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  padding: 1.25rem;
  background: #f9fafb;
  border-radius: 12px;
  border: 1px solid #e5e7eb;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.info-label {
  font-size: 0.75rem;
  font-weight: 600;
  color: #6b7280;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.info-value {
  font-size: 0.95rem;
  color: #111827;
  font-weight: 500;
}

.info-value.highlight {
  color: #8b5cf6;
  font-weight: 600;
  font-size: 1rem;
}

.status-badge {
  display: inline-block;
  padding: 0.375rem 0.75rem;
  border-radius: 6px;
  font-size: 0.875rem;
  font-weight: 600;
}

.status-confirmada {
  background: #d1fae5;
  color: #065f46;
}

.status-cancelada {
  background: #fee2e2;
  color: #991b1b;
}

.btn-close {
  width: 100%;
  border: none;
  border-radius: 12px;
  padding: 0.75rem 1.5rem;
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  color: #ffffff;
  background: #6b7280;
  transition: background 0.2s ease;
}

.btn-close:hover {
  background: #4b5563;
}
</style>
