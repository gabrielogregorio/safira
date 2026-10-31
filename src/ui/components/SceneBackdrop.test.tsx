import { render } from '@testing-library/react';
import { SceneBackdrop } from './SceneBackdrop';

describe('SceneBackdrop', () => {
  it('keeps every scene mounted so that they can cross fade', () => {
    const { container } = render(<SceneBackdrop theme="dark" />);

    expect(container.querySelectorAll('.scenery-layer')).toHaveLength(3);
  });

  it('activates only the scene of the theme', () => {
    const { container } = render(<SceneBackdrop theme="dark" />);

    expect(container.querySelector('.scenery-dark')).toHaveAttribute('data-active', 'true');
    expect(container.querySelector('.scenery-light')).toHaveAttribute('data-active', 'false');
  });

  it('stays out of the reach of screen readers', () => {
    const { container } = render(<SceneBackdrop theme="light" />);

    expect(container.firstChild).toHaveAttribute('aria-hidden', 'true');
  });
});
