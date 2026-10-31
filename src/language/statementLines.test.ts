import { snapBreakpoints } from './statementLines';

describe('snapBreakpoints', () => {
  it('keeps a breakpoint that is on a command', () => {
    expect(snapBreakpoints('mostre 1\nmostre 2', [2])).toEqual([2]);
  });

  it('moves a breakpoint on a comment or an empty line to the next command', () => {
    expect(snapBreakpoints('# nota\n\nmostre 1', [1, 2])).toEqual([3, 3]);
  });

  it('finds commands inside blocks and functions', () => {
    expect(snapBreakpoints('funcao f {\n# nota\nmostre 1\n}', [2])).toEqual([3]);
  });

  it('drops a breakpoint after the last command', () => {
    expect(snapBreakpoints('mostre 1\n\n', [3])).toEqual([]);
  });

  it('counts lines after the hidden version line', () => {
    expect(snapBreakpoints('#safira 0.9\n# nota\nmostre 1', [1])).toEqual([2]);
  });
});
