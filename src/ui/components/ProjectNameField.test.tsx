import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { ProjectNameField } from './ProjectNameField';

const openField = async (onRename = vi.fn()): Promise<{ field: HTMLInputElement; onRename: typeof onRename }> => {
  render(
    <>
      <ProjectNameField name="Velho" onRename={onRename} />
      <button type="button">Outside</button>
    </>,
  );
  await userEvent.click(screen.getByRole('button', { name: 'Velho' }));

  return { field: screen.getByLabelText<HTMLInputElement>('Project name'), onRename };
};

describe('ProjectNameField', () => {
  it('opens on click with the whole name selected', async () => {
    const { field } = await openField();

    expect(field).toHaveFocus();
    expect(field.selectionStart).toBe(0);
    expect(field.selectionEnd).toBe('Velho'.length);
  });

  it('saves on Enter and gives the focus back', async () => {
    const { onRename } = await openField();
    await userEvent.keyboard('Novo{Enter}');

    expect(onRename).toHaveBeenCalledTimes(1);
    expect(onRename).toHaveBeenCalledWith('Novo');
    expect(screen.getByRole('button', { name: 'Velho' })).toHaveFocus();
  });

  it('saves on a click outside', async () => {
    const { onRename } = await openField();
    await userEvent.keyboard('Novo');
    await userEvent.click(screen.getByRole('button', { name: 'Outside' }));

    expect(onRename).toHaveBeenCalledWith('Novo');
    expect(screen.getByRole('button', { name: 'Outside' })).toHaveFocus();
  });

  it('drops the typed text on Escape', async () => {
    const { onRename } = await openField();
    await userEvent.keyboard('Novo{Escape}');

    expect(onRename).not.toHaveBeenCalled();
    expect(screen.getByRole('button', { name: 'Velho' })).toHaveFocus();
  });

  it.each(['   ', 'Velho'])('keeps the name when the field ends as "%s"', async (typed) => {
    const { field, onRename } = await openField();
    await userEvent.clear(field);
    await userEvent.type(field, `${typed}{Enter}`);

    expect(onRename).not.toHaveBeenCalled();
  });

  it('trims the name and opens again after saving', async () => {
    const { onRename } = await openField();
    await userEvent.keyboard('  Novo  {Enter}');
    await userEvent.click(screen.getByRole('button', { name: 'Velho' }));
    await userEvent.keyboard('Outro{Enter}');

    expect(onRename.mock.calls).toEqual([['Novo'], ['Outro']]);
  });
});
