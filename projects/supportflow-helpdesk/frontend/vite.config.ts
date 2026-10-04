import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// In development, send API calls to the Spring Boot app on port 8090.
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5175,
    proxy: { '/api': 'http://localhost:8090' }
  }
})
