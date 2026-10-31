import { act, render } from '@testing-library/react';
import { saveFishes } from '@/ui/aquarium/aquariumStore';
import { AeroOrb } from './AeroOrb';

describe('AeroOrb', () => {
  beforeEach(() => {
    localStorage.clear();
  });

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

  it('shows the fish while the aquarium has some', () => {
    const { container } = render(<AeroOrb size={40} />);

    expect(container.querySelector('.aero-orb-fish')).not.toBeNull();
  });

  it('stays empty with the aquarium, and follows it live', () => {
    saveFishes([]);
    const { container } = render(<AeroOrb size={40} />);

    expect(container.querySelector('.aero-orb-fish')).toBeNull();

    act(() => {
      saveFishes([{ id: 1, species: 0, mass: 1 }]);
    });

    expect(container.querySelector('.aero-orb-fish')).not.toBeNull();
  });
});
