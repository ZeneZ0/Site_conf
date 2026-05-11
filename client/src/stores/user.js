import { defineStore } from 'pinia'
import axios from 'axios'

const getCookie = (name) => {
  let cookieValue = null
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';')
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim()
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1))
        break
      }
    }
  }
  return cookieValue
}

const setCsrfToken = () => {
  const csrftoken = getCookie('csrftoken')
  if (csrftoken) {
    axios.defaults.headers.common['X-CSRFToken'] = csrftoken
  }
}

setCsrfToken()
axios.defaults.withCredentials = true

export const useUserStore = defineStore('user', {
  state: () => ({
    user: {
      id: null,
      username: '',
      is_authenticated: false,
      is_superuser: false
    },
    otpRequired: true,
    otpKey: null
  }),

  getters: {
    isAuthenticated: (state) => state.user.is_authenticated,
    isSuperuser: (state) => state.user.is_superuser,
    username: (state) => state.user.username,
    getOtpRequired: (state) => state.otpRequired,
    getOtpKey: (state) => state.otpKey
  },

  actions: {
    async fetchUserInfo() {
      setCsrfToken()
      const response = await axios.get('/api/user/info/')
      this.user = {
        id: response.data.id,
        username: response.data.username,
        is_authenticated: response.data.is_authenticated,
        is_superuser: response.data.is_superuser
      }
      if (this.user.is_authenticated) {
        const otpStatus = await axios.get('/api/user/otp-status/')
        this.otpRequired = otpStatus.data.otp_required
      }
    },

    async login(username, password) {
      setCsrfToken()
      const response = await axios.post('/api/user/login/', { username, password })
      if (response.data.success) {
        await this.fetchUserInfo()
        return { success: true, requires_otp: response.data.requires_otp }
      }
      return { success: false }
    },

    async verifyOtp(otpCode) {
      setCsrfToken()
      const response = await axios.post('/api/user/verify-otp/', { otp_code: otpCode })
      if (response.data.success) {
        this.otpRequired = false
        this.otpKey = null
        return { success: true }
      }
      return { success: false }
    },

    async generateOtp() {
      setCsrfToken()
      const response = await axios.get('/api/user/generate-otp/')
      if (response.data.otp_key) {
        this.otpKey = response.data.otp_key
        return { success: true, otp_key: response.data.otp_key }
      }
      return { success: false }
    },

    async logout() {
      setCsrfToken()
      await axios.post('/api/user/logout/')
      this.user = {
        id: null,
        username: '',
        is_authenticated: false,
        is_superuser: false
      }
      this.otpRequired = true
      this.otpKey = null
    }
  }
})