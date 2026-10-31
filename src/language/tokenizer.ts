export type TokenKind = 'word' | 'number' | 'string' | 'symbol' | 'newline' | 'end';

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
const NUMBER_PATTERN = /\d+(?:\.\d+)?(?![\p{L}\p{N}_])/uy;
const COMBINING_MARKS = /\p{M}/gu;

export const removeAccents = (text: string): string => text.normalize('NFD').replace(COMBINING_MARKS, '');

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

export const tokenize = (source: string): TokenizedSource => {
  const tokens: Token[] = [];
  const comments: CommentRange[] = [];
  let position = 0;
  let line = 1;

  const push = (kind: TokenKind, end: number, terminated = true): void => {
    const text = source.slice(position, end);
    tokens.push({ kind, text, normalized: removeAccents(text), line, start: position, end, terminated });
    position = end;
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
    } else if (character === '#' || source.startsWith('//', position)) {
      const end = findLineEnd(source, position);
      comments.push({ start: position, end });
      position = end;
    } else if (character === '"') {
      const end = findStringEnd(source, position);
      const terminated = end - position >= 2 && source.charAt(end - 1) === '"';
      push('string', end, terminated);
    } else {
      const number = matchAt(NUMBER_PATTERN, source, position);
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
