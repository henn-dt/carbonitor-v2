// src/views/auth/Register.vue
<template>
  <div class="form-page">
    <div class="form-container">
      <h1 class="title">New Carbonitor Account</h1>
      <form @submit.prevent="handleRegister">
        <div class="form-group">
          <label for="username" class="form-label">username</label>
          <span class="icon form user"></span>
          <input 
            type="text" 
            id="username" 
            v-model="credentials.username"
            class="form-input" 
            placeholder="username"
            required
          >
        </div>

        <div class="form-group">
          <label for="email" class="form-label">email</label>
          <span class="icon form email"></span>
          <input 
            type="email" 
            id="email" 
            v-model="credentials.email"
            class="form-input" 
            placeholder="email"
            required
          >
        </div>

        <div class="form-group">
          <label for="password" class="form-label">password</label>
          <span class="icon form password"></span>
          <input 
            type="password" 
            id="password" 
            v-model="credentials.password"
            class="form-input" 
            placeholder="password"
            required
          >
        </div>

        <div class="form-group">
          <label for="confirm-password" class="form-label">confirm password</label>
          <span class="icon form password"></span>
          <input 
            type="password" 
            id="confirm-password" 
            v-model="credentials.confirm_password"
            class="form-input" 
            placeholder="confirm password"
            required
          >
        </div>

        <div>
          <button 
            type="submit" 
            class="form-sign-in_btn"
            :disabled="isLoading || !isPasswordsMatch"
          >
            {{ isLoading ? 'Registering...' : 'Register' }}
          </button>
        </div>

        <div class="text-center" style="margin-top: 1rem;">
          <router-link to="/auth/login" class="form-label">
            Already have an account? Sign in
          </router-link>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onUnmounted, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { RegisterCredentials } from '@/types/auth/RegisterCredentials'
import { container } from '@/di/container'
import { TYPES } from '@/di/types'
import type { IAuthService } from '@/services/IAuthService'

const router = useRouter()
const authService = container.get<IAuthService>(TYPES.AuthService)
const isLoading = ref(false)
const credentials = ref(new RegisterCredentials('', '', '', ''))
const isPasswordsMatch = computed(() => {
  return credentials.value.password === credentials.value.confirm_password
})
const handleRegister = async () => {
  if (!isPasswordsMatch.value) {
    // Here you would typically show an error message to the user
    return
  }

  try {
    isLoading.value = true
    await authService.register(credentials.value)
    router.push('/')
  } catch (error) {
    console.error('Registration failed:', error)
    // Here you would typically show an error message to the user
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
.text-center {
  text-align: center;
}
</style>