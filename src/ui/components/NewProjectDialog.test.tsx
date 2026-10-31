import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { NewProjectDialog } from './NewProjectDialog';

const setup = (initialExampleId: string | null = null) => {
  const onCreate = vi.fn();
  render(<NewProjectDialog initialExampleId={initialExampleId} onCreate={onCreate} onClose={vi.fn()} />);

  return onCreate;
};

const goAhead = (): Promise<void> => userEvent.click(screen.getByRole('button', { name: 'Go ahead' }));

describe('NewProjectDialog', () => {
  it('creates without any choice', async () => {
    const onCreate = setup();
    await goAhead();

    expect(onCreate).toHaveBeenCalledWith('New project', undefined);
  });

  it('uses the example title when there is no name', async () => {
    const onCreate = setup();
    await userEvent.click(screen.getByRole('button', { name: 'Lists' }));
    await goAhead();

    expect(onCreate).toHaveBeenCalledWith('Lists', expect.stringContaining('list of'));
  });

  it('prefers the typed name', async () => {
    const onCreate = setup();
    await userEvent.type(screen.getByLabelText('Project name (optional)'), 'Meu');
    await userEvent.click(screen.getByRole('button', { name: 'Lists' }));
    await goAhead();

    expect(onCreate).toHaveBeenCalledWith('Meu', expect.any(String));
  });

  it('comes with the example of the link already chosen', () => {
    setup('16-listas');

    expect(screen.getByRole('button', { name: 'Lists' })).toHaveAttribute('aria-pressed', 'true');
  });
});
