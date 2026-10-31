import { fireEvent, render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { FileSidebar } from './FileSidebar';

const setup = () => {
  const actions = { onOpen: vi.fn(), onCreateFile: vi.fn(), onCreateFolder: vi.fn(), onDelete: vi.fn() };
  render(
    <FileSidebar
      paths={['main.safira', 'dados/a.txt', 'vazia/.keep', 'new-file.safira']}
      activeFile="dados/a.txt"
      {...actions}
    />,
  );

  return actions;
};

const rightClick = (name: string): void => {
  fireEvent.contextMenu(screen.getByRole('button', { name }));
};

describe('FileSidebar', () => {
  it('shows files, folders and marks the open file', () => {
    setup();

    expect(screen.getByRole('button', { name: 'main.safira' })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'a.txt' })).toHaveAttribute('aria-current', 'page');
    expect(screen.getByRole('button', { name: 'vazia' })).toBeInTheDocument();
    expect(screen.queryByText('.keep')).not.toBeInTheDocument();
  });

  it('opens a file by its full path', async () => {
    const { onOpen } = setup();
    await userEvent.click(screen.getByRole('button', { name: 'a.txt' }));

    expect(onOpen).toHaveBeenCalledWith('dados/a.txt');
  });

  it('shows the new file in the tree with a free name, selected', async () => {
    setup();
    await userEvent.click(screen.getByRole('button', { name: 'New file' }));
    const input = screen.getByLabelText<HTMLInputElement>('File name');

    expect(input).toHaveValue('new-file-2.safira');
    expect(input).toHaveFocus();
    expect(input.selectionStart).toBe(0);
    expect(input.selectionEnd).toBe(input.value.length);
  });

  it('replaces the selected name with what is typed', async () => {
    const { onCreateFile } = setup();
    await userEvent.click(screen.getByRole('button', { name: 'New file' }));
    await userEvent.keyboard('notas{Enter}');

    expect(onCreateFile).toHaveBeenCalledExactlyOnceWith(null, 'notas');
    expect(screen.queryByLabelText('File name')).not.toBeInTheDocument();
  });

  it('keeps the provisional name when the focus moves away', async () => {
    const { onCreateFolder } = setup();
    await userEvent.click(screen.getByRole('button', { name: 'New folder' }));
    await userEvent.click(document.body);

    expect(onCreateFolder).toHaveBeenCalledExactlyOnceWith(null, 'new-folder');
  });

  it('falls back to the provisional name when the field is emptied', async () => {
    const { onCreateFolder } = setup();
    await userEvent.click(screen.getByRole('button', { name: 'New folder' }));
    await userEvent.keyboard('{Backspace}{Enter}');

    expect(onCreateFolder).toHaveBeenCalledWith(null, 'new-folder');
  });

  it('cancels with Escape', async () => {
    const { onCreateFile } = setup();
    await userEvent.click(screen.getByRole('button', { name: 'New file' }));
    await userEvent.keyboard('{Escape}');

    expect(onCreateFile).not.toHaveBeenCalled();
    expect(screen.queryByLabelText('File name')).not.toBeInTheDocument();
  });

  it('has no delete button on the rows', () => {
    setup();

    expect(screen.queryByRole('button', { name: /Delete/ })).not.toBeInTheDocument();
  });

  it('deletes from the right click menu', async () => {
    const { onDelete } = setup();
    rightClick('main.safira');
    await userEvent.click(await screen.findByRole('menuitem', { name: 'Delete' }));

    expect(onDelete).toHaveBeenCalledWith(expect.objectContaining({ kind: 'file', path: 'main.safira' }));
  });

  it('deletes a folder from the right click menu', async () => {
    const { onDelete } = setup();
    rightClick('dados');
    await userEvent.click(await screen.findByRole('menuitem', { name: 'Delete' }));

    expect(onDelete).toHaveBeenCalledWith(expect.objectContaining({ kind: 'folder', path: 'dados' }));
  });

  it('creates inside a folder from the right click menu, opening it if closed', async () => {
    const { onCreateFile } = setup();
    await userEvent.click(screen.getByRole('button', { name: 'dados', expanded: true }));
    rightClick('dados');
    await userEvent.click(await screen.findByRole('menuitem', { name: 'New file' }));
    await userEvent.keyboard('lib{Enter}');

    expect(onCreateFile).toHaveBeenCalledWith('dados', 'lib');
  });

  it('creates a folder inside a folder from the right click menu', async () => {
    const { onCreateFolder } = setup();
    rightClick('dados');
    await userEvent.click(await screen.findByRole('menuitem', { name: 'New folder' }));
    await userEvent.keyboard('sub{Enter}');

    expect(onCreateFolder).toHaveBeenCalledWith('dados', 'sub');
  });

  it('collapses a folder', async () => {
    setup();
    await userEvent.click(screen.getByRole('button', { name: 'dados', expanded: true }));

    expect(screen.queryByRole('button', { name: 'a.txt' })).not.toBeInTheDocument();
  });
});
