import { createRouter, createWebHistory } from 'vue-router'
import { Permission } from '@/types/permissions/PermissionEnum'
import { Routes } from '@/types/routes/Routes'
import { RoutePath } from '@/types/routes/RoutePath'
import setupNavigationGuards from '@/guards/NavigationGuard'
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: Routes.HOME.path,
      component: () => import('@/views/layouts/DefaultLayout.vue'),
      meta: { requiresAuth: true },
      children: [
        {
          path: RoutePath.EMPTY,
          name: Routes.HOME.name,
          component: () => import('@/views/user/Home.vue')
        },
        {
          path: Routes.PRODUCTS.segment,
          name: Routes.PRODUCTS.name,
          component: () => import('@/views/user/Products.vue'),
          meta: { requiresPermission: Permission.PRODUCT_READ }
        },
        {
          path: Routes.BUILDUPS.segment,
          name: Routes.BUILDUPS.name,
          component: () => import('@/views/user/Buildups.vue'),
          meta: { requiresPermission: Permission.BUILDUP_READ }
        },
        {
          path: Routes.MODELS.segment,
          name: Routes.MODELS.name,
          component: () => import('@/views/user/Models.vue'),
          meta: { requiresPermission: Permission.MODEL_READ }
        },
        {
          path: Routes.CATEGORIES.segment,
          name: Routes.CATEGORIES.name,
          component: () => import('@/views/user/Categories.vue'),
          meta: { requiresPermission: Permission.CATEGORY_READ }
        }
      ]
    },
    {
      path: Routes.ADMIN_DASHBOARD.path,
      component: () => import('@/views/layouts/AdminLayout.vue'),
      meta: { requiresAdmin: true },
      children: [
        {
          path: Routes.ADMIN_DASHBOARD.segment,
          name: Routes.ADMIN_DASHBOARD.name,
          component: () => import('@/views/admin/Dashboard.vue')
        },
        {
          path: Routes.ADMIN_USERS.segment,
          name: Routes.ADMIN_USERS.name,
          component: () => import('@/views/admin/Users.vue'),
          meta: { requiresPermission: Permission.ADMIN_USERS }
        },
        {
          path: Routes.ADMIN_ROLES.segment,
          name: Routes.ADMIN_ROLES.name,
          component: () => import('@/views/admin/Roles.vue'),
          meta: { requiresPermission: Permission.ADMIN_ROLES }
        },
        {
          path: Routes.ADMIN_PRODUCTS.segment,
          name: Routes.ADMIN_PRODUCTS.name,
          component: () => import('@/views/admin/Product.vue'),
          meta: { requiresPermission: Permission.ADMIN_PRODUCTS }
        }
      ]
    },
    {
      path: Routes.LOGIN.path,
      name: Routes.LOGIN.name,
      component: () => import('@/views/auth/Login.vue')
    },
    {
      path: Routes.REGISTER.path,
      name: Routes.REGISTER.name,
      component: () => import('@/views/auth/Register.vue')
    },
    // Catch-all route for 404
    {
      path: '/:pathMatch(.*)*',
      redirect: Routes.HOME
    }
  ]
})

setupNavigationGuards(router);

export default router