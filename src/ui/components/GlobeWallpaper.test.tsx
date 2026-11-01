import { act, fireEvent, render, screen } from '@testing-library/react';
import { GlobeWallpaper } from './GlobeWallpaper';

const IDLE_MILLISECONDS = 3000;

describe('GlobeWallpaper', () => {
  beforeEach(() => {
    vi.useFakeTimers();
  });

  afterEach(() => {
    vi.useRealTimers();
  });

  it('hides the close button while nobody moves the mouse and shows it again', () => {
    const { container } = render(<GlobeWallpaper onClose={vi.fn()} />);

    expect(container.firstChild).toHaveClass('wallpaper');
    expect(container.firstChild).not.toHaveClass('is-idle');

    act(() => {
      vi.advanceTimersByTime(IDLE_MILLISECONDS);
    });

    expect(container.firstChild).toHaveClass('is-idle');

    fireEvent.pointerMove(window);

    expect(container.firstChild).not.toHaveClass('is-idle');
  });

  it('closes by its button', () => {
    const onClose = vi.fn();
    render(<GlobeWallpaper onClose={onClose} />);
    fireEvent.click(screen.getByRole('button'));

    expect(onClose).toHaveBeenCalledOnce();
  });
});
