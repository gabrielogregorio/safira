import { readFileSync } from 'node:fs';
import { join } from 'node:path';
import type { SyntaxCategory } from '@/language/highlight';
import { DEFAULT_SETTINGS, loadSettings, THEME_IDS } from './settings';
import type { SyntaxGroup, VisionMode } from './vision';
import {
  applyVision,
  isVisionMode,
  SYNTAX_CUES,
  SYNTAX_GROUPS,
  syntaxCues,
  syntaxPalette,
  VISION_MODES,
  VISION_TOKEN_NAMES,
  visionTokens,
} from './vision';

type Triple = [number, number, number];

const SIMULATIONS: Partial<Record<VisionMode, number[][]>> = {
  // Machado, Oliveira and Fernandes (2009), severity 1.0, applied to linear RGB.
  protanopia: [
    [0.152286, 1.052583, -0.204868],
    [0.114503, 0.786281, 0.099216],
    [-0.003882, -0.048116, 1.051998],
  ],
  deuteranopia: [
    [0.367322, 0.860646, -0.227968],
    [0.280085, 0.672501, 0.047413],
    [-0.01182, 0.04294, 0.968881],
  ],
  tritanopia: [
    [1.255528, -0.076749, -0.178779],
    [-0.078411, 0.930809, 0.147602],
    [0.004733, 0.691367, 0.3039],
  ],
};

const SAMPLE: Record<SyntaxGroup, SyntaxCategory> = {
  control: 'condicionais',
  number: 'numerico',
  string: 'string',
  comment: 'comentario',
  io: 'exibicao',
  assign: 'atribuicao',
  ops: 'contas',
  stop: 'pare',
};

const AA_TEXT = 4.5;
const AAA_TEXT = 7;
const SMALLEST_COLOR_DISTANCE = 25;

const channels = (hex: string): Triple => [
  parseInt(hex.slice(1, 3), 16) / 255,
  parseInt(hex.slice(3, 5), 16) / 255,
  parseInt(hex.slice(5, 7), 16) / 255,
];

const toLinear = (channel: number): number =>
  channel <= 0.04045 ? channel / 12.92 : ((channel + 0.055) / 1.055) ** 2.4;

const linear = (hex: string): Triple => channels(hex).map(toLinear) as Triple;

const luminanceOf = ([red, green, blue]: Triple): number => 0.2126 * red + 0.7152 * green + 0.0722 * blue;

const contrast = (first: string, second: string): number => {
  const [low, high] = [luminanceOf(linear(first)), luminanceOf(linear(second))].sort((a, b) => a - b);

  return (high + 0.05) / (low + 0.05);
};

const labOf = ([red, green, blue]: Triple): Triple => {
  const xyz = [
    (0.4124 * red + 0.3576 * green + 0.1805 * blue) / 0.9505,
    0.2126 * red + 0.7152 * green + 0.0722 * blue,
    (0.0193 * red + 0.1192 * green + 0.9505 * blue) / 1.089,
  ].map((value) => (value > 0.008856 ? Math.cbrt(value) : 7.787 * value + 16 / 116));

  return [116 * xyz[1] - 16, 500 * (xyz[0] - xyz[1]), 200 * (xyz[1] - xyz[2])];
};

const simulate = (hex: string, vision: VisionMode): Triple => {
  const color = linear(hex);
  const matrix = SIMULATIONS[vision];

  if (matrix === undefined) {
    return color;
  }

  return matrix.map((row) =>
    Math.min(1, Math.max(0, row[0] * color[0] + row[1] * color[1] + row[2] * color[2])),
  ) as Triple;
};

const seenDistance = (first: string, second: string, vision: VisionMode): number => {
  const [a, b] = [labOf(simulate(first, vision)), labOf(simulate(second, vision))];

  return Math.hypot(a[0] - b[0], a[1] - b[1], a[2] - b[2]);
};

const stylesheet = readFileSync(join(__dirname, '../ui/styles.css'), 'utf8');

