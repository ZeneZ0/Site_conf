<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useUserStore } from '../stores/user.js'

const emit = defineEmits(['filter-change'])
const userStore = useUserStore()

const users = ref([])
const selectedUserId = ref(null)

const fetchUsers = async () => {
  if (userStore.isSuperuser) {
    try {
      const response = await axios.get('/api/user/list_users/')
      users.value = response.data
    } catch (error) {
      console.error('Ошибка получения списка пользователей:', error)
    }
  }
}

const onUserChange = () => {
  emit('filter-change', selectedUserId.value)
}

onMounted(() => {
  fetchUsers()
})
</script>
<template>
  <div v-if="userStore.isSuperuser" class="mb-3">
    <label class="form-label">Фильтр по пользователю:</label>
    <select class="form-select" v-model="selectedUserId" @change="onUserChange">
      <option :value="null">Все пользователи</option>
      <option v-for="user in users" :value="user.id">{{ user.username }}</option>
    </select>
  </div>
</template>

