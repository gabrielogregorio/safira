import { defineConfig, devices } from '@playwright/test';

const PREVIEW_PORT = 5556;

export default defineConfig({
  testDir: 'e2e',
  fullyParallel: false,
  workers: 1,
  reporter: [['list'], ['html', { open: 'never' }]],
  use: {
    baseURL: `http://127.0.0.1:${PREVIEW_PORT}`,
    locale: 'en-US',
    trace: 'retain-on-failure',
    screenshot: 'only-on-failure',
  },
  projects: [{ name: 'chromium', use: { ...devices['Desktop Chrome'] } }],
  webServer: {
    command: `pnpm run preview --host 127.0.0.1`,
    url: `http://127.0.0.1:${PREVIEW_PORT}`,
    reuseExistingServer: true,
  },
});
