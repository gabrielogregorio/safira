import { readFileSync, readdirSync, writeFileSync } from 'node:fs';
import { chromium } from '@playwright/test';

const MEMORY_LIMIT_MEGABYTES = Number(process.env['MEMORY_LIMIT_MB'] ?? 300);
const ROUNDS = 5;
const BASE_URL = 'http://127.0.0.1:5556/';
const KILOBYTES_PER_MEGABYTE = 1024;

const readProportionalMemory = (processId: string): number => {
  try {
    const match = /^Pss:\s+(\d+) kB/m.exec(readFileSync(`/proc/${processId}/smaps_rollup`, 'utf8'));

    return Number(match?.[1] ?? 0);
  } catch {
    return 0;
  }
};

const readCommandLine = (processId: string): string => {
  try {
    return readFileSync(`/proc/${processId}/cmdline`, 'utf8');
  } catch {
    return '';
  }
};

const readParentId = (processId: string): string => {
  try {
    const status = readFileSync(`/proc/${processId}/status`, 'utf8');

    return /^PPid:\s+(\d+)/m.exec(status)?.[1] ?? '';
  } catch {
    return '';
  }
};

const isDescendantOf = (processId: string, ancestorId: string): boolean => {
  let current = processId;

  while (current !== '' && current !== '0') {
    if (current === ancestorId) {
      return true;
    }

    current = readParentId(current);
  }

  return false;
};

const measureRenderers = (browserId: string): number => {
  const processIds = readdirSync('/proc').filter((name) => /^\d+$/.test(name));
  const renderers = processIds.filter(
    (processId) => readCommandLine(processId).includes('--type=renderer') && isDescendantOf(processId, browserId),
  );

  return renderers.reduce((total, processId) => total + readProportionalMemory(processId), 0) / KILOBYTES_PER_MEGABYTE;
};

const server = await chromium.launchServer();
const browserId = String(server.process().pid);
const browser = await chromium.connect(server.wsEndpoint());
const page = await browser.newPage({ locale: 'en-US' });
const measurements: number[] = [];

await page.goto(BASE_URL);

for (let round = 0; round < ROUNDS; round += 1) {
  await page.getByRole('button', { name: 'Create project' }).click();
  await page.getByLabel('Code editor').click();
  await page.keyboard.insertText('repita 300 vezes { mostre "linha" }');
  await page.getByRole('button', { name: 'Run', exact: true }).click();
  await page.getByText('Script finished').waitFor();
  await page.keyboard.press('Control+s');
  await page.getByRole('button', { name: 'Back to projects' }).click();
  measurements.push(measureRenderers(browserId));
  console.log(`round ${round + 1}: ${measurements.at(-1)?.toFixed(1)} MB`);
}

await browser.close();
await server.close();

const peak = Math.max(...measurements);
writeFileSync(
  'resourceUsageReport.json',
  JSON.stringify({ limit: MEMORY_LIMIT_MEGABYTES, peak, measurements }, null, 2),
);
console.log(`peak ${peak.toFixed(1)} MB, limit ${MEMORY_LIMIT_MEGABYTES} MB`);

if (peak > MEMORY_LIMIT_MEGABYTES) {
  process.exit(1);
}
