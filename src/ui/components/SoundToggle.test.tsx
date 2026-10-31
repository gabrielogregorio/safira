import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { SoundToggle } from './SoundToggle';

describe('SoundToggle', () => {
  it('says whether the sound is on', () => {
    const { rerender } = render(<SoundToggle isOn onChange={vi.fn()} />);

    expect(screen.getByRole('button', { name: 'Sound: On' })).toBeInTheDocument();

    rerender(<SoundToggle isOn={false} onChange={vi.fn()} />);

    expect(screen.getByRole('button', { name: 'Sound: Off' })).toBeInTheDocument();
  });

  it.each([
    [true, false],
    [false, true],
  ])('goes from %s to %s on click', async (current, next) => {
    const onChange = vi.fn();
    render(<SoundToggle isOn={current} onChange={onChange} />);
    await userEvent.click(screen.getByRole('button'));

    expect(onChange).toHaveBeenCalledWith(next);
  });
});
