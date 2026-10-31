import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { Aquarium } from './Aquarium';

const setup = () => {
  const onClose = vi.fn();
  render(<Aquarium origin={{ x: 10, y: 20 }} theme="light" isSoundOn={false} onClose={onClose} />);

  return onClose;
};

describe('Aquarium', () => {
  it('fills the screen and grows from the given point', () => {
    setup();
    const dialog = screen.getByRole('dialog', { name: 'Aquarium' });

    expect(dialog.style.getPropertyValue('--origin-x')).toBe('10px');
  });

  it('closes with the button', async () => {
    const onClose = setup();
    await userEvent.click(screen.getByRole('button', { name: 'Close' }));

    expect(onClose).toHaveBeenCalledTimes(1);
  });

  it('closes at once, without a closing animation', async () => {
    const onClose = setup();
    await userEvent.click(screen.getByRole('button', { name: 'Close' }));

    expect(onClose).toHaveBeenCalledTimes(1);
    expect(document.querySelector('.aquarium')?.className).toBe('aquarium');
  });

  it('closes with Escape', async () => {
    const onClose = setup();
    await userEvent.keyboard('{Escape}');

    expect(onClose).toHaveBeenCalledTimes(1);
  });
});
