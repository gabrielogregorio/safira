import commands from '../commands.json';
import { formatCode } from '../formatter';
import { parse } from '../parser';
import { runScript } from '../testHarness';
import type { Dictionary } from './dialects';
import { CHINESE, ENGLISH, JAPANESE, PORTUGUESE, SPANISH } from './dialects';
import type { Scenario } from './scenarios';
import {
  BLOCKS,
  CLOSING_STATEMENTS,
  COMPARISONS,
  CONSUMERS,
  STATEMENTS,
  SYMBOL_COMPARISONS,
  VALUES,
} from './scenarios';

const MARKER = /\[([a-zA-Z_]+)\]/g;
const ALTERNATIVES: Record<string, string[]> = Object.fromEntries(
  Object.entries(commands).map(([key, { phrases }]) => [key, phrases]),
);
ALTERNATIVES['digitadoNumero'] = [];
// `escreva` keeps the line open, as beside `escreval` in school pseudocode. `legacyGolden.json` records it.
ALTERNATIVES['mostre'] = (ALTERNATIVES['mostre'] ?? []).filter((phrase) => phrase !== 'escreva');

const fill = (code: string, dictionary: Dictionary): string =>
  code.replace(MARKER, (_marker, key: string) => dictionary[key] ?? `<<${key}>>`);

const renderLines = async (
  source: string,
  inputs: string[] = [],
): Promise<{ lines: string[]; error: string | null }> => {
  const { events, error } = await runScript(source, inputs);
  const lines: string[] = [];
  let isOpen = false;

  for (const event of events) {
    if (event.type === 'clear') {
      lines.length = 0;
      isOpen = false;
    } else if (isOpen) {
      lines[lines.length - 1] += event.text ?? '';
      isOpen = event.type === 'inline';
    } else {
      lines.push(event.text ?? '');
      isOpen = event.type === 'inline';
    }
  }

  return { lines, error: error?.message ?? null };
};

