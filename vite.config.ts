import { defineConfig } from 'vite';

export default defineConfig({
  server: {
    port: 3000,
    open: true
  },
  build: {
    target: 'esnext',
    minify: 'esbuild' // Usar esbuild en lugar de terser (más rápido y no requiere dependencia adicional)
  }
});
