import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import type { MockInstance } from 'vitest';
import { soundPlayer } from '@/ui/sound/sounds';
import { Aquarium } from './Aquarium';

const fakeContext = () =>
  new Proxy(
    {},
    { get: () => () => ({ addColorStop: vi.fn() }), set: () => true },
  ) as unknown as CanvasRenderingContext2D;

const allowMotion = (isAllowed: boolean): void => {
  vi.stubGlobal('matchMedia', () => ({ matches: isAllowed }));
};

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

  describe('motion', () => {
    let requestFrame: MockInstance<typeof window.requestAnimationFrame>;

    beforeEach(() => {
      vi.spyOn(HTMLCanvasElement.prototype, 'getContext').mockImplementation(fakeContext as never);
      requestFrame = vi.spyOn(window, 'requestAnimationFrame').mockReturnValue(1);
    });

    afterEach(() => {
      vi.restoreAllMocks();
      vi.unstubAllGlobals();
    });

    it('swims and offers food to the keyboard, which takes the focus first', async () => {
      allowMotion(true);
      const play = vi.spyOn(soundPlayer, 'play');
      setup();
      const feed = screen.getByRole('button', { name: 'Feed the fish' });

      expect(requestFrame).toHaveBeenCalled();
      expect(feed).toHaveFocus();

      await userEvent.keyboard(' ');

      expect(play).toHaveBeenCalledWith('foodDrop', 1);
    });

    it('shows a still picture and says why with the reduced motion preference', () => {
      allowMotion(false);
      setup();

      expect(requestFrame).not.toHaveBeenCalled();
      expect(screen.queryByRole('button', { name: 'Feed the fish' })).not.toBeInTheDocument();
      expect(screen.getByText('The animation is off because of your motion preference.')).toBeInTheDocument();
    });
  });
});
