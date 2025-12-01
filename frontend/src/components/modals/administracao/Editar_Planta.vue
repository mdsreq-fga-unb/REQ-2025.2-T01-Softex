<script setup lang="ts">
import { ref, watch, computed } from "vue";
import plantaImgDefault from "@/assets/planta.png";

type SeatPoint = {
  id: number;
  x: number; // em %
  y: number; // em %
};

type SavePayload = {
  nome: string;
  pontos: SeatPoint[];
};

const props = defineProps<{
  open: boolean;
  nomeInicial?: string;
  plantaUrl?: string | null;
  pontosIniciais?: SeatPoint[];
  plantaId?: number; // ID da planta para edição
  imagemArquivo?: File | null; // Arquivo de imagem novo (opcional)
}>();

const emit = defineEmits<{
  (e: "close"): void;
  (
    e: "save",
    payload: SavePayload & { plantaId?: number; imagemArquivo?: File | null }
  ): void;
}>();

const nome = ref<string>(props.nomeInicial ?? "");
const pontos = ref<SeatPoint[]>([]);
const nextId = ref<number>(1);

const plantaWrapper = ref<HTMLElement | null>(null);

const imagemPlanta = computed(() => props.plantaUrl || plantaImgDefault);

watch(
  () => props.open,
  (isOpen) => {
    if (isOpen) {
      nome.value = props.nomeInicial ?? "";

      // Resetar pontos e IDs começando do 1 para esta planta
      if (props.pontosIniciais && props.pontosIniciais.length > 0) {
        pontos.value = props.pontosIniciais.map((p, index) => ({
          id: index + 1, // IDs sempre começam do 1 para cada planta
          x: p.x,
          y: p.y,
        }));
        nextId.value = pontos.value.length + 1;
        console.log(
          `📍 Pontos carregados no editor: ${pontos.value.length} pontos`
        );
        console.log(
          `   IDs resetados: ${pontos.value.map((p) => p.id).join(", ")}`
        );
      } else {
        pontos.value = [];
        nextId.value = 1;
      }
    }
  },
  { immediate: true }
);

const onPlantaClick = (event: MouseEvent) => {
  if (!plantaWrapper.value) return;

  const rect = plantaWrapper.value.getBoundingClientRect();
  const x = ((event.clientX - rect.left) / rect.width) * 100;
  const y = ((event.clientY - rect.top) / rect.height) * 100;

  if (x < 0 || x > 100 || y < 0 || y > 100) return;

  pontos.value.push({
    id: nextId.value++,
    x,
    y,
  });
};

const removerPonto = (id: number) => {
  pontos.value = pontos.value.filter((p) => p.id !== id);
};

const salvar = () => {
  console.log("💾 Editar_Planta: Salvando...");
  console.log("   Nome:", nome.value.trim());
  console.log("   Pontos:", pontos.value.length);
  console.log("   Planta ID:", props.plantaId);

  emit("save", {
    nome: nome.value.trim(),
    pontos: pontos.value.map((p) => ({ ...p })),
    plantaId: props.plantaId,
    imagemArquivo: props.imagemArquivo || null,
  });
};

const cancelar = () => {
  emit("close");
};
</script>

<template>
  <div v-if="open" class="overlay">
    <div class="card">
      <h2 class="titulo">Editar planta</h2>

      <div class="nome-row">
        <label class="nome-label" for="nomePlanta">Nome da planta:</label>
        <input
          id="nomePlanta"
          v-model="nome"
          type="text"
          class="nome-input"
          placeholder="Ex: Escritório 1º andar - Layout A"
        />
      </div>

      <p class="texto-ajuda">
        Clique em qualquer ponto da planta para adicionar um lugar (marcado com
        o ponto verde). Para remover um lugar, clique diretamente sobre o ponto.
      </p>

      <div ref="plantaWrapper" class="planta-container" @click="onPlantaClick">
        <img
          :src="imagemPlanta"
          alt="Planta do escritório"
          class="planta-img"
        />

        <button
          v-for="p in pontos"
          :key="p.id"
          class="seat-dot"
          :style="{ left: p.x + '%', top: p.y + '%' }"
          @click.stop="removerPonto(p.id)"
          type="button"
        >
          <span class="seat-numero">{{ p.id }}</span>
        </button>
      </div>

      <p class="confirm-text">Gostaria de salvar as edições?</p>

      <div class="actions-row">
        <button class="btn btn-sim" type="button" @click="salvar">Sim</button>
        <button class="btn btn-nao" type="button" @click="cancelar">Não</button>
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
  z-index: 1100;
}

.card {
  background: #ffffff;
  border-radius: 18px;
  padding: 1.5rem 2rem 1.75rem;
  box-shadow: 0 18px 40px rgba(0, 0, 0, 0.35);
  max-width: 900px;
  width: 100%;
  max-height: 90vh;
  overflow: auto;
  text-align: center;
}

.titulo {
  font-size: 1.4rem;
  font-weight: 700;
  margin-bottom: 1rem;
}

.nome-row {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 0.75rem;
}

.nome-label {
  font-weight: 600;
  font-size: 0.95rem;
}

.nome-input {
  flex: 1;
  border-radius: 6px;
  border: 1px solid #d1d5db;
  padding: 0.35rem 0.75rem;
  font-size: 0.9rem;
}

.texto-ajuda {
  font-size: 0.85rem;
  color: #4b5563;
  margin-bottom: 0.75rem;
}

.planta-container {
  margin: 0 auto;
  border-radius: 18px;
  overflow: hidden;
  position: relative;
  background: #111827;
  max-width: 800px;
  width: 100%;
  aspect-ratio: 1 / 1;
}

.planta-img {
  width: 100%;
  height: 100%;
  display: block;
  object-fit: contain;
  pointer-events: none;
}

.seat-dot {
  position: absolute;
  width: 32px;
  height: 32px;
  border-radius: 999px;
  background: #22c55e;
  border: 2px solid #ffffff;
  box-shadow: 0 0 0 2px rgba(22, 163, 74, 0.4);
  transform: translate(-50%, -50%);
  cursor: pointer;
  padding: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 0.75rem;
  color: #ffffff;
  transition: transform 0.15s ease;
}

.seat-dot:hover {
  transform: translate(-50%, -50%) scale(1.1);
}

.seat-numero {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
}

.confirm-text {
  margin-top: 1rem;
  font-size: 0.9rem;
}

.actions-row {
  margin-top: 0.75rem;
  display: flex;
  justify-content: center;
  gap: 1rem;
}

.btn {
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

.btn:hover {
  opacity: 0.9;
  transform: translateY(-1px);
}

.btn-sim {
  background: #10b981;
}

.btn-nao {
  background: #ef4444;
}
</style>
