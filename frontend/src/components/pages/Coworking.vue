<script setup lang="ts">
import { ref, watch, computed, onMounted } from "vue";
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
import { useErrorLogger } from "@/composables/useErrorLogger";
import plantaImg from "@/assets/planta.png";
import ModalSalaReuniao from "@/components/modals/coworking/ModalSalaReuniao.vue";
import ModalCadeira from "@/components/modals/coworking/ModalCadeira.vue";

const { user, logout } = useAuth();
const { logError, logWarning } = useErrorLogger();
const router = useRouter();
const route = useRoute();

// ⭐ URL da API
const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

// -------------------------------------------------------
// USER INITIALS
// -------------------------------------------------------
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

// -------------------------------------------------------
// LOGOUT
// -------------------------------------------------------
const handleLogout = () => {
  logout();
  router.push("/login");
};

// -------------------------------------------------------
// TIPOS
// -------------------------------------------------------
type SeatStatus = "disponivel" | "ocupado" | "reservado";

type SeatPoint = {
  id: number;
  idCadeira?: number; // ID real da cadeira no banco
  x: number;
  y: number;
  status: SeatStatus;
  usuarioNome?: string;
  reservaInfo?: {
    usuario_nome: string;
    usuario_email?: string;
    data_inicio: string;
    data_fim: string;
    hora_inicio: string;
    hora_fim: string;
    status: string;
  };
};

type PlantaOption = {
  id: number;
  nome: string;
  img: string | null;
};

type ReservaPayload = {
  pessoas: number;
  tipo: "interna" | "externa";
  motivo: string;
  data: string;
  horaInicio: string;
  horaFim: string;
};

// -------------------------------------------------------
// UTIL
// -------------------------------------------------------
const buildImageUrl = (path?: string | null): string | null => {
  if (!path) return null;
  if (path.startsWith("http://") || path.startsWith("https://")) return path;
  return `${API_URL}${path.startsWith("/") ? "" : "/"}${path}`;
};

// -------------------------------------------------------
// ESTADOS
// -------------------------------------------------------
const plantas = ref<PlantaOption[]>([]);
const selectedPlantaId = ref<number | null>(null);

const selectedPlantaImg = computed(() => {
  const p = plantas.value.find((p) => p.id === selectedPlantaId.value);
  return p && p.img ? p.img : plantaImg;
});

const seats = ref<SeatPoint[]>([]);

// -------------------------------------------------------
// CARREGAR PLANTAS
// -------------------------------------------------------
const carregarPlantas = async () => {
  try {
    console.log("📥 Carregando plantas (coworking)...");

    const resp = await fetch(`${API_URL}/api/plantas/`);
    if (!resp.ok) {
      const text = await resp.text();
      throw new Error(`Erro ao carregar plantas: ${resp.status} - ${text}`);
    }

    const data = await resp.json();
    console.log("✅ Plantas recebidas:", data);

    plantas.value = data.map((p: any) => ({
      id: p.id_planta,
      nome: p.nome,
      img: buildImageUrl(p.mapa_imagem) || null,
    }));

    if (plantas.value.length === 0) {
      console.warn("⚠️ Nenhuma planta cadastrada na API.");
      selectedPlantaId.value = null;
      seats.value = [];
      return;
    }

    if (!selectedPlantaId.value) {
      selectedPlantaId.value = plantas.value[0].id;
    }

    if (selectedPlantaId.value) {
      await carregarSeatsDaPlanta(selectedPlantaId.value);
    }
  } catch (e) {
    console.error("❌ Erro ao carregar plantas:", e);
    logError(
      "Erro ao carregar plantas do coworking",
      { error: e },
      "Coworking.carregarPlantas",
      e instanceof Error ? e : new Error(String(e))
    );
  }
};

