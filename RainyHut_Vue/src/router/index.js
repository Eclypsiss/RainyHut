import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import Admin from '@/components/Admin.vue';
import Dishes from '@/components/Dishes.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue')
    },

    {
    path: '/dishes', // 菜单页面的路由路径
    name: 'Dishes',
    component: Dishes // 加载 Dishes 组件
    },

    {
    path: '/admin', // 管理员页面的路由路径
    name: 'Admin',
    component: Admin // 加载管理员页面的组件
    }
  ]
})

export default router
