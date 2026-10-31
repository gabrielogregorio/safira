import { getAllCommands } from './phrases';
import { removeAccents, tokenize } from './tokenizer';

export type SyntaxCategory =
  | 'numerico'
  | 'atribuicao'
  | 'loops'
  | 'lista'
  | 'logico'
  | 'entrada'
  | 'exibicao'
  | 'tempo'
  | 'condicionais'
  | 'contas'
  | 'string'
  | 'comentario'
  | 'pare';

export interface HighlightRange {
  start: number;
  end: number;
  category: SyntaxCategory;
}

interface PhraseEntry {
  words: string[];
  category: SyntaxCategory;
}

const SYMBOL_CATEGORIES: Record<string, SyntaxCategory> = {
  '+': 'contas',
  '-': 'contas',
  '*': 'contas',
  '/': 'contas',
  '%': 'contas',
  '**': 'contas',
  '=': 'atribuicao',
  ':=': 'atribuicao',
  '<-': 'atribuicao',
  '==': 'logico',
  '!=': 'logico',
  '<': 'logico',
  '>': 'logico',
  '<=': 'logico',
  '>=': 'logico',
  '&&': 'logico',
  '||': 'logico',
};

const buildPhraseIndex = (): Map<string, PhraseEntry[]> => {
  const index = new Map<string, PhraseEntry[]>();

  for (const [, definition] of getAllCommands()) {
    for (const phrase of definition.phrases) {
      const words = removeAccents(phrase).split(' ');
      const firstWord = words[0];
      const entries = index.get(firstWord) ?? [];
      entries.push({ words, category: definition.color as SyntaxCategory });
      index.set(firstWord, entries);
    }
  }

  for (const entries of index.values()) {
    entries.sort((first, second) => second.words.length - first.words.length);
  }

  return index;
};

const phraseIndex = buildPhraseIndex();

export const highlightCode = (code: string): HighlightRange[] => {
  const { tokens, comments } = tokenize(code);
  const ranges: HighlightRange[] = comments.map(({ start, end }) => ({ start, end, category: 'comentario' }));
  let index = 0;

  while (index < tokens.length) {
    const token = tokens[index];
    index += 1;

    if (token.kind === 'string' || token.kind === 'number') {
      const category = token.kind === 'string' ? 'string' : 'numerico';
      ranges.push({ start: token.start, end: token.end, category });
    } else if (token.kind === 'symbol' && SYMBOL_CATEGORIES[token.text] !== undefined) {
      ranges.push({ start: token.start, end: token.end, category: SYMBOL_CATEGORIES[token.text] });
    } else if (token.kind === 'word') {
      const startIndex = index - 1;
      const match = phraseIndex
        .get(token.normalized)
        ?.find((entry) => entry.words.every((word, offset) => tokens[startIndex + offset]?.normalized === word));

      if (match !== undefined) {
        const lastToken = tokens[startIndex + match.words.length - 1];
        ranges.push({ start: token.start, end: lastToken.end, category: match.category });
        index = startIndex + match.words.length;
      }
    }
  }

  return ranges.sort((first, second) => first.start - second.start);
};
