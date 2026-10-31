import { render } from '@testing-library/react';
import { SceneBackdrop } from './SceneBackdrop';

const layer = (container: HTMLElement, name: string): HTMLElement =>
  container.querySelector(`.scenery-${name}`) as HTMLElement;

describe('SceneBackdrop', () => {
  it('keeps every scene mounted so that they can cross fade', () => {
    const { container } = render(<SceneBackdrop phase={1} />);

    expect(container.querySelectorAll('.scenery-layer')).toHaveLength(3);
  });

  it('activates only the scene of the phase', () => {
    const { container } = render(<SceneBackdrop phase={1} />);

    expect(layer(container, 'dark')).toHaveAttribute('data-active', 'true');
    expect(layer(container, 'light')).toHaveAttribute('data-active', 'false');
    expect(layer(container, 'dark').style.opacity).toBe('1');
    expect(layer(container, 'light').style.opacity).toBe('0');
  });

  it('blends two scenes halfway through time', () => {
    const { container } = render(<SceneBackdrop phase={0.5} />);

    expect(Number(layer(container, 'light').style.opacity)).toBeCloseTo(0.5);
    expect(Number(layer(container, 'dark').style.opacity)).toBeCloseTo(0.5);
  });

  it('moves the sun and the moon with the time', () => {
    const { container } = render(<SceneBackdrop phase={0.5} />);

    expect(layer(container, 'light').style.getPropertyValue('--sky-offset')).toBe('0.5');
    expect(layer(container, 'dark').style.getPropertyValue('--sky-offset')).toBe('-0.5');
  });

  it('has stars only at night', () => {
    const { container } = render(<SceneBackdrop phase={1} />);

    expect(layer(container, 'dark').querySelectorAll('.scenery-twinkle').length).toBeGreaterThan(5);
    expect(layer(container, 'light').querySelector('.scenery-twinkle')).toBeNull();
  });

  it('stays out of the reach of screen readers', () => {
    const { container } = render(<SceneBackdrop phase={0} />);

    expect(container.firstChild).toHaveAttribute('aria-hidden', 'true');
  });
});
