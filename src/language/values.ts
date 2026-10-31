import type { Value } from './ast';

export type TypeName = 'string' | 'booleano' | 'float' | 'lista' | 'vazio';

export const typeNameOf = (value: Value): TypeName => {
  if (typeof value === 'string') {
    return 'string';
  }

  if (typeof value === 'boolean') {
    return 'booleano';
  }

  if (typeof value === 'number') {
    return 'float';
  }

  return Array.isArray(value) ? 'lista' : 'vazio';
};

const quoteListText = (text: string): string => {
  const quote = text.includes("'") && !text.includes('"') ? '"' : "'";

  return `${quote}${text}${quote}`;
};

const formatListItem = (value: Value): string =>
  typeof value === 'string' ? quoteListText(value) : formatValue(value);

export const formatValue = (value: Value): string => {
  if (typeof value === 'boolean') {
    return value ? 'True' : 'False';
  }

  if (Array.isArray(value)) {
    return `[${value.map(formatListItem).join(', ')}]`;
  }

  return value === null ? '' : String(value);
};

export const isTruthy = (value: Value): boolean => {
  if (Array.isArray(value)) {
    return value.length > 0;
  }

  return Boolean(value);
};

const toComparable = (value: Value): Value => (typeof value === 'boolean' ? Number(value) : value);

export const valuesAreEqual = (left: Value, right: Value): boolean => {
  if (Array.isArray(left) && Array.isArray(right)) {
    return left.length === right.length && left.every((item, index) => valuesAreEqual(item, right[index] ?? null));
  }

  return toComparable(left) === toComparable(right);
};

export const floorModulo = (dividend: number, divisor: number): number =>
  dividend - divisor * Math.floor(dividend / divisor);

export const capitalize = (text: string): string => text.charAt(0).toUpperCase() + text.slice(1).toLowerCase();

const SLICE_NO_STEP = 0;

export const sliceForward = (text: string, start: number, end: number, step: number | null): string => {
  const skip = step ?? SLICE_NO_STEP;
  let pending = skip;
  let result = '';

  for (let index = start; index <= end; index += 1) {
    if (pending === 0) {
      pending = skip;
      result += text.charAt(index - 1);
    } else {
      pending -= 1;
    }
  }

  return result;
};

export const sliceBackward = (text: string, start: number, end: number, step: number | null): string => {
  const skip = step ?? SLICE_NO_STEP;
  let pending = skip;
  let result = '';

  for (let index = end; index <= start; index += 1) {
    if (pending === 0) {
      pending = skip;
      result = text.charAt(start - index) + result;
    } else {
      pending -= 1;
    }
  }

  return result;
};
