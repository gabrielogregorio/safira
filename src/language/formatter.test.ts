import { formatCode } from './formatter';

describe('formatCode', () => {
  it('indents nested blocks with four spaces', () => {
    expect(formatCode('se 1 == 1 {\nmostre 1\nse 2 == 2 {\n      mostre 2\n   }\n}')).toBe(
      'se 1 == 1 {\n    mostre 1\n    se 2 == 2 {\n        mostre 2\n    }\n}',
    );
  });

  it('keeps a block that opens and closes on the same line at the same level', () => {
    expect(formatCode('se 1 == 1 { pare }\nmostre 1')).toBe('se 1 == 1 { pare }\nmostre 1');
  });

  it('does not go below zero with an extra closing brace', () => {
    expect(formatCode('}\nmostre 1')).toBe('}\nmostre 1');
  });
});
