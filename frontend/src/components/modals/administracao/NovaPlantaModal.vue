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
  (
    e: "edit-save",
    payload: {
      plantaId: number;
      nome: string;
      pontos: SeatPoint[];
      imagemArquivo?: File | null;
    }
  ): void;
}>();

// --------- STATE PRINCIPAL ---------
const plantas = ref<Planta[]>([]);
const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

const selectedPlantaId = ref<number | null>(null);

// Carregar plantas do backend
const carregarPlantas = async () => {
  try {
    console.log("📥 Carregando plantas do backend...");
    const response = await fetch(`${API_URL}/api/plantas/`);
    const data = await response.json();

    console.log("✅ Plantas carregadas:", data);

    // Mapear do formato do backend (id_planta) para o formato do frontend (id)
    plantas.value = data.map((p: any) => ({
      id: p.id_planta, // Backend retorna id_planta, frontend usa id
      nome: p.nome,
      escritorio: "Escritório", // TODO: adicionar escritorio no backend se necessário
    }));

    if (plantas.value.length > 0 && !selectedPlantaId.value) {
      const firstPlanta = plantas.value[0];
      if (firstPlanta) {
        selectedPlantaId.value = firstPlanta.id;
        // Carregar imagem e pontos da primeira planta
        await carregarImagemPlanta(firstPlanta.id);
        await carregarPontosPlanta(firstPlanta.id);
      }
    }
  } catch (error) {
    console.error("❌ Erro ao carregar plantas:", error);
    // Em caso de erro, manter vazio ou usar dados mockados
    plantas.value = [];
  }
};

// Função para carregar a imagem da planta do backend
const carregarImagemPlanta = async (plantaId: number) => {
  try {
    console.log("🖼️ Carregando imagem da planta:", plantaId);
    const response = await fetch(`${API_URL}/api/plantas/${plantaId}/`);
    const data = await response.json();

    if (data.mapa_imagem) {
      // Verificar se já é uma URL completa ou apenas o caminho
      if (
        data.mapa_imagem.startsWith("http://") ||
        data.mapa_imagem.startsWith("https://")
      ) {
        // Já é URL completa
        previewUrl.value = data.mapa_imagem;
      } else {
        // É caminho relativo, adicionar API_URL
        previewUrl.value = `${API_URL}${
          data.mapa_imagem.startsWith("/") ? "" : "/"
        }${data.mapa_imagem}`;
      }
      console.log("✅ Imagem carregada:", previewUrl.value);
    } else {
      // Se não houver imagem, usar padrão
      previewUrl.value = null;
      console.log("ℹ️ Planta sem imagem, usando padrão");
    }
  } catch (error) {
    console.error("❌ Erro ao carregar imagem da planta:", error);
    previewUrl.value = null;
  }
};

// Carregar plantas quando o modal abrir
watch(
  () => props.open,
  (isOpen) => {
    if (isOpen) {
      carregarPlantas();
    }
  }
);

// Carregar imagem e pontos da planta selecionada quando mudar
watch(selectedPlantaId, async (newId, oldId) => {
  if (newId && newId !== oldId) {
    console.log(`🔄 Planta trocada: ${oldId} → ${newId}`);
    await carregarImagemPlanta(newId);
    await carregarPontosPlanta(newId);
  }
});

