<script setup lang="ts">
import { ref, computed } from 'vue'
import Header from '@/components/Layout/Header.vue'
import plantaImg from '@/assets/planta.png'
import ModalSalaReuniao from '@/components/modals/coworking/ModalSalaReuniao.vue'
import ModalCadeira from '@/components/modals/coworking/ModalCadeira.vue'

type SeatStatus = 'disponivel' | 'ocupado' | 'reservado' | 'favorito'

type SeatPoint = {
  id: number
  x: number   // em %
  y: number   // em %
  status: SeatStatus
}

type PlantaOption = {
  id: number
  nome: string
  img: string
}

type ReservaPayload = {
  pessoas: number
  tipo: 'interna' | 'externa'
  motivo: string
  data: string
  horaInicio: string
  horaFim: string
}

type ReservaCadeiraPayload = ReservaPayload & {
  seatId: number
}

const plantas = ref<PlantaOption[]>([
  { id: 1, nome: 'Pavimento baixo - Coworking', img: plantaImg },
  { id: 2, nome: 'Pavimento superior - Coworking', img: plantaImg }
])

const selectedPlantaId = ref<number>(plantas.value[0].id)

const selectedPlantaImg = computed(() => {
  const p = plantas.value.find(p => p.id === selectedPlantaId.value)
  return p ? p.img : plantaImg
})

const seats = ref<SeatPoint[]>([
  { id: 1, x: 25, y: 30, status: 'disponivel' },
  { id: 2, x: 40, y: 32, status: 'ocupado' },
  { id: 3, x: 55, y: 35, status: 'reservado' },
  { id: 4, x: 30, y: 55, status: 'disponivel' },
  { id: 5, x: 45, y: 57, status: 'favorito' },
  { id: 6, x: 60, y: 59, status: 'disponivel' },
  { id: 7, x: 28, y: 75, status: 'disponivel' }
])

const selectedSeat = ref<SeatPoint | null>(null)

const showReservaModal = ref(false)

const showCadeiraModal = ref(false)

const handleSeatClick = (id: number) => {
  const seat = seats.value.find(s => s.id === id)
  if (!seat) return
  selectedSeat.value = seat
  showCadeiraModal.value = true
  console.log('Assento clicado:', seat)
}

const labelFromStatus = (status: SeatStatus): string => {
  switch (status) {
    case 'disponivel': return 'Disponível'
    case 'ocupado': return 'Ocupado'
    case 'reservado': return 'Reservado'
    case 'favorito': return 'Seu favorito'
  }
}

const handleSalvarReserva = (payload: ReservaPayload) => {
  console.log('Reserva de sala salva:', payload)
  showReservaModal.value = false
}

const handleReservaCadeira = (payload: ReservaCadeiraPayload) => {
  console.log('Reserva de cadeira:', payload)
  const seat = seats.value.find(s => s.id === payload.seatId)
  if (seat) {
    seat.status = 'reservado'
  }
  showCadeiraModal.value = false
}
</script>



<template>
  <div class="coworking-bg min-h-screen">
    <Header />

    <div class="wrapper">
      <div class="top-row">
        <div class="legend-card">
          <p class="legend-title">Legenda</p>
          <div class="legend-items">
            <div class="legend-item">
              <span class="legend-dot legend-disponivel" />
              <span>Disponível</span>
            </div>
            <div class="legend-item">
              <span class="legend-dot legend-ocupado" />
              <span>Ocupado</span>
            </div>
            <div class="legend-item">
              <span class="legend-dot legend-reservado" />
              <span>Reservado</span>
            </div>
          </div>
        </div>

        <button
        class="reserve-card"
        type="button"
        @click="showReservaModal = true"
        >
        <span class="reserve-plus">+</span>
        <span class="reserve-text">Reservar sala de reunião</span>
        </button>


      </div>

      <div class="planta-card">
        <div class="planta-header">
          <p class="planta-title">Espaço Coworking</p>

          <select
            v-model.number="selectedPlantaId"
            class="planta-select"
          >
            <option
              v-for="planta in plantas"
              :key="planta.id"
              :value="planta.id"
            >
              {{ planta.nome }}
            </option>
          </select>
        </div>

        <div class="planta-wrapper">
          <img
            :src="selectedPlantaImg"
            alt="Planta do coworking"
            class="planta-img"
          />

          <button
            v-for="seat in seats"
            :key="seat.id"
            type="button"
            class="seat-dot"
            :class="[
              seat.status === 'disponivel' ? 'seat-disponivel' : '',
              seat.status === 'ocupado' ? 'seat-ocupado' : '',
              seat.status === 'reservado' ? 'seat-reservado' : '',
            ]"
            :style="{ left: seat.x + '%', top: seat.y + '%'}"
            @click.stop="handleSeatClick(seat.id)"
          />
        </div>

        <p class="seat-info" v-if="selectedSeat">
          Assento {{ selectedSeat.id }} – Status:
          <strong>{{ labelFromStatus(selectedSeat.status) }}</strong>
          (em breve, aqui você pode abrir um modal de detalhes)
        </p>
        <p class="seat-info muted" v-else>
          Clique em um ponto da planta para ver os detalhes do assento.
        </p>
      </div>
    </div>
    <ModalSalaReuniao
    :open="showReservaModal"
    @close="showReservaModal = false"
    @save="handleSalvarReserva"
    />

    <ModalCadeira
    :open="showCadeiraModal"
    :seat="selectedSeat"
    @close="showCadeiraModal = false"
    @reserve="handleReservaCadeira"
    />


  </div>
