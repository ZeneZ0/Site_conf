<template>
  <div class="card">
    <div class="card-header">
      <h3>Материнские платы</h3>
    </div>
    <div class="card-body">
      <UserFilter model="motherboards" @filter-change="onFilterChange" />

      <div class="row mt-3 mb-4">
        <div class="col-md-12">
          <div class="card text-bg-info">
            <div class="card-body">
              <h5 class="card-title">Всего материнских плат</h5>
              <p class="card-text display-6">{{ stats.count || 0 }}</p>
            </div>
          </div>
        </div>
      </div>

      <div class="row mb-3">
        <div class="col">
          <input type="text" class="form-control" v-model="filters.name" placeholder="Фильтр по названию" @input="applyFilters">
        </div>
        <div class="col">
          <input type="text" class="form-control" v-model="filters.socket" placeholder="Фильтр по сокету" @input="applyFilters">
        </div>
        <div class="col">
          <input type="text" class="form-control" v-model="filters.form_factor" placeholder="Фильтр по форм-фактору" @input="applyFilters">
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
            <input type="text" class="form-control" v-model="newItem.socket" placeholder="Сокет" required>
          </div>
          <div class="col">
            <input type="text" class="form-control" v-model="newItem.form_factor" placeholder="Форм-фактор" required>
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
            <th>Название</th>
            <th>Сокет</th>
            <th>Форм-фактор</th>
            <th>Действия</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in filteredItems" :key="item.id">
            <td>{{ item.id }}</td>
            <td>{{ item.name }}</td>
            <td>{{ item.socket }}</td>
            <td>{{ item.form_factor }}</td>
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
          <h5 class="modal-title">Редактировать материнскую плату</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
        </div>
        <div class="modal-body">
          <div class="mb-2">
            <input type="text" class="form-control" v-model="editItem.name" placeholder="Название">
          </div>
          <div class="mb-2">
            <input type="text" class="form-control" v-model="editItem.socket" placeholder="Сокет">
          </div>
          <div class="mb-2">
            <input type="text" class="form-control" v-model="editItem.form_factor" placeholder="Форм-фактор">
          </div>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Отмена</button>
          <button type="button" class="btn btn-primary" @click="onUpdate" data-bs-dismiss="modal">Сохранить</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import UserFilter from './UserFilter.vue'

const items = ref([])
const stats = ref({})
const newItem = ref({ name: '', socket: '', form_factor: '' })
const editItem = ref({})
const currentUserId = ref(null)

const filters = ref({
  name: '',
  socket: '',
  form_factor: ''
})

const filteredItems = computed(() => {
  let result = items.value
  
  if (filters.value.name) {
    result = result.filter(item => 
      item.name.toLowerCase().includes(filters.value.name.toLowerCase())
    )
  }
  
  if (filters.value.socket) {
    result = result.filter(item => 
      item.socket.toLowerCase().includes(filters.value.socket.toLowerCase())
    )
  }
  
  if (filters.value.form_factor) {
    result = result.filter(item => 
      item.form_factor.toLowerCase().includes(filters.value.form_factor.toLowerCase())
    )
  }
  
  return result
})

const applyFilters = () => {}

const clearFilters = () => {
  filters.value = { name: '', socket: '', form_factor: '' }
}

const fetchItems = async () => {
  let url = '/api/motherboards/'
  if (currentUserId.value) {
    url += `?user_id=${currentUserId.value}`
  }
  const response = await axios.get(url)
  items.value = response.data
}

const fetchStats = async () => {
  let url = '/api/motherboards/stats/'
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

const onAdd = async () => {
  await axios.post('/api/motherboards/', newItem.value)
  newItem.value = { name: '', socket: '', form_factor: '' }
  await fetchItems()
  await fetchStats()
}

const onEditClick = (item) => {
  editItem.value = { ...item }
}

const onUpdate = async () => {
  await axios.put(`/api/motherboards/${editItem.value.id}/`, editItem.value)
  await fetchItems()
  await fetchStats()
}

const onDelete = async (id) => {
  if (confirm('Удалить?')) {
    await axios.delete(`/api/motherboards/${id}/`)
    await fetchItems()
    await fetchStats()
  }
}

const exportToExcel = () => {
  let url = '/api/motherboards/export-excel/'
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