const describeProblem = async (
  label: string,
  source: string,
  expected: string[],
  inputs?: string[],
): Promise<string[]> => {
  const { lines, error } = await renderLines(source, inputs);

  if (error === null && JSON.stringify(lines) === JSON.stringify(expected)) {
    return [];
  }

  const details = [
    label,
    `    code: ${JSON.stringify(source)}`,
    `    want: ${JSON.stringify(expected)}`,
    `    got:  ${JSON.stringify(lines)}`,
    ...(error === null ? [] : [`    error: ${error}`]),
  ];

  return [details.join('
')];
};

const collect = async (checks: Promise<string[]>[]): Promise<string[]> => (await Promise.all(checks)).flat();

const report = (problems: string[]): void => {
  expect(problems.length === 0 ? '' : `${String(problems.length)} problems\n${problems.slice(0, 12).join('\n')}`).toBe(
    '',
  );
};

const stripLines = (node: unknown): unknown => {
  if (Array.isArray(node)) {
    return node.map(stripLines);
  }

  if (typeof node === 'object' && node !== null) {
    return Object.fromEntries(
      Object.entries(node)
        .filter(([key]) => key !== 'line' && key !== 'variableName')
        .map(([key, value]) => [key, stripLines(value)]),
    );
  }

  return node;
};

const syntaxOf = (source: string): string => JSON.stringify(stripLines(parse(source)));

const uniqueInputs = (first: Scenario, second: Scenario): string[] => [
  ...(first.inputs ?? []),
  ...(second.inputs ?? []),
];

const indent = (code: string): string =>
  code
    .split('\n')
    .map((line) => `  ${line}`)
    .join('\n');

const usesFiles = ({ name }: Scenario): boolean => name.startsWith('file') || name === 'import';

const PORTUGUESE_COMMANDS = PORTUGUESE;

const showBoolean = (value: boolean): string => (value ? 'True' : 'False');

// Variables are global, so two nested loops need their own counters.
const atDepth = (blockCode: string, depth: number): string => blockCode.replace(/\bz(\d)\b/g, `z$1d${String(depth)}`);

export const defineCommandMatrix = (languageName: string, dictionary: Dictionary): void => {
  const code = (text: string): string => fill(text, dictionary);

  describe(`every command in ${languageName}`, () => {
    it('knows every word used by the scenarios', () => {
      const sources = [...STATEMENTS, ...CLOSING_STATEMENTS].map((scenario) => code(scenario.code));

      expect(sources.filter((source) => source.includes('<<'))).toEqual([]);
    });

    it.each([...STATEMENTS, ...CLOSING_STATEMENTS].map((scenario) => [scenario.name, scenario] as const))(
      '%s',
      async (_name, scenario) => {
        report(await describeProblem(scenario.name, code(scenario.code), scenario.output, scenario.inputs));
      },
    );

    it('means the same as in Portuguese', () => {
      const different = [...STATEMENTS, ...CLOSING_STATEMENTS].filter(
        (scenario) =>
          syntaxOf(fill(scenario.code, { ...dictionary, azul: 'azul' })) !==
          syntaxOf(fill(scenario.code, PORTUGUESE_COMMANDS)),
      );

      expect(different.map((scenario) => scenario.name)).toEqual([]);
    });
  });

  describe(`every phrase in ${languageName}`, () => {
    const keysOf = (scenario: Scenario): string[] => [
      ...new Set([...scenario.code.matchAll(MARKER)].map((match) => match[1])),
    ];

    it.each(STATEMENTS.map((scenario) => [scenario.name, scenario] as const))('%s', async (_name, scenario) => {
      const checks = keysOf(scenario).flatMap((key) =>
        (ALTERNATIVES[key] ?? []).map((phrase) =>
          describeProblem(
            `[${key}] as "${phrase}"`,
            code(scenario.code.replaceAll(`[${key}]`, phrase)),
            scenario.output,
            scenario.inputs,
          ),
        ),
      );

      report(await collect(checks));
    });
  });

  describe(`pairs in order in ${languageName}`, () => {
    it('runs every statement after every other', async () => {
      const checks = STATEMENTS.flatMap((first) =>
        STATEMENTS.filter((second) => !(usesFiles(first) && usesFiles(second))).map((second) =>
          describeProblem(
            `${first.name} then ${second.name}`,
            `${code(first.code)}\n${code(second.code)}`,
            [...first.output, ...second.output],
            uniqueInputs(first, second),
          ),
        ),
      );

      report(await collect(checks));
    }, 120_000);
  });

  describe(`nesting in ${languageName}`, () => {
    const repeated = <Item>(items: Item[], times: number): Item[] => Array.from({ length: times }, () => items).flat();
    const repeatedInputs = (scenario: Scenario, times: number): string[] => repeated(scenario.inputs ?? [], times);
    // A function or an import inside a block is declared once per pass, so these stay outside the loops of the test.
    const nestable = STATEMENTS.filter(
      (scenario) => !usesFiles(scenario) && !['break', 'continue'].includes(scenario.name),
    );

    it.each(BLOCKS.map((block) => [block.name, block] as const))('every statement inside %s', async (_name, block) => {
      const checks = nestable.map((scenario) =>
        describeProblem(
          `${scenario.name} inside ${block.name}`,
          code([block.setup ?? '', block.code.replace('{}', indent(scenario.code))].join('\n')),
          repeated(scenario.output, block.times),
          repeatedInputs(scenario, block.times),
        ),
      );

      report(await collect(checks));
    });

    it('every block inside every block', async () => {
      const inner = '[mostre] "n"';
      const checks = BLOCKS.flatMap((outer) =>
        BLOCKS.map((block) => {
          const middle = atDepth(block.code, 2).replace('{}', indent(inner));
          const source = [
            outer.setup ?? '',
            atDepth(block.setup ?? '', 2),
            outer.code.replace('{}', indent(middle)),
          ].join('\n');

          return describeProblem(
            `${block.name} inside ${outer.name}`,
            code(source),
            repeated(['n'], outer.times * block.times),
          );
        }),
      );

      report(await collect(checks));
    });

    it('three levels of blocks', async () => {
      const levels = BLOCKS.filter((block) => block.name !== 'function');
      const checks = levels.flatMap((first) =>
        levels.flatMap((second) =>
          levels.map((third) => {
            const body = atDepth(third.code, 3).replace('{}', '  [mostre] "n"');
            const middle = atDepth(second.code, 2).replace('{}', indent(body));
            const source = [
              first.setup ?? '',
              atDepth(second.setup ?? '', 2),
              atDepth(third.setup ?? '', 3),
              first.code.replace('{}', indent(middle)),
            ].join('\n');

            return describeProblem(
              `${first.name} > ${second.name} > ${third.name}`,
              code(source),
              repeated(['n'], first.times * second.times * third.times),
            );
          }),
        ),
      );

      report(await collect(checks));
    }, 60_000);
  });

  describe(`values in ${languageName}`, () => {
    it.each(CONSUMERS.map((consumer) => [consumer.name, consumer] as const))(
      'every value in %s',
      async (_name, consumer) => {
        const checks = VALUES.map((value) => {
          const source = [value.setup ?? '', consumer.code.replaceAll('{}', value.value)].join('\n');

          return describeProblem(`${value.name} in ${consumer.name}`, code(source), [value.shown]);
        });

        report(await collect(checks));
      },
    );

    it('every pair of numbers with every operator', async () => {
      const numbers = [-2, 0, 1, 2.5, 10];
      const operators: [string, (first: number, second: number) => number][] = [
        ['+', (first, second) => first + second],
        ['-', (first, second) => first - second],
        ['*', (first, second) => first * second],
        ['[matematica_add]', (first, second) => first + second],
        ['[matematica_sub]', (first, second) => first - second],
        ['[matematica_mult]', (first, second) => first * second],
      ];
      const checks = numbers.flatMap((first) =>
        numbers.flatMap((second) =>
          operators.map(([operator, calculate]) =>
            describeProblem(
              `${String(first)} ${operator} ${String(second)}`,
              code(`a1 = ${String(first)}\na2 = ${String(second)}\n[mostre] a1 ${operator} a2`),
              [String(calculate(first, second))],
            ),
          ),
        ),
      );

      report(await collect(checks));
    });
  });

  describe(`comparisons in ${languageName}`, () => {
    const pairs: [number, number][] = [
      [1, 2],
      [2, 2],
      [3, 2],
    ];

    it.each(COMPARISONS.map((comparison) => [comparison.key, comparison] as const))('%s', async (_key, comparison) => {
      const checks = pairs.flatMap(([first, second], index) => [
        describeProblem(
          `${comparison.key} value`,
          code(`[mostre] ${String(first)} [${comparison.key}] ${String(second)}`),
          [showBoolean(comparison.results[index])],
        ),
        describeProblem(
          `${comparison.key} in if`,
          code(
            `[se] ${String(first)} [${comparison.key}] ${String(second)} [se_final] {\n  [mostre] "s"\n} [se_nao] {\n  [mostre] "n"\n}`,
          ),
          [comparison.results[index] ? 's' : 'n'],
        ),
      ]);

      report(await collect(checks));
    });

    it.each(SYMBOL_COMPARISONS.map((comparison) => [comparison.symbol, comparison] as const))(
      '%s',
      async (_symbol, comparison) => {
        const checks = pairs.map(([first, second], index) =>
          describeProblem(comparison.symbol, code(`[mostre] ${String(first)} ${comparison.symbol} ${String(second)}`), [
            showBoolean(comparison.results[index]),
          ]),
        );

        report(await collect(checks));
      },
    );

    it('and, or in every order', async () => {
      const conditions: [string, boolean][] = [
        ['1 [logico_igual] 1', true],
        ['1 [logico_igual] 2', false],
      ];
      const checks = conditions.flatMap(([first, firstValue]) =>
        conditions.flatMap(([second, secondValue]) => [
          describeProblem(
            'and',
            code(`[se] ${first} [logico_e] ${second} [se_final] {\n  [mostre] "s"\n} [se_nao] {\n  [mostre] "n"\n}`),
            [firstValue && secondValue ? 's' : 'n'],
          ),
          describeProblem(
            'or',
            code(`[se] ${first} [logico_ou] ${second} [se_final] {\n  [mostre] "s"\n} [se_nao] {\n  [mostre] "n"\n}`),
            [firstValue || secondValue ? 's' : 'n'],
          ),
        ]),
      );

      report(await collect(checks));
    });
  });

  describe(`the formatter in ${languageName}`, () => {
    it.each([...STATEMENTS, ...CLOSING_STATEMENTS].map((scenario) => [scenario.name, scenario] as const))(
      'keeps the meaning of %s',
      (_name, scenario) => {
        const source = code(scenario.code);

        expect(syntaxOf(formatCode(source))).toBe(syntaxOf(source));
      },
    );
  });
};

export const LANGUAGES = [PORTUGUESE, ENGLISH, SPANISH, CHINESE, JAPANESE];

export const defineLanguageMixture = (): void => {
  describe('languages mixed in one script', () => {
    it.each(STATEMENTS.map((scenario) => [scenario.name, scenario] as const))(
      '%s word by word',
      async (_name, scenario) => {
        const rotations = LANGUAGES.map((_language, shift) => {
          let index = shift;

          return scenario.code.replace(MARKER, (_marker, key: string) => {
            index += 1;

            return LANGUAGES[index % LANGUAGES.length][key] ?? key;
          });
        });

        report(
          await collect(
            rotations.map((source) => describeProblem(scenario.name, source, scenario.output, scenario.inputs)),
          ),
        );
      },
    );

    it('each line in another language', async () => {
      const checks = LANGUAGES.flatMap((first) =>
        LANGUAGES.map((second) =>
          describeProblem(
            'mixed lines',
            `${fill('[mostre] "a"', first)}\n${fill('[repita] 1 [repitaVezes] {', second)}\n${fill('[mostre] "b"', first)}\n}`,
            ['a', 'b'],
          ),
        ),
      );

      report(await collect(checks));
    });
  });
};
