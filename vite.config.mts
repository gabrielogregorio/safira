import react from '@vitejs/plugin-react';
import { defineConfig } from 'vitest/config';

export default defineConfig({
  base: './',
  build: { outDir: 'build', sourcemap: true },
  resolve: { tsconfigPaths: true },
  plugins: [react()],
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: ['src/testSetup.ts'],
    include: ['src/**/*.test.{ts,tsx}'],
    coverage: {
      provider: 'v8',
      reporter: ['text-summary', 'html'],
      include: ['src/**/*.{ts,tsx}'],
      exclude: ['src/**/*.test.{ts,tsx}', 'src/testSetup.ts', 'src/main.tsx', 'src/ui/fakeWorker.ts', 'src/language/testHarness.ts', 'src/runtime/runner.worker.ts'],
      thresholds: { statements: 90, branches: 83, functions: 87, lines: 90 },
    },
  },
});
