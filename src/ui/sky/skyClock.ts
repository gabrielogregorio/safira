import type { ThemeId } from '@/settings/settings';
import { THEME_IDS } from '@/settings/settings';

const HOURS_PER_CYCLE = 12;
const MILLISECONDS_PER_HOUR = 3_600_000;
const FADE_START = 0.25;
const FADE_END = 0.75;
const SCENES = THEME_IDS.length;

export const CYCLE_MILLISECONDS = HOURS_PER_CYCLE * MILLISECONDS_PER_HOUR;
export const SKY_TICK_MILLISECONDS = 60_000;

export const phaseOfTheme = (theme: ThemeId): number => THEME_IDS.indexOf(theme);

// The phase walks through the scenes: 0 is the first theme at its peak, 1 the second, and it wraps at 3.
export const phaseAt = (theme: ThemeId, elapsedMilliseconds: number): number =>
  (phaseOfTheme(theme) + (elapsedMilliseconds / CYCLE_MILLISECONDS) * SCENES) % SCENES;

export const themeAtPhase = (phase: number): ThemeId => THEME_IDS[Math.round(phase) % SCENES];

const smoothStep = (value: number): number => {
  const amount = Math.min(1, Math.max(0, (value - FADE_START) / (FADE_END - FADE_START)));

  return amount * amount * (3 - 2 * amount);
};

export const sceneOpacity = (sceneIndex: number, phase: number): number => {
  const current = Math.floor(phase);
  const fade = smoothStep(phase - current);

  if (sceneIndex === current) {
    return 1 - fade;
  }

  return sceneIndex === (current + 1) % SCENES ? fade : 0;
};

// How far a scene is from its peak: negative before it, positive after it, which moves its sun or moon.
export const sceneOffset = (sceneIndex: number, phase: number): number =>
  ((phase - sceneIndex + SCENES * 1.5) % SCENES) - SCENES / 2;
