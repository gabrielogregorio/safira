import { render, screen } from '@testing-library/react';
import { SafiraCode, splitHighlightedCode } from './SafiraCode';

describe('SafiraCode', () => {
  it('keeps every character of the code', () => {
    const code = 'x = 1\nmostre "oi" # nota';

    expect(
      splitHighlightedCode(code)
        .map((piece) => piece.text)
        .join(''),
    ).toBe(code);
  });

  it('colors commands', () => {
    render(<SafiraCode code='mostre "oi"' />);

    expect(screen.getByText('mostre')).toHaveClass('syntax-exibicao');
    expect(screen.getByText('"oi"')).toHaveClass('syntax-string');
  });
});
