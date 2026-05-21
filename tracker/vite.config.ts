import { defineConfig } from 'vite';
import path from 'node:path';

export default defineConfig({
  build: {
    lib: {
      entry: path.resolve(__dirname, 'src/index.ts'),
      name: 'VebMonitoringTracker',
      fileName: () => 'tracker.min.js',
      formats: ['iife'],
    },
    minify: 'terser',
    terserOptions: {
      compress: {
        passes: 3,
        pure_funcs: ['console.log', 'console.debug'],
      },
      mangle: {
        properties: false,
      },
    },
    rollupOptions: {
      output: {
        extend: true,
      },
    },
    target: 'es2017',
    emptyOutDir: true,
  },
});
