import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { Modal } from './Modal';

describe('Modal', () => {
  afterEach(() => {
    vi.useRealTimers();
    vi.unstubAllGlobals();
  });

  it('names the dialog after its title', () => {
    render(
      <Modal title="Título" onClose={vi.fn()}>
        corpo
      </Modal>,
    );

    expect(screen.getByRole('dialog', { name: 'Título' })).toHaveTextContent('corpo');
  });

  it('closes with Escape', async () => {
    const onClose = vi.fn();
    render(
      <Modal title="Título" onClose={onClose}>
        corpo
      </Modal>,
    );
    await userEvent.keyboard('{Escape}');

    expect(onClose).toHaveBeenCalledTimes(1);
  });

  it('closes with the button', async () => {
    const onClose = vi.fn();
    render(
      <Modal title="Título" onClose={onClose}>
        corpo
      </Modal>,
    );
    await userEvent.click(screen.getByRole('button', { name: 'Close' }));

    expect(onClose).toHaveBeenCalledTimes(1);
  });

  it('closes when clicking on the overlay', async () => {
    const onClose = vi.fn();
    render(
      <Modal title="Título" onClose={onClose}>
        corpo
      </Modal>,
    );
    await userEvent.click(document.querySelector('.modal-backdrop') as Element);

    expect(onClose).toHaveBeenCalledTimes(1);
  });

  it('does not close when clicking inside', async () => {
    const onClose = vi.fn();
    render(
      <Modal title="Título" onClose={onClose}>
        corpo
      </Modal>,
    );
    await userEvent.click(screen.getByText('corpo'));

    expect(onClose).not.toHaveBeenCalled();
  });

  it('widens only when asked', () => {
    const { rerender } = render(
      <Modal title="Título" onClose={vi.fn()}>
        corpo
      </Modal>,
    );

    expect(screen.getByRole('dialog')).not.toHaveClass('modal-wide');

    rerender(
      <Modal title="Título" onClose={vi.fn()} isWide>
        corpo
      </Modal>,
    );

    expect(screen.getByRole('dialog')).toHaveClass('modal-wide');
  });

  it('leaves an inert copy playing the closing animation, and then removes it', () => {
    vi.stubGlobal('matchMedia', vi.fn().mockReturnValue({ matches: true }));
    vi.useFakeTimers();
    const { unmount } = render(
      <Modal title="Título" onClose={vi.fn()}>
        corpo
      </Modal>,
    );
    unmount();
    const ghost = document.querySelector('.modal-closing');

    expect(ghost).toHaveAttribute('aria-hidden', 'true');
    expect(ghost).not.toHaveAttribute('data-state');
    expect(ghost).toHaveTextContent('corpo');
    expect(ghost?.querySelector('[role="dialog"]')).toBeNull();

    vi.advanceTimersByTime(420);

    expect(document.querySelector('.modal-closing')).toBeNull();
  });

  it('closes at once without motion', () => {
    const { unmount } = render(
      <Modal title="Título" onClose={vi.fn()}>
        corpo
      </Modal>,
    );
    unmount();

    expect(document.querySelector('.modal-closing')).toBeNull();
  });

  it('focuses the marked element', () => {
    render(
      <Modal title="Título" onClose={vi.fn()}>
        <input aria-label="campo" data-autofocus />
      </Modal>,
    );

    expect(screen.getByLabelText('campo')).toHaveFocus();
  });
});
