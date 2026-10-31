import type { Statement } from './ast';
import type { Locale } from './messages';
import { parse } from './parser';
import { getAllCommands } from './phrases';
import { removeAccents, tokenize } from './tokenizer';
import { importCandidates } from './virtualFileSystem';

const SCRIPT_EXTENSION = '.safira';
const CURRENT_FOLDER = './';
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
    'toque C por 1s',
    'funcao nome {',
    'retorne 1',
  ],
  en: [
    'show "Hello!"',
    'play C by 1s',
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

const functionPhrases = getAllCommands().find(([key]) => key === 'funcoes')?.[1].phrases ?? [];

const importPhrases = (getAllCommands().find(([key]) => key === 'importe')?.[1].phrases ?? [])
  .slice()
  .sort((first, second) => second.length - first.length);

const importTextOf = (before: string): string | null => {
  const line = before.trimStart();
  const phrase = importPhrases.find((candidate) => normalize(line).startsWith(`${candidate} `));

  return phrase === undefined ? null : line.slice(phrase.length).trimStart();
};

// The rest of a project file, without the extension until the person has typed the whole name before it.
const restOfPath = (typedPath: string, scriptPaths: string[]): string | null => {
  const typed = typedPath.startsWith(CURRENT_FOLDER) ? typedPath.slice(CURRENT_FOLDER.length) : typedPath;
  const path = scriptPaths.find((candidate) => candidate.length > typed.length && candidate.startsWith(typed));

  if (path === undefined) {
    return null;
  }

  const name = path.slice(0, -SCRIPT_EXTENSION.length);

  return typed.length < name.length ? name.slice(typed.length) : path.slice(typed.length);
};

const fromProjectFiles = (importText: string, after: string, scriptPaths: string[]): string | null => {
  if (importText === '') {
    const first = scriptPaths[0];

    return first === undefined ? null : `"${CURRENT_FOLDER}${first.slice(0, -SCRIPT_EXTENSION.length)}"`;
  }

  const isQuoted = importText.startsWith('"');
  const typedPath = isQuoted ? importText.slice(1) : importText;

  if (typedPath.includes('"')) {
    return null;
  }

  const rest = restOfPath(typedPath, scriptPaths);

  if (rest === null) {
    return null;
  }

  const folder = typedPath === '' ? CURRENT_FOLDER : '';
  const closingQuote = isQuoted && !after.startsWith('"') ? '"' : '';

  return `${folder}${rest}${closingQuote}`;
};

interface FunctionSignature {
  name: string;
  parameters: string[];
}

const declaredIn = (source: string): Statement[] => {
  try {
    return parse(source);
  } catch {
    return [];
  }
};

const signaturesIn = (statements: Statement[]): FunctionSignature[] =>
  statements.flatMap((statement) =>
    statement.kind === 'functionDeclaration' ? [{ name: statement.name, parameters: statement.parameters ?? [] }] : [],
  );

// Functions of this file and of the files it imports, because only those exist when it runs.
const reachableFunctions = (document: string, scripts: Record<string, string>): FunctionSignature[] => {
  const statements = declaredIn(document);
  const imported = statements.flatMap((statement) => {
    const path = statement.kind === 'import' ? importCandidates('', statement.name).at(-1) : undefined;
    const source = path === undefined ? undefined : scripts[path];

    return source === undefined ? [] : signaturesIn(declaredIn(source));
  });

  return [...signaturesIn(statements), ...imported];
};

const isDeclaringFunction = (typedWords: string[]): boolean =>
  functionPhrases.includes(typedWords[0] ?? '') && typedWords.length > 1;

const fromFunctions = (
  typedWord: string,
  after: string,
  document: string,
  scripts: Record<string, string>,
): string | null => {
  if (after.startsWith('(')) {
    return null;
  }

  const found = reachableFunctions(document, scripts)
    .filter(({ name }) => normalize(name).startsWith(typedWord))
    .sort((first, second) => first.name.length - second.name.length)[0];

  return found === undefined ? null : `${found.name.slice(typedWord.length)}(${found.parameters.join(', ')})`;
};

export const suggestCompletion = (
  before: string,
  after: string,
  document: string,
  locale: Locale,
  scripts: Record<string, string> = {},
): string | null => {
  const importText = importTextOf(before);

  if (importText !== null && !INSIDE_WORD.test(after)) {
    const path = fromProjectFiles(importText, after, Object.keys(scripts));

    if (path !== null) {
      return path;
    }
  }

  const typedLine = normalize(before.trimStart());
  const typedWords = typedLine.split(/\s+/).filter(Boolean);
  const typedWord = /\s$/.test(before) ? '' : (typedWords.at(-1) ?? '');

  if (typedLine.length < MINIMUM_TYPED || INSIDE_WORD.test(after) || isInsideStringOrComment(before)) {
    return null;
  }

  if (typedWord === '') {
    return null;
  }

  const call =
    typedWord.length < MINIMUM_TYPED || isDeclaringFunction(typedWords)
      ? null
      : fromFunctions(typedWord, after, document, scripts);

  return (
    call ??
    fromStarters(typedLine, locale) ??
    fromPhrases(typedWords) ??
    (typedWord.length < MINIMUM_TYPED ? null : fromNames(typedWord, document))
  );
};
