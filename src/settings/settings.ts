import type { Locale } from '@/language/messages';
import type { VisionMode } from './vision';
import { isVisionMode } from './vision';
import { storageKey } from './storageKey';

export type ThemeId = 'light' | 'dark' | 'simple';
export type CodeFont = 'mono' | 'aero';

export const THEME_IDS: ThemeId[] = ['light', 'dark', 'simple'];

export interface LessonPlace {
  lessonId: string;
  step: number;
}

export interface Settings {
  locale: Locale | null;
  theme: ThemeId;
  vision: VisionMode;
  fontSize: number;
  sound: boolean;
  codeFont: CodeFont;
  suggestions: boolean;
  lessonMode: boolean;
  /** Professor Cat gave up on this browser, and lesson mode is gone with him. */
  catLeft: boolean;
  lessonPlace: LessonPlace | null;
  /** Steps done, as `lesson:step`. They survive a change of language. */
  lessonProgress: string[];
  panels: PanelSizes;
}

export interface PanelSizes {
  sidebar: number;
  output: number;
  inspector: number;
}

export type PanelName = keyof PanelSizes;

export const DEFAULT_FONT_SIZE = 15;
export const MINIMUM_FONT_SIZE = 10;
export const MAXIMUM_FONT_SIZE = 32;
export const FONT_SIZE_STEP = 2;

const STORAGE_KEY = storageKey('settings.v1');

export const DEFAULT_SETTINGS: Settings = {
  locale: null,
  theme: 'light',
  vision: 'default',
  fontSize: DEFAULT_FONT_SIZE,
  sound: true,
  codeFont: 'mono',
  suggestions: true,
  lessonMode: false,
  catLeft: false,
  lessonPlace: null,
  lessonProgress: [],
  panels: { sidebar: 220, output: 460, inspector: 240 },
};

export const PANEL_LIMITS: Record<PanelName, { minimum: number; maximum: number }> = {
  sidebar: { minimum: 140, maximum: 480 },
  output: { minimum: 240, maximum: 900 },
  inspector: { minimum: 100, maximum: 600 },
};

export const clampPanelSize = (panel: PanelName, size: number): number => {
  const { minimum, maximum } = PANEL_LIMITS[panel];

  return Math.round(Math.min(maximum, Math.max(minimum, size)));
};

export const loadSettings = (): Settings => {
  try {
    const parsed = JSON.parse(localStorage.getItem(STORAGE_KEY) ?? '{}') as Partial<Settings>;

    return { ...DEFAULT_SETTINGS, ...parsed, vision: isVisionMode(parsed.vision) ? parsed.vision : 'default' };
  } catch {
    return DEFAULT_SETTINGS;
  }
};

export const saveSettings = (settings: Settings): void => {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(settings));
  } catch {
    // The settings keep working for this session when the browser blocks storage.
  }
};

export const clampFontSize = (size: number): number => Math.min(MAXIMUM_FONT_SIZE, Math.max(MINIMUM_FONT_SIZE, size));
