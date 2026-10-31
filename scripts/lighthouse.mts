import { writeFileSync } from 'node:fs';
import { launch } from 'chrome-launcher';
import lighthouse from 'lighthouse';
import { chromium } from '@playwright/test';

const BASE_URL = 'http://127.0.0.1:5556/';
const SCORE_SCALE = 100;
const MINIMUM_SCORES: Record<string, number> = {
  accessibility: 95,
  'best-practices': 95,
  performance: 40,
};

const chrome = await launch({ chromePath: chromium.executablePath(), chromeFlags: ['--headless=new', '--no-sandbox'] });

await fetch(BASE_URL);
const result = await lighthouse(BASE_URL, {
  port: chrome.port,
  output: 'html',
  onlyCategories: Object.keys(MINIMUM_SCORES),
});

chrome.kill();

if (result === undefined) {
  throw new Error('Lighthouse returned no result');
}

writeFileSync('lighthouseReport.html', String(result.report));

const failures = Object.entries(MINIMUM_SCORES).filter(([category, minimum]) => {
  const score = Math.round((result.lhr.categories[category]?.score ?? 0) * SCORE_SCALE);
  console.log(`${category}: ${score} (minimum ${minimum})`);

  return score < minimum;
});

if (failures.length > 0) {
  process.exit(1);
}
