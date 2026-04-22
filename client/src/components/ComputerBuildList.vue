<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import UserFilter from './UserFilter.vue'

const items = ref([])
const stats = ref({})
const processors = ref([])
const videocards = ref([])
const motherboards = ref([])
const newItem = ref({ name: '', processor_id: null, videocard_id: null, motherboard_id: null, price: null })
const editItem = ref({})
const currentUserId = ref(null)

const filters = ref({
  name: '',
  processor: '',
  videocard: '',
  motherboard: '',
  price: ''
})

const filteredItems = computed(() => {
  let result = items.value
  
  if (filters.value.name) {
    result = result.filter(item => 
      item.name.toLowerCase().includes(filters.value.name.toLowerCase())
    )
  }
  
  if (filters.value.processor) {
    result = result.filter(item => 
      item.processor?.name.toLowerCase().includes(filters.value.processor.toLowerCase())
    )
  }
  
  if (filters.value.videocard) {
    result = result.filter(item => 
      item.videocard?.name.toLowerCase().includes(filters.value.videocard.toLowerCase())
    )
  }
  
  if (filters.value.motherboard) {
    result = result.filter(item => 
      item.motherboard?.name.toLowerCase().includes(filters.value.motherboard.toLowerCase())
    )
  }
  
  if (filters.value.price) {
    result = result.filter(item => 
      item.price === parseFloat(filters.value.price)
    )
  }
  
  return result
})

const applyFilters = () => {}

const clearFilters = () => {
  filters.value = { name: '', processor: '', videocard: '', motherboard: '', price: '' }
}

const fetchItems = async () => {
  let url = '/api/builds/'
  if (currentUserId.value) {
    url += `?user_id=${currentUserId.value}`
  }
  const response = await axios.get(url)
  items.value = response.data
}

