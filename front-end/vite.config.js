import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { VitePWA } from 'vite-plugin-pwa'

export default defineConfig({
  plugins: [
    react(),
    VitePWA({
      registerType: 'autoUpdate',
      manifest: {
        name: 'Soromais',
        short_name: 'Soromais',
        description: 'Identifique animais peçonhentos, veja os efeitos do veneno e encontre o hospital mais próximo com soro antiveneno disponível.',
        start_url: '/',
        display: 'standalone',
        background_color: '#f1fcf6',
        theme_color: '#00452e',
        icons: [
          {
            src: '/icons/soromais_app_icon_192x192.png',
            sizes: '192x192',
            type: 'image/png',
          },
          {
            src: '/icons/soromais_app_icon_512x512.png',
            sizes: '512x512',
            type: 'image/png',
          },
          {
            src: '/icons/soromais_app_icon_512x512.png',
            sizes: '512x512',
            type: 'image/png',
            purpose: 'maskable',
          },
        ],
      },
    }),
  ],
})
