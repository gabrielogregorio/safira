import { driveExecution } from '@/language/driver';
import { Interpreter, SafiraError } from '@/language/interpreter';
import type { Locale } from '@/language/messages';
import { parse } from '@/language/parser';
import { readScriptVersion } from '@/language/version';
import { VirtualFileSystem } from '@/language/virtualFileSystem';

export interface CheckCase {
  inputs?: string[];
  shows?: string[];
  hides?: string[];
}

export interface LessonCheck {
  /** Names of syntax kinds that must appear. `a|b` accepts either one. */
  uses?: string[];
  /** Compare upper and lower case too. Everything else about the text stays forgiving. */
  exact?: boolean;
  hint: string;
  cases: CheckCase[];
}

export type CheckFailureReason = 'command' | 'missing' | 'unexpected' | 'error' | 'limit';

export type CheckResult =
  { passed: true } | { passed: false; reason: CheckFailureReason; text: string; inputs: string[]; line?: number };

export interface CheckRequest {
  file: string;
  files: Record<string, string>;
  locale: Locale;
  check: LessonCheck;
}

const MAXIMUM_STEPS = 200_000;
const MAXIMUM_OUTPUT_ITEMS = 20_000;
const COMBINING_MARKS = /\p{M}/gu;
const NOT_LETTER_OR_NUMBER = /[^\p{L}\p{N}]+/gu;

/** Beginners should not fail because of a comma, an accent or a capital letter. */
export const normalizeOutput = (text: string, isExact = false): string => {
  const plain = text.normalize('NFD').replace(COMBINING_MARKS, '').replace(NOT_LETTER_OR_NUMBER, ' ').trim();

  return isExact ? plain : plain.toLowerCase();
};

const collectKinds = (node: unknown, kinds: Set<string>): Set<string> => {
  if (Array.isArray(node)) {
    node.forEach((item) => collectKinds(item, kinds));
  } else if (typeof node === 'object' && node !== null) {
    const { kind } = node as { kind?: unknown };

    if (typeof kind === 'string') {
      kinds.add(kind);
    }

    Object.values(node).forEach((value) => collectKinds(value, kinds));
  }

  return kinds;
};

const hasRequiredCommands = (source: string, uses: string[]): boolean => {
  const kinds = collectKinds(parse(readScriptVersion(source).body), new Set());

  return uses.every((options) => options.split('|').some((kind) => kinds.has(kind)));
};

class LimitReached extends Error {}

interface ProgramRun {
  output: string;
  failure: SafiraError | null;
  isOverLimit: boolean;
}

const runProgram = async (request: CheckRequest, inputs: string[]): Promise<ProgramRun> => {
  const interpreter = new Interpreter({ files: new VirtualFileSystem(request.files), locale: request.locale });
  const queue = [...inputs];
  const texts: string[] = [];
  let steps = 0;

  const countStep = (): undefined => {
    steps += 1;

    if (steps > MAXIMUM_STEPS) {
      throw new LimitReached();
    }

    return undefined;
  };

  try {
    await driveExecution(interpreter.run(request.file), {
      onStep: countStep,
      onOutput: (_inline, text) => {
        texts.push(text);

        if (texts.length > MAXIMUM_OUTPUT_ITEMS) {
          throw new LimitReached();
        }
      },
      onClear: () => undefined,
      onInput: () => Promise.resolve(queue.shift() ?? ''),
      onSleep: () => Promise.resolve(),
      onTone: () => Promise.resolve(),
      onFilesChanged: () => undefined,
    });
  } catch (error) {
    if (error instanceof LimitReached) {
      return { output: '', failure: null, isOverLimit: true };
    }

    if (error instanceof SafiraError) {
      return { output: texts.join(' '), failure: error, isOverLimit: false };
    }

    throw error;
  }

  return { output: texts.join(' '), failure: null, isOverLimit: false };
};

const findPhrase = (output: string, phrase: string, from: number): number => {
  // Only letters and numbers are left here, so the phrase is safe inside a pattern.
  const match = new RegExp(`(?<![\\p{L}\\p{N}])${phrase}(?![\\p{L}\\p{N}])`, 'gu');
  match.lastIndex = from;
  const found = match.exec(output);

  return found === null ? -1 : found.index + found[0].length;
};

const findPhraseInsideText = (output: string, phrase: string, from: number, isLatin: boolean): number => {
  if (isLatin) {
    return findPhrase(output, phrase, from);
  }

  // Chinese and Japanese have no spaces, so a word boundary would reject a correct sentence.
  const index = output.indexOf(phrase, from);

  return index === -1 ? -1 : index + phrase.length;
};

const isLatinText = (text: string): boolean => !/[\p{Script=Han}\p{Script=Hiragana}\p{Script=Katakana}]/u.test(text);

const checkCase = async (request: CheckRequest, testCase: CheckCase): Promise<CheckResult> => {
  const inputs = testCase.inputs ?? [];
  const { output, failure, isOverLimit } = await runProgram(request, inputs);
  const isExact = request.check.exact === true;

  if (isOverLimit) {
    return { passed: false, reason: 'limit', text: '', inputs };
  }

  if (failure !== null) {
    return { passed: false, reason: 'error', text: failure.message, inputs, line: failure.line };
  }

  const normalized = normalizeOutput(output, isExact);
  let position = 0;

  for (const text of testCase.shows ?? []) {
    const phrase = normalizeOutput(text, isExact);
    const found = findPhraseInsideText(normalized, phrase, position, isLatinText(phrase));

    if (found === -1) {
      return { passed: false, reason: 'missing', text, inputs };
    }

    position = found;
  }

  for (const text of testCase.hides ?? []) {
    const phrase = normalizeOutput(text, isExact);

    if (findPhraseInsideText(normalized, phrase, 0, isLatinText(phrase)) !== -1) {
      return { passed: false, reason: 'unexpected', text, inputs };
    }
  }

  return { passed: true };
};

export const checkProgram = async (request: CheckRequest): Promise<CheckResult> => {
  const source = request.files[request.file] ?? '';

  if (!hasRequiredCommands(source, request.check.uses ?? [])) {
    return { passed: false, reason: 'command', text: '', inputs: [] };
  }

  for (const testCase of request.check.cases) {
    const result = await checkCase(request, testCase);

    if (!result.passed) {
      return result;
    }
  }

  return { passed: true };
};
