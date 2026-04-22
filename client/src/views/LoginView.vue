<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import UserFilter from './UserFilter.vue'

const items = ref([])
const stats = ref({})
const newItem = ref({ name: '', memory: null, chipset: '', picture: null })
const editItem = ref({})
const fileInput = ref(null)
const editFileInput = ref(null)
const modalImageUrl = ref('')
const currentUserId = ref(null)

const filters = ref({
  name: '',
  memory: '',
  chipset: ''
})

const filteredItems = computed(() => {
  let result = items.value
  
  if (filters.value.name) {
    result = result.filter(item => 
      item.name.toLowerCase().includes(filters.value.name.toLowerCase())
    )
  }
  
  if (filters.value.memory) {
    result = result.filter(item => 
      item.memory === parseInt(filters.value.memory)
    )
  }
  
  if (filters.value.chipset) {
    result = result.filter(item => 
      item.chipset.toLowerCase().includes(filters.value.chipset.toLowerCase())
    )
  }
  
  return result
})

const applyFilters = () => {}

const clearFilters = () => {
  filters.value = { name: '', memory: '', chipset: '' }
}

const fetchItems = async () => {
  let url = '/api/videocards/'
  if (currentUserId.value) {
    url += `?user_id=${currentUserId.value}`
  }
  const response = await axios.get(url)
  items.value = response.data
}

const fetchStats = async () => {
  let url = '/api/videocards/stats/'
  if (currentUserId.value) {
    url += `?user_id=${currentUserId.value}`
  }
  const response = await axios.get(url)
  stats.value = response.data
}

const onFilterChange = (userId) => {
  currentUserId.value = userId
  fetchItems()
  fetchStats()
}

const onFileChange = (event) => {
  const file = event.target.files[0]
  if (file) {
    const reader = new FileReader()
    reader.onload = (e) => {
      newItem.value.picture = e.target.result
    }
    reader.readAsDataURL(file)
  }
}

const onEditFileChange = (event) => {
  const file = event.target.files[0]
  if (file) {
    const reader = new FileReader()
    reader.onload = (e) => {
      editItem.value.picture = e.target.result
    }
    reader.readAsDataURL(file)
  }
}

const onAdd = async () => {
  await axios.post('/api/videocards/', newItem.value)
  newItem.value = { name: '', memory: null, chipset: '', picture: null }
  if (fileInput.value) fileInput.value.value = ''
  await fetchItems()
  await fetchStats()
}

const onEditClick = (item) => {
  editItem.value = { ...item }
}

const onUpdate = async () => {
  await axios.put(`/api/videocards/${editItem.value.id}/`, editItem.value)
  await fetchItems()
  await fetchStats()
}

const onDelete = async (id) => {
  if (confirm('Удалить?')) {
    await axios.delete(`/api/videocards/${id}/`)
    await fetchItems()
    await fetchStats()
  }
}

const openModal = (url) => {
  modalImageUrl.value = url
  const modal = new bootstrap.Modal(document.getElementById('imageModal'))
  modal.show()
}

const exportToExcel = () => {
  let url = '/api/videocards/export-excel/'
  if (currentUserId.value) {
    url += `?user_id=${currentUserId.value}`
  }
  window.open(url, '_blank')
}

onMounted(() => {
  fetchItems()
  fetchStats()
})
</script>
<template>
  <div class="row justify-content-center mt-5">
    <div class="col-md-6">
      <div class="card">
        <div class="card-header">
          <h4 class="mb-0">Авторизация</h4>
        </div>
        <div class="card-body">
          <div v-if="error" class="alert alert-danger">{{ error }}</div>
          
          <form @submit.prevent="handleLogin" v-if="!otpStep">
            <div class="mb-3">
              <label class="form-label">Логин</label>
              <input type="text" class="form-control" v-model="loginForm.username" required>
            </div>
            <div class="mb-3">
              <label class="form-label">Пароль</label>
              <input type="password" class="form-control" v-model="loginForm.password" required>
            </div>
            <button type="submit" class="btn btn-primary w-100" :disabled="loading">
              {{ loading ? 'Вход...' : 'Войти' }}
            </button>
          </form>
          
          <div v-else>
            <div v-if="!otpKey">
              <p>Для входа требуется двухфакторная аутентификация</p>
              <button class="btn btn-primary w-100" @click="generateOtp" :disabled="loading">
                {{ loading ? 'Генерация...' : 'Сгенерировать OTP ключ' }}
              </button>
              <div v-if="generatedKey" class="mt-3">
                <label class="form-label">Ключ для Google Authenticator:</label>
                <code class="d-block p-2 bg-light text-center">{{ generatedKey }}</code>
                <p class="text-muted mt-2 small">Введите этот ключ в приложение Google Authenticator</p>
              </div>
            </div>
            <div v-else>
              <p>Введите код из Google Authenticator</p>
              <div class="mb-3">
                <input type="text" class="form-control" v-model="otpCode" placeholder="6-значный код" maxlength="6">
              </div>
              <button class="btn btn-success w-100" @click="verifyOtp" :disabled="loading">
                {{ loading ? 'Проверка...' : 'Подтвердить' }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

