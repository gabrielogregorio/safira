import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { examplesOf } from '@/content/content';
import { DEFAULT_SETTINGS, FONT_SIZE_STEP } from '@/settings/settings';
import { IdeMenuBar } from './IdeMenuBar';

const setup = (isRunning = false) => {
  const actions = {
    onNewTab: vi.fn(),
    onFormat: vi.fn(),
    onExportProject: vi.fn(),
    onImportArchive: vi.fn(),
    onRun: vi.fn(),
    onStop: vi.fn(),
    onToggleBreakpoint: vi.fn(),
    onClearBreakpoints: vi.fn(),
    onOpenExample: vi.fn(),
    onToggleLessonMode: vi.fn(),
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

const chooseRadio = async (submenu: string, item: string): Promise<void> => {
  await userEvent.click(screen.getByRole('menuitem', { name: 'Interface' }));
  await userEvent.click(await screen.findByRole('menuitem', { name: (name) => name.startsWith(submenu) }));
  await userEvent.click(await screen.findByRole('menuitemradio', { name: (name) => name.endsWith(item) }));
};

describe('IdeMenuBar', () => {
  afterEach(() => {
    vi.restoreAllMocks();
  });

  it('shows the six menus', () => {
    setup();

    expect(screen.getAllByRole('menuitem').map((item) => item.textContent)).toEqual([
      'File',
      'Run',
      'Learn',
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

  it('runs everything and runs to the next breakpoint', async () => {
    const { onRun } = setup();
    await choose('Run', 'Run all');
    await choose('Run', 'Run to breakpoint');

    expect(onRun.mock.calls).toEqual([['run'], ['debug']]);
  });

  it('only allows stopping while running', async () => {
    setup();
    await userEvent.click(screen.getByRole('menuitem', { name: 'Run' }));

    expect(await screen.findByRole('menuitem', { name: 'Stop execution' })).toHaveAttribute('aria-disabled', 'true');
  });

  it('opens an example', async () => {
    const { onOpenExample } = setup();
    await choose('Learn', 'Lists');

    expect(onOpenExample).toHaveBeenCalledWith('16-listas', expect.stringContaining('list of'));
  });

  it('opens a program, which plays its own note when hovered', async () => {
    const { onOpenExample } = setup();
    const [firstProgram] = examplesOf('en-us').filter((example) => example.id.startsWith('programa-'));
    await userEvent.click(screen.getByRole('menuitem', { name: 'Examples' }));
    const item = await screen.findByRole('menuitem', { name: firstProgram.title });

    expect(item).toHaveAttribute('data-hover-rate', '0.5');

    await userEvent.click(item);

    expect(onOpenExample).toHaveBeenCalledWith(firstProgram.id, firstProgram.text);
  });

  it.each([
    ['Theme', 'Dark', { theme: 'dark' }],
    ['Accessibility', 'Tritanopia (weak blue)', { vision: 'tritanopia' }],
    ['Code font', 'Istok Web', { codeFont: 'aero' }],
  ])('Interface > %s > %s changes the setting', async (submenu, item, change) => {
    const { onChangeSettings } = setup();
    await chooseRadio(submenu, item);

    expect(onChangeSettings).toHaveBeenCalledExactlyOnceWith(change);
  });

  it('turns the sound off', async () => {
    const { onChangeSettings } = setup();
    await userEvent.click(screen.getByRole('menuitem', { name: 'Interface' }));
    await userEvent.click(await screen.findByRole('menuitemcheckbox', { name: /Sound$/ }));

    expect(onChangeSettings).toHaveBeenCalledExactlyOnceWith({ sound: !DEFAULT_SETTINGS.sound });
  });

  it('opens the bug report and the blog in a new page', async () => {
    const open = vi.spyOn(window, 'open').mockReturnValue(null);
    setup();
    await choose('Help', 'Report a bug');
    await choose('Help', 'Community blog');

    expect(open.mock.calls).toEqual([
      ['https://github.com/safira-lang/safira-ide/issues', '_blank', 'noopener'],
      ['https://github.com/gabrielogregorio/safira/wiki', '_blank', 'noopener'],
    ]);
  });

  it('changes the font size within the limits', async () => {
    const { onChangeSettings } = setup();
    await choose('Interface', 'Increase font');

    expect(onChangeSettings).toHaveBeenCalledWith({ fontSize: DEFAULT_SETTINGS.fontSize + FONT_SIZE_STEP });
  });

  it('decreases the font size', async () => {
    const { onChangeSettings } = setup();
    await choose('Interface', 'Decrease font');

    expect(onChangeSettings).toHaveBeenCalledExactlyOnceWith({ fontSize: DEFAULT_SETTINGS.fontSize - FONT_SIZE_STEP });
  });
});
