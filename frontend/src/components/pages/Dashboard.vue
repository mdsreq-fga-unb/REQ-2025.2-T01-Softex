<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { useAuth } from '@/composables/useAuth'
import Header from '@/components/Layout/Header.vue'

const { user, logout } = useAuth()

// Dados das métricas
const metricas = ref({
  posicoesOcupadas: 32,
  totalPosicoes: 58,
  salasEmUso: 4,
  totalSalas: 6,
  reservasHoje: 18,
  reservasAtivas: 30,
  taxaOcupacao: 75
})

// Dados de ocupação por horário
const ocupacaoPorHorario = ref([
  { hora: '8h', porcentagem: 50, cor: 'bg-blue-900' },
  { hora: '10h', porcentagem: 78, cor: 'bg-blue-400' },
  { hora: '12h', porcentagem: 95, cor: 'bg-pink-500' },
  { hora: '14h', porcentagem: 70, cor: 'bg-blue-800' },
  { hora: '16h', porcentagem: 60, cor: 'bg-green-500' },
  { hora: '18h', porcentagem: 40, cor: 'bg-orange-500' },
])

// Distribuição de uso
const distribuicaoUso = ref([
  { tipo: 'Coworking', porcentagem: 50, cor: 'bg-blue-900' },
  { tipo: 'Salas', porcentagem: 30, cor: 'bg-blue-400' },
  { tipo: 'Livre', porcentagem: 20, cor: 'bg-pink-500' },
])

// Atividade recente
const atividadeRecente = ref([
  { nome: 'Maria Santos', acao: 'reservou sala Zeus', horario: '14:30-16:00 hoje', tipo: 'reserva' },
  { nome: 'Pedro Lima', acao: 'ocupou Posição A-15', horario: '13:45 hoje', tipo: 'ocupacao' },
  { nome: 'Sala Apolo', acao: 'liberada', horario: '14:30-16:00 hoje', tipo: 'liberacao' },
])

// Próximas reservas
const proximasReservas = ref([
  { titulo: 'Reunião de Projeto', local: 'Sala Hermes', horario: '15:00-16:30', tempo: 'Em 30 min' },
  { titulo: 'Apresentação Cliente', local: 'Sala Zeus', horario: '16:00-17:00', tempo: 'Em 1h30' },
  { titulo: 'Workshop Técnico', local: 'Sala Apolo', horario: '17:30-19:00', tempo: 'Em 3h' },
])

const porcentagemOcupacao = computed(() => {
  return Math.round((metricas.value.posicoesOcupadas / metricas.value.totalPosicoes) * 100)
})

const handleLogout = () => {
  logout()
  window.location.reload()
}

// Calcular ângulo do donut chart para cada segmento
const calcularAngulo = (porcentagem: number, offset: number = 0) => {
  const angulo = (porcentagem / 100) * 360
  return { angulo, offset }
}
</script>

