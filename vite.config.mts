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
    // The first test of a file renders the whole app while every worker is starting, and under coverage that took over 5 s.
    testTimeout: 20_000,
    include: ['src/**/*.test.{ts,tsx}'],
    coverage: {
      provider: 'v8',
      reporter: ['text-summary', 'html'],
      include: ['src/**/*.{ts,tsx}'],
      exclude: ['src/**/*.test.{ts,tsx}', 'src/testSetup.ts', 'src/main.tsx', 'src/ui/fakeWorker.ts', 'src/language/testHarness.ts', 'src/runtime/runner.worker.ts', 'src/lessons/lessonCheck.worker.ts', 'src/language/matrix/**'],
      thresholds: { statements: 90, branches: 83, functions: 87, lines: 90 },
    },
  },
});
