import { parse } from './parser';
import { readScriptVersion } from './version';

const collectLines = (node: unknown, lines: Set<number>): void => {
  if (Array.isArray(node)) {
    node.forEach((item) => {
      collectLines(item, lines);
    });
  } else if (typeof node === 'object' && node !== null) {
    const record = node as Record<string, unknown>;

    if (typeof record['line'] === 'number') {
      lines.add(record['line']);
    }

    Object.values(record).forEach((value) => {
      collectLines(value, lines);
    });
  }
};

export const snapBreakpoints = (source: string, breakpoints: number[]): number[] => {
  const lines = new Set<number>();
  collectLines(parse(readScriptVersion(source).body), lines);
  const sorted = [...lines].sort((first, second) => first - second);

  return breakpoints.flatMap((breakpoint) => sorted.find((line) => line >= breakpoint) ?? []);
};