<template>
  <div class="dashboard-container">
    <Header />


    <!-- Main Content -->
    <main class="main-content">
      <div class="content-header">
        <div>
          <h1 class="page-title">Dashboard</h1>
          <p class="page-subtitle">Visão Geral do co-working da Softex</p>
        </div>
        <Button variant="outline" class="report-btn">
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="mr-2">
            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
            <polyline points="7 10 12 15 17 10"></polyline>
            <line x1="12" y1="15" x2="12" y2="3"></line>
          </svg>
          Gerar Relatórios
        </Button>
      </div>

      <!-- Cards de Métricas -->
      <div class="metrics-grid">
        <!-- Card 1: Posições Ocupadas -->
        <Card class="border-l-4 border-l-blue-400">
          <CardContent class="p-6">
            <div class="flex justify-between items-center">
              <div class="space-y-1">
                <div class="text-sm font-medium text-muted-foreground">Posições Ocupadas</div>
                <div class="text-4xl font-bold text-blue-400">{{ metricas.posicoesOcupadas }}</div>
                <div class="text-sm text-muted-foreground">de {{ metricas.totalPosicoes }} totais</div>
              </div>
              <div class="w-16 h-16 rounded-xl bg-blue-400/10 flex items-center justify-center">
                <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#60a5fa" stroke-width="2">
                  <path d="M8 6h13"></path>
                  <path d="M8 12h13"></path>
                  <path d="M8 18h13"></path>
                  <path d="M3 6h.01"></path>
                  <path d="M3 12h.01"></path>
                  <path d="M3 18h.01"></path>
                </svg>
              </div>
            </div>
          </CardContent>
        </Card>

        <!-- Card 2: Salas em uso -->
        <Card class="border-l-4 border-l-blue-800">
          <CardContent class="p-6">
            <div class="flex justify-between items-center">
              <div class="space-y-1">
                <div class="text-sm font-medium text-muted-foreground">Salas em uso</div>
                <div class="text-4xl font-bold text-blue-800">{{ metricas.salasEmUso }}</div>
                <div class="text-sm text-muted-foreground">de {{ metricas.totalSalas }} Salas disponíveis</div>
              </div>
              <div class="w-16 h-16 rounded-xl bg-blue-800/10 flex items-center justify-center">
                <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#1e40af" stroke-width="2">
                  <rect x="2" y="7" width="20" height="14" rx="2" ry="2"></rect>
                  <path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"></path>
                </svg>
              </div>
            </div>
          </CardContent>
        </Card>

        <!-- Card 3: Reservas hoje -->
        <Card class="border-l-4 border-l-pink-500">
          <CardContent class="p-6">
            <div class="flex justify-between items-center">
              <div class="space-y-1">
                <div class="text-sm font-medium text-muted-foreground">Reservas hoje</div>
                <div class="text-4xl font-bold text-pink-500">{{ metricas.reservasHoje }}</div>
                <div class="text-sm text-muted-foreground">de {{ metricas.reservasAtivas }} reservas ativas</div>
              </div>
              <div class="w-16 h-16 rounded-xl bg-pink-500/10 flex items-center justify-center">
                <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#ec4899" stroke-width="2">
                  <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
                  <line x1="16" y1="2" x2="16" y2="6"></line>
                  <line x1="8" y1="2" x2="8" y2="6"></line>
                  <line x1="3" y1="10" x2="21" y2="10"></line>
                </svg>
              </div>
            </div>
          </CardContent>
        </Card>

        <!-- Card 4: Taxa de Ocupação -->
        <Card class="border-l-4 border-l-gray-500">
          <CardContent class="p-6">
            <div class="flex justify-between items-center">
              <div class="space-y-1">
                <div class="text-sm font-medium text-muted-foreground">Taxa de Ocupação</div>
                <div class="text-4xl font-bold text-gray-700">{{ metricas.taxaOcupacao }}%</div>
                <div class="text-sm text-muted-foreground">média semanal</div>
              </div>
              <div class="w-16 h-16 rounded-xl bg-gray-200 flex items-center justify-center">
                <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#6b7280" stroke-width="2">
                  <line x1="12" y1="2" x2="12" y2="22"></line>
                  <path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path>
                </svg>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      <!-- Charts -->
      <div class="charts-grid">
        <!-- Gráfico de Ocupação por Horário -->
        <Card>
          <CardHeader class="pb-4">
            <CardTitle>Ocupação por Horário</CardTitle>
          </CardHeader>
          <CardContent class="pb-6">
            <div class="bar-chart">
              <div class="bar-chart-y-axis">
                <span>100%</span>
                <span>75%</span>
                <span>50%</span>
                <span>25%</span>
                <span>0%</span>
              </div>
              <div class="bar-chart-content">
                <div 
                  v-for="item in ocupacaoPorHorario" 
                  :key="item.hora"
                  class="bar-wrapper"
                >
                  <div class="bar-container">
                    <div 
                      class="bar"
                      :class="item.cor"
                      :style="{ height: `${item.porcentagem}%` }"
                    >
                      <span v-if="item.porcentagem > 70" class="bar-label">{{ item.porcentagem }}%</span>
                    </div>
                  </div>
                  <span class="bar-hour">{{ item.hora }}</span>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        <!-- Gráfico de Distribuição de Uso -->
        <Card>
          <CardHeader class="pb-4">
            <CardTitle>Distribuição de uso</CardTitle>
          </CardHeader>
          <CardContent class="pb-6">
            <div class="flex gap-8 items-center">
            <div class="donut-chart">
              <svg viewBox="0 0 100 100" class="donut-svg">
                <!-- Coworking (50%) -->
                <circle
                  cx="50"
                  cy="50"
                  r="40"
                  fill="transparent"
                  stroke="#1e3a8a"
                  stroke-width="20"
                  stroke-dasharray="125.6 125.6"
                  stroke-dashoffset="0"
                  transform="rotate(-90 50 50)"
                />
                <!-- Salas (30%) -->
                <circle
                  cx="50"
                  cy="50"
                  r="40"
                  fill="transparent"
                  stroke="#60a5fa"
                  stroke-width="20"
                  stroke-dasharray="75.4 125.6"
                  stroke-dashoffset="-125.6"
                  transform="rotate(-90 50 50)"
                />
                <!-- Livre (20%) -->
                <circle
                  cx="50"
                  cy="50"
                  r="40"
                  fill="transparent"
                  stroke="#ff06eeff"
                  stroke-width="20"
                  stroke-dasharray="50.2 125.6"
                  stroke-dashoffset="-201"
                  transform="rotate(-90 50 50)"
                />
              </svg>
              <div class="donut-center">
                <div class="donut-percentage">{{ metricas.taxaOcupacao }}%</div>
                <div class="donut-label">Ocupação</div>
              </div>
            </div>
            
            <div class="flex flex-col gap-4">
              <div v-for="item in distribuicaoUso" :key="item.tipo" class="flex items-center gap-3">
                <div class="w-4 h-4 rounded" :class="item.cor"></div>
                <span class="text-sm">{{ item.tipo }} ({{ item.porcentagem }}%)</span>
              </div>
            </div>
            </div>
          </CardContent>
        </Card>
      </div>

      <!-- Listas -->
      <div class="lists-grid">
        <!-- Atividade Recente -->
        <Card>
          <CardHeader class="pb-4">
            <CardTitle>Atividade Recente</CardTitle>
          </CardHeader>
          <CardContent class="pb-6">
            <div class="space-y-4">
            <div v-for="(atividade, index) in atividadeRecente" :key="index" class="flex items-start gap-4">
              <div 
                class="w-2 h-2 rounded-full mt-2 flex-shrink-0"
                :class="{
                  'bg-green-500': atividade.tipo === 'reserva',
                  'bg-blue-500': atividade.tipo === 'ocupacao',
                  'bg-yellow-500': atividade.tipo === 'liberacao'
                }"
              ></div>
              <div class="flex-1">
                <div class="text-sm">
                  <span class="font-semibold">{{ atividade.nome }}</span> {{ atividade.acao }}
                </div>
                <div class="text-xs text-muted-foreground">{{ atividade.horario }}</div>
              </div>
            </div>
            </div>
          </CardContent>
        </Card>

        <!-- Próximas Reservas -->
        <Card>
          <CardHeader class="pb-4">
            <CardTitle>Próximas Reservas</CardTitle>
          </CardHeader>
          <CardContent class="pb-6">
            <div class="space-y-4">
              <div v-for="(reserva, index) in proximasReservas" :key="index" class="flex justify-between items-center gap-4">
                <div class="flex-1">
                  <div class="text-sm font-semibold">{{ reserva.titulo }}</div>
                  <div class="text-xs text-muted-foreground">{{ reserva.local }} - {{ reserva.horario }}</div>
                </div>
                <div 
                  class="px-3 py-1 rounded-full text-white text-xs font-medium whitespace-nowrap"
                  :class="{
                    'bg-purple-500': index === 0,
                    'bg-green-500': index === 1,
                    'bg-orange-500': index === 2
                  }"
                >
                  {{ reserva.tempo }}
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </main>

    <!-- Footer -->
    <footer class="footer">
      <span>© 2025 - Softex</span>
      <span>All rights reserved</span>
    </footer>
  </div>
