import { render, screen } from '@testing-library/react';
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
