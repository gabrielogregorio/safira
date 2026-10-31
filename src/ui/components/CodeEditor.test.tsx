import { render, screen } from '@testing-library/react';
import { CodeEditor } from './CodeEditor';

const baseProps = {
  label: 'Editor',
  fontSize: 15,
  codeFont: 'mono' as const,
  suggestions: true,
  locale: 'pt-br' as const,
  scripts: {},
  breakpoints: [],
  debugLine: null,
  errorLine: null,
  onChange: vi.fn(),
  onToggleBreakpoint: vi.fn(),
  onCursorChange: vi.fn(),
};

const content = (): Element => screen.getByRole('textbox', { name: 'Editor' });

describe('CodeEditor', () => {
  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it('shows the code with its colors', () => {
    render(<CodeEditor {...baseProps} value='mostre "oi"' />);

    expect(content()).toHaveTextContent('mostre "oi"');
    expect(document.querySelector('.syntax-exibicao')).toHaveTextContent('mostre');
  });

  it('takes the focus when it opens', () => {
    render(<CodeEditor {...baseProps} value="" />);

    expect(content()).toHaveFocus();
  });

  it('does not open the keyboard on a touch screen', () => {
    vi.stubGlobal('matchMedia', () => ({ matches: true, addListener: vi.fn(), removeListener: vi.fn() }));
    render(<CodeEditor {...baseProps} value="" />);

    expect(content()).not.toHaveFocus();
  });

  it('marks active breakpoints', () => {
    render(<CodeEditor {...baseProps} value={'a\nb'} breakpoints={[2]} />);

    expect(document.querySelectorAll('.breakpoint-dot-active')).toHaveLength(1);
  });

  it('marks the paused line and the failed line', () => {
    render(<CodeEditor {...baseProps} value={'a\nb'} debugLine={1} errorLine={2} />);

    expect(document.querySelector('.editor-line-debug')).toHaveTextContent('a');
    expect(document.querySelector('.editor-line-error')).toHaveTextContent('b');
  });

  it('follows a value changed from outside', () => {
    const { rerender } = render(<CodeEditor {...baseProps} value="a" />);
    rerender(<CodeEditor {...baseProps} value="b" />);

    expect(content()).toHaveTextContent('b');
  });

  it('ignores a line outside of the text', () => {
    render(<CodeEditor {...baseProps} value="a" breakpoints={[9]} errorLine={9} />);

    expect(document.querySelector('.breakpoint-dot-active')).toBeNull();
    expect(document.querySelector('.editor-line-error')).toBeNull();
  });
});
