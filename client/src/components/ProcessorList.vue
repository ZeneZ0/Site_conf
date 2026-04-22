<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import UserFilter from './UserFilter.vue'

const items = ref([])
const stats = ref({})
const newItem = ref({ name: '', cores: null, frequency: null, picture: null })
const editItem = ref({})
const fileInput = ref(null)
const editFileInput = ref(null)
const modalImageUrl = ref('')
const currentUserId = ref(null)

const filters = ref({
  name: '',
  cores: '',
  frequency: ''
})

const filteredItems = computed(() => {
  let result = items.value
  
  if (filters.value.name) {
    result = result.filter(item => 
      item.name.toLowerCase().includes(filters.value.name.toLowerCase())
    )
  }
  
  if (filters.value.cores) {
    result = result.filter(item => 
      item.cores === parseInt(filters.value.cores)
    )
  }
  
  if (filters.value.frequency) {
    result = result.filter(item => 
      item.frequency === parseFloat(filters.value.frequency)
    )
  }
  
  return result
})

const applyFilters = () => {}

const clearFilters = () => {
  filters.value = { name: '', cores: '', frequency: '' }
}

const fetchItems = async () => {
  let url = '/api/processors/'
  if (currentUserId.value) {
    url += `?user_id=${currentUserId.value}`
  }
  const response = await axios.get(url)
  items.value = response.data
}

const fetchStats = async () => {
  let url = '/api/processors/stats/'
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
  await axios.post('/api/processors/', newItem.value)
  newItem.value = { name: '', cores: null, frequency: null, picture: null }
  if (fileInput.value) fileInput.value.value = ''
  await fetchItems()
  await fetchStats()
}

const onEditClick = (item) => {
  editItem.value = { ...item }
}

const onUpdate = async () => {
  await axios.put(`/api/processors/${editItem.value.id}/`, editItem.value)
  await fetchItems()
  await fetchStats()
}

const onDelete = async (id) => {
  if (confirm('Удалить?')) {
    await axios.delete(`/api/processors/${id}/`)
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
  let url = '/api/processors/export-excel/'
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
  <div class="card">
    <div class="card-header">
      <h3>Процессоры</h3>
    </div>
    <div class="card-body">
      <UserFilter model="processors" @filter-change="onFilterChange" />

      <div class="row mt-3 mb-4">
        <div class="col-md-3">
          <div class="card text-bg-info">
            <div class="card-body">
              <h5 class="card-title">Всего</h5>
              <p class="card-text display-6">{{ stats.count || 0 }}</p>
            </div>
          </div>
        </div>
        <div class="col-md-3">
          <div class="card text-bg-success">
            <div class="card-body">
              <h5 class="card-title">Ср. ядра</h5>
              <p class="card-text display-6">{{ stats.avg_cores?.toFixed(1) || 0 }}</p>
            </div>
          </div>
        </div>
        <div class="col-md-3">
          <div class="card text-bg-warning">
            <div class="card-body">
              <h5 class="card-title">Макс. частота</h5>
              <p class="card-text display-6">{{ stats.max_frequency || 0 }} ГГц</p>
            </div>
          </div>
        </div>
        <div class="col-md-3">
          <div class="card text-bg-danger">
            <div class="card-body">
              <h5 class="card-title">Мин. частота</h5>
              <p class="card-text display-6">{{ stats.min_frequency || 0 }} ГГц</p>
            </div>
          </div>
        </div>
      </div>

      <div class="row mb-3">
        <div class="col">
          <input type="text" class="form-control" v-model="filters.name" placeholder="Фильтр по названию" @input="applyFilters">
        </div>
        <div class="col">
          <input type="number" class="form-control" v-model="filters.cores" placeholder="Фильтр по ядрам" @input="applyFilters">
        </div>
        <div class="col">
          <input type="number" step="0.1" class="form-control" v-model="filters.frequency" placeholder="Фильтр по частоте" @input="applyFilters">
        </div>
        <div class="col-auto">
          <button class="btn btn-secondary" @click="clearFilters">Сбросить</button>
        </div>
        <div class="col-auto">
          <button class="btn btn-success" @click="exportToExcel">Экспорт в Excel</button>
        </div>
      </div>

      <form @submit.prevent="onAdd" class="mb-4">
        <div class="row">
          <div class="col">
            <input type="text" class="form-control" v-model="newItem.name" placeholder="Название" required>
          </div>
          <div class="col">
            <input type="number" class="form-control" v-model="newItem.cores" placeholder="Ядра" required>
          </div>
          <div class="col">
            <input type="number" step="0.1" class="form-control" v-model="newItem.frequency" placeholder="Частота" required>
          </div>
          <div class="col">
            <input type="file" class="form-control" @change="onFileChange" ref="fileInput">
          </div>
          <div class="col-auto">
            <button class="btn btn-primary" type="submit">Добавить</button>
          </div>
        </div>
      </form>

      <table class="table table-striped">
        <thead>
          <tr>
            <th>ID</th>
            <th>Изображение</th>
            <th>Название</th>
            <th>Ядра</th>
            <th>Частота</th>
            <th>Действия</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in filteredItems" :key="item.id">
            <td>{{ item.id }}</td>
            <td>
              <img v-if="item.picture" :src="item.picture" width="50" @click="openModal(item.picture)" style="cursor: pointer">
              <span v-else>Нет фото</span>
            </td>
            <td>{{ item.name }}</td>
            <td>{{ item.cores }}</td>
            <td>{{ item.frequency }}</td>
            <td>
              <button class="btn btn-sm btn-warning me-1" @click="onEditClick(item)" data-bs-toggle="modal" data-bs-target="#editModal">Изменить</button>
              <button class="btn btn-sm btn-danger" @click="onDelete(item.id)">Удалить</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>

  <div class="modal fade" id="editModal" tabindex="-1">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">Редактировать процессор</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
        </div>
        <div class="modal-body">
          <div class="mb-2">
            <input type="text" class="form-control" v-model="editItem.name" placeholder="Название">
          </div>
          <div class="mb-2">
            <input type="number" class="form-control" v-model="editItem.cores" placeholder="Ядра">
          </div>
          <div class="mb-2">
            <input type="number" step="0.1" class="form-control" v-model="editItem.frequency" placeholder="Частота">
          </div>
          <div class="mb-2">
            <input type="file" class="form-control" @change="onEditFileChange" ref="editFileInput">
          </div>
          <img v-if="editItem.picture" :src="editItem.picture" width="100" class="mt-2">
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Отмена</button>
          <button type="button" class="btn btn-primary" @click="onUpdate" data-bs-dismiss="modal">Сохранить</button>
        </div>
      </div>
    </div>
  </div>

  <div class="modal fade" id="imageModal" tabindex="-1">
    <div class="modal-dialog modal-lg">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">Просмотр изображения</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
        </div>
        <div class="modal-body text-center">
          <img :src="modalImageUrl" class="img-fluid">
        </div>
      </div>
    </div>
  </div>
</template>

