import { appendOutput, EMPTY_TERMINAL, MAXIMUM_TERMINAL_LINES } from './terminalBuffer';

const line = (text: string) => ({ inline: false, text, color: '' });
const inline = (text: string) => ({ inline: true, text, color: '#fff' });

describe('appendOutput', () => {
  it('puts each mostre on its own line', () => {
    expect(appendOutput(EMPTY_TERMINAL, [line('a'), line('b')]).lines).toHaveLength(2);
  });

  it('joins mostre nessa linha on the same line', () => {
    const result = appendOutput(EMPTY_TERMINAL, [inline('a'), inline('b')]);

    expect(result.lines.map((segments) => segments.map((segment) => segment.text))).toEqual([['a', 'b']]);
    expect(result.isLastLineOpen).toBe(true);
  });

  it('closes an open line with mostre', () => {
    const result = appendOutput(EMPTY_TERMINAL, [inline('a'), line('b'), line('c')]);

    expect(result.lines.map((segments) => segments.length)).toEqual([2, 1]);
    expect(result.isLastLineOpen).toBe(false);
  });

  it('keeps an inline line open between batches', () => {
    const first = appendOutput(EMPTY_TERMINAL, [inline('a')]);

    expect(appendOutput(first, [line('b')]).lines).toHaveLength(1);
  });

  it('keeps only the most recent lines', () => {
    const items = Array.from({ length: MAXIMUM_TERMINAL_LINES + 1 }, (_value, index) => line(String(index)));
    const result = appendOutput(EMPTY_TERMINAL, items);

    expect(result.lines).toHaveLength(MAXIMUM_TERMINAL_LINES);
    expect(result.lines[0]?.[0]?.text).toBe('1');
  });
});
