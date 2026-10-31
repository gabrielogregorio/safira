import type { SyntaxCategory } from '@/language/highlight';
import type { ThemeId } from './settings';
import { SYNTAX_PALETTES } from './settings';

export type VisionMode =
  | 'default'
  | 'protanopia'
  | 'deuteranopia'
  | 'tritanopia'
  | 'achromatopsia'
  | 'lowVision'
  | 'lightSensitivity'
  | 'calm';

export const VISION_MODES: VisionMode[] = [
  'default',
  'protanopia',
  'deuteranopia',
  'tritanopia',
  'achromatopsia',
  'lowVision',
  'lightSensitivity',
  'calm',
];

export const isVisionMode = (value: unknown): value is VisionMode => VISION_MODES.includes(value as VisionMode);

export const SYNTAX_GROUPS = ['control', 'number', 'string', 'comment', 'io', 'assign', 'ops', 'stop'] as const;

export type SyntaxGroup = (typeof SYNTAX_GROUPS)[number];

const GROUP_OF: Record<SyntaxCategory, SyntaxGroup> = {
  condicionais: 'control',
  loops: 'control',
  numerico: 'number',
  string: 'string',
  comentario: 'comment',
  lista: 'io',
  entrada: 'io',
  exibicao: 'io',
  tempo: 'io',
  atribuicao: 'assign',
  logico: 'ops',
  contas: 'ops',
  pare: 'stop',
};

export interface SyntaxCue {
  weight?: string;
  style?: string;
  decoration?: string;
}

// Color alone never carries the meaning in these modes, and without colors the shape of the text has to.
export const SYNTAX_CUES: Record<SyntaxGroup, SyntaxCue> = {
  control: { weight: '700' },
  number: {},
  string: { decoration: 'underline' },
  comment: { style: 'italic' },
  io: {},
  assign: { style: 'italic' },
  ops: { weight: '700', style: 'italic' },
  stop: { weight: '700', decoration: 'underline' },
};

type GroupColors = Record<SyntaxGroup, string>;
type Surface = 'light' | 'dark';

const groupColors = (colors: string[]): GroupColors =>
  Object.fromEntries(SYNTAX_GROUPS.map((group, index) => [group, colors[index]])) as GroupColors;

// Each list was searched to stay apart in the vision it serves and in full color vision. See `vision.test.ts`.
const VISION_SYNTAX: Partial<Record<VisionMode, Record<Surface, GroupColors>>> = {
  protanopia: {
    light: groupColors(['#d61e54', '#9b0e00', '#1e8303', '#050a00', '#2673ba', '#5308a3', '#3100fc', '#730054']),
    dark: groupColors(['#50ffd3', '#ffff20', '#d0adff', '#c38796', '#ff6249', '#ffff98', '#ff2cff', '#65ac15']),
  },
  deuteranopia: {
    light: groupColors(['#cf05b3', '#1e4500', '#b300f6', '#050519', '#133384', '#d90075', '#0000ff', '#da211c']),
    dark: groupColors(['#00aa97', '#ce9817', '#0799ff', '#fffff5', '#ffff9b', '#30b058', '#d7aaff', '#ffff00']),
  },
  tritanopia: {
    light: groupColors(['#cd009c', '#a35886', '#0065ff', '#280014', '#7900df', '#7e0002', '#004400', '#dd1700']),
    dark: groupColors(['#18fbfb', '#ff38ff', '#3eab00', '#ffd7d7', '#ca8e1f', '#c3ff92', '#ff6300', '#a080ff']),
  },
  achromatopsia: {
    light: groupColors(['#000000', '#6a6a6a', '#4a4a4a', '#6a6a6a', '#000000', '#000000', '#4a4a4a', '#000000']),
    dark: groupColors(['#ffffff', '#a8a8a8', '#d0d0d0', '#a8a8a8', '#ffffff', '#ffffff', '#d0d0d0', '#ffffff']),
  },
  lowVision: {
    light: groupColors(['#704e0d', '#b30000', '#960450', '#3d3d3d', '#000000', '#006600', '#0c00ff', '#840fab']),
    dark: groupColors(['#ff8204', '#ff6190', '#ff38ff', '#c9c9c9', '#ffffff', '#00ff00', '#2b9bff', '#fff800']),
  },
  lightSensitivity: {
    light: groupColors(['#d99a5b', '#8fb8a0', '#d9c47a', '#948b7e', '#b0a7c9', '#a3bd6e', '#d48a8a', '#e07f5f']),
    dark: groupColors(['#d99a5b', '#8fb8a0', '#d9c47a', '#948b7e', '#b0a7c9', '#a3bd6e', '#d48a8a', '#e07f5f']),
  },
};

