import { act, render, renderHook, screen } from '@testing-library/react';
import { TypedLine, useTypedText } from './TypedText';

const withMotion = (hasMotion: boolean): void => {
  window.matchMedia = vi.fn().mockReturnValue({ matches: hasMotion });
};

describe('useTypedText', () => {
  afterEach(() => {
    vi.useRealTimers();
  });

  it('arrives whole without motion', () => {
    withMotion(false);

    expect(renderHook(() => useTypedText('oi')).result.current).toMatchObject({ shown: 'oi', isDone: true });
  });

  it('types letter by letter, counting an emoji as one', () => {
    withMotion(true);
    vi.useFakeTimers();
    const { result } = renderHook(() => useTypedText('a🎉b'));

    expect(result.current.shown).toBe('');

    act(() => {
      vi.advanceTimersByTime(50);
    });

    expect(result.current.shown).toBe('a🎉');

    act(() => {
      vi.advanceTimersByTime(30);
    });

    expect(result.current).toMatchObject({ shown: 'a🎉b', isDone: true });
  });

  it('finishes on demand and starts over with a new text', () => {
    withMotion(true);
    const { result, rerender } = renderHook(({ text }) => useTypedText(text), { initialProps: { text: 'longo' } });

    act(() => {
      result.current.finish();
    });

    expect(result.current.shown).toBe('longo');

    rerender({ text: 'novo' });

    expect(result.current).toMatchObject({ shown: '', isDone: false });
  });
});

describe('TypedLine', () => {
  afterEach(() => {
    vi.useRealTimers();
  });

  it('gives screen readers the whole sentence while the letters arrive', () => {
    withMotion(true);
    vi.useFakeTimers();
    const { container } = render(<TypedLine text="olá" />);

    act(() => {
      vi.advanceTimersByTime(25);
    });

    expect(container.querySelector('[aria-hidden="true"]')).toHaveTextContent(/^o$/);
    expect(screen.getByText('olá')).toHaveClass('visually-hidden');
  });

  it('becomes plain text when it finishes', () => {
    withMotion(false);
    const { container } = render(<TypedLine text="olá" />);

    expect(container.innerHTML).toBe('olá');
  });
});
