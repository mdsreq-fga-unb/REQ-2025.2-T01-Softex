<script setup lang="ts">
import { computed } from 'vue'

type FluxoStatus = 'andamento' | 'concluido'
type ResultadoStatus = 'aprovado' | 'pendente' | 'negado'

type ReservaCadeira = {
  id: number
  titulo: string           // Ex: "Estação 13 — Coworking"
  estacao: string          // Ex: "Estação 13"
  fluxo: FluxoStatus       // andamento | concluido
  status: ResultadoStatus  // aprovado | pendente | negado
  dataInicio: string       // "dd/mm/aaaa"
  dataFim: string          // "dd/mm/aaaa"
  horaInicio: string       // "hh:mm"  -> agora OBRIGATÓRIO
  horaFim: string          // "hh:mm"  -> agora OBRIGATÓRIO
}

const props = defineProps<{
  open: boolean
  reserva: ReservaCadeira | null
}>()

const emit = defineEmits<{
  (e: 'close'): void
}>()

const statusLabel = computed(() => {
  if (!props.reserva) return ''
  switch (props.reserva.status) {
    case 'aprovado':
      return 'Aprovada'
    case 'pendente':
      return 'Pendente de aprovação'
    case 'negado':
      return 'Negada'
  }
})

const statusClass = computed(() => {
  if (!props.reserva) return ''
  switch (props.reserva.status) {
    case 'aprovado':
      return 'badge badge-ok'
    case 'pendente':
      return 'badge badge-wait'
    case 'negado':
      return 'badge badge-denied'
  }
})

const statusMensagem = computed(() => {
  const r = props.reserva
  if (!r) return ''
  if (r.status === 'pendente') {
    return 'Sua reserva está aguardando aprovação.'
  }
  if (r.status === 'aprovado') {
    return 'Sua reserva foi aprovada. Aparecerá em "Em andamento" até ser concluída.'
  }
  // negado
  return 'Sua reserva foi negada. Reservas negadas aparecem apenas na aba "Concluído".'
})

const fluxoAvisoInvalido = computed(() => {
  const r = props.reserva
  if (!r) return false
  // regra: em andamento => apenas pendente/aprovado
  //       negado => só em concluído
  if (r.fluxo === 'andamento' && r.status === 'negado') return true
  if (r.fluxo === 'concluido' && r.status === 'pendente') return true
  return false
})

const fechar = () => emit('close')
</script>

<template>
  <div v-if="open && reserva" class="overlay">
    <div class="card">
      <div class="header">
        <h2 class="title">Reserva estação de trabalho</h2>
        <button class="close-btn" type="button" @click="fechar">×</button>
      </div>

      <div class="content">
        <p class="descricao">
          Aqui você encontra os detalhes da reserva da sua estação de trabalho.
        </p>

        <div class="linha-info">
          <span class="label">Estação:</span>
          <span class="valor">{{ reserva.estacao }}</span>
        </div>

        <div class="linha-info">
          <span class="label">Período:</span>
          <span class="valor">
            {{ reserva.dataInicio }} → {{ reserva.dataFim }}
          </span>
        </div>

        <!-- Horário agora sempre aparece -->
        <div class="linha-info">
          <span class="label">Horário:</span>
          <span class="valor">
            {{ reserva.horaInicio }} → {{ reserva.horaFim }}
          </span>
        </div>

        <div class="linha-info status-row">
          <span class="label">Status da reserva:</span>
          <span :class="statusClass">{{ statusLabel }}</span>
        </div>

        <p class="mensagem-status">
          {{ statusMensagem }}
        </p>

        <p v-if="fluxoAvisoInvalido" class="mensagem-erro">
          Atenção: combinação de status e aba inválida.
          Verifique se esta reserva está sendo listada na aba correta
          (Em andamento / Concluído).
        </p>
      </div>

      <div class="actions">
        <button class="btn-fechar" type="button" @click="fechar">
          Fechar
        </button>
      </div>
    </div>
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
  z-index: 90;
}

.card {
  width: 100%;
  max-width: 420px;
  background: #ffffff;
  border-radius: 18px;
  box-shadow: 0 18px 40px rgba(0, 0, 0, 0.35);
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.8rem 1.4rem;
  border-bottom: 1px solid #e5e7eb;
}

.title {
  font-size: 1rem;
  font-weight: 700;
}

.close-btn {
  border: none;
  background: transparent;
  font-size: 1.4rem;
  line-height: 1;
  cursor: pointer;
}

.content {
  padding: 1.1rem 1.4rem 0.5rem;
}

.descricao {
  font-size: 0.8rem;
  color: #4b5563;
  margin-bottom: 0.9rem;
}

.linha-info {
  display: flex;
  justify-content: space-between;
  gap: 0.75rem;
  font-size: 0.85rem;
  margin-bottom: 0.4rem;
}

.status-row {
  align-items: center;
}

.label {
  font-weight: 600;
  color: #111827;
}

.valor {
  color: #111827;
}

.badge {
  border-radius: 999px;
  padding: 0.1rem 0.7rem;
  font-size: 0.75rem;
  font-weight: 600;
}

.badge-ok {
  background: #dcfce7;
  color: #166534;
}

.badge-wait {
  background: #fef9c3;
  color: #854d0e;
}

.badge-denied {
  background: #fee2e2;
  color: #b91c1c;
}

.mensagem-status {
  font-size: 0.78rem;
  color: #4b5563;
  margin-top: 0.6rem;
}

.mensagem-erro {
  font-size: 0.75rem;
  color: #b91c1c;
  margin-top: 0.5rem;
}

.actions {
  padding: 0.8rem 1.4rem 1rem;
  display: flex;
  justify-content: flex-end;
}

.btn-fechar {
  border-radius: 999px;
  padding: 0.4rem 1.2rem;
  font-size: 0.85rem;
  font-weight: 600;
  border: none;
  cursor: pointer;
  background: #6366f1;
  color: #ffffff;
}
</style>