const THEME_SURFACE: Record<ThemeId, Surface> = { light: 'light', dark: 'dark', simple: 'dark' };

const glossyFace = (top: string, middle: string, low: string, deep: string): string =>
  `radial-gradient(ellipse 90% 70% at 50% 18%, ${top} 0%, ${middle} 42%, ${low} 72%, ${deep} 100%)`;

const BLUE_RUN = {
  'aero-run-face': glossyFace('#bfe0ff', '#4a9be8', '#1a66c2', '#0b478f'),
  'aero-run-edge': '#0b478f',
};
const ORANGE_STOP = {
  'aero-stop-face': glossyFace('#ffe0b8', '#d98324', '#a85a00', '#7a3f00'),
  'aero-stop-edge': '#a85a00',
};

const COLOR_BLIND_LIGHT = {
  ...BLUE_RUN,
  ...ORANGE_STOP,
  'color-error': '#8f4600',
  'color-warning': '#0a4f8f',
  'color-error-line': '#ffe3c2',
  'color-debug-line': '#c6e6ff',
};
const COLOR_BLIND_DARK = {
  ...BLUE_RUN,
  ...ORANGE_STOP,
  'color-error': '#ffb066',
  'color-warning': '#8fd0ff',
  'color-error-line': '#5a3a14',
  'color-debug-line': '#1c4a78',
};

const GRAY_BUTTONS = {
  'aero-run-face': glossyFace('#b5b5b5', '#6e6e6e', '#4d4d4d', '#333333'),
  'aero-run-edge': '#333333',
  'aero-stop-face': glossyFace('#6e6e6e', '#333333', '#1c1c1c', '#000000'),
  'aero-stop-edge': '#000000',
};

const DIM_SURFACES = {
  'aero-face': glossyFace('#4a453c', '#35312a', '#28251f', '#1c1a17'),
  'aero-edge': '#5a5346',
  'aero-ink': '#d8cfc0',
  'aero-plus': '#1c1a17',
  'aero-plate': '#2a2620',
  'aero-run-face': glossyFace('#6f8a5c', '#4d6640', '#3a4f30', '#2a3a22'),
  'aero-run-edge': '#2a3a22',
  'aero-stop-face': glossyFace('#9a6a5a', '#7a4a3a', '#5e362a', '#46261c'),
  'aero-stop-edge': '#46261c',
  'color-text': '#d8cfc0',
  'color-muted': '#b8ae9e',
  'color-panel': 'rgb(28 26 23 / 96%)',
  'color-panel-strong': '#1c1a17',
  'color-field': '#141210',
  'color-border': 'rgb(216 207 192 / 30%)',
  'color-line': 'rgb(216 207 192 / 30%)',
  'color-accent': '#d9a860',
  'color-error': '#e8a090',
  'color-warning': '#d9b870',
  'color-error-line': '#4a2620',
  'color-debug-line': '#3a3226',
  'color-hover': 'rgb(216 207 192 / 14%)',
};

const solidSurfaces = (ink: string, paper: string, accent: string, error: string, warning: string) => ({
  'color-text': ink,
  'color-muted': ink,
  'color-panel': paper,
  'color-panel-strong': paper,
  'color-field': paper,
  'color-border': ink,
  'color-line': ink,
  'color-accent': accent,
  'color-error': error,
  'color-warning': warning,
});