</template>

<style scoped>
.dashboard-container {
  min-height: 100vh;
  background: linear-gradient(to bottom, #00107B 0%, #320D73 54%, #746388 100%);
  display: flex;
  flex-direction: column;
}

/* Header */
.user-section {
  display: flex;
  align-items: center;
  gap: 1rem;
  color: white;
}

.user-name {
  font-weight: 500;
}

.user-role {
  color: rgba(255, 255, 255, 0.7);
  font-size: 0.875rem;
  text-transform: capitalize;
}

.user-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 0.875rem;
}

.logout-btn {
  background: rgba(255, 255, 255, 0.1);
  border: none;
  padding: 0.5rem;
  border-radius: 0.5rem;
  cursor: pointer;
  color: white;
  transition: background 0.2s;
}

.logout-btn:hover {
  background: rgba(255, 255, 255, 0.2);
}

/* Navigation */
.navigation {
  display: flex;
  gap: 2rem;
  padding: 0 2rem;
  overflow-x: auto;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 1rem 0;
  color: rgba(255, 255, 255, 0.7);
  text-decoration: none;
  border-bottom: 2px solid transparent;
  transition: all 0.2s;
  white-space: nowrap;
}

.nav-item:hover {
  color: white;
}

.nav-item.active {
  color: white;
  border-bottom-color: white;
}

