import { fireEvent, render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { FileSidebar } from './FileSidebar';

const setup = (canRename = true) => {
  const actions = {
    onOpen: vi.fn(),
    onCreateFile: vi.fn(),
    onCreateFolder: vi.fn(),
    onDelete: vi.fn(),
    onRename: vi.fn(),
    onRenameProject: vi.fn(),
  };
  render(
    <FileSidebar
      projectName="Projeto"
      paths={['main.safira', 'dados/a.txt', 'vazia/.keep', 'new-file.safira']}
      activeFile="dados/a.txt"
      canRename={canRename}
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

  const startRename = async (name: string): Promise<HTMLInputElement> => {
    rightClick(name);
    await userEvent.click(await screen.findByRole('menuitem', { name: 'Rename' }));

    return screen.findByRole<HTMLInputElement>('textbox');
  };

  it('renames a file from the right click, selecting only the name', async () => {
    const { onRename } = setup();
    const input = await startRename('main.safira');

    expect(input).toHaveValue('main.safira');
    expect(input).toHaveFocus();
    expect(input.selectionEnd).toBe('main'.length);

    await userEvent.keyboard('inicio{Enter}');

    expect(onRename).toHaveBeenCalledExactlyOnceWith(expect.objectContaining({ path: 'main.safira' }), 'inicio.safira');
    expect(screen.queryByRole('textbox')).not.toBeInTheDocument();
  });

  it('renames a folder when the focus moves away', async () => {
    const { onRename } = setup();
    const input = await startRename('vazia');

    expect(input.selectionEnd).toBe('vazia'.length);

    await userEvent.keyboard('cheia');
    await userEvent.click(document.body);

    expect(onRename).toHaveBeenCalledExactlyOnceWith(expect.objectContaining({ path: 'vazia' }), 'cheia');
  });

  it('refuses a name in use and stays open on Enter', async () => {
    const { onRename } = setup();
    const input = await startRename('main.safira');
    await userEvent.keyboard('new-file{Enter}');

    expect(screen.getByRole('alert')).toHaveTextContent('This name is invalid or already in use');
    expect(input).toHaveAttribute('aria-invalid', 'true');
    expect(input).toBeInTheDocument();
    expect(onRename).not.toHaveBeenCalled();
  });

  it('drops a refused name when the focus moves away', async () => {
    const { onRename } = setup();
    await startRename('main.safira');
    await userEvent.keyboard('new-file{Enter}');
    await userEvent.click(document.body);

    expect(onRename).not.toHaveBeenCalled();
    expect(screen.getByRole('button', { name: 'main.safira' })).toBeInTheDocument();
  });

  it('changes nothing on Escape or with the same name', async () => {
    const { onRename } = setup();
    await startRename('main.safira');
    await userEvent.keyboard('outro{Escape}');
    await startRename('main.safira');
    await userEvent.keyboard('{Enter}');

    expect(onRename).not.toHaveBeenCalled();
  });

  it('does not offer rename while a program runs', async () => {
    setup(false);
    rightClick('main.safira');

    expect(await screen.findByRole('menuitem', { name: 'Rename' })).toHaveAttribute('aria-disabled', 'true');
  });

  it('shows the project name on top and renames it with a click', async () => {
    const { onRenameProject } = setup();
    const heading = screen.getByRole('heading', { level: 1 });

    expect(heading).toHaveTextContent('Projeto');
    expect(heading.compareDocumentPosition(screen.getByRole('heading', { name: 'Files' }))).toBe(
      Node.DOCUMENT_POSITION_FOLLOWING,
    );

    await userEvent.click(screen.getByRole('button', { name: 'Projeto' }));
    await userEvent.keyboard('Outro{Enter}');

    expect(onRenameProject).toHaveBeenCalledWith('Outro');
  });

  it('keeps the click on another item while a new name is open', async () => {
    const { onOpen, onCreateFile } = setup();
    await userEvent.click(screen.getByRole('button', { name: 'New file' }));
    await userEvent.click(screen.getByRole('button', { name: 'main.safira' }));

    expect(onOpen).toHaveBeenCalledWith('main.safira');
    expect(onCreateFile).toHaveBeenCalledExactlyOnceWith(null, 'new-file-2.safira');
  });
});
