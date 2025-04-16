import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'

// Get the port from environment variable or default to 8080
const frontendPort = process.env.FRONTEND_PORT ? parseInt(process.env.FRONTEND_PORT) : 8080
const backendPort = process.env.BACKEND_PORT ? parseInt(process.env.BACKEND_PORT) : 5000
const basePath = process.env.VITE_BASE_PATH ? process.env.VITE_BASE_PATH : './'

const isProduction = process.env.NODE_ENV === 'production';
const APIbaseURL = isProduction ? '' : `http://localhost:${backendPort}`;

// https://vite.dev/config/
export default defineConfig({
  base: basePath,
  plugins: [
    vue(),
    //vueDevTools(),
  ],
  resolve: {
    dedupe: ['three'],
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
      'three': 'three'
    },
  },
  optimizeDeps: {
    include: ['@speckle/viewer'],
    esbuildOptions: {
      target: 'es2020',
    },
  },
  build: {
    commonjsOptions: {
      include: [/@speckle\/viewer/, /node_modules/],
    },
  },
  define: {
    //'import.meta.env.VITE_API_BASE_URL': JSON.stringify(`/api`)
    'import.meta.env.VITE_API_BASE_URL': JSON.stringify(APIbaseURL)
  },
  server: {
    host: true, // or '0.0.0.0' - both work, 'true' is more idiomatic
    port: frontendPort, // allows override via environment variable,
    cors: true,
    hmr: {
      protocol: 'ws',
      host: '0.0.0.0' ,
    },
    allowedHosts: true ,// accepts all hosts,
    watch: {
      usePolling: true // More reliable in Docker environments
    },
    // This is the important part
    fs: {
      strict: false // Allows accessing files outside of root directory
    },
    // Completely open allowed hosts in dev mode
    proxy: {}, // No direct proxy handled by Vite
  }
})
