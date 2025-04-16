<script setup lang="ts">
  import { computed, ref } from 'vue'
  import { useRoute, useRouter } from 'vue-router'
  import { Permission } from '@/types/permissions/PermissionEnum'
import { getAuthStore } from '@/stores/storeAccessor';
import type { IAuthService } from '@/services/IAuthService';
import { TYPES } from '@/di/types';
import { container } from '@/di/container';
import { Routes } from '@/types/routes/Routes';
  
  const route = useRoute();
  const authStore = getAuthStore();
  
  const router = useRouter()
  const authService = container.get<IAuthService>(TYPES.AuthService)
  const currentRoute = computed(() => route.path);
  const isAdmin = computed(() => authStore.getPermissions?.includes(Permission.ADMIN));

  const isCollapsed = ref(false);

  const toggleNavigation = () => {
    isCollapsed.value = !isCollapsed.value;
  };
  
  const menuSections = [
  {
    header: 'Dashboard',
    items: [
      { path: '/', name: 'Home', icon: 'home' }
    ]
  },
  {
    header: 'Material Analysis',
    items: [
      { path: '/products', name: 'Products', icon: 'product' },
      { path: '/buildups', name: 'Buildups', icon: 'buildup' }
    ]
  },
  {
    header: 'Project Analysis',
    items: [
      { path: '/models', name: 'Models', icon: 'model' }
    ]
  },
  {
    header: 'Management',
    items: [
      { path: '/categories', name: 'Categories', icon: 'category' }
    ]
  },
  {
    header: 'Administration',
    requiresAdmin: true,
    items: [
      { path: '/admin', name: 'Admin Panel', icon: 'admin' }
    ]
  }
];

// Logout handler
const handleLogout = async () => {

  try {

    await authService.logout()


    
    
  } catch (error) {
    console.error('Logout failed:', error)
    // add error message to the user?
  } finally {
    router.push(Routes.LOGIN.path);
  }

};
</script>

<template>
    <div class="container">
      <nav class="navbar" :class="{ 'collapsed': isCollapsed }">
        <div class="nav-header">
        <div class="form-title">
          <!-- Replace with your logo -->
          <span alt="Logo" class="app-logo"></span>
          <span alt="Logo" class="app-title"></span>
        </div>
        </div>

        <div class="nav-menu">
          <div v-for="(section, sIndex) in menuSections" :key="'section-' + sIndex">
          <!-- Only show section if it doesn't require admin OR user is admin -->
          <div v-if="(!section.requiresAdmin || isAdmin) && section.items.length > 0" class="nav-section">
            <router-link 
              v-for="item in section.items" 
              :key="item.path"
              :to="item.path"
              class="nav-item"
              :class="{ 'active': currentRoute === item.path || (item.path.startsWith('/admin') && currentRoute.startsWith('/admin')) }"
            >
              <span :class="['icon', item.icon]"></span>
              <span class="text" v-if="!isCollapsed">{{ item.name }}</span>
            </router-link>
          </div>
          <div v-if="(!section.requiresAdmin || isAdmin) && sIndex < menuSections.length - 1" class="separator"></div>
          </div>
         

        </div>

        <div class="nav-footer">
        <button class="form-sign-in_btn symbol" @click="handleLogout">
          <span class="icon logout"></span>
        </button>
        </div>
      </nav>
      <div class="main-content">
        <router-view></router-view>
      </div>
    </div>
</template>

<style scoped>


  </style>