// src/views/auth/LoginView.vue
<template>
  <div class="form-page">
    <div class="form-container">
      <div class ="form-title">
        <span alt="Logo" class="app-logo"></span>
        <span alt="Logo" class="app-title"></span>
      </div>
      <h1 class="title">Sign in to Carbonitor</h1>

      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label for="email" class="form-label group-title">Email or Username</label>
          <span class="icon form email"></span>
          <input 
            type="input" 
            id="email" 
            v-model="credentials.emailOrUsername"
            class="form-input" 
            placeholder="Enter your email or username"
            required
          >
        </div>

        <div class="form-group">
          <label for="password" class="form-label group-title">password</label>
          <span class="icon form password"></span>
          <input 
            type="password" 
            id="password" 
            v-model="credentials.password"
            class="form-input" 
            placeholder="enter your password"
            required
          >
        </div>

        <div class="flex-row">
          <label class="form-checkbox">
            <input 
              type="checkbox" 
              id="remember"
              v-model="credentials.rememberMe"
            >
            <span class="form-label">remember me</span>
          </label>

          <router-link to="/auth/forgot-password" class="form-label">Forgot password?</router-link>
        </div>

        <div>
          <button 
            type="submit" 
            class="form-sign-in_btn" 
            :disabled="isLoading"
          >
            {{ isLoading ? 'Signing in...' : 'Sign In' }}
          </button>
        </div>

<!--         <div class="separator">
          <hr class="line">
          <span>Or</span>
          <hr class="line">
        </div>

        <div>
          <button 
            type="button" 
            class="form-sign-in_btn SSO"
            @click="handleSSOLogin"
            :disabled="isLoading"
          >
            Sign In with SSO
          </button>
        </div> -->

        <div class="text-center" style="margin-top: 1rem;">
          <router-link to="/auth/register" class="form-label">
            Don't have an account? Sign up
          </router-link>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { LoginCredentials } from '@/types/auth/LoginCredentials'
import { container } from '@/di/container'
import { TYPES } from '@/di/types'
import type { IAuthService } from '@/services/IAuthService'
import { Routes } from '@/types/routes/Routes'

const router = useRouter()
const authService = container.get<IAuthService>(TYPES.AuthService)

const isLoading = ref(false)
const credentials = ref(new LoginCredentials('', '', false))

const handleLogin = async () => {
  try {
    isLoading.value = true
    await authService.login(credentials.value)
    // After successful login, check for redirect path
    const redirectPath = sessionStorage.getItem('redirectPath');
    // Clear the redirect path from session storage
    sessionStorage.removeItem('redirectPath');
    // Redirect to the stored path or home
    if (redirectPath) {
      router.push(redirectPath);
    } else {
      router.push(Routes.HOME.path);
    }
  } catch (error) {
    console.error('Login failed:', error)
    // Here you would typically show an error message to the user
  } finally {
    isLoading.value = false
  }
}

const handleSSOLogin = () => {
  // Implement SSO login logic here
  console.log('SSO login not implemented')
}
</script>