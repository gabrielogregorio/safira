import { render } from '@testing-library/react';
import { AeroOrb } from './AeroOrb';

describe('AeroOrb', () => {
  it('draws at the asked size, hidden from screen readers', () => {
    const { container } = render(<AeroOrb size={96} />);
    const orb = container.querySelector('svg');

    expect(orb).toHaveAttribute('width', '96');
    expect(orb).toHaveAttribute('aria-hidden', 'true');
  });

  it('keeps its gradients apart from other orbs on the page', () => {
    const { container } = render(
      <>
        <AeroOrb size={40} />
        <AeroOrb size={40} />
      </>,
    );
    const ids = [...container.querySelectorAll('linearGradient')].map((gradient) => gradient.id);

    expect(new Set(ids).size).toBe(ids.length);
  });
});
