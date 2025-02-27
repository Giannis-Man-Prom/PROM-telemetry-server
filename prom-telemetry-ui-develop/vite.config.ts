import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  build: {
      rollupOptions: {
          output: {
              assetFileNames: (assetInfo) => {
                  if (assetInfo.name === 'scichart2d.wasm' || assetInfo.name === 'scichart3d.wasm') {
                      return 'js/[name][extname]';
                  }
                  return 'assets/[name][extname]';
              },
          },
      },
  },
  publicDir: 'public',
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  server: {
      host: '0.0.0.0',
      port: 8080
    // proxy: {
    //   "/api/v1/": {
    //     target: "127.0.0.1:5000",
    //     changeOrigin: true,
    //     secure: false,
    //   }
    // }
  }
})
