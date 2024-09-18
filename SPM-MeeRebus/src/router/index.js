import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import APItest from '../views/APItest.vue'
import CalendarView from '../views/CalendarView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/apitest',
      name: 'apiTest',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/APItest.vue')
    },
    {
      path: '/calendartest',
      name: 'calendarTest',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/CalendarView.vue')
    }
  ]
})

export default router
