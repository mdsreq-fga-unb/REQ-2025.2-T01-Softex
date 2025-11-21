<script setup lang="ts">
import Header from '@/components/Layout/Header.vue'
import { ref, computed } from 'vue'
import NovoUsuarioModal from '@/components/modals/administracao/NovoUsuarioModal.vue'
import SlackConfigModal from '@/components/modals/administracao/SlackConfigModal.vue'
import NovaPlantaModal from '@/components/modals/administracao/NovaPlantaModal.vue'
import ModalSala from '@/components/modals/administracao/ModalSala.vue'
import EditarUsuario from '@/components/modals/administracao/EditarUsuario.vue' // 👈 novo import

const search = ref('')

type Usuario = {
  id: number
  nome: string
  email: string
  funcao: string
  status: string
}

const usuarios = ref<Usuario[]>([
  { id: 1, nome: 'Ana Claudia', email: 'ana@softex.br', funcao: 'TI', status: 'Ativo' },
  { id: 2, nome: 'Ana Claudia 2', email: 'ana2@softex.br', funcao: 'Marketing', status: 'Ativo' }
])

const filteredUsuarios = computed(() => {
  return usuarios.value.filter(u =>
    u.nome.toLowerCase().includes(search.value.toLowerCase()) ||
    u.email.toLowerCase().includes(search.value.toLowerCase()) ||
    u.funcao.toLowerCase().includes(search.value.toLowerCase())
  )
})

const showNovoUsuarioModal = ref(false)

const funcoes = [
  'TI','Financeiro','Marketing','Jurídico','Administrativo','Projetos'
]

const abrirModalNovoUsuario = () => {
  showNovoUsuarioModal.value = true
}

const handleSalvarUsuario = (novo: Omit<Usuario, 'id' | 'status'>) => {
  const novoId = usuarios.value.length
    ? Math.max(...usuarios.value.map(u => u.id)) + 1
    : 1

  usuarios.value.push({
    id: novoId,
    status: 'Ativo',
    ...novo
  })

  console.log('Usuário salvo:', novo)
}

type SlackConfig = {
  reservaEstacao: string
  alertaDiaReserva: string
  espelhoSala: string
  mensagemSalaCodigo: string
}

const showSlackModal = ref(false)

const slackConfig = ref<SlackConfig>({
  reservaEstacao: '',
  alertaDiaReserva: '',
  espelhoSala: '',
  mensagemSalaCodigo: ''
})

const abrirSlackModal = () => { showSlackModal.value = true }

const handleSalvarSlack = (config: SlackConfig) => {
  slackConfig.value = { ...config }
  console.log('Config Slack salva:', slackConfig.value)
}

const showNovaPlantaModal = ref(false)

const escritorios = ref<string[]>([
  'Escritório 1º andar',
  'Escritório 2º andar',
  'Escritório 3º andar'
])

const abrirNovaPlantaModal = () => {
  showNovaPlantaModal.value = true
}

const handleNovaPlantaSalva = (payload: any) => {
  console.log('Nova planta salva:', payload)
}
const showModalSala = ref(false)

type Sala = { id: number; nome: string }

const salas = ref<Sala[]>([
  { id: 1, nome: 'Sala 1' },
  { id: 2, nome: 'Sala 2' },
  { id: 3, nome: 'Sala 3' }
])

const abrirAdicionarSala = () => {
  showModalSala.value = true
}

const handleSalvarSala = ({ nome }: { nome: string }) => {
  const novoId = salas.value.length
    ? Math.max(...salas.value.map(s => s.id)) + 1
    : 1

  salas.value.push({ id: novoId, nome })
}

const handleExcluirSala = (salaId: number) => {
  salas.value = salas.value.filter(s => s.id !== salaId)
}

const showEditarUsuarioModal = ref(false)
const usuarioSelecionado = ref<Usuario | null>(null)

const abrirEditarUsuario = (usuario: Usuario) => {
  usuarioSelecionado.value = { ...usuario }
  showEditarUsuarioModal.value = true
}

const handleSalvarUsuarioEditado = (atualizado: Usuario) => {
  const idx = usuarios.value.findIndex(u => u.id === atualizado.id)
  if (idx !== -1) {
    usuarios.value[idx] = { ...usuarios.value[idx], ...atualizado }
  }
  showEditarUsuarioModal.value = false
}

const handleExcluirUsuario = (id: number) => {
  usuarios.value = usuarios.value.filter(u => u.id !== id)
  showEditarUsuarioModal.value = false
}
</script>


<template>
  <div class="admin-bg min-h-screen">
    <Header />

    <div class="max-w-6xl mx-auto pt-10 px-4">
      <h1 class="page-title">Gerenciamento do sistema</h1>
      <p class="page-subtitle">
        Gerencie usuários, permissões, notificações e lugares do sistema
      </p>

      <div class="actions-container">
        <div class="search-wrapper">
          <input
            v-model="search"
            type="text"
            placeholder="Buscar..."
            class="search-input"
          />
          <svg class="search-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
            />
          </svg>
        </div>

        <button class="action-btn bg-permissoes">
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
    />

  </div>
</template>

<style scoped>
.admin-bg {
  min-height: 100vh;
  background: linear-gradient(
    to bottom right,
    #00107b,
    #320d73,
    #746388
  );
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
  margin-top: 1.5rem;
  background: white;
  padding: 1rem;
  border-radius: 16px;
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 0.75rem;
  box-shadow: 0 4px 10px rgba(0,0,0,0.08);
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
  box-shadow: 0 0 0 2px rgba(59,130,246,0.4);
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
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

@media (max-width: 500px) {
  .action-btn {
    flex: 1 1 100%;
  }
}

.action-btn:hover {
  opacity: 0.85;
}

.bg-permissoes { background-color: #6100df; }
.bg-slack      { background-color: #f051d6; }
.bg-plantas    { background-color: #ca51f0; }
.bg-salas      { background-color: #3551f0; }
.bg-novo       { background-color: #cd5177; }

/* Tabela */

.table-wrapper {
  margin-top: 1.5rem;
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 10px rgba(0,0,0,0.08);
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
