import { createRouter, createWebHistory } from 'vue-router'
import Auth from '@/components/pages/Auth.vue'
import Dashboard from '@/components/pages/Dashboard.vue'
import Administracao from '@/components/pages/Administracao.vue'
import Coworking from '@/components/pages/Coworking.vue'
import Reservas from '@/components/pages/MinhasReservas.vue'
import Salas from '@/components/pages/SalasDeReuniao.vue'
import { useAuth } from '@/composables/useAuth'
import { useErrorLogger } from '@/composables/useErrorLogger'

// const router = createRouter({
//   history: createWebHistory(),
//   routes: [
//     { path: '/', component: Auth },
//     { path: '/login', component: Auth },
//     { path: '/dashboard', component: Dashboard, meta: { requiresAuth: true } },
//     { path: '/administracao', component: Administracao, meta: { requiresAuth: true } },
//     { path: '/cadastro', component: Cadastro },
//     { path: '/coworking', component: Coworking, meta: { requiresAuth: true } },
//     { path: '/reservas', component: Reservas, meta: { requiresAuth: true } },
//     { path: '/salas', component: Salas, meta: { requiresAuth: true } },
//   ]
// })
const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: Auth },
    { path: '/login', component: Auth },
    { path: '/dashboard', component: Dashboard},
    { path: '/administracao', component: Administracao},
    { path: '/coworking', component: Coworking},
    { path: '/reservas', component: Reservas},
    { path: '/salas', component: Salas },
    { 
      path: '/:pathMatch(.*)*', 
      name: 'NotFound',
      component: () => import('@/components/pages/NotFound.vue')
    }
  ]
})

router.beforeEach((to, from, next) => {
  const { isAuthenticated } = useAuth()
  const { logError, logWarning } = useErrorLogger()

  if (to.name === 'NotFound') {
    logError(
      'Página não encontrada',
      { path: to.path, from: from.path, fullPath: to.fullPath },
      'router.beforeEach'
    )
  }

  if (to.meta.requiresAuth && !isAuthenticated.value) {
    logWarning(
      'Tentativa de acesso a página protegida sem autenticação',
      { path: to.path, from: from.path },
      'router.beforeEach'
    )
    next('/login')
  } else {
    next()
  }
})

router.onError((error) => {
  const { logError } = useErrorLogger()
  logError(
    'Erro de navegação',
    { error },
    'router.onError',
    error instanceof Error ? error : new Error(String(error))
  )
})

export default router
