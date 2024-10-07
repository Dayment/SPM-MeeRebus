import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import APItest from '../views/APItest.vue'
import CalendarView from '../views/CalendarView.vue'
import LoginView from '@/views/LoginView.vue'
import TeamSchedule from '@/views/TeamSchedule.vue'
import ManagersDirectors from '../views/ManagersDirectors.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'Login',
      component: LoginView,
    },
    {
      path: '/apitest',
      name: 'apiTest',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/APItest.vue'),
    },
    {
      path: '/calendartest',
      name: 'calendarTest',

      component: () => import('../views/CalendarView.vue'),
    },
    {
      path: '/home',
      name: 'Home',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/HomeView.vue')
    },
    {
      path: '/team',
      name: 'Team',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/TeamSchedule.vue')
    },
    {
      path: '/dept',
      name: 'Dept',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/ManagersDirectors.vue')
    },
    {
      path: '/company',
      name: 'Company',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/CompanySchedule.vue')
    },
    {
      path: '/events',
      name: 'Events',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/Events.vue')
    },
  ]
})

export default router;