// Função para carregar pontos da planta do backend
const carregarPontosPlanta = async (plantaId: number) => {
  try {
    console.log(`📍 Carregando pontos da planta ${plantaId}...`);
    const response = await fetch(`${API_URL}/api/plantas/${plantaId}/`);
    const data = await response.json();

    if (data.pontos && Array.isArray(data.pontos)) {
      // Resetar IDs começando do 1 para cada planta
      pontos.value = data.pontos.map((p: any, index: number) => ({
        id: index + 1, // IDs sempre começam do 1 para cada planta
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

const selectedPlanta = computed(
  () => plantas.value.find((p) => p.id === selectedPlantaId.value) ?? null
);

const pontos = ref<SeatPoint[]>([
  { id: 2, x: 40, y: 32 },
  { id: 3, x: 55, y: 35 },
  { id: 4, x: 0, y: 55 },
]);

// --------- MODAIS INTERNOS ---------
const showUploadModal = ref(false);
const showEditarPlanta = ref(false);
const showConfirmExcluir = ref(false);

// --------- CAMPOS DA NOVA PLANTA / UPLOAD ---------
const novoNome = ref("");
const novoEscritorio = ref("");
const arquivo = ref<File | null>(null);
const previewUrl = ref<string | null>(null);

const handleArquivoChange = (event: Event) => {
  const target = event.target as HTMLInputElement;
  const file = target.files?.[0];
  if (!file) {
    arquivo.value = null;
    previewUrl.value = null;
    return;
  }
  arquivo.value = file;
  previewUrl.value = URL.createObjectURL(file);
};

const abrirNovaPlanta = () => {
  novoNome.value = "";
  novoEscritorio.value = props.escritorios[0] ?? "";
  arquivo.value = null;
  previewUrl.value = null;
};

const salvarPlanta = () => {
  const nome = novoNome.value || `Planta ${plantas.value.length + 1}`;
  const escritorio =
    novoEscritorio.value || props.escritorios[0] || "Sem escritório";

  const payload: NovaPlantaPayload = {
    nome,
    escritorio,
    arquivo: arquivo.value,
    previewUrl: previewUrl.value,
  };

  // Não criar ID local - o backend retornará o ID real após salvar
  emit("save", payload);

  // Recarregar plantas após salvar (o handler no componente pai fará o POST)
  // A lista será atualizada quando o modal for reaberto
};

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

    // Remove da lista local
    plantas.value = plantas.value.filter((p) => p.id !== id);

    if (plantas.value.length > 0) {
      const novaSelecionada = plantas.value[0];

      if (!novaSelecionada) {
        // fallback de segurança
        selectedPlantaId.value = null;
        previewUrl.value = null;
        pontos.value = [];
        showConfirmExcluir.value = false;
        return;
      }

      selectedPlantaId.value = novaSelecionada.id;

      // Recarrega imagem e pontos da nova planta
      await carregarImagemPlanta(novaSelecionada.id);
      await carregarPontosPlanta(novaSelecionada.id);
    } else {
      // Não sobrou nenhuma planta
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

// --------- EDITAR PLANTA (ABRIR MODAL EDITOR) ---------
const abrirEditarPlanta = async () => {
  if (!selectedPlanta.value) {
    console.error("❌ Nenhuma planta selecionada para editar");
    return;
  }

  console.log("✏️ Abrindo edição da planta:", selectedPlanta.value);

  // Carregar pontos da planta do backend se houver
  try {
    const response = await fetch(
      `${API_URL}/api/plantas/${selectedPlanta.value.id}/`
    );
    const data = await response.json();

    if (data.pontos) {
      // Resetar IDs começando do 1 para esta planta
      pontos.value = data.pontos.map((p: any, index: number) => ({
        id: index + 1, // IDs sempre começam do 1 para cada planta
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

    // Atualizar URL da imagem se existir
    if (data.mapa_imagem) {
      // Verificar se já é URL completa
      if (
        data.mapa_imagem.startsWith("http://") ||
        data.mapa_imagem.startsWith("https://")
      ) {
        previewUrl.value = data.mapa_imagem;
      } else {
        previewUrl.value = `${API_URL}${
          data.mapa_imagem.startsWith("/") ? "" : "/"
        }${data.mapa_imagem}`;
      }
      console.log("🖼️ Imagem atualizada:", previewUrl.value);
    }
  } catch (error) {
    console.error("⚠️ Erro ao carregar detalhes da planta:", error);
    // Continuar mesmo com erro - pode ser planta nova sem dados ainda
  }

  showEditarPlanta.value = true;
};

// recebe nome + pontos do Editar_Planta
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
    // Recarregar imagem e pontos da planta atualizada
    if (plantaId) {
      await carregarImagemPlanta(plantaId);
      await carregarPontosPlanta(plantaId);
    }
  }, 1000);
};

// --------- UPLOAD MODAL (CONFIRM) ---------

void handleArquivoChange
void abrirNovaPlanta
void salvarPlanta

const handleUploadConfirm = async (data: {
  file: File | null;
  previewUrl: string | null;
  nome: string;
}) => {
  arquivo.value = data.file;
  novoNome.value = data.nome;
  showUploadModal.value = false;

  console.log("📤 HandleUploadConfirm:", {
    temArquivo: !!data.file,
    temPlantaSelecionada: !!selectedPlanta.value,
    plantaId: selectedPlanta.value?.id,
    nome: data.nome,
  });

  // Se houver uma planta selecionada E uma imagem, atualizar a planta no backend
  if (selectedPlanta.value && data.file) {
    try {
      console.log("💾 Atualizando planta com nova imagem...");

      const formData = new FormData();
      formData.append("nome", data.nome || selectedPlanta.value.nome);
      formData.append("mapa_imagem", data.file);

      // Manter pontos existentes
      const responseGet = await fetch(
        `${API_URL}/api/plantas/${selectedPlanta.value.id}/`
      );
      const plantaAtual = await responseGet.json();

      // Enviar pontos apenas se existirem
      if (
        plantaAtual.pontos &&
        Array.isArray(plantaAtual.pontos) &&
        plantaAtual.pontos.length > 0
      ) {
        const pontosLimpos = plantaAtual.pontos.map((p: any) => ({
          x: p.x,
          y: p.y,
        }));
        formData.append("pontos", JSON.stringify(pontosLimpos));
      }
      // Se não houver pontos, não enviar - o serializer usa lista vazia por padrão

      const response = await fetch(
        `${API_URL}/api/plantas/${selectedPlanta.value.id}/`,
        {
          method: "PUT",
          body: formData,
        }
      );

      // Verificar se a resposta é JSON antes de fazer parse
      const contentType = response.headers.get("content-type");
      if (!contentType || !contentType.includes("application/json")) {
        const text = await response.text();
        console.error("❌ Resposta não é JSON:", text.substring(0, 200));
        console.error(
          `Erro ao atualizar planta: O servidor retornou uma resposta inválida (status ${response.status}). Verifique o console para mais detalhes.`
        );
        return;
      }

      const updatedData = await response.json();

      if (!response.ok) {
        console.error("❌ Erro ao atualizar planta:", updatedData);
        console.error(
          "Erro ao salvar imagem: " +
            (updatedData.detail || JSON.stringify(updatedData))
        );
        return;
      }

      console.log("✅ Planta atualizada com sucesso!", updatedData);

      // Atualizar preview com a URL do backend
      if (updatedData.mapa_imagem) {
        // Verificar se já é URL completa
        if (
          updatedData.mapa_imagem.startsWith("http://") ||
          updatedData.mapa_imagem.startsWith("https://")
        ) {
          previewUrl.value = updatedData.mapa_imagem;
        } else {
          previewUrl.value = `${API_URL}${
            updatedData.mapa_imagem.startsWith("/") ? "" : "/"
          }${updatedData.mapa_imagem}`;
        }
        console.log("🖼️ Imagem atualizada:", previewUrl.value);
      }

      // Recarregar plantas para atualizar lista
      await carregarPlantas();

      console.log("✅ Imagem salva com sucesso!");
    } catch (error) {
      console.error("❌ Erro ao salvar imagem:", error);
      console.error(
        "Erro ao salvar imagem: " +
          (error instanceof Error ? error.message : String(error))
      );
    }
  } else if (data.file && data.previewUrl && !selectedPlanta.value) {
    // Se não houver planta selecionada, criar nova planta com a imagem
    try {
      console.log("🆕 Criando nova planta com imagem...");

      const formData = new FormData();
      formData.append(
        "nome",
        data.nome || `Planta ${plantas.value.length + 1}`
      );
      formData.append("mapa_imagem", data.file);
      // Não enviar pontos se for vazio - o backend tratará como lista vazia

      console.log("📤 Enviando POST para criar planta...");

      const response = await fetch(`${API_URL}/api/plantas/`, {
        method: "POST",
        body: formData,
      });

      console.log("📥 Resposta recebida:", {
        status: response.status,
        statusText: response.statusText,
        contentType: response.headers.get("content-type"),
        ok: response.ok,
      });

      // Verificar se a resposta é JSON antes de fazer parse
      const contentType = response.headers.get("content-type") || "";
      let newPlanta;

      if (contentType.includes("application/json")) {
        newPlanta = await response.json();
      } else {
        // Se não for JSON, ler como texto para ver o erro
        const text = await response.text();
        console.error("❌ Resposta não é JSON. Resposta completa:", text);
        console.error(
          `Erro ao criar planta (Status ${response.status}): O servidor retornou uma resposta inválida. Verifique o console e o terminal do Django para mais detalhes.`
        );
        return;
      }

      if (!response.ok) {
        console.error("❌ Erro ao criar planta:", newPlanta);
        console.error(
          "Erro ao criar planta: " +
            (newPlanta.detail || JSON.stringify(newPlanta))
        );
        return;
      }

      console.log("✅ Nova planta criada com sucesso!", newPlanta);

      // Atualizar preview com a URL do backend
      if (newPlanta.mapa_imagem) {
        // Verificar se já é URL completa
        if (
          newPlanta.mapa_imagem.startsWith("http://") ||
          newPlanta.mapa_imagem.startsWith("https://")
        ) {
          previewUrl.value = newPlanta.mapa_imagem;
        } else {
          previewUrl.value = `${API_URL}${
            newPlanta.mapa_imagem.startsWith("/") ? "" : "/"
          }${newPlanta.mapa_imagem}`;
        }
        console.log("🖼️ Imagem da nova planta:", previewUrl.value);
      }

      // Limpar campos
      arquivo.value = null;
      novoNome.value = "";

      // Recarregar plantas para incluir a nova
      await carregarPlantas();

      // Selecionar a planta recém-criada
      if (newPlanta.id_planta) {
        selectedPlantaId.value = newPlanta.id_planta;
        console.log("📌 Selecionando nova planta:", newPlanta.id_planta);

        // Aguardar um pouco para garantir que a planta foi adicionada à lista
        setTimeout(async () => {
          if (selectedPlanta.value) {
            console.log("✅ Nova planta selecionada:", selectedPlanta.value);
            // Recarregar imagem da planta recém-criada
            await carregarImagemPlanta(newPlanta.id_planta);
          } else {
            console.warn(
              "⚠️ Planta não encontrada na lista, tentando recarregar..."
            );
            await carregarPlantas();
            selectedPlantaId.value = newPlanta.id_planta;
          }
        }, 500);
      }

      console.log("✅ Planta criada com sucesso!");
    } catch (error) {
      console.error("❌ Erro ao criar planta:", error);
      console.error(
        "Erro ao criar planta: " +
          (error instanceof Error ? error.message : String(error))
      );
    }
  } else if (selectedPlanta.value && !data.file) {
    // Se não houver arquivo novo, recarregar imagem do backend
    await carregarImagemPlanta(selectedPlanta.value.id);
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