// -------------------------------------------------------
// CARREGAR SEATS
// -------------------------------------------------------
const carregarSeatsDaPlanta = async (plantaId: number) => {
  try {
    console.log(`📍 Carregando pontos da planta ${plantaId} para coworking...`);

    const resp = await fetch(`${API_URL}/api/plantas/${plantaId}/`);
    if (!resp.ok) {
      const text = await resp.text();
      throw new Error(
        `Erro ao carregar planta ${plantaId}: ${resp.status} - ${text}`
      );
    }

    const data = await resp.json();
    console.log("📄 Detalhes da planta:", data);

    if (data.pontos && Array.isArray(data.pontos)) {
      seats.value = data.pontos.map((p: any, index: number) => ({
        id: p.id || index + 1,
        idCadeira: p.id_cadeira,
        x: p.x,
        y: p.y,
        status: "disponivel",
        usuarioNome: undefined,
      }));
      console.log(
        `✅ ${seats.value.length} assentos gerados para planta ${plantaId}`
      );

      // Carregar reservas existentes para esta planta
      await carregarReservasCadeira();
    } else {
      console.log("ℹ️ Planta sem pontos cadastrados.");
      seats.value = [];
    }
  } catch (e) {
    console.error(`❌ Erro ao carregar pontos da planta ${plantaId}:`, e);
    logError(
      "Erro ao carregar seats da planta",
      { plantaId, error: e },
      "Coworking.carregarSeatsDaPlanta",
      e instanceof Error ? e : new Error(String(e))
    );
    seats.value = [];
  }

  selectedSeat.value = null;
};

// -------------------------------------------------------
// MONTAGEM
// -------------------------------------------------------
onMounted(() => {
  carregarPlantas();
});

watch(selectedPlantaId, async (novoId, antigoId) => {
  if (novoId && novoId !== antigoId) {
    console.log(`🔄 Mudando para planta ${novoId}`);
    await carregarSeatsDaPlanta(novoId);
  }
});

// -------------------------------------------------------
// FUNÇÕES DE USUÁRIO
// -------------------------------------------------------
const getNomeUsuarioLogado = (): string => {
  let currentUser = user.value;

  if (!currentUser) {
    try {
      const storedUser =
        localStorage.getItem("user") ||
        localStorage.getItem("auth_user") ||
        localStorage.getItem("currentUser");

      if (storedUser) {
        currentUser = JSON.parse(storedUser);
      }
    } catch (e) {
      logError(
        "Erro ao carregar usuário do localStorage",
        { error: e },
        "Coworking.getNomeUsuarioLogado",
        e instanceof Error ? e : new Error(String(e))
      );
    }
  }

  if (!currentUser) {
    logWarning(
      "Usuário não encontrado ao obter nome",
      { localStorageKeys: Object.keys(localStorage) },
      "Coworking.getNomeUsuarioLogado"
    );
    return "";
  }

  const firstName = currentUser.first_name || "";
  const lastName = currentUser.last_name || "";
  const username = currentUser.username || "";

  if (firstName && lastName) return `${firstName} ${lastName}`;
  if (firstName) return firstName;
  if (lastName) return lastName;
  if (username) return username;

  return "";
};

const getIniciaisUsuario = (nome?: string): string => {
  if (!nome) return "";

  const partes = nome
    .trim()
    .split(" ")
    .filter((p) => p.length > 0);

  if (partes.length >= 2) {
    const primeira = partes[0];
    const ultima = partes[partes.length - 1];
    return `${primeira[0]}${ultima[0]}`.toUpperCase();
  }

  if (partes.length === 1) {
    return partes[0][0]?.toUpperCase() || "";
  }

  return "";
};

const deveMostrarIniciais = (seat: SeatPoint): boolean => {
  const mostrar =
    (seat.status === "ocupado" || seat.status === "reservado") &&
    !!seat.usuarioNome;

  if (!mostrar && (seat.status === "ocupado" || seat.status === "reservado")) {
    console.log("Seat sem usuarioNome:", seat);
  }

  return mostrar;
};

