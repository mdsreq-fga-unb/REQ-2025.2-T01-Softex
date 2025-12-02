<script setup lang="ts">
import { ref, computed, onMounted } from "vue"; // 👈 adicionado onMounted
import { useRouter, useRoute } from "vue-router";
import {
  Home,
  LogOut,
  Gauge,
  MapPin,
  Sofa,
  Calendar,
  Settings,
} from "lucide-vue-next";
import { useAuth } from "@/composables/useAuth";
import { useFormatTipoFuncao } from "@/composables/useFormatTipoFuncao";
import NovoUsuarioModal from "@/components/modals/administracao/NovoUsuarioModal.vue";
import SlackConfigModal from "@/components/modals/administracao/SlackConfigModal.vue";
import NovaPlantaModal from "@/components/modals/administracao/NovaPlantaModal.vue";
import ModalSala from "@/components/modals/administracao/ModalSala.vue";
import EditarUsuario from "@/components/modals/administracao/EditarUsuario.vue";
import PermissoesModal from "@/components/modals/administracao/PermissoesModal.vue";

const { user, logout, authenticatedFetch } = useAuth();
const { formatTipoFuncao } = useFormatTipoFuncao();
const router = useRouter();
const route = useRoute();

const userInitials = computed(() => {
  if (!user.value) return "U";
  const firstName = user.value.first_name || "";
  const lastName = user.value.last_name || "";
  if (firstName && lastName) {
    return `${firstName[0]}${lastName[0]}`.toUpperCase();
  }
  if (firstName) {
    return firstName.substring(0, 2).toUpperCase();
  }
  return "U";
});

const handleLogout = () => {
  logout();
  router.push("/login");
};

const search = ref("");

// -------------------------------------------------------
// USUÁRIOS
// -------------------------------------------------------
type AdminUsuario = {
  id: number;
  nome: string;
  email: string;
  funcao: string;
  status: string;
};

const usuarios = ref<AdminUsuario[]>([
  {
    id: 1,
    nome: "Ana Claudia",
    email: "ana@softex.br",
    funcao: "TI",
    status: "Ativo",
  },
  {
    id: 2,
    nome: "Ana Claudia 2",
    email: "ana2@softex.br",
    funcao: "Marketing",
    status: "Ativo",
  },
]);

const filteredUsuarios = computed(() => {
  return usuarios.value.filter(
    (u) =>
      u.nome.toLowerCase().includes(search.value.toLowerCase()) ||
      u.email.toLowerCase().includes(search.value.toLowerCase()) ||
      u.funcao.toLowerCase().includes(search.value.toLowerCase())
  );
});

const showNovoUsuarioModal = ref(false);

const funcoes = [
  "TI",
  "Financeiro",
  "Marketing",
  "Jurídico",
  "Administrativo",
  "Projetos",
];

const abrirModalNovoUsuario = () => {
  showNovoUsuarioModal.value = true;
};

const handleSalvarUsuario = (novo: Omit<AdminUsuario, "id" | "status">) => {
  const novoId = usuarios.value.length
    ? Math.max(...usuarios.value.map((u) => u.id)) + 1
    : 1;

  usuarios.value.push({
    id: novoId,
    status: "Ativo",
    ...novo,
  });

  console.log("Usuário salvo:", novo);
};

// -------------------------------------------------------
// SLACK
// -------------------------------------------------------
type SlackConfig = {
  reservaEstacao: string;
  alertaDiaReserva: string;
  espelhoSala: string;
  mensagemSalaCodigo: string;
};

const showSlackModal = ref(false);

const slackConfig = ref<SlackConfig>({
  reservaEstacao: "",
  alertaDiaReserva: "",
  espelhoSala: "",
  mensagemSalaCodigo: "",
});

const abrirSlackModal = () => {
  showSlackModal.value = true;
};

const handleSalvarSlack = (config: SlackConfig) => {
  slackConfig.value = { ...config };
  console.log("Config Slack salva:", slackConfig.value);
};