/* Main Content */
.main-content {
  flex: 1;
  padding: 2rem;
  max-width: 1400px;
  margin: 0 auto;
  width: 100%;
}

.content-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 2rem;
}

.page-title {
  font-size: 2rem;
  font-weight: 600;
  color: white;
  margin-bottom: 0.5rem;
}

.page-subtitle {
  color: rgba(255, 255, 255, 0.7);
  font-size: 1rem;
}

.report-btn {
  background: white;
  color: #1C2457;
}

/* Metrics Grid */
.metrics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}


/* Charts Grid */
.charts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}


/* Bar Chart */
.bar-chart {
  display: flex;
  gap: 1rem;
  height: 250px;
}

.bar-chart-y-axis {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding-right: 0.5rem;
  font-size: 0.75rem;
  color: hsl(var(--muted-foreground));
}

.bar-chart-content {
  flex: 1;
  display: flex;
  align-items: flex-end;
  gap: 1rem;
  border-bottom: 1px solid hsl(var(--border));
}

.bar-wrapper {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
}

.bar-container {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: flex-end;
  justify-content: center;
}

.bar {
  width: 100%;
  max-width: 60px;
  border-radius: 0.375rem 0.375rem 0 0;
  position: relative;
  display: flex;
  align-items: flex-start;
  justify-content: center;
  padding-top: 0.5rem;
  transition: all 0.3s;
}

.bar:hover {
  opacity: 0.8;
  transform: translateY(-2px);
}

.bar-label {
  color: white;
  font-size: 0.75rem;
  font-weight: 600;
}

.bar-hour {
  font-size: 0.875rem;
  color: hsl(var(--muted-foreground));
  padding-top: 0.5rem;
}

/* Donut Chart */
.donut-chart {
  position: relative;
  width: 200px;
  height: 200px;
  flex-shrink: 0;
}

.donut-svg {
  width: 100%;
  height: 100%;
}

.donut-center {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  text-align: center;
}

.donut-percentage {
  font-size: 2rem;
  font-weight: 700;
  color: hsl(var(--foreground));
}

.donut-label {
  font-size: 0.875rem;
  color: hsl(var(--muted-foreground));
}

/* Lists Grid */
.lists-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}



/* Footer */
.footer {
  padding: 1.5rem 2rem;
  display: flex;
  justify-content: center;
  gap: 1rem;
  color: rgba(255, 255, 255, 0.7);
  font-size: 0.875rem;
}

/* Responsive */
@media (max-width: 768px) {
  .metrics-grid,
  .charts-grid,
  .lists-grid {
    grid-template-columns: 1fr;
  }
  
  .header-content {
    flex-direction: column;
    gap: 1rem;
  }
  
  .navigation {
    gap: 1rem;
  }
  
  .donut-content {
    flex-direction: column;
  }
}
</style>
