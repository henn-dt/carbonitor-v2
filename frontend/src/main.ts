import './assets/main.css'
import './assets/base.css'
import './assets/style.css'
import './assets/icons.css'
import './assets/buttons.css'
import './assets/table.css'
import './assets/graphs.css'
import 'reflect-metadata';

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import { container } from './di/container';
import type { IAuthService } from './services/IAuthService';
import { TYPES } from './di/types';
import { getAuthStore, initializeStores } from './stores/storeAccessor';
import { createRefreshableService } from '@/composables/createRefreshableService'
import { useRefreshableService } from '@/composables/useRefreshableService'
import { prefetchAllData, startAllBackgroundRefreshes, stopAllBackgroundRefreshes } from './services/ServiceAccessor'


const app = createApp(App)

app.use(createPinia())

initializeStores();

app.use(router)
app.provide('container', container)
const authService = container.get<IAuthService>(TYPES.AuthService)
authService.initAuthData();


prefetchAllData();

// Start background refreshes
startAllBackgroundRefreshes();


// Mount the app
const appInstance = app.mount('#app');

// Set up app cleanup when window is being unloaded
window.addEventListener('beforeunload', () => {
  // Stop all background refreshes
  stopAllBackgroundRefreshes();
  
  // Unmount the app if needed
  if (appInstance) {
    app.unmount();
  }
});

// For development: clean up when hot module reloads
if (import.meta.hot) {
  import.meta.hot.dispose(() => {
    stopAllBackgroundRefreshes();
  });
}
