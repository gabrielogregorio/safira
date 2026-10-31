import { execFileSync } from 'node:child_process';
import { appendFileSync, readFileSync, readdirSync, writeFileSync } from 'node:fs';
import { chromium } from '@playwright/test';

const MEMORY_LIMIT_MEGABYTES = Number(process.env['MEMORY_LIMIT_MB'] ?? 300);
const ROUNDS = 5;
const BASE_URL = 'http://127.0.0.1:5556/';
const KILOBYTES_PER_MEGABYTE = 1024;
const SAMPLE_MILLISECONDS = 500;
const IDLE_MILLISECONDS = 8000;
const MILLISECONDS_PER_SECOND = 1000;
const FIRST_TIME_FIELD_AFTER_THE_NAME = 11;
const CLOCK_TICKS_PER_SECOND = Number(execFileSync('/usr/bin/getconf', ['CLK_TCK']).toString());

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

const readCpuTicks = (processId: string): number => {
  try {
    const stat = readFileSync(`/proc/${processId}/stat`, 'utf8');
    const fields = stat.slice(stat.lastIndexOf(')') + 2).split(' ');

    return Number(fields[FIRST_TIME_FIELD_AFTER_THE_NAME]) + Number(fields[FIRST_TIME_FIELD_AFTER_THE_NAME + 1]);
  } catch {
    return 0;
  }
};

const percentOfOneCore = (cpuSeconds: number, seconds: number): number => Math.round((cpuSeconds / seconds) * 100);

const server = await chromium.launchServer();
const browserId = String(server.process().pid);
const browser = await chromium.connect(server.wsEndpoint());
const page = await browser.newPage({ locale: 'en-US' });
const usage = { peakSiteMegabytes: 0, peakChromeMegabytes: 0, peakCpuPercent: 0 };
const cpuSecondsByPhase = { flow: 0, idle: 0 };
const lastTicks = new Map<string, number>();
let phase: keyof typeof cpuSecondsByPhase = 'flow';
let lastSampleAt = performance.now();

// Everything under the browser counts for CPU, because the gem is drawn by the GPU process.
const sample = (): void => {
  const processIds = readdirSync('/proc').filter((name) => /^\d+$/.test(name) && isDescendantOf(name, browserId));
  const now = performance.now();
  let newTicks = 0;
  let siteKilobytes = 0;
  let chromeKilobytes = 0;

  for (const processId of processIds) {
    const memory = readProportionalMemory(processId);
    const ticks = readCpuTicks(processId);
    chromeKilobytes += memory;
    newTicks += Math.max(ticks - (lastTicks.get(processId) ?? ticks), 0);
    lastTicks.set(processId, ticks);

    if (readCommandLine(processId).includes('--type=renderer')) {
      siteKilobytes += memory;
    }
  }

  const cpuSeconds = newTicks / CLOCK_TICKS_PER_SECOND;
  const seconds = (now - lastSampleAt) / MILLISECONDS_PER_SECOND;
  lastSampleAt = now;
  cpuSecondsByPhase[phase] += cpuSeconds;
  usage.peakCpuPercent = Math.max(usage.peakCpuPercent, percentOfOneCore(cpuSeconds, seconds));
  usage.peakSiteMegabytes = Math.max(usage.peakSiteMegabytes, siteKilobytes / KILOBYTES_PER_MEGABYTE);
  usage.peakChromeMegabytes = Math.max(usage.peakChromeMegabytes, chromeKilobytes / KILOBYTES_PER_MEGABYTE);
};

const sampler = setInterval(sample, SAMPLE_MILLISECONDS);
const startedAt = performance.now();

await page.goto(BASE_URL);

for (let round = 0; round < ROUNDS; round += 1) {
  await page.getByRole('button', { name: 'Create project' }).click();
  await page.getByRole('button', { name: 'Go ahead' }).click();
  await page.getByLabel('Code editor').click();
  await page.keyboard.insertText('repita 300 vezes { mostre "linha" }');
  await page.getByRole('button', { name: 'Run', exact: true }).click();
  await page.getByText('Script finished').waitFor();
  await page.keyboard.press('Control+s');
  await page.getByRole('button', { name: 'Back to projects' }).click();
  console.log(`round ${round + 1}: ${usage.peakSiteMegabytes.toFixed(1)} MB at peak so far`);
}

const flowSeconds = (performance.now() - startedAt) / MILLISECONDS_PER_SECOND;

// The page sits open for hours: the sky and the gem must not eat the machine while nobody touches it.
sample();
phase = 'idle';
await page.mouse.move(600, 400);
await page.waitForTimeout(IDLE_MILLISECONDS);
sample();
clearInterval(sampler);

await browser.close();
await server.close();

const report = {
  limitMegabytes: MEMORY_LIMIT_MEGABYTES,
  peakSiteMegabytes: Math.round(usage.peakSiteMegabytes),
  peakChromeMegabytes: Math.round(usage.peakChromeMegabytes),
  peakCpuPercentOfOneCore: usage.peakCpuPercent,
  averageCpuPercentInUse: percentOfOneCore(cpuSecondsByPhase.flow, flowSeconds),
  averageCpuPercentIdle: percentOfOneCore(cpuSecondsByPhase.idle, IDLE_MILLISECONDS / MILLISECONDS_PER_SECOND),
};
const summary = [
  `Memory: ${report.peakSiteMegabytes} MB in the site, ${report.peakChromeMegabytes} MB in the whole browser (limit ${report.limitMegabytes} MB in the site)`,
  `CPU in use: ${report.averageCpuPercentInUse}% on average, ${report.peakCpuPercentOfOneCore}% at peak, of one core`,
  `CPU idle: ${report.averageCpuPercentIdle}% of one core, with the page open and nobody touching it`,
].join('\n');

writeFileSync('resourceUsageReport.json', JSON.stringify(report, null, 2));
console.log(summary);

if (process.env['GITHUB_STEP_SUMMARY'] !== undefined) {
  appendFileSync(process.env['GITHUB_STEP_SUMMARY'], `${summary}\n`);
}

if (usage.peakSiteMegabytes > MEMORY_LIMIT_MEGABYTES) {
  console.error(`The site went over ${MEMORY_LIMIT_MEGABYTES} MB`);
  process.exit(1);
}
