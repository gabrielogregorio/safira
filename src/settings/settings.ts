import type { SyntaxCategory } from '@/language/highlight';
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

export const SYNTAX_PALETTES: Record<ThemeId, Record<SyntaxCategory, string>> = {
  light: {
    numerico: '#0c7a7a',
    atribuicao: '#3f7a08',
    loops: '#7a6108',
    lista: '#1441b5',
    logico: '#c4005e',
    entrada: '#1441b5',
    exibicao: '#1441b5',
    tempo: '#1441b5',
    condicionais: '#b84300',
    contas: '#d00000',
    string: '#c22f00',
    comentario: '#127012',
    pare: '#d00000',
  },
  dark: {
    numerico: '#99ffcc',
    atribuicao: '#aaff80',
    loops: '#ffcc88',
    lista: '#80d4ff',
    logico: '#eb99ff',
    entrada: '#eb99ff',
    exibicao: '#00e68a',
    tempo: '#80d4ff',
    condicionais: '#ffcc88',
    contas: '#eb99ff',
    string: '#ffff68',
    comentario: '#cfcfcf',
    pare: '#fda0a0',
  },
  simple: {
    numerico: '#c48aff',
    atribuicao: '#b8ff75',
    loops: '#f94fff',
    lista: '#91fdff',
    logico: '#ff7d93',
    entrada: '#ff7d93',
    exibicao: '#78aeff',
    tempo: '#91fdff',
    condicionais: '#f94fff',
    contas: '#ff7d93',
    string: '#fff891',
    comentario: '#8cbd7d',
    pare: '#ff6b6b',
  },
};