export const VISION_TOKENS: Partial<Record<VisionMode, Record<Surface, Record<string, string>>>> = {
  protanopia: { light: COLOR_BLIND_LIGHT, dark: COLOR_BLIND_DARK },
  deuteranopia: { light: COLOR_BLIND_LIGHT, dark: COLOR_BLIND_DARK },
  tritanopia: {
    light: { 'color-error': '#a3142c', 'color-warning': '#00635b', 'color-debug-line': '#d6d0f5' },
    dark: { 'color-error': '#ffb0ba', 'color-warning': '#7fe3d8', 'color-debug-line': '#3a3a78' },
  },
  achromatopsia: {
    light: {
      ...GRAY_BUTTONS,
      'color-error': '#000000',
      'color-warning': '#4a4a4a',
      'color-error-line': '#c8c8c8',
      'color-debug-line': '#ececec',
    },
    dark: {
      ...GRAY_BUTTONS,
      'color-error': '#ffffff',
      'color-warning': '#d0d0d0',
      'color-error-line': '#5e5e5e',
      'color-debug-line': '#333333',
    },
  },
  lowVision: {
    light: solidSurfaces('#000000', '#ffffff', '#00008b', '#a00000', '#5a4000'),
    dark: solidSurfaces('#ffffff', '#000000', '#ffff00', '#ffb0b0', '#ffe066'),
  },
  lightSensitivity: { light: DIM_SURFACES, dark: DIM_SURFACES },
};

const allTokenNames = (): string[] => [
  ...new Set(
    Object.values(VISION_TOKENS).flatMap((surfaces) => [...Object.keys(surfaces.light), ...Object.keys(surfaces.dark)]),
  ),
];

export const VISION_TOKEN_NAMES = allTokenNames();

export const visionTokens = (vision: VisionMode, theme: ThemeId): Record<string, string> =>
  VISION_TOKENS[vision]?.[THEME_SURFACE[theme]] ?? {};

export const hasVisionPalette = (vision: VisionMode): boolean => VISION_SYNTAX[vision] !== undefined;

export const syntaxPalette = (vision: VisionMode, theme: ThemeId): Record<SyntaxCategory, string> => {
  const colors = VISION_SYNTAX[vision]?.[THEME_SURFACE[theme]];

  if (colors === undefined) {
    return SYNTAX_PALETTES[theme];
  }

  return Object.fromEntries(Object.entries(GROUP_OF).map(([category, group]) => [category, colors[group]])) as Record<
    SyntaxCategory,
    string
  >;
};

export const syntaxCues = (vision: VisionMode): Record<SyntaxCategory, SyntaxCue> | null =>
  hasVisionPalette(vision)
    ? (Object.fromEntries(
        Object.entries(GROUP_OF).map(([category, group]) => [category, SYNTAX_CUES[group]]),
      ) as Record<SyntaxCategory, SyntaxCue>)
    : null;

// Applies the mode to the page. Everything it sets is cleared first, so leaving a mode leaves nothing behind.
export const applyVision = (root: HTMLElement, vision: VisionMode, theme: ThemeId): void => {
  root.dataset['vision'] = vision;

  for (const name of VISION_TOKEN_NAMES) {
    root.style.removeProperty(`--${name}`);
  }

  for (const [name, value] of Object.entries(visionTokens(vision, theme))) {
    root.style.setProperty(`--${name}`, value);
  }

  const cues = syntaxCues(vision);

  for (const [category, color] of Object.entries(syntaxPalette(vision, theme))) {
    const cue = cues?.[category as SyntaxCategory];
    root.style.setProperty(`--syntax-${category}`, color);
    root.style.setProperty(`--syntax-${category}-weight`, cue?.weight ?? 'inherit');
    root.style.setProperty(`--syntax-${category}-style`, cue?.style ?? 'inherit');
    root.style.setProperty(`--syntax-${category}-decoration`, cue?.decoration ?? 'none');
  }
};