const themeBackground = (theme: string): string => {
  const block = theme === 'light' ? stylesheet : stylesheet.slice(stylesheet.indexOf(`:root[data-theme='${theme}']`));
  const color = /--color-panel-strong: (#[0-9a-f]{6});/.exec(block)?.[1];

  if (color === undefined) {
    throw new Error(`no editor background for ${theme}`);
  }

  return color;
};

const backgroundOf = (vision: VisionMode, theme: (typeof THEME_IDS)[number]): string =>
  visionTokens(vision, theme)['color-panel-strong'] ?? themeBackground(theme);

const everyCase = VISION_MODES.flatMap((vision) => THEME_IDS.map((theme) => [vision, theme] as const));
const colorBlindCases = (['protanopia', 'deuteranopia', 'tritanopia'] as const).flatMap((vision) =>
  THEME_IDS.map((theme) => [vision, theme] as const),
);
const groupPairs = SYNTAX_GROUPS.flatMap((first, index) =>
  SYNTAX_GROUPS.slice(index + 1).map((second) => [first, second]),
);

describe('vision modes', () => {
  it.each(everyCase)('keeps the code of %s readable in the %s theme', (vision, theme) => {
    const floor = vision === 'lowVision' ? AAA_TEXT : AA_TEXT;
    const background = backgroundOf(vision, theme);

    for (const [category, color] of Object.entries(syntaxPalette(vision, theme))) {
      expect(contrast(color, background), `${category} ${color} on ${background}`).toBeGreaterThanOrEqual(floor);
    }
  });

  it.each(colorBlindCases)('keeps code groups apart as %s sees them in the %s theme', (vision, theme) => {
    const palette = syntaxPalette(vision, theme);

    for (const [first, second] of groupPairs) {
      const [a, b] = [palette[SAMPLE[first]], palette[SAMPLE[second]]];

      expect(seenDistance(a, b, vision), `${first} ${a} and ${second} ${b}`).toBeGreaterThanOrEqual(
        SMALLEST_COLOR_DISTANCE,
      );
      expect(seenDistance(a, b, 'default'), `${first} ${a} and ${second} ${b}`).toBeGreaterThanOrEqual(
        SMALLEST_COLOR_DISTANCE,
      );
    }
  });

  it.each(THEME_IDS)('tells every group apart without any color in the %s theme', (theme) => {
    const palette = syntaxPalette('achromatopsia', theme);
    const looks = SYNTAX_GROUPS.map((group) => {
      const color = palette[SAMPLE[group]];

      expect(color.slice(1, 3)).toBe(color.slice(3, 5));
      expect(color.slice(3, 5)).toBe(color.slice(5, 7));

      return JSON.stringify([color, SYNTAX_CUES[group]]);
    });

    expect(new Set(looks).size).toBe(SYNTAX_GROUPS.length);
  });

  it.each(['protanopia', 'deuteranopia'] as const)('keeps Run and Stop apart in %s', (vision) => {
    for (const theme of THEME_IDS) {
      const tokens = visionTokens(vision, theme);

      expect(seenDistance(tokens['aero-run-edge'], tokens['aero-stop-edge'], vision)).toBeGreaterThan(
        SMALLEST_COLOR_DISTANCE,
      );
      expect(seenDistance(tokens['color-error'], tokens['color-warning'], vision)).toBeGreaterThan(
        SMALLEST_COLOR_DISTANCE,
      );
    }
  });

  it.each(everyCase)('keeps error and warning text readable in %s with the %s theme', (vision, theme) => {
    const tokens = visionTokens(vision, theme);
    const background = backgroundOf(vision, theme);

    for (const name of ['color-error', 'color-warning']) {
      const color = tokens[name];

      if (color !== undefined) {
        expect(contrast(color, background), `${name} ${color}`).toBeGreaterThanOrEqual(AA_TEXT);
      }
    }
  });

  it('never shows a bright surface or bright code to whoever is sensitive to light', () => {
    for (const theme of THEME_IDS) {
      expect(luminanceOf(linear(backgroundOf('lightSensitivity', theme)))).toBeLessThan(0.02);

      for (const color of Object.values(syntaxPalette('lightSensitivity', theme))) {
        expect(luminanceOf(linear(color))).toBeLessThan(0.6);
      }
    }
  });

  it('follows the theme with the default colors and with the calm mode', () => {
    expect(syntaxPalette('default', 'dark')).toEqual(syntaxPalette('calm', 'dark'));
    expect(syntaxPalette('default', 'dark')).not.toEqual(syntaxPalette('default', 'light'));
    expect(syntaxCues('default')).toBeNull();
    expect(syntaxCues('calm')).toBeNull();
  });

  it('follows the theme inside a color mode too', () => {
    expect(syntaxPalette('protanopia', 'light')).not.toEqual(syntaxPalette('protanopia', 'dark'));
  });

  it('applies a mode and leaves nothing behind when it ends', () => {
    const root = document.createElement('div');
    applyVision(root, 'lowVision', 'dark');

    expect(root.dataset['vision']).toBe('lowVision');
    expect(root.style.getPropertyValue('--color-panel-strong')).toBe('#000000');
    expect(root.style.getPropertyValue('--syntax-comentario-style')).toBe('italic');

    applyVision(root, 'default', 'dark');

    for (const name of VISION_TOKEN_NAMES) {
      expect(root.style.getPropertyValue(`--${name}`)).toBe('');
    }

    expect(root.style.getPropertyValue('--syntax-comentario-style')).toBe('inherit');
  });

  it('recognizes only known modes', () => {
    expect(isVisionMode('tritanopia')).toBe(true);
    expect(isVisionMode('sepia')).toBe(false);
  });

  it('starts with the default mode and ignores a mode it does not know', () => {
    localStorage.clear();

    expect(loadSettings().vision).toBe(DEFAULT_SETTINGS.vision);

    localStorage.setItem('safira.settings.v1', JSON.stringify({ vision: 'sepia' }));

    expect(loadSettings().vision).toBe('default');
    localStorage.clear();
  });
});
