<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
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
import { useErrorLogger } from "@/composables/useErrorLogger";
import CadeiraModal from "@/components/modals/reservas/Cadeira.vue";
import SalaReuniaoModal from "@/components/modals/reservas/SalaReuniao.vue";

const { user, logout, authenticatedFetch } = useAuth();
const { formatTipoFuncao } = useFormatTipoFuncao();
const { logError } = useErrorLogger();
const router = useRouter();
const route = useRoute();

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

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

type ReservaStatus = "andamento" | "concluido";
type ResultadoSala = "aprovado" | "pendente" | "negado";
type ResultadoEstacao = "aprovado" | "pendente";

type ReservaBase = {
  id: number;
  titulo: string;
  descricao: string;
  status: ReservaStatus;
  dataInicio: string;
  dataFim: string;
  horaInicio?: string;
  horaFim?: string;
};

type ReservaSala = ReservaBase & {
  tipo: "sala";
  resultado: ResultadoSala; // sala pode ser negada
};

type ReservaEstacao = ReservaBase & {
  tipo: "estacao";
  resultado: ResultadoEstacao; // estação NÃO pode ser negada
};

type Reserva = ReservaSala | ReservaEstacao;

const activeTab = ref<ReservaStatus>("andamento");
const reservas = ref<Reserva[]>([]);
const isLoading = ref(false);

// Função para formatar data de YYYY-MM-DD para DD/MM/YYYY
const formatarData = (data: string | undefined | null): string => {
  if (!data) return "";
  try {
    const dataPart = data.split("T")[0];
    if (!dataPart) return data;
    const [ano, mes, dia] = dataPart.split("-");
    if (!ano || !mes || !dia) return data;
    return `${dia}/${mes}/${ano}`;
  } catch {
    return data || "";
  }
};

// Função para formatar hora de HH:MM:SS para HH:MM
const formatarHora = (hora: string | undefined | null): string => {
  if (!hora) return "";
  return hora.substring(0, 5); // Pega apenas HH:MM
};

// Função para determinar se a reserva está em andamento ou concluída
const determinarStatus = (
  dataFim: string | undefined | null,
  horaFim?: string | undefined | null
): ReservaStatus => {
  if (!dataFim) return "andamento";

  const hoje = new Date();
  hoje.setHours(0, 0, 0, 0);

  try {
    const dataPart = dataFim.split("T")[0];
    if (!dataPart) return "andamento";
    const [ano, mes, dia] = dataPart.split("-");
    if (!ano || !mes || !dia) return "andamento";

    const dataFimDate = new Date(
      parseInt(ano),
      parseInt(mes) - 1,
      parseInt(dia)
    );
    dataFimDate.setHours(0, 0, 0, 0);

    // Se a data de fim já passou, está concluída
    if (dataFimDate < hoje) {
      return "concluido";
    }

    // Se for hoje e tiver hora de fim, verificar se já passou
    if (dataFimDate.getTime() === hoje.getTime() && horaFim) {
      const partes = horaFim.split(":");
      if (
        partes.length >= 2 &&
        partes[0] !== undefined &&
        partes[1] !== undefined
      ) {
        const hora = parseInt(partes[0]);
        const minuto = parseInt(partes[1]);
        if (!isNaN(hora) && !isNaN(minuto)) {
          const agora = new Date();
          const horaFimDate = new Date();
          horaFimDate.setHours(hora, minuto, 0, 0);

          if (agora > horaFimDate) {
            return "concluido";
          }
        }
      }
    }

    return "andamento";
  } catch {
    return "andamento";
  }
};

// Função para mapear status do backend para resultado do frontend
const mapearResultado = (
  status: string,
  tipo: "sala" | "estacao"
): ResultadoSala | ResultadoEstacao => {
  if (status === "confirmada") {
    return "aprovado";
  }
  if (status === "cancelada") {
    return tipo === "sala" ? "negado" : "aprovado"; // Estação não pode ser negada
  }
  return "pendente";
};

