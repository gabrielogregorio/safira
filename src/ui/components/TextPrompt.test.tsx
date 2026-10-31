import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { TextPrompt } from './TextPrompt';

const setup = (initialValue = '') => {
  const onSubmit = vi.fn();
  render(<TextPrompt title="T" label="Nome" initialValue={initialValue} onSubmit={onSubmit} onClose={vi.fn()} />);

  return onSubmit;
};

describe('TextPrompt', () => {
  it('sends the trimmed text', async () => {
    const onSubmit = setup();
    await userEvent.type(screen.getByLabelText('Nome'), '  novo  {Enter}');

    expect(onSubmit).toHaveBeenCalledWith('novo');
  });

  it('refuses an empty text', async () => {
    const onSubmit = setup();
    await userEvent.click(screen.getByRole('button', { name: 'Save' }));

    expect(onSubmit).not.toHaveBeenCalled();
  });

  it('starts with the current value and the focus', () => {
    setup('velho');

    expect(screen.getByLabelText('Nome')).toHaveValue('velho');
    expect(screen.getByLabelText('Nome')).toHaveFocus();
  });
});
