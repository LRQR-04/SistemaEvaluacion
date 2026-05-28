import { createRouter, createWebHistory } from 'vue-router'
import AuthLayout from '../layouts/LayoutAuth.vue'
import MainLayout from '../layouts/MainLayout.vue'

import Login from '../views/Login.vue'
import Registro from '../views/Register.vue'

import Dashboard from '../views/Dashboard.vue'
import Examenes from '../views/Exams.vue'
import Usuarios from '../views/Users.vue'
import Evaluacion from '../views/Evaluacion.vue'
import ResultadoEvaluacion from '../views/ResultadoEvaluacion.vue'
import Resultados from '../views/Resultados.vue'

const routes = [
  {
    path: '/',
    component: MainLayout,
    children: [
      { path: '', component: Dashboard, meta: { requiresAuth: true } },
      {
        path: 'usuarios',
        component: Usuarios,
        meta: {
          requiresAuth: true,
          roles: ['admin', 'docente'],
        },
      },
      {
        path: 'examenes',
        component: Examenes,
        meta: {
          requiresAuth: true,
          roles: ['admin', 'docente'],
        },
      },
      {
        path: 'evaluacion',
        component: Evaluacion,
        meta: {
          requiresAuth: true,
          roles: ['docente'],
        },
      },
      {
        path: 'resultado-evaluacion',
        name: 'resultado-evaluacion',
        component: ResultadoEvaluacion,
        meta: {
          requiresAuth: true,
          roles: ['docente'],
        },
      },
      {
        path: 'resultados',
        component: Resultados,
        meta: {
          requiresAuth: true,
          roles: ['admin'],
        },
      },
      {
        path: 'mis-resultados',
        component: Resultados,
        meta: {
          requiresAuth: true,
          roles: ['estudiante'],
        },
      },
    ],
  },
  {
    path: '/',
    component: AuthLayout,
    children: [
      { path: 'login', component: Login },
      { path: 'registro', component: Registro },
    ],
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')

  if (!token && to.meta.requiresAuth) {
    return next('/login')
  }

  const user = token ? JSON.parse(atob(token.split('.')[1])) : null

  if (to.meta.roles && !to.meta.roles.includes(user?.rol)) {
    return next('/')
  }

  next()
})

export default router
