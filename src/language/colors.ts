import { removeAccents } from './tokenizer';

const BLUE = '#4da3ff';
const GREEN = '#35d07f';
const RED = '#ff5252';
const YELLOW = '#ffe14d';
const ORANGE = '#ff9a3d';
const PURPLE = '#b277ff';
const PINK = '#ff7ac6';
const BLACK = '#000000';
const WHITE = '#ffffff';
const GRAY = '#a8b3bd';
const BROWN = '#b5794a';
const CYAN = '#3ddcff';
const MAGENTA = '#ff4dd2';
const GOLD = '#ffd24a';
const SILVER = '#cfd8dc';
const TURQUOISE = '#3fe0c5';

// Shades that read well on the dark terminal, in every language the commands accept.
const NAMED_COLORS: Record<string, string> = {
  azul: BLUE,
  blue: BLUE,
  verde: GREEN,
  green: GREEN,
  vermelho: RED,
  rojo: RED,
  red: RED,
  amarelo: YELLOW,
  amarillo: YELLOW,
  yellow: YELLOW,
  laranja: ORANGE,
  naranja: ORANGE,
  orange: ORANGE,
  roxo: PURPLE,
  morado: PURPLE,
  purple: PURPLE,
  violeta: PURPLE,
  violet: PURPLE,
  lilas: PURPLE,
  rosa: PINK,
  pink: PINK,
  preto: BLACK,
  negro: BLACK,
  black: BLACK,
  branco: WHITE,
  blanco: WHITE,
  white: WHITE,
  cinza: GRAY,
  gris: GRAY,
  gray: GRAY,
  grey: GRAY,
  marrom: BROWN,
  marron: BROWN,
  brown: BROWN,
  ciano: CYAN,
  cian: CYAN,
  cyan: CYAN,
  magenta: MAGENTA,
  dourado: GOLD,
  dorado: GOLD,
  gold: GOLD,
  prata: SILVER,
  plateado: SILVER,
  silver: SILVER,
  turquesa: TURQUOISE,
  turquoise: TURQUOISE,
  蓝色: BLUE,
  绿色: GREEN,
  红色: RED,
  黄色: YELLOW,
  橙色: ORANGE,
  紫色: PURPLE,
  粉色: PINK,
  黑色: BLACK,
  白色: WHITE,
  灰色: GRAY,
  棕色: BROWN,
  金色: GOLD,
  银色: SILVER,
  青: BLUE,
  緑: GREEN,
  赤: RED,
  黄色い: YELLOW,
  オレンジ: ORANGE,
  紫: PURPLE,
  ピンク: PINK,
  黒: BLACK,
  白: WHITE,
  灰色い: GRAY,
  茶色: BROWN,
  銀色: SILVER,
};

const HEX_DIGITS = '(?:[0-9a-f]{8}|[0-9a-f]{6}|[0-9a-f]{3,4})';
const HASH_COLOR = new RegExp(`^#${HEX_DIGITS}$`);
const ZERO_X_COLOR = new RegExp(`^0x(${HEX_DIGITS})$`);

// Accepts a color name, #331, #ff1122 or 0xff1122, and returns null for anything else.
export const resolveColor = (text: string): string | null => {
  const color = removeAccents(text.trim()).toLowerCase();
  const zeroX = ZERO_X_COLOR.exec(color);

  if (zeroX !== null) {
    return `#${zeroX[1]}`;
  }

  return HASH_COLOR.test(color) ? color : (NAMED_COLORS[color] ?? null);
};
