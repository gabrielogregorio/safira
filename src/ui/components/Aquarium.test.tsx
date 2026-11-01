import { act, fireEvent, render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import type { MockInstance } from 'vitest';
import { saveFishes } from '@/ui/aquarium/aquariumStore';
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

const FISH_POINT = { clientX: 0, clientY: 30 };
const OPEN_WATER = { clientX: 500, clientY: 300 };
const FAR_WATER = { clientX: 800, clientY: 300 };
const SPECIES_VOICE = 1.25;

// With no randomness a lonely fish never leaves the corner where it was placed, so a test can point at it.
const keepOneFishStill = (): void => {
  saveFishes([{ id: 0, species: 1, mass: 1 }]);
  vi.spyOn(Math, 'random').mockReturnValue(0);
};

const water = (): HTMLCanvasElement => {
  const canvas = screen.getByRole<HTMLCanvasElement>('img', { name: 'Aquarium' });
  canvas.setPointerCapture = vi.fn();

  return canvas;
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

  it('turns into a wallpaper when nobody moves', () => {
    vi.useFakeTimers();
    setup();

    expect(screen.getByRole('dialog')).not.toHaveClass('is-idle');

    act(() => {
      vi.advanceTimersByTime(3000);
    });

    expect(screen.getByRole('dialog')).toHaveClass('is-idle');
    vi.useRealTimers();
  });

  it('plays the sea of the theme while it is open, and only if the sound is on', () => {
    const hold = vi.spyOn(soundPlayer, 'hold').mockResolvedValue();
    const release = vi.spyOn(soundPlayer, 'release');
    const { unmount } = render(<Aquarium origin={{ x: 0, y: 0 }} theme="dark" isSoundOn onClose={vi.fn()} />);

    expect(hold).toHaveBeenCalledExactlyOnceWith('seaDark', 1, 0.48);

    unmount();

    expect(release).toHaveBeenCalled();
    vi.restoreAllMocks();
  });

  it('keeps the right click for the water, not for the browser menu', () => {
    setup();

    expect(fireEvent.contextMenu(water())).toBe(false);
  });

  describe('motion', () => {
    let requestFrame: MockInstance<typeof window.requestAnimationFrame>;
    let getContext: MockInstance;

    beforeEach(() => {
      getContext = vi.spyOn(HTMLCanvasElement.prototype, 'getContext').mockImplementation(fakeContext as never);
      requestFrame = vi.spyOn(window, 'requestAnimationFrame').mockReturnValue(1);
    });

    afterEach(() => {
      vi.restoreAllMocks();
      vi.unstubAllGlobals();
      localStorage.clear();
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

    it('draws a new frame only after enough time has passed, and always asks for the next one', () => {
      const fillRect = vi.fn();
      getContext.mockImplementation(
        () =>
          new Proxy(fakeContext(), {
            get: (_target, name) => (name === 'fillRect' ? fillRect : vi.fn(() => ({ addColorStop: vi.fn() }))),
          }),
      );
      vi.spyOn(performance, 'now').mockReturnValue(1000);
      allowMotion(true);
      setup();
      const [[draw]] = requestFrame.mock.calls;
      requestFrame.mockClear();

      draw(1010);

      expect(fillRect).not.toHaveBeenCalled();
      expect(requestFrame).toHaveBeenCalledTimes(1);

      draw(1100);

      expect(fillRect).toHaveBeenCalledTimes(1);
      expect(requestFrame).toHaveBeenCalledTimes(2);
    });

    it('feeds open water and scares a fish with the voice of its species', () => {
      keepOneFishStill();
      allowMotion(true);
      const play = vi.spyOn(soundPlayer, 'play');
      setup();
      const canvas = water();

      fireEvent.pointerDown(canvas, { ...OPEN_WATER, pointerId: 7 });
      fireEvent.pointerUp(canvas, OPEN_WATER);

      expect(canvas.setPointerCapture).toHaveBeenCalledWith(7);
      expect(play).toHaveBeenCalledExactlyOnceWith('foodDrop', 1);

      play.mockClear();
      fireEvent.pointerDown(canvas, FISH_POINT);
      fireEvent.pointerUp(canvas, FISH_POINT);

      expect(play).toHaveBeenCalledExactlyOnceWith('fishFlee', SPECIES_VOICE);
    });

    it('passes the buttons on, so the right button feeds even over a fish', () => {
      keepOneFishStill();
      allowMotion(true);
      const play = vi.spyOn(soundPlayer, 'play');
      setup();
      const canvas = water();

      fireEvent.pointerDown(canvas, { ...FISH_POINT, buttons: 2 });
      fireEvent.pointerUp(canvas, FISH_POINT);

      expect(play).toHaveBeenCalledExactlyOnceWith('foodDrop', 1);
    });

    it('reads the second button of a chord from the pointer moves', () => {
      keepOneFishStill();
      allowMotion(true);
      const play = vi.spyOn(soundPlayer, 'play');
      setup();
      const canvas = water();

      fireEvent.pointerDown(canvas, { ...FISH_POINT, buttons: 1 });
      fireEvent.pointerMove(canvas, { ...FISH_POINT, buttons: 3 });
      fireEvent.pointerUp(canvas, FISH_POINT);

      expect(play).toHaveBeenCalledExactlyOnceWith('foodDrop', 1);
    });

    it('feeds nothing after a drag', () => {
      allowMotion(true);
      const play = vi.spyOn(soundPlayer, 'play');
      setup();
      const canvas = water();

      fireEvent.pointerDown(canvas, OPEN_WATER);
      fireEvent.pointerMove(canvas, FAR_WATER);
      fireEvent.pointerUp(canvas, FAR_WATER);

      expect(play).not.toHaveBeenCalled();
    });

    it('forgets a press that the browser cancels', () => {
      allowMotion(true);
      const play = vi.spyOn(soundPlayer, 'play');
      setup();
      const canvas = water();

      fireEvent.pointerDown(canvas, OPEN_WATER);
      fireEvent.pointerCancel(canvas, OPEN_WATER);
      fireEvent.pointerUp(canvas, OPEN_WATER);

      expect(play).not.toHaveBeenCalled();
    });

    it('drops food with the wheel only while a button is held', () => {
      allowMotion(true);
      const play = vi.spyOn(soundPlayer, 'play');
      setup();
      const canvas = water();

      fireEvent.wheel(canvas);

      expect(play).not.toHaveBeenCalled();

      fireEvent.pointerDown(canvas, OPEN_WATER);
      fireEvent.wheel(canvas);

      expect(play).toHaveBeenCalledExactlyOnceWith('foodDrop', 1);
    });

    it('does not answer the pointer in a still picture', () => {
      allowMotion(false);
      const play = vi.spyOn(soundPlayer, 'play');
      setup();
      const canvas = water();

      fireEvent.pointerDown(canvas, OPEN_WATER);
      fireEvent.wheel(canvas);
      fireEvent.pointerUp(canvas, OPEN_WATER);

      expect(play).not.toHaveBeenCalled();
    });

    it('stays out of the way when the browser gives no canvas to draw on', async () => {
      getContext.mockReturnValue(null);
      allowMotion(true);
      const play = vi.spyOn(soundPlayer, 'play');
      setup();
      const canvas = water();

      fireEvent.pointerDown(canvas, OPEN_WATER);
      fireEvent.wheel(canvas);
      fireEvent.pointerUp(canvas, OPEN_WATER);
      await userEvent.click(screen.getByRole('button', { name: 'Feed the fish' }));

      expect(requestFrame).not.toHaveBeenCalled();
      expect(play).not.toHaveBeenCalledWith('foodDrop', 1);
    });
  });
});