// -------------------------------------------------------
// PLANTAS
// -------------------------------------------------------
const showNovaPlantaModal = ref(false);

const abrirNovaPlantaModal = () => {
  showNovaPlantaModal.value = true;
};

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

// se tiver auth com token, usa aqui
const getAuthHeaders = (): Record<string, string> => {
  const token =
    localStorage.getItem("accessToken") ||
    localStorage.getItem("token") ||
    localStorage.getItem("authToken");

  if (token) {
    return { Authorization: `Bearer ${token}` };
  }

  // retorna um objeto vazio, mas ainda do tipo Record<string, string>
  return {};
};

const handleNovaPlantaSalva = async (payload: {
  nome: string;
  escritorio: string;
  arquivo?: File | null;
  previewUrl?: string | null;
}) => {
  console.log("🌱 Salvando nova planta:", payload);

  try {
    const formData = new FormData();
    formData.append("nome", payload.nome);

    if (payload.arquivo) {
      formData.append("mapa_imagem", payload.arquivo);
      console.log("📎 Imagem adicionada:", payload.arquivo.name);
    }

    console.log("📤 Enviando POST para:", `${API_URL}/api/plantas/`);
    const response = await authenticatedFetch(`${API_URL}/api/plantas/`, {
      method: "POST",
      body: formData,
    });

    const data = await response.json();

    if (!response.ok) {
      console.error("❌ Erro ao criar planta:", data);
      console.error(
        "Erro ao criar planta: " + (data.detail || JSON.stringify(data))
      );
      return;
    }

    console.log("✅ Planta criada com sucesso:", data);
    showNovaPlantaModal.value = false;
  } catch (error) {
    console.error("❌ Erro ao salvar planta:", error);
    console.error(
      "Erro ao salvar planta: " +
        (error instanceof Error ? error.message : String(error))
    );
  }
};

const handleEditSave = async (payload: {
  plantaId: number;
  nome: string;
  pontos: Array<{ id?: number; x: number; y: number }>;
  imagemArquivo?: File | null;
}) => {
  console.log("✏️ Administracao: Salvando edição da planta");
  console.log("   Planta ID:", payload.plantaId);
  console.log("   Nome:", payload.nome);
  console.log("   Pontos:", payload.pontos.length);
  console.log("   Tem imagem:", !!payload.imagemArquivo);

  try {
    const formData = new FormData();
    formData.append("nome", payload.nome);

    if (payload.imagemArquivo) {
      formData.append("mapa_imagem", payload.imagemArquivo);
      console.log("📎 Imagem adicionada:", payload.imagemArquivo.name);
    }

    const pontosLimpos = payload.pontos.map((p) => ({
      x: p.x,
      y: p.y,
    }));
    formData.append("pontos", JSON.stringify(pontosLimpos));

    console.log(
      "📤 Enviando PUT para:",
      `${API_URL}/api/plantas/${payload.plantaId}/`
    );
    console.log("📊 Dados enviados:", {
      nome: payload.nome,
      pontos: `${pontosLimpos.length} pontos`,
      temImagem: !!payload.imagemArquivo,
    });

    const response = await authenticatedFetch(
      `${API_URL}/api/plantas/${payload.plantaId}/`,
      {
        method: "PUT",
        body: formData,
      }
    );

    const data = await response.json();

    if (!response.ok) {
      console.error("❌ Erro ao atualizar planta:", data);
      console.error(
        "Erro ao atualizar planta: " + (data.detail || JSON.stringify(data))
      );
      return;
    }

    console.log("✅ Planta atualizada com sucesso!", data);
  } catch (error) {
    console.error("❌ Erro ao atualizar planta:", error);
    console.error(
      "Erro ao atualizar planta: " +
        (error instanceof Error ? error.message : String(error))
    );
  }
};

