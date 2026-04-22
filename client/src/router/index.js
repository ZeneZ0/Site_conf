import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '../stores/user.js'
import ProcessorList from '../components/ProcessorList.vue'
import VideoCardList from '../components/VideoCardList.vue'
import MotherboardList from '../components/MotherboardList.vue'
import ComputerBuildList from '../components/ComputerBuildList.vue'
import LoginView from '../views/LoginView.vue'

const routes = [
  { path: '/login', name: 'Login', component: LoginView },
  { path: '/processors', name: 'Processors', component: ProcessorList, meta: { requiresAuth: true } },
  { path: '/videocards', name: 'VideoCards', component: VideoCardList, meta: { requiresAuth: true } },
  { path: '/motherboards', name: 'Motherboards', component: MotherboardList, meta: { requiresAuth: true } },
  { path: '/builds', name: 'Builds', component: ComputerBuildList, meta: { requiresAuth: true } },
  { path: '/', redirect: '/builds' }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

router.beforeEach(async (to, from) => {
  const userStore = useUserStore()
  
  if (!userStore.user.is_authenticated && !userStore.user.id) {
    await userStore.fetchUserInfo()
  }
  
  if (to.meta.requiresAuth && !userStore.isAuthenticated) {
    return '/login'
  }
  
  if (to.path === '/login' && userStore.isAuthenticated && !userStore.getOtpRequired) {
    return '/'
  }
})

export default router