// Carregar reservas do backend
const carregarReservas = async () => {
  if (!user.value) {
    console.log("⚠️ Usuário não autenticado, não é possível carregar reservas");
    return;
  }

  isLoading.value = true;
  try {
    // Buscar reservas de salas
    const responseSalas = await authenticatedFetch(`${API_URL}/api/reservas/`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    });

    // Buscar reservas de cadeiras
    const responseCadeiras = await authenticatedFetch(
      `${API_URL}/api/reservas/cadeira/`,
      {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      }
    );

    const reservasSalas: Reserva[] = [];
    const reservasCadeiras: Reserva[] = [];

    if (responseSalas.ok) {
      const salas = await responseSalas.json();
      if (Array.isArray(salas)) {
        reservasSalas.push(
          ...salas.map((r: any) => {
            const dataFim = r.data_fim
              ? typeof r.data_fim === "string"
                ? r.data_fim.split("T")[0]
                : r.data_fim
              : undefined;
            const dataInicio = r.data_inicio
              ? typeof r.data_inicio === "string"
                ? r.data_inicio.split("T")[0]
                : r.data_inicio
              : undefined;

            return {
              id: r.id_reserva || 0,
              titulo: `${r.sala_nome || "Sala"} — ${r.sala_id || ""}`,
              descricao: r.descricao || "Reserva de sala de reunião",
              tipo: "sala" as const,
              status: determinarStatus(dataFim || undefined),
              resultado: mapearResultado(r.status || "confirmada", "sala"),
              dataInicio: formatarData(dataInicio || undefined),
              dataFim: formatarData(dataFim || undefined),
            } as ReservaSala;
          })
        );
      }
    }

    if (responseCadeiras.ok) {
      const cadeiras = await responseCadeiras.json();
      if (Array.isArray(cadeiras)) {
        reservasCadeiras.push(
          ...cadeiras.map((r: any) => {
            const dataFim = r.data_fim || undefined;
            const dataInicio = r.data_inicio || undefined;

            return {
              id: r.id_reserva_cadeira || 0,
              titulo: `Estação ${r.cadeira_id || ""} — Coworking`,
              descricao: "Reserva de estação de trabalho",
              tipo: "estacao" as const,
              status: determinarStatus(
                dataFim || undefined,
                r.hora_fim || undefined
              ),
              resultado: mapearResultado(r.status || "confirmada", "estacao"),
              dataInicio: formatarData(dataInicio || undefined),
              dataFim: formatarData(dataFim || undefined),
              horaInicio: formatarHora(r.hora_inicio),
              horaFim: formatarHora(r.hora_fim),
            } as ReservaEstacao;
          })
        );
      }
    }

    // Combinar e ordenar por data de fim (mais recentes primeiro)
    reservas.value = [...reservasSalas, ...reservasCadeiras].sort((a, b) => {
      try {
        // Ordenar por data de fim (mais recentes primeiro)
        const partesA = a.dataFim.split("/");
        const partesB = b.dataFim.split("/");

        if (partesA.length === 3 && partesB.length === 3) {
          const dataA = new Date(`${partesA[2]}-${partesA[1]}-${partesA[0]}`);
          const dataB = new Date(`${partesB[2]}-${partesB[1]}-${partesB[0]}`);
          return dataB.getTime() - dataA.getTime();
        }
        return 0;
      } catch {
        return 0;
      }
    });

    console.log("✅ Reservas carregadas:", reservas.value.length);
  } catch (e) {
    console.error("❌ Erro ao carregar reservas:", e);
    logError(
      "Erro ao carregar reservas",
      { error: e },
      "MinhasReservas.carregarReservas",
      e instanceof Error ? e : new Error(String(e))
    );
  } finally {
    isLoading.value = false;
  }
};

onMounted(() => {
  carregarReservas();
});

const reservasFiltradas = computed(() =>
  reservas.value.filter((r) => r.status === activeTab.value)
);

const selecionarTab = (tab: ReservaStatus) => {
  activeTab.value = tab;
};

const showCadeiraModal = ref(false);
const showSalaModal = ref(false);

const reservaCadeiraSelecionada = ref<any | null>(null);
const reservaSalaSelecionada = ref<any | null>(null);

const handleClickReserva = (reserva: Reserva) => {
  console.log("Reserva clicada:", reserva);

  if (reserva.tipo === "estacao") {
    reservaCadeiraSelecionada.value = reserva;
    showCadeiraModal.value = true;
  } else {
    reservaSalaSelecionada.value = reserva;
    showSalaModal.value = true;
  }
};

const labelResultado = (
  resultado: ResultadoSala | ResultadoEstacao
): string => {
  if (resultado === "aprovado") return "Aprovada";
  if (resultado === "pendente") return "Pendente";
  return "Negada";
};
</script>

