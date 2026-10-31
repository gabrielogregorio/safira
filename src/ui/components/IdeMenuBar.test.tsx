import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { DEFAULT_SETTINGS } from '@/settings/settings';
import { IdeMenuBar } from './IdeMenuBar';

const setup = (isRunning = false) => {
  const actions = {
    onOpenFile: vi.fn(),
    onNewTab: vi.fn(),
    onSave: vi.fn(),
    onSaveAs: vi.fn(),
    onFormat: vi.fn(),
    onExportProject: vi.fn(),
    onImportArchive: vi.fn(),
    onRun: vi.fn(),
    onStop: vi.fn(),
    onToggleBreakpoint: vi.fn(),
    onClearBreakpoints: vi.fn(),
    onOpenExample: vi.fn(),
    onChangeSettings: vi.fn(),
    onToggleFullScreen: vi.fn(),
    onShowCommands: vi.fn(),
  };
  render(<IdeMenuBar locale="en-us" settings={DEFAULT_SETTINGS} isRunning={isRunning} {...actions} />);

  return actions;
};

const choose = async (menu: string, item: string): Promise<void> => {
  await userEvent.click(screen.getByRole('menuitem', { name: menu }));
  await userEvent.click(await screen.findByRole('menuitem', { name: (name) => name.startsWith(item) }));
};

describe('IdeMenuBar', () => {
  it('shows the five menus', () => {
    setup();

    expect(screen.getAllByRole('menuitem').map((item) => item.textContent)).toEqual([
      'File',
      'Run',
      'Examples',
      'Interface',
      'Help',
    ]);
  });

  it('shows the shortcut beside the action', async () => {
    setup();
    await userEvent.click(screen.getByRole('menuitem', { name: 'Run' }));

    expect(await screen.findByRole('menuitem', { name: 'Run allCtrl+Enter' })).toBeInTheDocument();
  });

  it.each([
    ['File', 'Open file', 'onOpenFile'],
    ['File', 'SaveCtrl+S', 'onSave'],
    ['File', 'Export project (.zip)', 'onExportProject'],
    ['File', 'Format code', 'onFormat'],
    ['Run', 'Clear breakpoints', 'onClearBreakpoints'],
    ['Help', 'Available commands', 'onShowCommands'],
  ] as const)('%s > %s calls its action', async (menu, item, action) => {
    const actions = setup();
    await choose(menu, item);

    expect(actions[action]).toHaveBeenCalledTimes(1);
  });

  it('runs line by line', async () => {
    const { onRun } = setup();
    await choose('Run', 'Run line by line');

    expect(onRun).toHaveBeenCalledWith('step');
  });

  it('only allows stopping while running', async () => {
    setup();
    await userEvent.click(screen.getByRole('menuitem', { name: 'Run' }));

    expect(await screen.findByRole('menuitem', { name: 'Stop execution' })).toHaveAttribute('aria-disabled', 'true');
  });

  it('opens an example', async () => {
    const { onOpenExample } = setup();
    await choose('Examples', 'Listas');

    expect(onOpenExample).toHaveBeenCalledWith('16-listas', expect.stringContaining('lista de compras'));
  });

  it('changes the font size within the limits', async () => {
    const { onChangeSettings } = setup();
    await choose('Interface', 'Increase font');

    expect(onChangeSettings).toHaveBeenCalledWith({ fontSize: DEFAULT_SETTINGS.fontSize + 1 });
  });
});
