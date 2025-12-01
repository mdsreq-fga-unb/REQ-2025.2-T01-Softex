<script setup lang="ts">
import { ref, computed, watch } from "vue";
import { X, MapPin } from "lucide-vue-next";
import plantaImg from "@/assets/planta.png";
import ModalUploadImagem from "@/components/modals/administracao/ModalUploadImagem.vue";
import EditarPlanta from "@/components/modals/administracao/Editar_Planta.vue";
import ConfirmarExclusao from "@/components/modals/ConfirmarExclusao.vue";

// --------- TIPOS ---------
type Planta = {
  id: number;
  nome: string;
  escritorio: string;
};

type NovaPlantaPayload = {
  nome: string;
  escritorio: string;
  arquivo?: File | null;
  previewUrl?: string | null;
};

type SeatPoint = {
  id: number;
  x: number; // em %
  y: number; // em %
};

// --------- PROPS / EMITS ---------
const props = defineProps<{
  open: boolean;
  escritorios: string[];
}>();

const emit = defineEmits<{
  (e: "close"): void;
  (e: "save", payload: NovaPlantaPayload): void;
  (e: "edit-save", payload: {
    plantaId: number;
    nome: string;
    pontos: SeatPoint[];
    imagemArquivo?: File | null;
  }): void;
}>();

// --------- STATE PRINCIPAL ---------
const plantas = ref<Planta[]>([]);
const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

const selectedPlantaId = ref<number | null>(null);

// Preview e pontos da planta selecionada
const previewUrl = ref<string | null>(null);
const pontos = ref<SeatPoint[]>([]);

// --------- MODAIS INTERNOS ---------
const showUploadModal = ref(false);
const showEditarPlanta = ref(false);
const showConfirmExcluir = ref(false);

// --------- CAMPOS DA NOVA PLANTA / UPLOAD ---------
const novoNome = ref("");
const novoEscritorio = ref("");
const arquivo = ref<File | null>(null);

// --------- HELPERS BACKEND ---------
const buildImageUrl = (path?: string | null): string | null => {
  if (!path) return null;
  if (path.startsWith("http://") || path.startsWith("https://")) {
    return path;
  }
  return `${API_URL}${path.startsWith("/") ? "" : "/"}${path}`;
};

// --------- CARREGAR PLANTAS ---------
const carregarPlantas = async () => {
  try {
    console.log("📥 Carregando plantas do backend...");
    const response = await fetch(`${API_URL}/api/plantas/`);
    if (!response.ok) {
      const text = await response.text();
      throw new Error(
        `Erro ao carregar plantas: ${response.status} - ${text}`
      );
    }

    const data = await response.json();
    console.log("✅ Plantas carregadas:", data);

    // Mapear do formato do backend (id_planta) para o formato do frontend (id)
    plantas.value = data.map((p: any) => ({
      id: p.id_planta,
      nome: p.nome,
      escritorio: "Escritório", // placeholder, se precisar vem do backend depois
    }));

    if (plantas.value.length === 0) {
      selectedPlantaId.value = null;
      previewUrl.value = null;
      pontos.value = [];
      return;
    }

    // Se não houver planta selecionada ainda, seleciona a primeira
    if (!selectedPlantaId.value) {
      selectedPlantaId.value = plantas.value[0].id;
    }

    // Carrega dados da planta selecionada
    if (selectedPlantaId.value) {
      await carregarImagemPlanta(selectedPlantaId.value);
      await carregarPontosPlanta(selectedPlantaId.value);
    }
  } catch (error) {
    console.error("❌ Erro ao carregar plantas:", error);
    plantas.value = [];
    selectedPlantaId.value = null;
    previewUrl.value = null;
    pontos.value = [];
  }
};

// --------- CARREGAR IMAGEM DA PLANTA ---------
const carregarImagemPlanta = async (plantaId: number) => {
  try {
    console.log("🖼️ Carregando imagem da planta:", plantaId);
    const response = await fetch(`${API_URL}/api/plantas/${plantaId}/`);
    if (!response.ok) {
      const text = await response.text();
      throw new Error(
        `Erro ao carregar planta ${plantaId}: ${response.status} - ${text}`
      );
    }

    const data = await response.json();

    if (data.mapa_imagem) {
      previewUrl.value = buildImageUrl(data.mapa_imagem);
      console.log("✅ Imagem carregada:", previewUrl.value);
    } else {
      previewUrl.value = null;
      console.log("ℹ️ Planta sem imagem, usando padrão");
    }
  } catch (error) {
    console.error("❌ Erro ao carregar imagem da planta:", error);
    previewUrl.value = null;
  }
};

