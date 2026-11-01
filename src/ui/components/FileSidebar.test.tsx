import { createEvent, fireEvent, render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { FileSidebar } from './FileSidebar';

const setup = (canRename = true) => {
  const actions = {
    onOpen: vi.fn(),
    onCreateFile: vi.fn(),
    onCreateFolder: vi.fn(),
    onDelete: vi.fn(),
    onRename: vi.fn(),
    onMove: vi.fn(),
    onDownload: vi.fn(),
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

const rowOf = (name: string): HTMLElement => screen.getByRole('button', { name }).parentElement as HTMLElement;

const placeRow = (row: HTMLElement): void => {
  vi.spyOn(row, 'getBoundingClientRect').mockReturnValue({ top: 100, height: 20 } as DOMRect);
};

// jsdom has no DragEvent, so the plain event it falls back to drops the height of the pointer.
const fireAtHeight = (
  create: typeof createEvent.dragOver,
  row: HTMLElement,
  dataTransfer: object,
  clientY: number,
): void => {
  const event = create(row, { dataTransfer });
  Object.defineProperty(event, 'clientY', { value: clientY });
  fireEvent(row, event);
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

  it('renames the selected file with F2', async () => {
    setup();
    await userEvent.keyboard('{F2}');

    expect(screen.getByRole('textbox')).toHaveFocus();
  });

  it('ignores F2 while renaming is not allowed', async () => {
    setup(false);
    await userEvent.keyboard('{F2}');

    expect(screen.queryByRole('textbox')).not.toBeInTheDocument();
  });

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

  it('moves a file into a folder by dragging', () => {
    const { onMove } = setup();
    const row = (name: string): HTMLElement => screen.getByRole('button', { name }).parentElement as HTMLElement;
    const dataTransfer = { setData: vi.fn(), effectAllowed: '' };
    fireEvent.dragStart(row('main.safira'), { dataTransfer });
    fireEvent.dragOver(row('vazia'), { dataTransfer, clientY: 0 });
    fireEvent.drop(row('vazia'), { dataTransfer, clientY: 0 });

    expect(onMove).toHaveBeenCalledExactlyOnceWith(
      expect.objectContaining({ path: 'main.safira' }),
      expect.objectContaining({ target: expect.any(String) as string }),
    );
  });

  it('does not drag while a program runs', () => {
    setup(false);

    expect(screen.getByRole('button', { name: 'main.safira' }).parentElement).toHaveAttribute('draggable', 'false');
  });

  it.each(['main.safira', 'vazia'])('offers to download %s from the right click', async (name) => {
    const { onDownload } = setup();
    rightClick(name);
    await userEvent.click(await screen.findByRole('menuitem', { name: 'Download' }));

    expect(onDownload).toHaveBeenCalledExactlyOnceWith(expect.objectContaining({ name }));
  });

  it('moves the focused file with Alt and the arrows, and says so', async () => {
    const { onMove } = setup();
    screen.getByRole('button', { name: 'new-file.safira' }).focus();
    await userEvent.keyboard('{Alt>}{ArrowUp}{/Alt}');

    expect(onMove).toHaveBeenCalledExactlyOnceWith(
      expect.objectContaining({ path: 'new-file.safira' }),
      expect.objectContaining({ target: 'new-file.safira' }),
    );
    expect(screen.getByRole('status')).toHaveTextContent('Moved: new-file.safira');
  });

  it('ignores the arrows without Alt, and Alt while a program runs', async () => {
    setup(false);
    const { onMove } = setup();
    screen.getAllByRole('button', { name: 'main.safira' })[1].focus();
    await userEvent.keyboard('{ArrowUp}');

    expect(onMove).not.toHaveBeenCalled();
  });

  it('lists move up and down in the menu and locks the edge', async () => {
    setup();
    rightClick('dados');

    expect(await screen.findByRole('menuitem', { name: /Move up/ })).toHaveAttribute('data-disabled');
    expect(screen.getByRole('menuitem', { name: /Move down/ })).not.toHaveAttribute('data-disabled');
  });

  it('chooses a folder in a modal opened by the keyboard', async () => {
    const { onMove } = setup();
    screen.getByRole('button', { name: 'main.safira' }).focus();
    await userEvent.keyboard('{Alt>}m{/Alt}');
    await userEvent.click(await screen.findByRole('button', { name: 'vazia' }));

    expect(onMove).toHaveBeenCalledExactlyOnceWith(
      expect.objectContaining({ path: 'main.safira' }),
      expect.objectContaining({ target: 'vazia/main.safira' }),
    );
    expect(screen.queryByRole('dialog')).not.toBeInTheDocument();
  });

  it('moves a file out to the root of the project from the menu', async () => {
    const { onMove } = setup();
    rightClick('a.txt');
    await userEvent.click(await screen.findByRole('menuitem', { name: /Move to/ }));
    await userEvent.click(await screen.findByRole('button', { name: 'Project root' }));

    expect(onMove).toHaveBeenCalledExactlyOnceWith(
      expect.objectContaining({ path: 'dados/a.txt' }),
      expect.objectContaining({ target: 'a.txt' }),
    );
  });

  it('marks the edge of a file under the dragged item, and drops it there', () => {
    const { onMove } = setup();
    const dataTransfer = { setData: vi.fn(), effectAllowed: '' };
    const row = rowOf('new-file.safira');
    placeRow(row);
    fireEvent.dragStart(rowOf('main.safira'), { dataTransfer });

    fireAtHeight(createEvent.dragOver, row, dataTransfer, 102);

    expect(row).toHaveAttribute('data-drop', 'before');

    fireAtHeight(createEvent.dragOver, row, dataTransfer, 118);

    expect(row).toHaveAttribute('data-drop', 'after');

    fireAtHeight(createEvent.drop, row, dataTransfer, 118);

    expect(onMove).toHaveBeenCalledExactlyOnceWith(
      expect.objectContaining({ path: 'main.safira' }),
      expect.objectContaining({ target: 'main.safira' }),
    );
    expect(row).not.toHaveAttribute('data-drop');
  });

  it('keeps a wide middle on a folder for dropping inside it', () => {
    setup();
    const dataTransfer = { setData: vi.fn(), effectAllowed: '' };
    const row = rowOf('vazia');
    placeRow(row);
    fireEvent.dragStart(rowOf('main.safira'), { dataTransfer });

    fireAtHeight(createEvent.dragOver, row, dataTransfer, 104);

    expect(row).toHaveAttribute('data-drop', 'before');

    fireAtHeight(createEvent.dragOver, row, dataTransfer, 110);

    expect(row).toHaveAttribute('data-drop', 'inside');

    fireAtHeight(createEvent.dragOver, row, dataTransfer, 116);

    expect(row).toHaveAttribute('data-drop', 'after');
  });

  it('takes the mark away over a place that cannot receive the item', () => {
    setup();
    const dataTransfer = { setData: vi.fn(), effectAllowed: '' };
    const dragged = rowOf('main.safira');
    const other = rowOf('vazia');
    fireEvent.dragStart(dragged, { dataTransfer });
    fireEvent.dragOver(other, { dataTransfer, clientY: 0 });

    expect(other).toHaveAttribute('data-drop');

    const isAllowed = !fireEvent.dragOver(dragged, { dataTransfer, clientY: 0 });

    expect(isAllowed).toBe(false);
    expect(other).not.toHaveAttribute('data-drop');
  });

  it('moves a file to the root when dropped outside the rows', () => {
    const { onMove } = setup();
    const dataTransfer = { setData: vi.fn(), effectAllowed: '' };
    const sidebar = screen.getByRole('navigation', { name: 'Files' });
    fireEvent.dragStart(rowOf('a.txt'), { dataTransfer });

    expect(fireEvent.dragOver(sidebar, { dataTransfer })).toBe(false);

    fireEvent.drop(sidebar, { dataTransfer });

    expect(onMove).toHaveBeenCalledExactlyOnceWith(
      expect.objectContaining({ path: 'dados/a.txt' }),
      expect.objectContaining({ target: 'a.txt' }),
    );
  });

  it('refuses a drag that did not start in the tree', () => {
    const { onMove } = setup();
    const dataTransfer = { setData: vi.fn(), effectAllowed: '' };
    const sidebar = screen.getByRole('navigation', { name: 'Files' });

    expect(fireEvent.dragOver(sidebar, { dataTransfer })).toBe(true);
    expect(fireEvent.dragOver(rowOf('vazia'), { dataTransfer, clientY: 0 })).toBe(true);

    fireEvent.drop(sidebar, { dataTransfer });

    expect(onMove).not.toHaveBeenCalled();
  });

  it('moves the focused file down with Alt and the arrow', async () => {
    const { onMove } = setup();
    screen.getByRole('button', { name: 'main.safira' }).focus();
    await userEvent.keyboard('{Alt>}{ArrowDown}{/Alt}');

    expect(onMove).toHaveBeenCalledExactlyOnceWith(
      expect.objectContaining({ path: 'main.safira' }),
      expect.objectContaining({ target: 'main.safira' }),
    );
    expect(screen.getByRole('status')).toHaveTextContent('Moved: main.safira');
  });

  it('stays quiet when the arrow finds the edge of the list', async () => {
    const { onMove } = setup();
    screen.getByRole('button', { name: 'dados' }).focus();
    await userEvent.keyboard('{Alt>}{ArrowUp}{/Alt}');

    expect(onMove).not.toHaveBeenCalled();
    expect(screen.getByRole('status')).toBeEmptyDOMElement();
  });

  it.each([
    [/Move up/, 'new-file.safira'],
    [/Move down/, 'main.safira'],
  ])('steps with %s from the right click menu', async (item, name) => {
    const { onMove } = setup();
    rightClick(name);
    await userEvent.click(await screen.findByRole('menuitem', { name: item }));

    expect(onMove).toHaveBeenCalledExactlyOnceWith(
      expect.objectContaining({ path: name }),
      expect.objectContaining({ target: name }),
    );
  });

  it('closes the move modal without moving', async () => {
    const { onMove } = setup();
    screen.getByRole('button', { name: 'main.safira' }).focus();
    await userEvent.keyboard('{Alt>}m{/Alt}');
    await screen.findByRole('dialog');
    await userEvent.keyboard('{Escape}');

    expect(screen.queryByRole('dialog')).not.toBeInTheDocument();
    expect(onMove).not.toHaveBeenCalled();
  });

  it('finishes a new name at once when the focus leaves by keyboard', async () => {
    const { onCreateFile } = setup();
    await userEvent.click(screen.getByRole('button', { name: 'New file' }));
    await userEvent.tab();

    expect(onCreateFile).toHaveBeenCalledExactlyOnceWith(null, 'new-file-2.safira');
    expect(screen.queryByLabelText('File name')).not.toBeInTheDocument();
  });

  it('says when there is nowhere to go', async () => {
    render(
      <FileSidebar
        projectName="P"
        paths={['main.safira']}
        activeFile="main.safira"
        canRename
        onOpen={vi.fn()}
        onCreateFile={vi.fn()}
        onCreateFolder={vi.fn()}
        onDelete={vi.fn()}
        onRename={vi.fn()}
        onMove={vi.fn()}
        onDownload={vi.fn()}
        onRenameProject={vi.fn()}
      />,
    );
    rightClick('main.safira');
    await userEvent.click(await screen.findByRole('menuitem', { name: /Move to/ }));

    expect(await screen.findByText('There is no folder to move this to.')).toBeInTheDocument();
  });
});
