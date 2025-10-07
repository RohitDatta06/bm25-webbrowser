import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'


export default defineConfig({
  plugins: [react()],
  server: {
    host: true,              // allows local dev on all interfaces
    port: 5173,
  },
  preview: {
    port: 10001,             // or any
    allowedHosts: [
      "bm25-frontend.onrender.com"  // 👈 your Render frontend URL
    ],
  },
});
