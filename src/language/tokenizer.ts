export type TokenKind = 'word' | 'number' | 'string' | 'color' | 'symbol' | 'newline' | 'end';

export interface Token {
  kind: TokenKind;
  text: string;
  normalized: string;
  line: number;
  start: number;
  end: number;
  terminated: boolean;
}

export interface CommentRange {
  start: number;
  end: number;
}

export interface TokenizedSource {
  tokens: Token[];
  comments: CommentRange[];
}

const TWO_CHARACTER_SYMBOLS = new Set(['**', '==', '!=', '<=', '>=', ':=', '<-', '&&', '||']);
const WORD_PATTERN = /[\p{L}\p{N}_']+/uy;
// Chinese and Japanese glue the unit to the number, as in 1秒.
const NUMBER_PATTERN = /\d+(?:\.\d+)?(?!(?![\p{Script=Han}\p{Script=Hiragana}\p{Script=Katakana}])[\p{L}\p{N}_])/uy;
const COMBINING_MARKS = /\p{M}/gu;

export const removeAccents = (text: string): string => text.normalize('NFD').replace(COMBINING_MARKS, '');

const COLOR_PATTERN = /#(?:[0-9a-f]{8}|[0-9a-f]{6}|[0-9a-f]{3,4})(?![\p{L}\p{N}_])/iuy;
const COLOR_WORDS = new Set(['cor', 'color', 'en', 'in', '颜色', '色']);
const TONE_WORDS = new Set(['toque', 'tocar', 'toca', 'play', '播放', '鳴らす'].map((word) => removeAccents(word)));
const TIME_BEFORE_UNIT_PATTERN = /\d+(?:\.\d+)?(?=m?s(?![\p{L}\p{N}_]))/uy;

const matchAt = (pattern: RegExp, source: string, position: number): string | null => {
  pattern.lastIndex = position;

  return pattern.exec(source)?.[0] ?? null;
};

const findLineEnd = (source: string, position: number): number => {
  const lineEnd = source.indexOf('\n', position);

  return lineEnd === -1 ? source.length : lineEnd;
};

const findStringEnd = (source: string, position: number): number => {
  const lineEnd = findLineEnd(source, position);
  const closing = source.indexOf('"', position + 1);

  return closing === -1 || closing > lineEnd ? lineEnd : closing + 1;
};

const WIDE_SYMBOLS: Record<string, string> = {
  ',': ',',
  '、': ',',
  '(': '(',
  ')': ')',
  '{': '{',
  '}': '}',
  '=': '=',
  '+': '+',
  '-': '-',
  '*': '*',
  '/': '/',
  '<': '<',
  '>': '>',
  ':': ':',
};
const OPENING_QUOTES = new Set(['“', '「']);
// C# is a sharp and `cor #331` is a color: neither starts a comment.
const GLUED_OR_AFTER_COLOR = /(?:[\p{L}\p{N}]|(?:cor|color|en|in|颜色|色)\s+)$/iu;
const PLAIN_QUOTE = '"';

/**
 * A Chinese or Japanese keyboard types these by default, and nothing should break because of that.
 * Each symbol keeps its length, so positions in the text stay right. Strings and comments stay as they are.
 */
export const normalizeWideSymbols = (source: string): string => {
  let result = '';
  let closingQuote: string | null = null;
  let isInComment = false;

  for (const character of source) {
    if (character === '\n') {
      closingQuote = null;
      isInComment = false;
      result += character;
    } else if (isInComment) {
      result += character;
    } else if (closingQuote !== null) {
      const isClosing: boolean = character === closingQuote;
      result += isClosing ? PLAIN_QUOTE : character;
      closingQuote = isClosing ? null : closingQuote;
    } else if (character === PLAIN_QUOTE) {
      closingQuote = PLAIN_QUOTE;
      result += character;
    } else if (OPENING_QUOTES.has(character)) {
      closingQuote = character === '「' ? '」' : '”';
      result += PLAIN_QUOTE;
    } else {
      isInComment = character === '#' && !GLUED_OR_AFTER_COLOR.test(result);
      result += WIDE_SYMBOLS[character] ?? character;
    }
  }

  return result;
};

export const tokenize = (rawSource: string): TokenizedSource => {
  const source = normalizeWideSymbols(rawSource);
  const tokens: Token[] = [];
  const comments: CommentRange[] = [];
  let position = 0;
  let line = 1;

  const push = (kind: TokenKind, end: number, terminated = true): void => {
    const text = source.slice(position, end);
    tokens.push({ kind, text, normalized: removeAccents(text), line, start: position, end, terminated });
    position = end;
  };

  // A # is a comment everywhere, except right after the word that introduces a color.
  const afterColorWord = (): boolean => {
    const previous = tokens.at(-1);

    return previous?.kind === 'word' && COLOR_WORDS.has(previous.normalized.toLowerCase());
  };

  // On a line that plays notes, a # glued to a note is a sharp, and 1s is a number and its unit.
  const isToneLine = (): boolean => {
    const lastBreak = tokens.findLastIndex((token) => token.kind === 'newline');
    const first = tokens[lastBreak + 1] as Token | undefined;

    return first?.kind === 'word' && TONE_WORDS.has(first.normalized.toLowerCase());
  };

  const isSharp = (): boolean => {
    const previous = tokens.at(-1);

    return previous?.kind === 'word' && previous.end === position && isToneLine();
  };

  while (position < source.length) {
    const character = source.charAt(position);

    if (character === '\n') {
      push('newline', position + 1);
      line += 1;
    } else if (character === ';') {
      push('newline', position + 1);
    } else if (character === ' ' || character === '\t' || character === '\r') {
      position += 1;
    } else if (character === '#' && afterColorWord() && matchAt(COLOR_PATTERN, source, position) !== null) {
      push('color', position + (matchAt(COLOR_PATTERN, source, position) as string).length);
    } else if (character === '#' && isSharp()) {
      push('symbol', position + 1);
    } else if (character === '#' || source.startsWith('//', position)) {
      const end = findLineEnd(source, position);
      comments.push({ start: position, end });
      position = end;
    } else if (character === '"') {
      const end = findStringEnd(source, position);
      const terminated = end - position >= 2 && source.charAt(end - 1) === '"';
      push('string', end, terminated);
    } else {
      const timed = isToneLine() ? matchAt(TIME_BEFORE_UNIT_PATTERN, source, position) : null;
      const number = timed ?? matchAt(NUMBER_PATTERN, source, position);
      const word = matchAt(WORD_PATTERN, source, position);

      if (number !== null) {
        push('number', position + number.length);
      } else if (word !== null) {
        push('word', position + word.length);
      } else if (TWO_CHARACTER_SYMBOLS.has(source.slice(position, position + 2))) {
        push('symbol', position + 2);
      } else {
        push('symbol', position + 1);
      }
    }
  }

  tokens.push({
    kind: 'end',
    text: '',
    normalized: '',
    line,
    start: source.length,
    end: source.length,
    terminated: true,
  });

  return { tokens, comments };
};
