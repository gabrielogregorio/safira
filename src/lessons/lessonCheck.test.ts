import { Interpreter } from '@/language/interpreter';
import { runScript } from '@/language/testHarness';
import type { CheckRequest, LessonCheck } from './lessonCheck';
import { checkProgram, normalizeOutput } from './lessonCheck';

const FILE = 'main.safira';

const check = (source: string, lessonCheck: Omit<LessonCheck, 'hint'>, files = {}) => {
  const request: CheckRequest = {
    file: FILE,
    files: { ...files, [FILE]: source },
    locale: 'pt-br',
    check: { hint: 'Dica', ...lessonCheck },
  };

  return checkProgram(request);
};

describe('checkProgram', () => {
  it('answers with an empty text when the case has no more inputs', async () => {
    await expect(
      check('n = o que o usuario digitar\nmostre "[" + n + "]"\nse n == "" entao mostre "vazio"', {
        cases: [{ shows: ['vazio'] }],
      }),
    ).resolves.toEqual({ passed: true });
  });

  it('answers that no key is down', async () => {
    await expect(
      check('se apertar Enter entao mostre "sim" senao mostre "nao"', { cases: [{ shows: ['nao'] }] }),
    ).resolves.toEqual({ passed: true });
  });

  it('goes past a note without waiting for it', async () => {
    await expect(check('toque C por 9 segundos\nmostre "a"', { cases: [{ shows: ['a'] }] })).resolves.toEqual({
      passed: true,
    });
  });

  it('treats a file that does not exist as a program without commands', async () => {
    const request: CheckRequest = {
      file: 'nada.safira',
      files: {},
      locale: 'pt-br',
      check: { hint: 'Dica', uses: ['print'], cases: [] },
    };

    await expect(checkProgram(request)).resolves.toMatchObject({ passed: false, reason: 'command' });
  });

  it('does not hide an error that is not from the script', async () => {
    vi.spyOn(Interpreter.prototype, 'run').mockImplementationOnce(() => {
      throw new TypeError('quebrou');
    });

    await expect(check('mostre 1', { cases: [{}] })).rejects.toThrow(TypeError);
  });

  it('accepts a program that shows the text', async () => {
    await expect(check('mostre "Olá, mundo!"', { cases: [{ shows: ['Olá, mundo!'] }] })).resolves.toEqual({
      passed: true,
    });
  });

  it('forgives capitals, accents and punctuation', async () => {
    await expect(check('mostre "ola mundo"', { cases: [{ shows: ['Olá, Mundo!'] }] })).resolves.toEqual({
      passed: true,
    });
  });

  it('tells apart words glued together from a wrong text', async () => {
    await expect(
      check('c = "Lima"\nmostre "Eu moro em" + c', { cases: [{ shows: ['Eu moro em Lima'] }] }),
    ).resolves.toMatchObject({ reason: 'spacing' });
  });

  it('can demand exact capitals', async () => {
    await expect(check('mostre "safira"', { exact: true, cases: [{ shows: ['SAFIRA'] }] })).resolves.toMatchObject({
      passed: false,
      reason: 'missing',
      text: 'SAFIRA',
    });
  });

  it('wants the texts in order', async () => {
    await expect(check('mostre "b"\nmostre "a"', { cases: [{ shows: ['a', 'b'] }] })).resolves.toMatchObject({
      reason: 'missing',
      text: 'b',
    });
  });

  it('does not take a number inside another number', async () => {
    await expect(check('mostre 100', { cases: [{ shows: ['10'] }] })).resolves.toMatchObject({ reason: 'missing' });
  });

  it('finds a word inside a Chinese sentence', async () => {
    await expect(check('mostre "我住在利马"', { cases: [{ shows: ['利马'] }] })).resolves.toEqual({ passed: true });
  });

  it('feeds each case with its answers', async () => {
    const source = 'n = o número que o usuário digitar\nmostre n * 2';
    const cases = [
      { inputs: ['2'], shows: ['4'] },
      { inputs: ['5'], shows: ['10'] },
    ];

    await expect(check(source, { cases })).resolves.toEqual({ passed: true });
    await expect(check('n = entrada\nmostre 4', { cases })).resolves.toMatchObject({
      reason: 'missing',
      text: '10',
      inputs: ['5'],
    });
  });

  it('refuses a text that should not be there', async () => {
    await expect(check('mostre "par"\nmostre "ímpar"', { cases: [{ hides: ['ímpar'] }] })).resolves.toMatchObject({
      reason: 'unexpected',
      text: 'ímpar',
    });
  });

  it('asks for the commands of the lesson', async () => {
    await expect(check('mostre 1', { uses: ['repeat'], cases: [{ shows: ['1'] }] })).resolves.toMatchObject({
      reason: 'command',
    });
    await expect(
      check('repita 1 vezes {\n  mostre 1\n}', { uses: ['while|repeat'], cases: [{ shows: ['1'] }] }),
    ).resolves.toEqual({ passed: true });
  });

  it('finds commands nested in blocks and expressions', async () => {
    const source = 'se 1 for igual a 1 então {\n  n = um número aleatório entre 1 e 2\n  mostre "ok"\n}';

    await expect(check(source, { uses: ['random'], cases: [{ shows: ['ok'] }] })).resolves.toEqual({ passed: true });
  });

  it('reports the error of the program', async () => {
    await expect(check('mostre nada', { cases: [{ shows: ['1'] }] })).resolves.toMatchObject({
      reason: 'error',
      line: 1,
    });
  });

  it.each(['enquanto verdadeiro {\n  n = 1\n}', 'enquanto verdadeiro {\n  mostre 1\n}'])(
    'gives up on an endless program: %s',
    async (source) => {
      await expect(check(source, { cases: [{ shows: ['1'] }] })).resolves.toMatchObject({ reason: 'limit' });
    },
  );

  it('sees the other files of the project', async () => {
    await expect(
      check('importe "bib"\nmostre idade', { cases: [{ shows: ['25'] }] }, { 'bib.safira': 'idade = 25' }),
    ).resolves.toEqual({ passed: true });
  });
});

describe('normalizeOutput', () => {
  it('leaves only plain letters and numbers', () => {
    expect(normalizeOutput('  Olá,   MUNDO! 10 ')).toBe('ola mundo 10');
    expect(normalizeOutput('Olá!', true)).toBe('Ola');
  });
});

describe('a name without quotes', () => {
  it('reports which name has no value', async () => {
    const { error } = await runScript('cidade = lima');

    expect(error?.missingName).toBe('lima');
  });
});