const fetchStats = async () => {
  let url = '/api/builds/stats/'
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

const fetchProcessors = async () => {
  const response = await axios.get('/api/processors/')
  processors.value = response.data
}

const fetchVideocards = async () => {
  const response = await axios.get('/api/videocards/')
  videocards.value = response.data
}

const fetchMotherboards = async () => {
  const response = await axios.get('/api/motherboards/')
  motherboards.value = response.data
}

const onAdd = async () => {
  await axios.post('/api/builds/', newItem.value)
  newItem.value = { name: '', processor_id: null, videocard_id: null, motherboard_id: null, price: null }
  await fetchItems()
  await fetchStats()
}

const onEditClick = (item) => {
  editItem.value = { ...item, processor_id: item.processor?.id, videocard_id: item.videocard?.id, motherboard_id: item.motherboard?.id }
}

const onUpdate = async () => {
  await axios.put(`/api/builds/${editItem.value.id}/`, editItem.value)
  await fetchItems()
  await fetchStats()
}

const onDelete = async (id) => {
  if (confirm('Удалить?')) {
    await axios.delete(`/api/builds/${id}/`)
    await fetchItems()
    await fetchStats()
  }
}

const exportToExcel = () => {
  let url = '/api/builds/export-excel/'
  if (currentUserId.value) {
    url += `?user_id=${currentUserId.value}`
  }
  window.open(url, '_blank')
}

onMounted(() => {
  fetchItems()
  fetchStats()
  fetchProcessors()
  fetchVideocards()
  fetchMotherboards()
})
</script>
<template>
  <div class="card">
    <div class="card-header">
      <h3>Сборки ПК</h3>
    </div>
    <div class="card-body">
      <UserFilter model="builds" @filter-change="onFilterChange" />

      <div class="row mt-3 mb-4">
        <div class="col-md-3">
          <div class="card text-bg-info">
            <div class="card-body">
              <h5 class="card-title">Всего сборок</h5>
              <p class="card-text display-6">{{ stats.count || 0 }}</p>
            </div>
          </div>
        </div>
        <div class="col-md-3">
          <div class="card text-bg-success">
            <div class="card-body">
              <h5 class="card-title">Ср. цена</h5>
              <p class="card-text display-6">{{ stats.avg_price?.toFixed(0) || 0 }} ₽</p>
            </div>
          </div>
        </div>
        <div class="col-md-3">
          <div class="card text-bg-warning">
            <div class="card-body">
              <h5 class="card-title">Макс. цена</h5>
              <p class="card-text display-6">{{ stats.max_price || 0 }} ₽</p>
            </div>
          </div>
        </div>
        <div class="col-md-3">
          <div class="card text-bg-danger">
            <div class="card-body">
              <h5 class="card-title">Мин. цена</h5>
              <p class="card-text display-6">{{ stats.min_price || 0 }} ₽</p>
            </div>
          </div>
        </div>
      </div>

      <div class="row mb-3">
        <div class="col">
          <input type="text" class="form-control" v-model="filters.name" placeholder="Фильтр по названию" @input="applyFilters">
        </div>
        <div class="col">
          <input type="text" class="form-control" v-model="filters.processor" placeholder="Фильтр по процессору" @input="applyFilters">
        </div>
        <div class="col">
          <input type="text" class="form-control" v-model="filters.videocard" placeholder="Фильтр по видеокарте" @input="applyFilters">
        </div>
        <div class="col">
          <input type="text" class="form-control" v-model="filters.motherboard" placeholder="Фильтр по мат. плате" @input="applyFilters">
        </div>
        <div class="col">
          <input type="number" class="form-control" v-model="filters.price" placeholder="Фильтр по цене" @input="applyFilters">
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
            <select class="form-select" v-model="newItem.processor_id" required>
              <option :value="null">Выберите процессор</option>
              <option :value="p.id" v-for="p in processors">{{ p.name }}</option>
            </select>
          </div>
          <div class="col">
            <select class="form-select" v-model="newItem.videocard_id" required>
              <option :value="null">Выберите видеокарту</option>
              <option :value="v.id" v-for="v in videocards">{{ v.name }}</option>
            </select>
          </div>
          <div class="col">
            <select class="form-select" v-model="newItem.motherboard_id" required>
              <option :value="null">Выберите мат. плату</option>
              <option :value="m.id" v-for="m in motherboards">{{ m.name }}</option>
            </select>
          </div>
          <div class="col">
            <input type="number" step="0.01" class="form-control" v-model="newItem.price" placeholder="Цена" required>
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
            <th>Процессор</th>
            <th>Видеокарта</th>
            <th>Мат. плата</th>
            <th>Цена</th>
            <th>Действия</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in filteredItems" :key="item.id">
            <td>{{ item.id }}</td>
            <td>{{ item.name }}</td>
            <td>{{ item.processor?.name }}</td>
            <td>{{ item.videocard?.name }}</td>
            <td>{{ item.motherboard?.name }}</td>
            <td>{{ item.price }}</td>
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
          <h5 class="modal-title">Редактировать сборку</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
        </div>
        <div class="modal-body">
          <div class="mb-2">
            <input type="text" class="form-control" v-model="editItem.name" placeholder="Название">
          </div>
          <div class="mb-2">
            <select class="form-select" v-model="editItem.processor_id">
              <option :value="null">Выберите процессор</option>
              <option :value="p.id" v-for="p in processors">{{ p.name }}</option>
            </select>
          </div>
          <div class="mb-2">
            <select class="form-select" v-model="editItem.videocard_id">
              <option :value="null">Выберите видеокарту</option>
              <option :value="v.id" v-for="v in videocards">{{ v.name }}</option>
            </select>
          </div>
          <div class="mb-2">
            <select class="form-select" v-model="editItem.motherboard_id">
              <option :value="null">Выберите мат. плату</option>
              <option :value="m.id" v-for="m in motherboards">{{ m.name }}</option>
            </select>
          </div>
          <div class="mb-2">
            <input type="number" step="0.01" class="form-control" v-model="editItem.price" placeholder="Цена">
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