<template>
  <div class="reservas-container min-h-screen">
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
        <div class="tabs-row">
          <button
            type="button"
            class="tab-btn"
            :class="{ 'tab-active': activeTab === 'andamento' }"
            @click="selecionarTab('andamento')"
          >
            Em andamento
          </button>

          <span class="tab-separator">/</span>

          <button
            type="button"
            class="tab-btn"
            :class="{ 'tab-active': activeTab === 'concluido' }"
            @click="selecionarTab('concluido')"
          >
            Concluído
          </button>
        </div>

        <div class="card">
          <h2 class="card-title">Meu histórico</h2>

          <div v-if="isLoading" class="empty-state">
            <p>Carregando reservas...</p>
          </div>

          <div v-else-if="reservasFiltradas.length === 0" class="empty-state">
            <p>
              Você ainda não possui reservas
              <span v-if="activeTab === 'andamento'">em andamento.</span>
              <span v-else>concluídas.</span>
            </p>
            <p class="empty-hint">
              Assim que você fizer uma reserva de sala ou estação, ela aparecerá
              aqui.
            </p>
          </div>

          <div v-else class="lista-reservas">
            <button
              v-for="reserva in reservasFiltradas"
              :key="reserva.id"
              type="button"
              class="reserva-item"
              @click="handleClickReserva(reserva)"
            >
              <div class="reserva-main">
                <p class="reserva-titulo">{{ reserva.titulo }}</p>
                <p class="reserva-desc">{{ reserva.descricao }}</p>
              </div>

              <div class="reserva-meta">
                <span
                  class="badge status"
                  :class="{
                    'status-ok': reserva.resultado === 'aprovado',
                    'status-wait': reserva.resultado === 'pendente',
                    'status-denied': reserva.resultado === 'negado',
                  }"
                >
                  {{ labelResultado(reserva.resultado) }}
                </span>

                <span class="badge tipo">
                  {{ reserva.tipo === "sala" ? "Sala de reunião" : "Estação" }}
                </span>
                <span class="badge periodo">
                  {{ reserva.dataInicio }} — {{ reserva.dataFim }}
                </span>
              </div>
            </button>
          </div>
        </div>
      </div>
    </div>

    <CadeiraModal
      :open="showCadeiraModal"
      :reserva="reservaCadeiraSelecionada"
      @close="showCadeiraModal = false"
    />

    <SalaReuniaoModal
      :open="showSalaModal"
      :reserva="reservaSalaSelecionada"
      @close="showSalaModal = false"
    />
  </div>
</template>

<style scoped>
.reservas-container {
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

.tabs-row {
  grid-column: 1 / -1;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 0;
}

.tab-btn {
  background: transparent;
  border: none;
  color: rgba(255, 255, 255, 0.6);
  font-size: 0.9rem;
  font-weight: 500;
  cursor: pointer;
  padding: 0.2rem 0.4rem;
  transition: color 0.12s ease;
}

.tab-btn:hover {
  color: rgba(255, 255, 255, 0.9);
}

.tab-active {
  color: #ffffff;
  font-weight: 700;
}

.tab-separator {
  color: rgba(255, 255, 255, 0.6);
  font-size: 1.1rem;
}

.card {
  grid-column: 1 / -1;
  background: #ffffff;
  border-radius: 24px;
  padding: 2rem 2.5rem 2.3rem;
  box-shadow: 0 18px 40px rgba(0, 0, 0, 0.35);
}

.card-title {
  text-align: left;
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 1.5rem;
  color: #111827;
}

.empty-state {
  text-align: center;
  padding: 2rem 1rem;
  color: #4b5563;
  font-size: 0.88rem;
}

.empty-hint {
  margin-top: 0.4rem;
  font-size: 0.8rem;
  color: #9ca3af;
}

.lista-reservas {
  display: flex;
  flex-direction: column;
  gap: 0.7rem;
}

.reserva-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
  width: 100%;
  border: none;
  border-radius: 12px;
  background: #f9fafb;
  border: 1px solid #e5e7eb;
  padding: 1rem 1.5rem;
  cursor: pointer;
  text-align: left;
  transition: box-shadow 0.12s ease, transform 0.1s ease, background 0.12s ease,
    border-color 0.12s ease;
}

.reserva-item:hover {
  background: #ffffff;
  border-color: #d1d5db;
  box-shadow: 0 4px 12px rgba(15, 23, 42, 0.12);
  transform: translateY(-1px);
}

.reserva-main {
  display: flex;
  flex-direction: column;
  gap: 0.1rem;
}

.reserva-titulo {
  font-weight: 600;
  font-size: 0.9rem;
  color: #111827;
}

.reserva-desc {
  font-size: 0.8rem;
  color: #6b7280;
}

.reserva-meta {
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.badge {
  border-radius: 6px;
  padding: 0.25rem 0.75rem;
  font-size: 0.75rem;
  font-weight: 500;
  white-space: nowrap;
}

.badge.tipo {
  background: #312e81;
  color: #e5e7eb;
}

.badge.periodo {
  background: #d1d5db;
  color: #111827;
}

.badge.status {
  font-weight: 600;
}

.status-ok {
  background: #dcfce7;
  color: #166534;
}

.status-wait {
  background: #fef9c3;
  color: #854d0e;
}

.status-denied {
  background: #fee2e2;
  color: #b91c1c;
}

@media (max-width: 700px) {
  .card {
    padding: 1.5rem 1.2rem 1.8rem;
  }

  .reserva-item {
    flex-direction: column;
    align-items: flex-start;
  }

  .reserva-meta {
    align-items: flex-start;
  }
}
</style>
