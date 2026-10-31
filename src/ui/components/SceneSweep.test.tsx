import { fireEvent, render } from '@testing-library/react';
import { canAnimateScenes, SceneSweep } from './SceneSweep';

describe('SceneSweep', () => {
  it('warns when the wave finishes crossing the screen', () => {
    const onFinished = vi.fn();
    const { container } = render(<SceneSweep kind="language" onFinished={onFinished} />);
    const wave = container.querySelector('.scene-sweep-wave') as Element;
    fireEvent(wave, new Event('webkitAnimationEnd', { bubbles: true }));
    fireEvent(wave, new Event('animationend', { bubbles: true }));

    expect(onFinished).toHaveBeenCalledTimes(1);
  });

  it('is hidden from screen readers', () => {
    const { container } = render(<SceneSweep kind="theme" onFinished={vi.fn()} />);

    expect(container.firstChild).toHaveAttribute('aria-hidden', 'true');
  });

  it('does not animate without browser support', () => {
    expect(canAnimateScenes()).toBe(false);
  });

  it('respects the reduced motion preference', () => {
    vi.stubGlobal('matchMedia', () => ({ matches: false }));
    expect(canAnimateScenes()).toBe(false);

    vi.stubGlobal('matchMedia', () => ({ matches: true }));
    expect(canAnimateScenes()).toBe(true);

    vi.unstubAllGlobals();
  });
});
