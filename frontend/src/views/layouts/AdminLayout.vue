<template>
    <div class="admin-layout">
      <!-- Sidebar -->
      <aside class="sidebar" :class="{ 'sidebar--collapsed': isSidebarCollapsed }">
        <div class="sidebar__header">
          <img src="@/assets/logo.svg" alt="Carbonitor Logo" class="sidebar__logo" />
          <button 
            class="sidebar__toggle" 
            @click="toggleSidebar"
            :aria-label="isSidebarCollapsed ? 'Expand sidebar' : 'Collapse sidebar'"
          >
            <span class="icon toggle" :class="{ 'toggle--collapsed': isSidebarCollapsed }"></span>
          </button>
        </div>
  
        <div class="sidebar__user">
          <div class="avatar">
            <span class="avatar__initials">{{ userInitials }}</span>
          </div>
          <div v-if="!isSidebarCollapsed" class="sidebar__user-info">
            <p class="sidebar__user-name">{{ authStore.user?.username }}</p>
            <p class="sidebar__user-role">Admin</p>
          </div>
        </div>
  
        <nav class="sidebar__nav">
          <ul class="sidebar__menu">
            <li>
              <router-link 
                to="/admin" 
                class="sidebar__link"
                :class="{ 'active': $route.name === 'admin-dashboard' }"
              >
                <span class="icon dashboard"></span>
                <span v-if="!isSidebarCollapsed" class="sidebar__link-text">Dashboard</span>
              </router-link>
            </li>
            <li v-if="hasPermission(Permission.ADMIN_USERS)">
              <router-link 
                to="/admin/users" 
                class="sidebar__link"
                :class="{ 'active': $route.name === 'admin-users' }"
              >
                <span class="icon users"></span>
                <span v-if="!isSidebarCollapsed" class="sidebar__link-text">Users</span>
              </router-link>
            </li>
            <li v-if="hasPermission(Permission.ADMIN_ROLES)">
              <router-link 
                to="/admin/roles" 
                class="sidebar__link"
                :class="{ 'active': $route.name === 'admin-roles' }"
              >
                <span class="icon roles"></span>
                <span v-if="!isSidebarCollapsed" class="sidebar__link-text">Roles</span>
              </router-link>
            </li>
            <li v-if="hasPermission(Permission.ADMIN_PRODUCTS)">
              <router-link 
                to="/admin/products" 
                class="sidebar__link"
                :class="{ 'active': $route.name === 'admin-products' }"
              >
                <span class="icon products"></span>
                <span v-if="!isSidebarCollapsed" class="sidebar__link-text">Products</span>
              </router-link>
            </li>
          </ul>
        </nav>
  
        <div class="sidebar__footer">
          <button class="sidebar__link sidebar__logout" @click="handleLogout">
            <span class="icon logout"></span>
            <span v-if="!isSidebarCollapsed" class="sidebar__link-text">Logout</span>
          </button>
        </div>
      </aside>
  
      <!-- Main content -->
      <main class="content" :class="{ 'content--expanded': isSidebarCollapsed }">
        <header class="header">
          <div class="header__left">
            <h1 class="header__title">{{ pageTitle }}</h1>
          </div>
          <div class="header__right">
            <div class="header__actions">
              <button class="header__action notifications">
                <span class="icon notification"></span>
                <span class="header__notification-badge" v-if="notificationCount > 0">{{ notificationCount }}</span>
              </button>
              <div class="header__profile" @click="toggleProfileMenu">
                <div class="avatar avatar--small">
                  <span class="avatar__initials">{{ userInitials }}</span>
                </div>
                <span class="header__username">{{ authStore.user?.username }}</span>
                <span class="icon dropdown"></span>
  
                <!-- Profile dropdown -->
                <div class="dropdown-menu" v-if="isProfileMenuOpen">
                  <ul class="dropdown-menu__list">
                    <li class="dropdown-menu__item">
                      <router-link to="/profile" class="dropdown-menu__link">
                        <span class="icon profile"></span>
                        <span>Profile</span>
                      </router-link>
                    </li>
                    <li class="dropdown-menu__item">
                      <router-link to="/settings" class="dropdown-menu__link">
                        <span class="icon settings"></span>
                        <span>Settings</span>
                      </router-link>
                    </li>
                    <li class="dropdown-menu__separator"></li>
                    <li class="dropdown-menu__item">
                      <button class="dropdown-menu__link dropdown-menu__link--danger" @click="handleLogout">
                        <span class="icon logout"></span>
                        <span>Logout</span>
                      </button>
                    </li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
        </header>
  
        <div class="content__wrapper">
          <router-view />
        </div>
      </main>
    </div>
  </template>
  
  <script setup lang="ts">
  import { ref, computed, onMounted, onBeforeUnmount, watch } from 'vue'
  import { useRouter, useRoute } from 'vue-router'
  import { useAuthStore } from '@/stores/authStore'
  import { Permission } from '@/types/permissions/PermissionEnum'
  
  const router = useRouter()
  const route = useRoute()
  const authStore = useAuthStore()
  
  // State
  const isSidebarCollapsed = ref(localStorage.getItem('admin-sidebar-collapsed') === 'true')
  const isProfileMenuOpen = ref(false)
  const notificationCount = ref(3) // Example count, replace with actual notification system
  
  // Computed
  const userInitials = computed(() => {
    const username = authStore.user?.username || ''
    return username.substring(0, 2).toUpperCase()
  })
  
  const pageTitle = computed(() => {
    switch (route.name) {
      case 'admin-dashboard': 
        return 'Dashboard'
      case 'admin-users': 
        return 'User Management'
      case 'admin-roles': 
        return 'Role Management'
      case 'admin-products': 
        return 'Product Management'
      default: 
        return 'Admin Panel'
    }
  })
  
  // Methods
  const toggleSidebar = () => {
    isSidebarCollapsed.value = !isSidebarCollapsed.value
    localStorage.setItem('admin-sidebar-collapsed', isSidebarCollapsed.value.toString())
  }
  
  const toggleProfileMenu = () => {
    isProfileMenuOpen.value = !isProfileMenuOpen.value
  }
  
  const handleLogout = async () => {
    try {
      await authStore.logout()
      router.push({ name: 'login' })
    } catch (error) {
      console.error('Logout failed', error)
    }
  }
  
  const hasPermission = (permission: Permission): boolean => {
    return authStore.getPermissions?.includes(permission) || false
  }
  
  // Close profile menu when clicking outside
  const handleClickOutside = (event: MouseEvent) => {
    const profileMenu = document.querySelector('.header__profile')
    if (isProfileMenuOpen.value && profileMenu && !profileMenu.contains(event.target as Node)) {
      isProfileMenuOpen.value = false
    }
  }
  
  // Lifecycle hooks
  onMounted(() => {
    document.addEventListener('click', handleClickOutside)
  })
  
  onBeforeUnmount(() => {
    document.removeEventListener('click', handleClickOutside)
  })
  
  // Reset profile menu when route changes
  watch(route, () => {
    isProfileMenuOpen.value = false
  })
  </script>
  
  <style scoped>
  .admin-layout {
    display: flex;
    height: 100vh;
    overflow: hidden;
  }
  
  /* Sidebar */
  .sidebar {
    width: 250px;
    height: 100%;
    background-color: #1a1a2e;
    color: #fff;
    display: flex;
    flex-direction: column;
    transition: width 0.3s ease;
    overflow-y: auto;
    z-index: 10;
  }
  
  .sidebar--collapsed {
    width: 80px;
  }
  
  .sidebar__header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1rem;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  }
  
  .sidebar__logo {
    height: 35px;
  }
  
  .sidebar__toggle {
    background: none;
    border: none;
    color: #fff;
    cursor: pointer;
    font-size: 1.2rem;
    padding: 0.5rem;
  }
  
  .sidebar__user {
    display: flex;
    align-items: center;
    padding: 1rem;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  }
  
  .sidebar__user-info {
    margin-left: 0.75rem;
    overflow: hidden;
  }
  
  .sidebar__user-name {
    font-weight: 600;
    margin: 0;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
  
  .sidebar__user-role {
    color: #a0aec0;
    font-size: 0.8rem;
    margin: 0;
  }
  
  .sidebar__nav {
    flex: 1;
    padding: 1rem 0;
    overflow-y: auto;
  }
  
  .sidebar__menu {
    list-style: none;
    padding: 0;
    margin: 0;
  }
  
  .sidebar__link {
    display: flex;
    align-items: center;
    padding: 0.75rem 1rem;
    color: #a0aec0;
    text-decoration: none;
    transition: all 0.2s ease;
    border-left: 3px solid transparent;
  }
  
  .sidebar__link:hover, .sidebar__link.active {
    background-color: rgba(255, 255, 255, 0.05);
    color: #fff;
    border-left-color: #4299e1;
  }
  
  .sidebar__link-text {
    margin-left: 0.75rem;
    white-space: nowrap;
  }
  
  .sidebar__footer {
    padding: 1rem;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
  }
  
  .sidebar__logout {
    width: 100%;
    text-align: left;
    background: none;
    border: none;
    cursor: pointer;
    color: #a0aec0;
  }
  
  .sidebar__logout:hover {
    color: #f56565;
  }
  
  /* Content area */
  .content {
    flex: 1;
    display: flex;
    flex-direction: column;
    background-color: #f7fafc;
    overflow-y: auto;
    transition: margin-left 0.3s ease;
  }
  
  .content--expanded {
    margin-left: 0;
  }
  
  .header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1rem 1.5rem;
    background-color: #fff;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    z-index: 5;
  }
  
  .header__title {
    margin: 0;
    font-size: 1.5rem;
    font-weight: 600;
    color: #2d3748;
  }
  
  .header__actions {
    display: flex;
    align-items: center;
  }
  
  .header__action {
    background: none;
    border: none;
    cursor: pointer;
    position: relative;
    padding: 0.5rem;
    margin-right: 1rem;
  }
  
  .header__notification-badge {
    position: absolute;
    top: 0;
    right: 0;
    background-color: #e53e3e;
    color: #fff;
    font-size: 0.7rem;
    width: 18px;
    height: 18px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  
  .header__profile {
    display: flex;
    align-items: center;
    cursor: pointer;
    padding: 0.5rem;
    border-radius: 4px;
    position: relative;
  }
  
  .header__profile:hover {
    background-color: #f0f4f8;
  }
  
  .header__username {
    margin: 0 0.5rem;
    font-weight: 500;
  }
  
  .content__wrapper {
    flex: 1;
    padding: 1.5rem;
    overflow-y: auto;
  }
  
  /* Avatar */
  .avatar {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    background-color: #4299e1;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #fff;
    font-weight: 600;
    flex-shrink: 0;
  }
  
  .avatar--small {
    width: 32px;
    height: 32px;
    font-size: 0.8rem;
  }
  
  .avatar__initials {
    line-height: 1;
  }
  
  /* Dropdown menu */
  .dropdown-menu {
    position: absolute;
    top: 100%;
    right: 0;
    background-color: #fff;
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
    border-radius: 4px;
    min-width: 200px;
    z-index: 20;
    margin-top: 0.5rem;
  }
  
  .dropdown-menu__list {
    list-style: none;
    padding: 0.5rem 0;
    margin: 0;
  }
  
  .dropdown-menu__item {
    margin: 0;
  }
  
  .dropdown-menu__separator {
    height: 1px;
    background-color: #e2e8f0;
    margin: 0.5rem 0;
  }
  
  .dropdown-menu__link {
    display: flex;
    align-items: center;
    padding: 0.5rem 1rem;
    text-decoration: none;
    color: #4a5568;
    font-size: 0.9rem;
    transition: background-color 0.2s;
    width: 100%;
    text-align: left;
    background: none;
    border: none;
    cursor: pointer;
  }
  
  .dropdown-menu__link:hover {
    background-color: #f7fafc;
  }
  
  .dropdown-menu__link--danger {
    color: #e53e3e;
  }
  
  .dropdown-menu__link--danger:hover {
    background-color: #fff5f5;
  }
  
  .dropdown-menu__link span:last-child {
    margin-left: 0.75rem;
  }
  
  /* Icons */
  .icon {
    width: 20px;
    height: 20px;
    background-position: center;
    background-repeat: no-repeat;
    background-size: contain;
    display: inline-block;
  }
  
  .icon.toggle {
    /* Replace with actual toggle icon */
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='white'%3E%3Cpath stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M11 19l-7-7 7-7m8 14l-7-7 7-7' /%3E%3C/svg%3E");
  }
  
  .icon.toggle--collapsed {
    /* Replace with actual toggle collapsed icon */
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='white'%3E%3Cpath stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M13 5l7 7-7 7M5 5l7 7-7 7' /%3E%3C/svg%3E");
  }
  
  .icon.dashboard {
    /* Replace with actual dashboard icon */
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='%23a0aec0'%3E%3Cpath stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6' /%3E%3C/svg%3E");
  }
  
  .icon.users {
    /* Replace with actual users icon */
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='%23a0aec0'%3E%3Cpath stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z' /%3E%3C/svg%3E");
  }
  
  .icon.roles {
    /* Replace with actual roles icon */
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='%23a0aec0'%3E%3Cpath stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z' /%3E%3C/svg%3E");
  }
  
  .icon.products {
    /* Replace with actual products icon */
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='%23a0aec0'%3E%3Cpath stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4' /%3E%3C/svg%3E");
  }
  
  .icon.notification {
    /* Replace with actual notification icon */
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='%234a5568'%3E%3Cpath stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9' /%3E%3C/svg%3E");
  }
  
  .icon.dropdown {
    /* Replace with actual dropdown icon */
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='%234a5568'%3E%3Cpath stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M19 9l-7 7-7-7' /%3E%3C/svg%3E");
    width: 16px;
    height: 16px;
  }
  
  .icon.profile {
    /* Replace with actual profile icon */
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='%234a5568'%3E%3Cpath stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z' /%3E%3C/svg%3E");
  }
  
  .icon.settings {
    /* Replace with actual settings icon */
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='%234a5568'%3E%3Cpath stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z' /%3E%3Cpath stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M15 12a3 3 0 11-6 0 3 3 0 016 0z' /%3E%3C/svg%3E");
  }
  
  .icon.logout {
    /* Replace with actual logout icon */
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='%23a0aec0'%3E%3Cpath stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1' /%3E%3C/svg%3E");
  }
  
  /* Responsive adjustments */
  @media (max-width: 768px) {
    .sidebar {
      position: fixed;
      left: 0;
      top: 0;
      bottom: 0;
      transform: translateX(-100%);
      transition: transform 0.3s ease;
      box-shadow: 2px 0 10px rgba(0, 0, 0, 0.1);
    }
    
    .sidebar--open {
      transform: translateX(0);
    }
    
    .content {
      margin-left: 0 !important;
    }
    
    .header__title {
      font-size: 1.2rem;
    }
    
    .header__username {
      display: none;
    }
  }
  </style>