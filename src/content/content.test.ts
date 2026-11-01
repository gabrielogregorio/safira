import { LOCALES } from '@/i18n/i18n';
import { parse } from '@/language/parser';
import { runScript } from '@/language/testHarness';
import { readScriptVersion } from '@/language/version';
import { checkProgram } from '@/lessons/lessonCheck';
import { examplesOf, findExampleByPrefix, lessonsOf, toExample } from './content';

const EXAMPLE_COUNT = 34;
const LESSON_COUNT = 13;
const MAIN_FILE = 'main.safira';
const PROGRAM_INPUTS = ['2', '2', '2', ...Array.from({ length: 20 }, () => '0')];
const LONG_CODE_LINES = 16;
const LATIN_COMMAND =
  /^\s*(show|print|if|else|repeat|while|for|wait|play|function|return|try|list|add|remove|create|read|mostre|se|repita)\b/;
const LATIN_COMMAND_LINE: Partial<Record<(typeof LOCALES)[number]['id'], RegExp>> = {
  'zh-cn': LATIN_COMMAND,
  ja: LATIN_COMMAND,
};

const invalidLines = (source: string): string[] =>
  parse(readScriptVersion(source).body).flatMap((statement) =>
    statement.kind === 'invalid' ? [statement.detail] : [],
  );

const scriptLines = (source: string): string[] =>
  source.split('\n').filter((line) => line.trim() !== '' && !line.trim().startsWith('#'));

const checkOf = (locale: (typeof LOCALES)[number]['id']) =>
  lessonsOf(locale).flatMap((lesson) =>
    lesson.steps.flatMap((step, index) =>
      step.check === null ? [] : [{ name: `${lesson.id} step ${String(index + 1)}`, step, check: step.check }],
    ),
  );

describe.each(LOCALES.map((locale) => [locale.id] as const))('content in %s', (locale) => {
  const examples = examplesOf(locale);
  const lessons = lessonsOf(locale);

  it('has the same examples and lessons as Portuguese', () => {
    expect(examples).toHaveLength(EXAMPLE_COUNT);
    expect(lessons).toHaveLength(LESSON_COUNT);
    expect(examples.map((example) => example.id)).toEqual(examplesOf('pt-br').map((example) => example.id));
    expect(
      lessons.map((lesson) => [lesson.id, lesson.steps.length, lesson.steps.map((step) => step.check !== null)]),
    ).toEqual(
      lessonsOf('pt-br').map((lesson) => [
        lesson.id,
        lesson.steps.length,
        lesson.steps.map((step) => step.check !== null),
      ]),
    );
  });

  it('names every example and lesson', () => {
    expect(examples.filter((example) => example.title === example.id)).toEqual([]);
    expect(lessons.filter((lesson) => lesson.title === lesson.id)).toEqual([]);
  });

  it('marks the ready-made programs with an emoji', () => {
    const programs = examples.filter((example) => example.id.startsWith('programa-'));

    expect(programs.filter((program) => !/^\p{Extended_Pictographic}/u.test(program.title))).toEqual([]);
  });

  it.each(examples.map((example) => [example.id, example.text] as const))('%s is short and valid', async (id, text) => {
    expect(readScriptVersion(text)).toMatchObject({ version: '0.9', isDeclared: true });
    expect(scriptLines(text).length).toBeLessThanOrEqual(LONG_CODE_LINES);

    if (!id.startsWith('21')) {
      expect(invalidLines(text)).toEqual([]);
    }

    expect((await runScript(text, PROGRAM_INPUTS)).error).toBeNull();
  });

  it('only teaches code that runs', async () => {
    for (const lesson of lessons) {
      for (const step of lesson.steps) {
        expect([lesson.id, step.title, invalidLines(step.code)]).toEqual([lesson.id, step.title, []]);

        if (step.check === null) {
          expect(scriptLines(step.code).length).toBeGreaterThan(0);
          expect((await runScript(step.code, PROGRAM_INPUTS)).error).toBeNull();
        }
      }
    }
  });

  it('every step teaches through comments in the code', () => {
    for (const lesson of lessons) {
      expect(lesson.steps.filter((step) => step.title === '' || !step.code.includes('#'))).toEqual([]);
      expect(lesson.steps.filter((step) => /```/.test(step.text))).toEqual([]);
    }
  });

  it.each(checkOf(locale).map(({ name, step, check }) => [name, step, check] as const))(
    '%s accepts its solution and rejects the starting code',
    async (_name, step, check) => {
      const run = (code: string) => checkProgram({ file: MAIN_FILE, files: { [MAIN_FILE]: code }, locale, check });

      expect(step.solution).not.toBeNull();
      await expect(run(step.solution ?? '')).resolves.toEqual({ passed: true });
      await expect(run(step.code)).resolves.toMatchObject({ passed: false });
    },
  );

  it('teaches with the commands of its language', () => {
    const scripts = [
      ...examples.map((example) => example.text),
      ...lessons.flatMap((lesson) => lesson.steps.flatMap((step) => [step.code, step.solution ?? ''])),
    ];
    const foreign = LATIN_COMMAND_LINE[locale];

    expect(
      foreign === undefined ? [] : scripts.flatMap((script) => script.split('\n')).filter((line) => foreign.test(line)),
    ).toEqual([]);
  });

  it('finds the example that explains a command', () => {
    expect(findExampleByPrefix(locale, '16')?.id).toBe('16-listas');
    expect(findExampleByPrefix(locale, '99')).toBeUndefined();
  });
});

describe('toExample', () => {
  it('names an example after its file when it has no title', () => {
    expect(toExample(['./pt-br/examples/01-sem-titulo.safira', 'mostre 1']).title).toBe('01-sem-titulo');
  });
});

describe('older scripts', () => {
  const legacy = import.meta.glob<string>('../language/legacyExamples/*.safira', {
    eager: true,
    query: '?raw',
    import: 'default',
  });

  it.each(Object.entries(legacy).filter(([path]) => !path.includes('21-tente')))('%s still parses', (_path, text) => {
    expect(invalidLines(text)).toEqual([]);
  });
});