</template>

<style scoped>
.coworking-bg {
  background: linear-gradient(
    to bottom right,
    #00107b,
    #320d73,
    #746388
  );
  padding-bottom: 3rem;
}

.wrapper {
  max-width: 1100px;
  margin: 0 auto;
  padding: 2.5rem 1rem 0;
}

.top-row {
  display: flex;
  justify-content: space-between;
  gap: 1.5rem;
  align-items: flex-start;
  margin-bottom: 1.75rem;
}

.legend-card {
  background: #ffffff;
  border-radius: 16px;
  padding: 0.9rem 1.1rem;
  box-shadow: 0 12px 30px rgba(0, 0, 0, 0.25);
  min-width: 240px;
}

.legend-title {
  font-size: 0.9rem;
  font-weight: 700;
  margin-bottom: 0.4rem;
}

.legend-items {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem 1rem;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 0.35rem;
  font-size: 0.8rem;
  color: #374151;
}

.legend-dot {
  width: 10px;
  height: 10px;
  border-radius: 999px;
  border: 2px solid #ffffff;
  box-shadow: 0 0 0 2px rgba(148, 163, 184, 0.5);
}

.legend-disponivel {
  background: #22c55e;
  box-shadow: 0 0 0 2px rgba(34, 197, 94, 0.4);
}
.legend-ocupado {
  background: #ef4444;
  box-shadow: 0 0 0 2px rgba(248, 113, 113, 0.5);
}
.legend-reservado {
  background: #eab308;
  box-shadow: 0 0 0 2px rgba(234, 179, 8, 0.5);
}
.legend-favorito {
  background: #3b82f6;
  box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.5);
}

.reserve-card {
  border: none;
  background: linear-gradient(135deg, #8b5cf6, #ec4899);
  color: #ffffff;
  border-radius: 18px;
  padding: 0.9rem 1.8rem;
  display: inline-flex;
  align-items: center;
  gap: 0.6rem;
  box-shadow: 0 18px 40px rgba(0, 0, 0, 0.45);
  cursor: pointer;
  font-weight: 600;
  font-size: 0.98rem;
  transition: transform 0.1s ease, box-shadow 0.12s ease, opacity 0.12s ease;
}

.reserve-card:hover {
  transform: translateY(-2px);
  opacity: 0.96;
  box-shadow: 0 22px 48px rgba(0, 0, 0, 0.6);
}

.reserve-plus {
  font-size: 1.4rem;
  font-weight: 700;
}

.reserve-text {
  white-space: nowrap;
}

.planta-card {
  background: #f9fafb;
  border-radius: 18px;
  padding: 1.5rem 1.7rem 1.8rem;
  box-shadow: 0 18px 40px rgba(0, 0, 0, 0.35);
}

.planta-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
}

.planta-title {
  font-weight: 600;
  font-size: 0.95rem;
}

.planta-select {
  min-width: 220px;
  border: 1px solid #d1d5db;
  padding: 0.35rem 0.8rem;
  font-size: 0.9rem;
  background: #ffffff;
}

.planta-wrapper {
  margin-top: 0.8rem;
  border-radius: 18px;
  overflow: hidden;
  position: relative;
  background: #111827;

  width: 100%;
  max-width: 1000px;
  margin-left: auto;
  margin-right: auto;

  /* travamos no quadrado (mesma ideia do 1400x1400) */
  aspect-ratio: 1 / 1;
}

.planta-img {
  width: 100%;
  height: 100%;
  display: block;
  object-fit: fill; /* preenche exatamente a área do wrapper */
}

.seat-dot {
  position: absolute;
  width: 14px;
  height: 14px;
  border-radius: 999px;
  border: 2px solid #ffffff;
  transform: translate(-50%, -50%);
  cursor: pointer;
}

.seat-disponivel {
  background: #22c55e;
  box-shadow: 0 0 0 2px rgba(34, 197, 94, 0.4);
}

.seat-ocupado {
  background: #ef4444;
  box-shadow: 0 0 0 2px rgba(248, 113, 113, 0.5);
}

.seat-reservado {
  background: #eab308;
  box-shadow: 0 0 0 2px rgba(234, 179, 8, 0.5);
}

.seat-favorito {
  background: #3b82f6;
  box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.5);
}

.seat-info {
  margin-top: 0.75rem;
  font-size: 0.86rem;
  color: #111827;
}

.seat-info.muted {
  color: #6b7280;
}

@media (max-width: 800px) {
  .top-row {
    flex-direction: column;
    align-items: stretch;
  }

  .reserve-card {
    align-self: flex-end;
  }

  .planta-select {
    min-width: 0;
    width: 50%;
  }
}
</style>
