import { removeAccents } from './tokenizer';

export type KeyMode = 'press' | 'hold' | 'release';

const NAMES_OF_KEYS: Record<string, string[]> = {
  arrowup: [
    'arrowup',
    'up',
    'cima',
    'pra cima',
    'para cima',
    'seta para cima',
    'seta pra cima',
    'seta cima',
    'arriba',
    '上',
  ],
  arrowdown: [
    'arrowdown',
    'down',
    'baixo',
    'pra baixo',
    'para baixo',
    'seta para baixo',
    'seta pra baixo',
    'seta baixo',
    'abajo',
    '下',
  ],
  arrowleft: [
    'arrowleft',
    'left',
    'esquerda',
    'pra esquerda',
    'para esquerda',
    'para a esquerda',
    'seta esquerda',
    'izquierda',
    '左',
  ],
  arrowright: [
    'arrowright',
    'right',
    'direita',
    'pra direita',
    'para direita',
    'para a direita',
    'seta direita',
    'derecha',
    '右',
  ],
  enter: ['enter', 'return', 'entrar', '回车', 'エンター'],
  space: ['space', 'spacebar', 'espaco', 'barra de espaco', 'espacio', '空格', 'スペース'],
  escape: ['escape', 'esc'],
  shift: ['shift'],
  control: ['control', 'ctrl'],
  alt: ['alt'],
  tab: ['tab'],
  backspace: ['backspace'],
  delete: ['delete', 'del'],
};

const plain = (text: string): string => removeAccents(text.trim()).toLowerCase();

const KEY_OF_NAME = new Map(
  Object.entries(NAMES_OF_KEYS).flatMap(([key, names]) => names.map((name) => [plain(name), key] as const)),
);

/** The name of a key in any language, any case. Null when no key has that name. */
export const normalizeKey = (name: string): string | null => {
  if (name === ' ') {
    return 'space';
  }

  const text = plain(name);

  return KEY_OF_NAME.get(text) ?? (Array.from(text).length === 1 ? text : null);
};

/** `Shift+Enter` becomes `['shift', 'enter']`. Null when one of the keys does not exist. */
export const parseKeyCombo = (text: string): string[] | null => {
  const keys = text.split('+').map(normalizeKey);

  return keys.every((key) => key !== null) ? keys : null;
};

export class KeyTracker {
  private readonly held = new Set<string>();
  private readonly counts = new Map<string, number>();
  private readonly seen = new Map<string, number>();

  private count(event: string): number {
    return this.counts.get(event) ?? 0;
  }

  public press(key: string): void {
    if (!this.held.has(key)) {
      this.held.add(key);
      this.counts.set(`press:${key}`, this.count(`press:${key}`) + 1);
    }
  }

  public release(key: string): void {
    if (this.held.delete(key)) {
      this.counts.set(`release:${key}`, this.count(`release:${key}`) + 1);
    }
  }

  /** A window that loses the focus never hears the keys go up. */
  public clear(): void {
    this.held.clear();
  }

  /** Each condition sees each press once, so two conditions on one key do not take it from each other. */
  public check(mode: KeyMode, keys: string[]): boolean {
    if (mode === 'hold') {
      return keys.every((key) => this.held.has(key));
    }

    const main = keys[keys.length - 1];
    const condition = `${mode}:${keys.join('+')}`;
    const current = this.count(`${mode}:${main}`);

    if (current === (this.seen.get(condition) ?? 0)) {
      return false;
    }

    this.seen.set(condition, current);

    return keys.slice(0, -1).every((key) => this.held.has(key));
  }
}