// -------------------------------------------------------
// INTERAÇÃO COM OS ASSENTOS
// -------------------------------------------------------
const selectedSeat = ref<{ id: number; status: SeatStatus } | null>(null);
const selectedReservaInfo = ref<any | null>(null);
const showReservaModal = ref(false);
const showCadeiraModal = ref(false);

const handleSeatClick = async (id: number) => {
  const seat = seats.value.find((s) => s.id === id);
  if (!seat) return;

  selectedSeat.value = {
    id: seat.id,
    status: seat.status,
  };

  // Se a cadeira estiver reservada, buscar informações da reserva
  if (seat.status === "reservado" && seat.idCadeira) {
    try {
      const resp = await fetch(`${API_URL}/api/reservas/cadeira/`, {
        headers: {
          "Content-Type": "application/json",
        },
        credentials: "include",
      });

      if (resp.ok) {
        const reservas = await resp.json();
        const reserva = reservas.find(
          (r: any) =>
            r.cadeira_id === seat.idCadeira && r.status === "confirmada"
        );

        if (reserva) {
          selectedReservaInfo.value = {
            usuario_nome: reserva.usuario_nome || "Usuário desconhecido",
            usuario_email: reserva.usuario_email,
            data_inicio: reserva.data_inicio,
            data_fim: reserva.data_fim,
            hora_inicio: reserva.hora_inicio,
            hora_fim: reserva.hora_fim,
            status: reserva.status,
          };
        } else {
          // Se não encontrou, usar informações já armazenadas no seat
          selectedReservaInfo.value = seat.reservaInfo || null;
        }
      }
    } catch (e) {
      console.error("❌ Erro ao buscar informações da reserva:", e);
      // Usar informações já armazenadas no seat como fallback
      selectedReservaInfo.value = seat.reservaInfo || null;
    }
  } else {
    selectedReservaInfo.value = null;
  }

  showCadeiraModal.value = true;
  console.log("Assento clicado:", seat);
};

const labelFromStatus = (status: SeatStatus): string => {
  switch (status) {
    case "disponivel":
      return "Disponível";
    case "ocupado":
      return "Ocupado";
    case "reservado":
      return "Reservado";
  }
};

// -------------------------------------------------------
// RESERVA DE SALA
// -------------------------------------------------------
const handleSalvarReserva = (payload: ReservaPayload) => {
  console.log("Reserva de sala salva:", payload);
  showReservaModal.value = false;
};

// -------------------------------------------------------
// CARREGAR RESERVAS DE CADEIRA
// -------------------------------------------------------
const carregarReservasCadeira = async () => {
  try {
    if (!user.value) {
      console.log(
        "⚠️ Usuário não autenticado, não é possível carregar reservas"
      );
      return;
    }

    const url = `${API_URL}/api/reservas/cadeira/`;
    console.log("🔗 Carregando reservas de:", url);

    const resp = await fetch(url, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
      credentials: "include",
    });

    console.log("📡 Resposta do servidor:", resp.status, resp.statusText);

    if (!resp.ok) {
      if (resp.status === 401) {
        console.log("⚠️ Não autenticado para carregar reservas");
        return;
      }
      if (resp.status === 404) {
        console.log(
          "⚠️ Endpoint não encontrado. Verifique se as rotas estão configuradas corretamente."
        );
        return;
      }
      const errorText = await resp.text();
      console.error("❌ Erro na resposta:", errorText);
      throw new Error(
        `Erro ao carregar reservas: ${resp.status} - ${errorText}`
      );
    }

    const reservas = await resp.json();
    console.log("📋 Reservas de cadeira carregadas:", reservas);

    // Atualizar status dos assentos baseado nas reservas
    reservas.forEach((reserva: any) => {
      const seatIndex = seats.value.findIndex(
        (s) => s.idCadeira === reserva.cadeira_id
      );

      if (seatIndex !== -1 && reserva.status === "confirmada") {
        seats.value[seatIndex].status = "reservado";
        seats.value[seatIndex].usuarioNome = reserva.usuario_nome || undefined;
        seats.value[seatIndex].reservaInfo = {
          usuario_nome: reserva.usuario_nome || "Usuário desconhecido",
          usuario_email: reserva.usuario_email,
          data_inicio: reserva.data_inicio,
          data_fim: reserva.data_fim,
          hora_inicio: reserva.hora_inicio,
          hora_fim: reserva.hora_fim,
          status: reserva.status,
        };
      }
    });
  } catch (e) {
    console.error("❌ Erro ao carregar reservas de cadeira:", e);
    logError(
      "Erro ao carregar reservas de cadeira",
      { error: e },
      "Coworking.carregarReservasCadeira",
      e instanceof Error ? e : new Error(String(e))
    );
  }
};

