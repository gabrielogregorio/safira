import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { VISION_MODES } from '@/settings/vision';
import { VisionToggle } from './VisionToggle';

describe('VisionToggle', () => {
  it('names the current mode', () => {
    render(<VisionToggle vision="tritanopia" onChange={vi.fn()} />);

    expect(screen.getByRole('button', { name: 'Accessibility: Tritanopia (weak blue)' })).toBeInTheDocument();
  });

  it('walks through every mode and comes back to the first', async () => {
    const onChange = vi.fn();
    const { rerender } = render(<VisionToggle vision="default" onChange={onChange} />);

    for (const mode of VISION_MODES) {
      rerender(<VisionToggle vision={mode} onChange={onChange} />);
      await userEvent.click(screen.getByRole('button'));
    }

    expect(onChange.mock.calls.map(([mode]) => mode as string)).toEqual([...VISION_MODES.slice(1), VISION_MODES[0]]);
  });
});
