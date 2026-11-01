import { fireEvent, render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import type { ComponentProps } from 'react';
import { soundPlayer } from '@/ui/sound/sounds';
import { HomeScreen } from './HomeScreen';

const project = { id: '1', name: 'Jogo', files: {}, breakpoints: {}, updatedAt: 0 };

const setup = (props: Partial<ComponentProps<typeof HomeScreen>> = {}) => {
  const actions = {
    onStartCreating: vi.fn(),
    onCancelCreating: vi.fn(),
    onCreate: vi.fn(),
    onImportProject: vi.fn(),
    onOpenAquarium: vi.fn(),
    onExportProject: vi.fn(),
    onRename: vi.fn(),
    onDelete: vi.fn(),
  };
  render(
    <HomeScreen
      projects={[project]}
      isCreating={false}
      initialExampleId={null}
      preferenceToggles={null}
      settingsButton={null}
      {...actions}
      {...props}
    />,
  );

  return actions;
};

describe('HomeScreen', () => {
  it.each([
    ['Safira on GitHub', 'https://github.com/gabrielogregorio/safira'],
    ['Safira wiki', 'https://github.com/gabrielogregorio/safira/wiki'],
  ])('links to %s in a new tab', (name, href) => {
    setup();
    const link = screen.getByRole('link', { name });

    expect(link).toHaveAttribute('href', href);
    expect(link).toHaveAttribute('target', '_blank');
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  it('opens the aquarium from the center of the orb', async () => {
    const { onOpenAquarium } = setup();
    const orb = screen.getByRole('button', { name: 'Open the aquarium' });
    vi.spyOn(orb, 'getBoundingClientRect').mockReturnValue(new DOMRect(10, 20, 100, 60));
    await userEvent.click(orb);

    expect(onOpenAquarium).toHaveBeenCalledExactlyOnceWith({ x: 60, y: 50 });
  });

  it('opens the file picker from the import button', async () => {
    setup();
    const click = vi.spyOn(screen.getByLabelText('Import project (.zip)', { selector: 'input' }), 'click');
    await userEvent.click(screen.getByRole('button', { name: 'Import project (.zip)' }));

    expect(click).toHaveBeenCalledOnce();
  });

  it('exports the project of the row', async () => {
    const { onExportProject } = setup();
    await userEvent.click(screen.getByRole('button', { name: 'Export Jogo' }));

    expect(onExportProject).toHaveBeenCalledExactlyOnceWith(project);
  });

  it('closes the delete confirmation with Escape, keeping the project', async () => {
    const { onDelete } = setup();
    await userEvent.click(screen.getByRole('button', { name: 'Delete Jogo' }));
    await userEvent.keyboard('{Escape}');

    expect(screen.queryByRole('dialog')).not.toBeInTheDocument();
    expect(onDelete).not.toHaveBeenCalled();
  });

  it('keeps the highlight while the file passes over other elements', () => {
    setup();
    fireEvent.dragEnter(document, { dataTransfer: { types: ['Files'], files: [] } });
    fireEvent(document, Object.assign(new Event('dragleave'), { relatedTarget: document.body }));

    expect(screen.getByTestId('drop-target')).toBeInTheDocument();
  });

  it('hides the highlight and imports nothing when the drop brings no file', () => {
    const play = vi.spyOn(soundPlayer, 'play').mockResolvedValue(undefined);
    const { onImportProject } = setup();
    fireEvent.dragEnter(document, { dataTransfer: { types: ['Files'], files: [] } });
    fireEvent.drop(document, { dataTransfer: { types: ['Files'], files: [] } });

    expect(screen.queryByTestId('drop-target')).not.toBeInTheDocument();
    expect(onImportProject).not.toHaveBeenCalled();
    expect(play).not.toHaveBeenCalledWith('import');
  });
});