// --------- CARREGAR PONTOS DA PLANTA ---------
const carregarPontosPlanta = async (plantaId: number) => {
  try {
    console.log(`📍 Carregando pontos da planta ${plantaId}...`);
    const response = await fetch(`${API_URL}/api/plantas/${plantaId}/`);
    if (!response.ok) {
      const text = await response.text();
      throw new Error(
        `Erro ao carregar pontos da planta ${plantaId}: ${response.status} - ${text}`
      );
    }

    const data = await response.json();

    if (data.pontos && Array.isArray(data.pontos)) {
      pontos.value = data.pontos.map((p: any, index: number) => ({
        id: index + 1, // sempre começa em 1
        x: p.x,
        y: p.y,
      }));
      console.log(
        `✅ ${pontos.value.length} pontos carregados para planta ${plantaId}`
      );
      console.log(
        `   IDs dos pontos: ${pontos.value.map((p) => p.id).join(", ")}`
      );
    } else {
      pontos.value = [];
      console.log(`ℹ️ Planta ${plantaId} não tem pontos cadastrados`);
    }
  } catch (error) {
    console.error(`❌ Erro ao carregar pontos da planta ${plantaId}:`, error);
    pontos.value = [];
  }
};

// --------- REAÇÕES ---------
watch(
  () => props.open,
  (isOpen) => {
    if (isOpen) {
      carregarPlantas();
    }
  }
);

watch(selectedPlantaId, async (newId, oldId) => {
  if (newId && newId !== oldId) {
    console.log(`🔄 Planta trocada: ${oldId} → ${newId}`);
    await carregarImagemPlanta(newId);
    await carregarPontosPlanta(newId);
  }
});

const selectedPlanta = computed(
  () => plantas.value.find((p) => p.id === selectedPlantaId.value) ?? null
);

// --------- EXCLUIR PLANTA ---------
const excluirCarregando = ref(false);
const excluirErro = ref<string | null>(null);

const confirmarExcluir = async () => {
  if (!selectedPlanta.value) return;

  const id = selectedPlanta.value.id;
  excluirErro.value = null;
  excluirCarregando.value = true;

  try {
    console.log("🗑️ Chamando DELETE para planta ID:", id);

    const response = await fetch(`${API_URL}/api/plantas/${id}/`, {
      method: "DELETE",
    });

    if (!response.ok) {
      const text = await response.text();
      console.error("❌ Erro ao excluir planta (resposta):", text);
      excluirErro.value =
        "Erro ao excluir planta. Verifique o backend ou tente novamente.";
      return;
    }

    console.log("✅ Planta excluída no backend com sucesso");

    plantas.value = plantas.value.filter((p) => p.id !== id);

    if (plantas.value.length > 0) {
      const novaSelecionada = plantas.value[0];

      if (!novaSelecionada) {
        selectedPlantaId.value = null;
        previewUrl.value = null;
        pontos.value = [];
        showConfirmExcluir.value = false;
        return;
      }

      selectedPlantaId.value = novaSelecionada.id;
      await carregarImagemPlanta(novaSelecionada.id);
      await carregarPontosPlanta(novaSelecionada.id);
    } else {
      selectedPlantaId.value = null;
      previewUrl.value = null;
      pontos.value = [];
    }

    showConfirmExcluir.value = false;
  } catch (error) {
    console.error("❌ Erro de rede ao excluir planta:", error);
    excluirErro.value =
      "Erro de comunicação com o servidor ao excluir a planta.";
  } finally {
    excluirCarregando.value = false;
  }
};

// --------- FECHAR MODAL PRINCIPAL ---------
const fechar = () => {
  emit("close");
};

const handleOverlayClick = (e: MouseEvent) => {
  if (e.target === e.currentTarget) {
    fechar();
  }
};

// --------- ABRIR NOVA PLANTA ---------
const abrirNovaPlanta = () => {
  selectedPlantaId.value = null;
  novoNome.value = "";
  novoEscritorio.value = props.escritorios[0] ?? "";
  arquivo.value = null;
  previewUrl.value = null;

  showUploadModal.value = true;
};

// --------- EDITAR PLANTA (ABRIR MODAL EDITOR) ---------
const abrirEditarPlanta = async () => {
  if (!selectedPlanta.value) {
    console.error("❌ Nenhuma planta selecionada para editar");
    return;
  }

  console.log("✏️ Abrindo edição da planta:", selectedPlanta.value);

  try {
    const response = await fetch(
      `${API_URL}/api/plantas/${selectedPlanta.value.id}/`
    );
    const data = await response.json();

    if (data.pontos) {
      pontos.value = data.pontos.map((p: any, index: number) => ({
        id: index + 1,
        x: p.x,
        y: p.y,
      }));
      console.log("📍 Pontos carregados para edição:", pontos.value);
      console.log(
        `   IDs dos pontos (resetados): ${pontos.value
          .map((p) => p.id)
          .join(", ")}`
      );
    } else {
      pontos.value = [];
    }

    if (data.mapa_imagem) {
      previewUrl.value = buildImageUrl(data.mapa_imagem);
      console.log("🖼️ Imagem atualizada:", previewUrl.value);
    }
  } catch (error) {
    console.error("⚠️ Erro ao carregar detalhes da planta:", error);
  }

  showEditarPlanta.value = true;
};

