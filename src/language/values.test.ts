import {
  capitalize,
  floorModulo,
  formatValue,
  isTruthy,
  sliceBackward,
  sliceForward,
  typeNameOf,
  valuesAreEqual,
} from './values';

describe('values', () => {
  it.each([
    ['a', 'string'],
    [true, 'booleano'],
    [1, 'float'],
    [[1], 'lista'],
    [null, 'vazio'],
  ] as const)('names the type of %j', (value, name) => {
    expect(typeNameOf(value as never)).toBe(name);
  });

  it.each([
    [1.5, '1.5'],
    [3, '3'],
    [true, 'True'],
    [false, 'False'],
    [null, ''],
    ['oi', 'oi'],
    [[1, 'a', true], "[1, 'a', True]"],
    [["d'agua"], '["d\'agua"]'],
    [[[1]], '[[1]]'],
  ] as const)('prints %j as the original language did', (value, text) => {
    expect(formatValue(value as never)).toBe(text);
  });

  it.each([
    [0, false],
    ['', false],
    [[], false],
    [null, false],
    [1, true],
    ['0', true],
    [[0], true],
  ] as const)('treats %j as %s', (value, expected) => {
    expect(isTruthy(value as never)).toBe(expected);
  });

  it('compares like the original language', () => {
    expect(valuesAreEqual(1, 1)).toBe(true);
    expect(valuesAreEqual(true, 1)).toBe(true);
    expect(valuesAreEqual('1', 1)).toBe(false);
    expect(valuesAreEqual([1, 'a'], [1, 'a'])).toBe(true);
    expect(valuesAreEqual([1], [1, 2])).toBe(false);
  });

  it('keeps the sign of the divisor in a modulo', () => {
    expect(floorModulo(-7, 3)).toBe(2);
    expect(floorModulo(7, 3)).toBe(1);
  });

  it('capitalizes only the first letter', () => {
    expect(capitalize('sAfirA x')).toBe('Safira x');
  });

  it('slices forward from 1 and includes the end', () => {
    expect(sliceForward('abcdef', 1, 3, null)).toBe('abc');
  });

  it('skips letters in a slice with a step', () => {
    expect(sliceForward('abcdef', 1, 6, 1)).toBe('bdf');
  });

  it('keeps the original backward slice', () => {
    expect(sliceBackward('abcdef', 5, 2, null)).toBe('abcd');
  });
});
