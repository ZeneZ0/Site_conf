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

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../stores/user.js'

const router = useRouter()
const userStore = useUserStore()

const loginForm = ref({ username: '', password: '' })
const otpStep = ref(false)
const otpKey = ref(null)
const generatedKey = ref(null)
const otpCode = ref('')
const loading = ref(false)
const error = ref(null)

const handleLogin = async () => {
  loading.value = true
  error.value = null
  
  const result = await userStore.login(loginForm.value.username, loginForm.value.password)
  
  console.log('Login result:', result)
  console.log('userStore.getOtpRequired:', userStore.getOtpRequired)
  
  if (result.success) {
    if (result.requires_otp && userStore.getOtpRequired) {
      console.log('Переход на OTP шаг')
      otpStep.value = true
    } else {
      console.log('Переход на главную')
      router.push('/')
    }
  } else {
    error.value = result.error || 'Ошибка входа'
  }
  
  loading.value = false
}

const generateOtp = async () => {
  loading.value = true
  const result = await userStore.generateOtp()
  console.log('Generate OTP result:', result)
  if (result.success) {
    generatedKey.value = result.otp_key
    otpKey.value = true
  } else {
    error.value = result.error
  }
  loading.value = false
}

const verifyOtp = async () => {
  if (!otpCode.value || otpCode.value.length !== 6) {
    error.value = 'Введите 6-значный код'
    return
  }
  
  loading.value = true
  const result = await userStore.verifyOtp(otpCode.value)
  console.log('Verify OTP result:', result)
  if (result.success) {
    router.push('/')
  } else {
    error.value = result.error
  }
  loading.value = false
}
</script>