// --------- SALVAR EDIÇÃO (RECEBE DO Editar_Planta) ---------
const handleSalvarEdicao = (payload: {
  nome: string;
  pontos: SeatPoint[];
  plantaId?: number;
  imagemArquivo?: File | null;
}) => {
  if (!selectedPlanta.value) {
    console.error("❌ Nenhuma planta selecionada!");
    return;
  }

  const plantaId = payload.plantaId || selectedPlanta.value.id;

  if (!plantaId) {
    console.error("❌ ID da planta não encontrado!", {
      payload,
      selectedPlanta: selectedPlanta.value,
    });
    console.error(
      "Erro: ID da planta não encontrado. Por favor, recarregue a página."
    );
    return;
  }

  selectedPlanta.value.nome = payload.nome;
  pontos.value = payload.pontos;
  showEditarPlanta.value = false;

  console.log("📤 NovaPlantaModal: Emitindo edit-save", {
    plantaId,
    nome: payload.nome,
    pontos: payload.pontos.length,
    temImagem: !!payload.imagemArquivo,
  });

  emit("edit-save", {
    plantaId,
    nome: payload.nome,
    pontos: payload.pontos,
    imagemArquivo: payload.imagemArquivo,
  });

  // Recarregar plantas, imagem e pontos após editar
  setTimeout(async () => {
    await carregarPlantas();
    if (plantaId) {
      await carregarImagemPlanta(plantaId);
      await carregarPontosPlanta(plantaId);
    }
  }, 1000);
};

// --------- UPLOAD MODAL (CRIAR NOVA PLANTA) ---------
const handleUploadConfirm = async (data: {
  file: File | null;
  previewUrl: string | null;
  nome: string;
}) => {
  arquivo.value = data.file;
  novoNome.value = data.nome;
  showUploadModal.value = false;

  console.log("📤 HandleUploadConfirm (CRIAÇÃO):", {
    temArquivo: !!data.file,
    plantaSelecionadaId: selectedPlantaId.value,
    nome: data.nome,
  });

  if (!data.file) {
    console.warn("⚠️ Nenhum arquivo enviado, não vou criar planta.");
    return;
  }

  try {
    console.log("🆕 Criando nova planta com imagem...");

    const formData = new FormData();
    formData.append(
      "nome",
      data.nome || `Planta ${plantas.value.length + 1}`
    );
    formData.append("mapa_imagem", data.file);

    const response = await fetch(`${API_URL}/api/plantas/`, {
      method: "POST",
      body: formData,
    });

    console.log("📥 Resposta do POST:", {
      status: response.status,
      statusText: response.statusText,
      contentType: response.headers.get("content-type"),
      ok: response.ok,
    });

    const contentType = response.headers.get("content-type") || "";
    let newPlanta: any;

    if (contentType.includes("application/json")) {
      newPlanta = await response.json();
    } else {
      const text = await response.text();
      console.error("❌ Resposta não é JSON:", text);
      return;
    }

    if (!response.ok) {
      console.error("❌ Erro ao criar planta:", newPlanta);
      return;
    }

    console.log("✅ Nova planta criada!", newPlanta);

    if (newPlanta.mapa_imagem) {
      previewUrl.value = buildImageUrl(newPlanta.mapa_imagem);
    }

    await carregarPlantas();

    if (newPlanta.id_planta) {
      selectedPlantaId.value = newPlanta.id_planta;
      console.log("📌 Selecionando nova planta:", newPlanta.id_planta);
    }
  } catch (error) {
    console.error("❌ Erro ao criar planta:", error);
  }
};
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
              Nesta tela, você poderá visualizar as plantas cadastradas do seu
              escritório. Todas as plantas adicionadas serão disponibilizadas
              automaticamente para os usuários e a numeração dos lugares será
              gerada de forma automática.
            </p>
          </div>

          <div class="info-cards-row">
            <div class="info-card-small">
              <strong>Recomendação:</strong>
              para melhor experiência e evitar erros de carregamento,
              recomenda-se realizar este procedimento em um computador
              (desktop).
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

      <!-- Modal padrão de confirmação de exclusão -->
      <ConfirmarExclusao
        :open="showConfirmExcluir"
        @close="showConfirmExcluir = false"
        @confirm="confirmarExcluir"
      />
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
    :planta-id="selectedPlanta?.id"
    :imagem-arquivo="arquivo"
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
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.3),
    0 10px 10px -5px rgba(0, 0, 0, 0.2);
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
  background: linear-gradient(135deg, #1c2457 0%, #2f2365 100%);
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
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
}
.excluir {
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
}
.adicionar {
  background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%);
}
.salvar {
  background: linear-gradient(135deg, #7c3aed 0%, #6d28d9 100%);
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
  border-color: #7c3aed;
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
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1),
    0 2px 4px -1px rgba(0, 0, 0, 0.06);
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
</style>