// -------------------------------------------------------
// RESERVA DE CADEIRA
// -------------------------------------------------------
const handleReservaCadeira = async (payload: {
  seatId: number;
  dataInicio: string;
  dataFim: string;
  horaInicio: string;
  horaFim: string;
}) => {
  const seatIndex = seats.value.findIndex((s) => s.id === payload.seatId);

  if (seatIndex === -1) {
    logError(
      "Falha ao reservar cadeira: assento não encontrado",
      { seatId: payload.seatId },
      "Coworking.handleReservaCadeira"
    );
    showCadeiraModal.value = false;
    return;
  }

  const seatAtual = seats.value[seatIndex];

  if (!seatAtual) {
    logError(
      "Falha ao reservar cadeira: assento inválido",
      { seatIndex, seatId: payload.seatId },
      "Coworking.handleReservaCadeira"
    );
    showCadeiraModal.value = false;
    return;
  }

  if (!seatAtual.idCadeira) {
    logError(
      "Falha ao reservar cadeira: idCadeira não encontrado",
      { seat: seatAtual },
      "Coworking.handleReservaCadeira"
    );
    showCadeiraModal.value = false;
    return;
  }

  if (!user.value) {
    logError(
      "Falha ao reservar cadeira: usuário não autenticado",
      { seatId: payload.seatId },
      "Coworking.handleReservaCadeira"
    );
    alert(
      "Você precisa estar autenticado para fazer uma reserva. Por favor, faça login novamente."
    );
    showCadeiraModal.value = false;
    return;
  }

  // Verificar autenticação no backend antes de fazer a reserva
  try {
    const authCheck = await fetch(`${API_URL}/api/auth/check/`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
      credentials: "include",
    });

    if (!authCheck.ok || !(await authCheck.json()).authenticated) {
      alert("Sua sessão expirou. Por favor, faça login novamente.");
      logout();
      router.push("/login");
      showCadeiraModal.value = false;
      return;
    }
  } catch (authError) {
    console.error("❌ Erro ao verificar autenticação:", authError);
    // Continuar mesmo assim, pode ser um problema temporário
  }

  try {
    const url = `${API_URL}/api/reservas/cadeira/`;
    const payloadData = {
      cadeira: seatAtual.idCadeira,
      data_inicio: payload.dataInicio,
      data_fim: payload.dataFim,
      hora_inicio: payload.horaInicio,
      hora_fim: payload.horaFim,
    };

    console.log("🔗 Criando reserva em:", url);
    console.log("📦 Dados da reserva:", payloadData);

    const response = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      credentials: "include",
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

      // Se o erro for de autenticação, redirecionar para login
      if (response.status === 401 || response.status === 403) {
        if (
          errorData.detail?.includes("Authentication credentials") ||
          errorData.detail?.includes("not provided")
        ) {
          alert(
            "Sua sessão expirou ou não foi reconhecida. Por favor, faça login novamente."
          );
          logout();
          router.push("/login");
          showCadeiraModal.value = false;
          return;
        }
      }

      throw new Error(
        errorData.detail ||
          errorData.error ||
          errorData.message ||
          `Erro ao criar reserva: ${response.status} - ${errorText}`
      );
    }

    const reservaCriada = await response.json();
    console.log("✅ Reserva criada com sucesso:", reservaCriada);

    // Atualizar o assento localmente
    const nomeUsuario = getNomeUsuarioLogado();
    seats.value[seatIndex] = {
      ...seatAtual,
      status: "reservado",
      usuarioNome: nomeUsuario || reservaCriada.usuario_nome,
    };

    showCadeiraModal.value = false;
  } catch (e) {
    console.error("❌ Erro ao criar reserva:", e);
    logError(
      "Erro ao criar reserva de cadeira",
      { error: e, payload },
      "Coworking.handleReservaCadeira",
      e instanceof Error ? e : new Error(String(e))
    );
    alert(
      e instanceof Error ? e.message : "Erro ao criar reserva. Tente novamente."
    );
  }
};
</script>

