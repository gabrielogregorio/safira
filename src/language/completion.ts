import type { Locale } from './messages';
import { getAllCommands } from './phrases';
import { removeAccents, tokenize } from './tokenizer';

const MINIMUM_TYPED = 2;
const MINIMUM_PHRASE = 4;
const LONGEST_PHRASE_WORDS = 4;
const INSIDE_WORD = /^[\p{L}\p{N}_]/u;

// Whole lines that a beginner is likely to want, shown first and always valid Safira.
export const STARTER_LINES: Record<'pt' | 'en' | 'es', string[]> = {
  pt: [
    'mostre "Olá!"',
    'mostre nessa linha "Olá!"',
    'repita 3 vezes {',
    'se 1 for igual a 1 entao {',
    'enquanto 1 for menor que 10 {',
    'para cada x de 0 ate 10 {',
    'espere 1 segundos',
    'limpe a tela',
    'tente {',
    'importe biblioteca',
    'funcao nome {',
    'retorne 1',
  ],
  en: [
    'show "Hello!"',
    'repeat 3 times {',
    'if 1 is equal to 1 then {',
    'while 1 is less than 10 {',
    'try {',
    'return 1',
  ],
  es: ['muestra "¡Hola!"', 'repetir 3 veces {', 'mientras 1 sea menor que 10 {', 'volver 1'],
};

const normalize = (text: string): string => removeAccents(text).toLowerCase();

const startersFor = (locale: Locale): string[] => {
  if (locale === 'pt-br') {
    return STARTER_LINES.pt;
  }

  return locale === 'es' ? STARTER_LINES.es : STARTER_LINES.en;
};

const allPhrases = getAllCommands()
  .flatMap(([, definition]) => definition.phrases)
  .filter((phrase) => phrase.length >= MINIMUM_PHRASE)
  .sort((first, second) => first.length - second.length);

const isInsideStringOrComment = (line: string): boolean => {
  const { tokens, comments } = tokenize(line);
  const lastToken = tokens.at(-2);

  return comments.length > 0 || (lastToken?.kind === 'string' && !lastToken.terminated);
};

const remainderOf = (typed: string, candidate: string): string | null => {
  const isContinuation = candidate.length > typed.length && normalize(candidate).startsWith(typed);

  return isContinuation ? candidate.slice(typed.length) : null;
};

const fromStarters = (typedLine: string, locale: Locale): string | null => {
  for (const line of startersFor(locale)) {
    const remainder = remainderOf(typedLine, line);

    if (remainder !== null) {
      return remainder;
    }
  }

  return null;
};

const fromPhrases = (typedWords: string[]): string | null => {
  const longest = Math.min(LONGEST_PHRASE_WORDS, typedWords.length);

  for (let count = longest; count > 0; count -= 1) {
    const typed = typedWords.slice(-count).join(' ');

    if (typed.length >= MINIMUM_TYPED && !allPhrases.includes(typed)) {
      for (const phrase of allPhrases) {
        const remainder = remainderOf(typed, phrase);

        if (remainder !== null) {
          return remainder;
        }
      }
    }
  }

  return null;
};

// Names the person already used in this file, the most used first.
const fromNames = (typedWord: string, document: string): string | null => {
  const uses = new Map<string, number>();

  for (const token of tokenize(document).tokens) {
    if (token.kind === 'word') {
      uses.set(token.text, (uses.get(token.text) ?? 0) + 1);
    }
  }

  const names = [...uses.entries()]
    .filter(([name]) => name.length > typedWord.length && normalize(name).startsWith(typedWord))
    .sort((first, second) => second[1] - first[1]);

  return names[0] === undefined ? null : names[0][0].slice(typedWord.length);
};

export const suggestCompletion = (before: string, after: string, document: string, locale: Locale): string | null => {
  const typedLine = normalize(before.trimStart());
  const typedWords = typedLine.split(/\s+/).filter(Boolean);
  const typedWord = /\s$/.test(before) ? '' : (typedWords.at(-1) ?? '');

  if (typedLine.length < MINIMUM_TYPED || INSIDE_WORD.test(after) || isInsideStringOrComment(before)) {
    return null;
  }

  if (typedWord === '') {
    return null;
  }

  return (
    fromStarters(typedLine, locale) ??
    fromPhrases(typedWords) ??
    (typedWord.length < MINIMUM_TYPED ? null : fromNames(typedWord, document))
  );
};
