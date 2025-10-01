import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'https://localhost:8080',
        changeOrigin: true,
        secure: false
      },
      '/auth': {
        target: 'https://localhost:8080',
        changeOrigin: true,
        secure: false
      },
      '/logout': {
        target: 'https://localhost:8080',
        changeOrigin: true,
        secure: false
      },
      '/socket.io': {
        target: 'https://localhost:8080',
        changeOrigin: true,
        secure: false,
        ws: true
      }
    }
  },
  build: {
    outDir: 'dist',
    assetsDir: 'assets'
  }
})