// -------------------------------------------------------
// SALAS DE REUNIÃO (INTEGRADAS COM BACKEND)
// -------------------------------------------------------
const showModalSala = ref(false);

type Sala = { id: number; nome: string };

const salas = ref<Sala[]>([]);

// 👉 FALTAVA ISSO: função pra carregar salas do back
const carregarSalas = async () => {
  try {
    console.log("📥 Carregando salas de reunião da API...");

    const resp = await fetch(`${API_URL}/api/salas-reuniao/`, {
      headers: {
        "Content-Type": "application/json",
        ...getAuthHeaders(),
      },
    });

    if (!resp.ok) {
      const text = await resp.text();
      throw new Error(`Erro ao carregar salas: ${resp.status} - ${text}`);
    }

    const data = await resp.json();
    console.log("✅ Salas recebidas:", data);

    salas.value = data.map((s: any) => ({
      id: s.id,
      nome: s.nome,
    }));
  } catch (e) {
    console.error("❌ Erro ao carregar salas de reunião:", e);
  }
};

// 👉 E aqui o onMounted chamando ela
onMounted(() => {
  carregarSalas();
});

const abrirAdicionarSala = () => {
  showModalSala.value = true;
};

// 👉 Ajustado para chamar o backend (POST) em vez de só mock
const handleSalvarSala = async ({ nome }: { nome: string }) => {
  try {
    console.log("📨 Criando sala de reunião...", { nome });

    const resp = await fetch(`${API_URL}/api/salas-reuniao/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        ...getAuthHeaders(),
      },
      body: JSON.stringify({ nome }),
    });

    const data = await resp.json();

    if (!resp.ok) {
      console.error("❌ Erro ao criar sala:", data);
      return;
    }

    console.log("✅ Sala criada com sucesso:", data);

    salas.value.push({
      id: data.id,
      nome: data.nome,
    });

    showModalSala.value = false;
  } catch (e) {
    console.error("❌ Erro ao salvar sala:", e);
  }
};

// 👉 Ajustado para DELETE no backend
const handleExcluirSala = async (salaId: number) => {
  try {
    console.log("🗑 Excluindo sala de reunião id=", salaId);

    const resp = await fetch(`${API_URL}/api/salas-reuniao/${salaId}/`, {
      method: "DELETE",
      headers: {
        ...getAuthHeaders(),
      },
    });

    if (!resp.ok && resp.status !== 204) {
      const text = await resp.text();
      throw new Error(`Erro ao excluir sala: ${resp.status} - ${text}`);
    }

    console.log("✅ Sala excluída com sucesso");

    salas.value = salas.value.filter((s) => s.id !== salaId);
  } catch (e) {
    console.error("❌ Erro ao excluir sala:", e);
  }
};

// -------------------------------------------------------
// EDIÇÃO DE USUÁRIO
// -------------------------------------------------------
const showEditarUsuarioModal = ref(false);
const usuarioSelecionado = ref<AdminUsuario | null>(null);

const abrirEditarUsuario = (usuario: AdminUsuario) => {
  usuarioSelecionado.value = { ...usuario };
  showEditarUsuarioModal.value = true;
};

const handleSalvarUsuarioEditado = (atualizado: AdminUsuario) => {
  const idx = usuarios.value.findIndex((u) => u.id === atualizado.id);

  if (idx !== -1) {
    usuarios.value[idx] = { ...usuarios.value[idx], ...atualizado };
  }
  showEditarUsuarioModal.value = false;
};

const handleExcluirUsuario = (id: number) => {
  usuarios.value = usuarios.value.filter((u) => u.id !== id);
  showEditarUsuarioModal.value = false;
};

// -------------------------------------------------------
// PERMISSÕES
// -------------------------------------------------------
type PerfilPermissao = {
  id: number;
  nome: string;
  descricao?: string;
  acessoBasico: boolean;
  dashboards: boolean;
  salasReuniao: boolean;
  administracao: boolean;
};

const showPermissoesModal = ref(false);

const perfisPermissao = ref<PerfilPermissao[]>([
  {
    id: 1,
    nome: "Padrão (colaboradores)",
    descricao: "Acesso ao coworking e Minhas Reservas",
    acessoBasico: true,
    dashboards: false,
    salasReuniao: false,
    administracao: false,
  },
  {
    id: 2,
    nome: "Gestores",
    descricao: "Dashboards e salas de reunião",
    acessoBasico: true,
    dashboards: true,
    salasReuniao: true,
    administracao: false,
  },
  {
    id: 3,
    nome: "Administradores",
    descricao: "Acesso total ao sistema",
    acessoBasico: true,
    dashboards: true,
    salasReuniao: true,
    administracao: true,
  },
]);

const abrirPermissoes = () => {
  showPermissoesModal.value = true;
};

const handleSalvarPermissoes = (novos: PerfilPermissao[]) => {
  perfisPermissao.value = novos;
  console.log("Perfis de permissão atualizados:", novos);
};
</script>

<template>
  <div class="admin-container min-h-screen">
    <!-- Navbar -->
    <nav class="navbar">
      <!-- Top Section - Header -->
      <div class="navbar-header">
        <div class="header-left">
          <div class="logo-container">
            <img
              src="../../assets/LOGO_SOFTEX_VERTICAL_BRANCO_OFFLINE.png"
              alt="Softex"
              class="logo-image"
            />
            <div class="logo-text">
              <div class="brand-top">
                <span class="brand-main">Coworking</span>
              </div>
              <span class="brand-desc">Sistema de gestão de Espaços</span>
            </div>
          </div>
        </div>

        <div class="header-right">
          <router-link to="/dashboard" class="header-icon-link">
            <Home class="header-icon" />
          </router-link>
          <div class="user-info">
            <span class="navbar-user-name">{{
              user ? `${user.first_name} ${user.last_name}` : "Usuário"
            }}</span>
            <span class="user-role">{{
              formatTipoFuncao(user?.tipo_funcao)
            }}</span>
          </div>
          <div class="user-avatar">
            {{ userInitials }}
          </div>
          <button class="logout-button" @click="handleLogout">
            <LogOut class="logout-icon" />
          </button>
        </div>
      </div>

      <!-- Bottom Section - Navigation Links -->
      <div class="navbar-nav">
        <router-link
          to="/dashboard"
          class="nav-link"
          :class="{ active: route.path === '/dashboard' }"
        >
          <Gauge class="nav-icon" />
          <span>Dashboard</span>
        </router-link>
        <router-link
          to="/coworking"
          class="nav-link"
          :class="{ active: route.path === '/coworking' }"
        >
          <MapPin class="nav-icon" />
          <span>Coworking</span>
        </router-link>
        <router-link
          to="/salas"
          class="nav-link"
          :class="{ active: route.path === '/salas' }"
        >
          <Sofa class="nav-icon" />
          <span>Salas de reunião</span>
        </router-link>
        <router-link
          to="/reservas"
          class="nav-link"
          :class="{ active: route.path === '/reservas' }"
        >
          <Calendar class="nav-icon" />
          <span>Minhas Reservas</span>
        </router-link>
        <router-link
          v-if="user?.tipo_funcao === 'Administrativo'"
          to="/administracao"
          class="nav-link"
          :class="{ active: route.path === '/administracao' }"
        >
          <Settings class="nav-icon" />
          <span>Administração</span>
        </router-link>
      </div>
    </nav>

    <div class="dashboard-content">
      <div class="dashboard-grid">
        <div class="dashboard-header">
          <div>
            <h1 class="page-title">Gerenciamento do sistema</h1>
            <p class="page-subtitle">
              Gerencie usuários, permissões, notificações e lugares do sistema
            </p>
          </div>
        </div>

        <div class="actions-container">
          <div class="search-wrapper">
            <input
              v-model="search"
              type="text"
              placeholder="Buscar..."
              class="search-input"
            />
            <svg
              class="search-icon"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
              />
            </svg>
          </div>

          <button class="action-btn bg-permissoes" @click="abrirPermissoes">
            <i class="fa-solid fa-lock"></i> Permissões
          </button>

          <button @click="abrirSlackModal" class="action-btn bg-slack">
            <i class="fa-brands fa-slack"></i> Slack
          </button>

          <button class="action-btn bg-novo" @click="abrirNovaPlantaModal">
            <i class="fa-solid fa-plus"></i>Plantas
          </button>

          <button @click="abrirAdicionarSala" class="action-btn bg-salas">
            <i class="fa-solid fa-chair"></i> Salas
          </button>

          <button @click="abrirModalNovoUsuario" class="action-btn bg-novo">
            <i class="fa-solid fa-plus"></i> Novo usuário
          </button>
        </div>

        <div class="table-wrapper">
          <table class="w-full">
            <thead class="table-head">
              <tr>
                <th class="th">Nome</th>
                <th class="th">Email</th>
                <th class="th">Função</th>
                <th class="th">Status</th>
                <th class="th">Ações</th>
              </tr>
            </thead>

            <tbody>
              <tr v-for="user in filteredUsuarios" :key="user.id" class="tr">
                <td class="td">{{ user.nome }}</td>
                <td class="td td-email">{{ user.email }}</td>
                <td class="td">{{ user.funcao }}</td>
                <td class="td">{{ user.status }}</td>
                <td class="td">
                  <button class="btn-editar" @click="abrirEditarUsuario(user)">
                    Editar
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <NovoUsuarioModal
      :open="showNovoUsuarioModal"
      :funcoes="funcoes"
      @close="showNovoUsuarioModal = false"
      @save="handleSalvarUsuario"
    />

    <SlackConfigModal
      :open="showSlackModal"
      :initial-config="slackConfig"
      @close="showSlackModal = false"
      @save="handleSalvarSlack"
    />

    <NovaPlantaModal
      :open="showNovaPlantaModal"
      :escritorios="escritorios"
      @close="showNovaPlantaModal = false"
      @save="handleNovaPlantaSalva"
      @edit-save="handleEditSave"
    />
    <ModalSala
      :open="showModalSala"
      modo="criar"
      :salas="salas"
      @close="showModalSala = false"
      @save="handleSalvarSala"
      @delete="handleExcluirSala"
    />
    <EditarUsuario
      :open="showEditarUsuarioModal"
      :usuario="usuarioSelecionado"
      :funcoes="funcoes"
      @close="showEditarUsuarioModal = false"
      @save="handleSalvarUsuarioEditado"
      @delete="handleExcluirUsuario"
      @resend-password="(id) => console.log('Reenviar senha para usuário', id)"
    />

    <PermissoesModal
      :open="showPermissoesModal"
      :perfis="perfisPermissao"
      @close="showPermissoesModal = false"
      @save="handleSalvarPermissoes"
    />
  </div>
</template>

<style scoped>
.admin-container {
  min-height: 100vh;
  background: linear-gradient(
    to bottom,
    #1c2457 0%,
    #2f2365 40%,
    #4a2e70 70%,
    #6c5885 100%
  );
  display: flex;
  flex-direction: column;
  width: 100%;
}

.dashboard-content {
  flex: 1;
  padding: 2rem;
  width: 100%;
}

.dashboard-grid {
  max-width: 1600px;
  margin: 0 auto;
  width: 100%;
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  gap: 2rem;
}

.dashboard-header {
  grid-column: 1 / -1;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 0;
  width: 100%;
}

.navbar {
  background: #1c2457;
  width: 100%;
  z-index: 100;
}

.navbar-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 2rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.header-left {
  display: flex;
  align-items: center;
}

.logo-container {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.logo-image {
  height: 48px;
  width: auto;
  object-fit: contain;
}

.logo-text {
  display: flex;
  flex-direction: column;
}

.brand-top {
  display: flex;
  align-items: baseline;
  gap: 0.5rem;
}

.brand-main {
  color: white;
  font-size: 1.25rem;
  font-weight: 600;
}

.brand-desc {
  color: rgba(255, 255, 255, 0.6);
  font-size: 0.875rem;
  font-weight: 400;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.header-icon-link {
  display: flex;
  align-items: center;
  justify-content: center;
  text-decoration: none;
  cursor: pointer;
}

.header-icon {
  width: 24px;
  height: 24px;
  color: white;
  cursor: pointer;
}

.user-info {
  display: flex;
  flex-direction: column;
  text-align: right;
}

.navbar-user-name {
  color: #ffffff;
  font-size: 0.875rem;
  font-weight: 500;
}

.user-role {
  color: rgba(255, 255, 255, 0.6);
  font-size: 0.75rem;
}

.user-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: #7c3aed;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 0.875rem;
}

.logout-button {
  background: none;
  border: none;
  cursor: pointer;
  padding: 0.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  transition: opacity 0.2s;
}

.logout-button:hover {
  opacity: 0.7;
}

.logout-icon {
  width: 20px;
  height: 20px;
}

.navbar-nav {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 2rem;
  padding: 0.75rem 2rem;
  background: rgba(28, 36, 87, 0.8);
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: white;
  text-decoration: none;
  font-size: 0.875rem;
  padding: 0.5rem 0;
  position: relative;
  transition: opacity 0.2s;
}

.nav-link:hover {
  opacity: 0.8;
}

.nav-link.active {
  font-weight: 500;
}

.nav-link.active::after {
  content: "";
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: white;
}

.nav-icon {
  width: 18px;
  height: 18px;
}

.page-title {
  font-size: 1.875rem;
  font-weight: bold;
  color: white;
}

.page-subtitle {
  font-size: 0.875rem;
  color: rgba(255, 255, 255, 0.8);
  margin-top: 0.25rem;
}

.actions-container {
  grid-column: 1 / -1;
  background: white;
  padding: 1rem;
  border-radius: 16px;
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 0.75rem;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.08);
}

.search-wrapper {
  width: 16rem;
  position: relative;
}

.search-input {
  width: 100%;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  padding: 0.5rem 2.5rem;
  outline: none;
}

.search-input:focus {
  border-color: #3b82f6;
  box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.4);
}

.search-icon {
  width: 20px;
  height: 20px;
  position: absolute;
  left: 0.75rem;
  top: 0.55rem;
  color: #9ca3af;
}

.action-btn {
  flex: 1 1 120px;
  padding: 0.7rem 1rem;
  border-radius: 10px;
  font-weight: 500;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  cursor: pointer;
  transition: opacity 0.2s;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

@media (max-width: 500px) {
  .action-btn {
    flex: 1 1 100%;
  }
}

.action-btn:hover {
  opacity: 0.85;
}

.bg-permissoes {
  background-color: #6100df;
}
.bg-slack {
  background-color: #f051d6;
}
.bg-plantas {
  background-color: #ca51f0;
}
.bg-salas {
  background-color: #3551f0;
}
.bg-novo {
  background-color: #cd5177;
}

/* Tabela */

.table-wrapper {
  grid-column: 1 / -1;
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.08);
}

.table-head {
  background: #e5e7eb;
  color: #374151;
  font-size: 0.875rem;
  text-align: left;
}

.th {
  padding: 0.5rem 1rem;
}

.tr {
  border-bottom: 1px solid #e5e7eb;
}

.td {
  padding: 0.75rem 1rem;
}

.td-email {
  color: #2563eb;
  text-decoration: underline;
  cursor: pointer;
}

.btn-editar {
  color: #2563eb;
  cursor: pointer;
}

.btn-editar:hover {
  text-decoration: underline;
}
</style>
