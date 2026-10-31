import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { FileSidebar } from './FileSidebar';

const setup = () => {
  const actions = { onOpen: vi.fn(), onNewFile: vi.fn(), onNewFolder: vi.fn(), onDelete: vi.fn() };
  render(<FileSidebar paths={['main.safira', 'dados/a.txt', 'vazia/.keep']} activeFile="dados/a.txt" {...actions} />);

  return actions;
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

  it('creates at the root', async () => {
    const { onNewFile, onNewFolder } = setup();
    await userEvent.click(screen.getByRole('button', { name: 'New file' }));
    await userEvent.click(screen.getByRole('button', { name: 'New folder' }));

    expect(onNewFile).toHaveBeenCalledWith(null);
    expect(onNewFolder).toHaveBeenCalledWith(null);
  });

  it('creates inside a folder', async () => {
    const { onNewFile, onNewFolder } = setup();
    await userEvent.click(screen.getByRole('button', { name: 'New file in dados' }));
    await userEvent.click(screen.getByRole('button', { name: 'New folder in dados' }));

    expect(onNewFile).toHaveBeenCalledWith('dados');
    expect(onNewFolder).toHaveBeenCalledWith('dados');
  });

  it('asks to delete files and folders', async () => {
    const { onDelete } = setup();
    await userEvent.click(screen.getByRole('button', { name: 'Delete dados' }));

    expect(onDelete).toHaveBeenCalledWith(expect.objectContaining({ kind: 'folder', path: 'dados' }));
  });

  it('collapses a folder', async () => {
    setup();
    await userEvent.click(screen.getByRole('button', { name: 'dados', expanded: true }));

    expect(screen.queryByRole('button', { name: 'a.txt' })).not.toBeInTheDocument();
  });
});
