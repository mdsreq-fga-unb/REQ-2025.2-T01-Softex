import { createRouter, createWebHistory } from 'vue-router'
import Auth from '@/components/pages/Auth.vue'
import Dashboard from '@/components/pages/Dashboard.vue'
import Administracao from '@/components/pages/Administracao.vue'
import Cadastro from '@/components/pages/Cadastro.vue'
import Coworking from '@/components/pages/Coworking.vue'
import Reservas from '@/components/pages/MinhasReservas.vue'
import Salas from '@/components/pages/SalasDeReuniao.vue'

import { useAuth } from '@/composables/useAuth'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: Auth },
    { path: '/login', component: Auth },
    { path: '/dashboard', component: Dashboard, meta: { requiresAuth: true } },
    { path: '/administracao', component: Administracao, meta: { requiresAuth: true } },
    { path: '/cadastro', component: Cadastro },
    { path: '/coworking', component: Coworking, meta: { requiresAuth: true } },
    { path: '/reservas', component: Reservas, meta: { requiresAuth: true } },
    { path: '/salas', component: Salas, meta: { requiresAuth: true } },
  ]
})

router.beforeEach((to, from, next) => {
  const { isAuthenticated } = useAuth()

  if (to.meta.requiresAuth && !isAuthenticated.value) {
    next('/login')
  } else {
    next()
  }
})

export default router
