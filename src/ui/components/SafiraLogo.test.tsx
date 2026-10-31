import { render } from '@testing-library/react';
import * as gemRenderer from '@/ui/gem/gemRenderer';
import { SafiraLogo } from './SafiraLogo';

describe('SafiraLogo', () => {
  afterEach(() => {
    vi.restoreAllMocks();
  });

  it('shows the 3D gem, hidden from screen readers', () => {
    vi.spyOn(gemRenderer, 'startGem').mockReturnValue(vi.fn());
    const { container } = render(<SafiraLogo size={40} />);

    expect(container.querySelector('canvas')).toHaveAttribute('aria-hidden', 'true');
  });

  it('falls back to the flat logo without WebGL', () => {
    vi.spyOn(gemRenderer, 'startGem').mockReturnValue(null);
    const { container } = render(<SafiraLogo size={40} />);

    expect(container.querySelector('canvas')).toBeNull();
    expect(container.querySelector('svg')).toHaveAttribute('aria-hidden', 'true');
  });

  it('stops the gem when it leaves the screen', () => {
    const stop = vi.fn();
    vi.spyOn(gemRenderer, 'startGem').mockReturnValue(stop);
    render(<SafiraLogo size={40} />).unmount();

    expect(stop).toHaveBeenCalled();
  });
});
