import { fireEvent, render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { Terminal } from './Terminal';

const buffer = {
  lines: [[{ text: 'oi', color: '#ff0000' }], [{ text: 'tudo', color: '' }]],
  isLastLineOpen: false,
};

describe('Terminal', () => {
  it('shows each line with its color', () => {
    render(<Terminal buffer={buffer} footer={null} isWaitingInput={false} onSubmitInput={vi.fn()} />);

    expect(screen.getByText('oi')).toHaveStyle({ color: '#ff0000' });
    expect(screen.getByRole('log')).toHaveTextContent('oitudo');
  });

  describe('keyboard', () => {
    const setup = (isListeningKeys = true) => {
      const onKey = vi.fn();
      const onKeysLost = vi.fn();
      render(
        <Terminal
          buffer={buffer}
          footer={null}
          isWaitingInput={false}
          onSubmitInput={vi.fn()}
          isListeningKeys={isListeningKeys}
          onKey={onKey}
          onKeysLost={onKeysLost}
        />,
      );

      return { onKey, onKeysLost, log: screen.getByRole('log') };
    };

    it('asks for a click while the program area has no focus', async () => {
      const { log } = setup();
      await userEvent.click(screen.getByRole('button', { name: 'Click here to use the keyboard' }));

      expect(log).toHaveFocus();
      expect(screen.queryByRole('button', { name: 'Click here to use the keyboard' })).not.toBeInTheDocument();
    });

    it('sends keys only from the program area', async () => {
      const { onKey, log } = setup();
      await userEvent.keyboard('a');

      expect(onKey).not.toHaveBeenCalled();

      await userEvent.click(log);
      await userEvent.keyboard('{ArrowUp}');

      expect(onKey).toHaveBeenNthCalledWith(1, 'arrowup', true);
      expect(onKey).toHaveBeenNthCalledWith(2, 'arrowup', false);
    });

    it('sends nothing while the program does not listen', async () => {
      const { onKey, log } = setup(false);
      await userEvent.click(log);
      await userEvent.keyboard('a');

      expect(onKey).not.toHaveBeenCalled();
    });

    it('leaves the shortcuts of the browser alone', async () => {
      const { onKey, log } = setup();
      await userEvent.click(log);
      await userEvent.keyboard('{Control>}r{/Control}');

      expect(onKey).not.toHaveBeenCalledWith('r', true);
    });

    it('lets go of the keys when the area loses the focus', async () => {
      const { onKeysLost, log } = setup();
      await userEvent.click(log);
      await userEvent.click(document.body);

      expect(onKeysLost).toHaveBeenCalled();
    });

    it('offers the keys on the screen, for a phone', () => {
      const { onKey } = setup();
      const up = screen.getByRole('button', { name: 'Up' });

      fireEvent.pointerDown(up);
      fireEvent.pointerUp(up);
      fireEvent.pointerCancel(up);

      expect(onKey.mock.calls).toEqual([
        ['arrowup', true],
        ['arrowup', false],
        ['arrowup', false],
      ]);
    });
  });

  it('fills the screen and comes back, keeping the focus', async () => {
    render(<Terminal buffer={buffer} footer={null} isWaitingInput={false} onSubmitInput={vi.fn()} />);
    await userEvent.click(screen.getByRole('button', { name: 'Maximize the program' }));

    expect(screen.getByRole('region', { name: 'Terminal' })).toHaveClass('terminal-maximized');
    expect(screen.getByRole('log')).toHaveFocus();

    await userEvent.click(screen.getByRole('button', { name: 'Minimize the program' }));

    expect(screen.getByRole('region', { name: 'Terminal' })).not.toHaveClass('terminal-maximized');
  });

  it('shows the footer', () => {
    render(<Terminal buffer={buffer} footer="fim" isWaitingInput={false} onSubmitInput={vi.fn()} />);

    expect(screen.getByText('fim')).toBeInTheDocument();
  });

  it('only offers the field when the program is waiting', () => {
    render(<Terminal buffer={buffer} footer={null} isWaitingInput={false} onSubmitInput={vi.fn()} />);

    expect(screen.queryByRole('textbox')).not.toBeInTheDocument();
  });

  it('focuses the field, sends the text and clears it', async () => {
    const onSubmitInput = vi.fn();
    render(<Terminal buffer={buffer} footer={null} isWaitingInput onSubmitInput={onSubmitInput} />);
    const field = screen.getByRole('textbox');

    expect(field).toHaveFocus();

    await userEvent.type(field, 'Ana{Enter}');

    expect(onSubmitInput).toHaveBeenCalledWith('Ana');
    expect(field).toHaveValue('');
  });

  it('does not treat printed text as HTML', () => {
    const hostile = { lines: [[{ text: '<img src=x>', color: '' }]], isLastLineOpen: false };
    render(<Terminal buffer={hostile} footer={null} isWaitingInput={false} onSubmitInput={vi.fn()} />);

    expect(screen.getByText('<img src=x>')).toBeInTheDocument();
    expect(document.querySelector('.terminal img')).toBeNull();
  });
});