<template>
  <div class="coworking-container min-h-screen">
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
            <span class="user-role">Administrador</span>
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

            <select v-model.number="selectedPlantaId" class="planta-select">
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

            <div
              v-for="seat in seats"
              :key="seat.id"
              class="seat-wrapper"
              :style="{ left: seat.x + '%', top: seat.y + '%' }"
            >
              <button
                type="button"
                class="seat-dot"
                :class="[
                  seat.status === 'disponivel' ? 'seat-disponivel' : '',
                  seat.status === 'ocupado' ? 'seat-ocupado' : '',
                  seat.status === 'reservado' ? 'seat-reservado' : '',
                  deveMostrarIniciais(seat) ? 'seat-com-usuario' : '',
                ]"
                @click.stop="handleSeatClick(seat.id)"
              >
                <span v-if="deveMostrarIniciais(seat)" class="seat-iniciais">
                  {{ getIniciaisUsuario(seat.usuarioNome) }}
                </span>
                <span v-else class="seat-numero">{{ seat.id }}</span>
              </button>
              <div v-if="deveMostrarIniciais(seat)" class="seat-label">
                {{ seat.usuarioNome }}
              </div>
            </div>
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
    </div>
    <ModalSalaReuniao
      :open="showReservaModal"
      @close="showReservaModal = false"
      @save="handleSalvarReserva"
    />

    <ModalCadeira
      :open="showCadeiraModal"
      :seat="selectedSeat"
      :reserva-info="selectedReservaInfo"
      @close="showCadeiraModal = false"
      @reserve="handleReservaCadeira"
    />
  </div>
</template>

<style scoped>
.coworking-container {
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

.top-row {
  grid-column: 1 / -1;
  display: flex;
  justify-content: space-between;
  gap: 1.5rem;
  align-items: flex-start;
  margin-bottom: 0;
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
  grid-column: 2 / 12;
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

  aspect-ratio: 1 / 1;
}

.planta-img {
  width: 100%;
  height: 100%;
  display: block;
  object-fit: fill;
}

.seat-wrapper {
  position: absolute;
  transform: translate(-50%, -50%);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.25rem;
}

.seat-dot {
  position: relative;
  width: 32px;
  height: 32px;
  border-radius: 999px;
  border: 2px solid #ffffff;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0;
  font-weight: 600;
  font-size: 0.75rem;
  color: #ffffff;
  transition: transform 0.15s ease, box-shadow 0.15s ease;
}

.seat-dot:hover {
  transform: scale(1.1);
}

.seat-numero,
.seat-iniciais {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
  font-weight: 700;
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

.seat-com-usuario {
  width: 36px;
  height: 36px;
}

.seat-label {
  background: rgba(0, 0, 0, 0.8);
  color: #ffffff;
  padding: 0.25rem 0.6rem;
  border-radius: 8px;
  font-size: 0.7rem;
  font-weight: 500;
  white-space: nowrap;
  pointer-events: none;
  backdrop-filter: blur(4px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
  margin-top: 0.15rem;
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
