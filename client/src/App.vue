<template>
  <div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center">
      <h1>Компьютерный конфигуратор</h1>
      <div>
        <span v-if="userStore.isAuthenticated" class="me-3">Привет, {{ userStore.username }}!</span>
        <span v-else class="me-3 text-muted">Вы не авторизованы</span>
        <button v-if="userStore.isAuthenticated" class="btn btn-outline-danger" @click="handleLogout">Выход</button>
        <a href="/admin" class="btn btn-outline-primary ms-2" target="_blank">Вход в админку</a>
      </div>
    </div>
    <nav class="nav nav-tabs mt-3 mb-4">
      <router-link class="nav-link" to="/builds">Сборки</router-link>
      <router-link class="nav-link" to="/processors">Процессоры</router-link>
      <router-link class="nav-link" to="/videocards">Видеокарты</router-link>
      <router-link class="nav-link" to="/motherboards">Материнские платы</router-link>
    </nav>
    <router-view />
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useUserStore } from './stores/user.js'

const router = useRouter()
const userStore = useUserStore()

const handleLogout = async () => {
  await userStore.logout()
  router.push('/login')
}
</script>