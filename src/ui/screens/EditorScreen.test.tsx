import { EditorView } from '@codemirror/view';
import { act, fireEvent, render, screen, waitFor, within } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { strToU8, zipSync } from 'fflate';
import { loadProjects } from '@/projects/projectStore';
import type { RunnerEvent, RunnerFailure } from '@/runtime/protocol';
import { DEFAULT_SETTINGS, FONT_SIZE_STEP, loadSettings } from '@/settings/settings';
import { App } from '@/ui/App';
import { downloadFile, downloadProject } from '@/ui/archiveFiles';
import { FakeWorker } from '@/ui/fakeWorker';
import type { RunnerWorker, WorkerFactory } from '@/ui/hooks/useRunner';
import { soundPlayer } from '@/ui/sound/sounds';

vi.mock('@/ui/archiveFiles', async (importOriginal) => ({
  ...(await importOriginal<typeof import('@/ui/archiveFiles')>()),
  downloadFile: vi.fn(),
  downloadProject: vi.fn(),
}));

const MAIN = 'main.safira';

let worker: FakeWorker;

const createFakeWorker: WorkerFactory = () => {
  worker = new FakeWorker();

  return worker;
};

interface OpenOptions {
  file?: string;
  breakpoints?: Record<string, number[]>;
  order?: string[];
  createWorker?: WorkerFactory;
}

const openProject = (files: Record<string, string>, options: OpenOptions = {}): void => {
  const { file, breakpoints = {}, order, createWorker = createFakeWorker } = options;
  localStorage.setItem('safira.projects.v1', JSON.stringify([{ id: '1', name: 'P', files, breakpoints, order }]));
  const route = file === undefined ? '#/projects/1' : '#/projects/1/' + encodeURIComponent(file);
  window.history.replaceState(null, '', route);
  render(<App createWorker={createWorker} />);
};

const savedProject = () => loadProjects()[0];

const editor = (): EditorView =>
  EditorView.findFromDOM(document.querySelector('.cm-editor') as HTMLElement) as EditorView;

const shownText = (): string => editor().state.doc.toString();

const replaceText = (text: string): void => {
  act(() => {
    editor().dispatch({ changes: { from: 0, to: editor().state.doc.length, insert: text } });
  });
};

const tabs = (): (string | null)[] => [...document.querySelectorAll('.tab')].map((tab) => tab.textContent);

const activeTab = (): Element | null => document.querySelector('.tab-active');

const choose = async (menu: string, item: string): Promise<void> => {
  await userEvent.click(screen.getByRole('menuitem', { name: menu }));
  await userEvent.click(await screen.findByRole('menuitem', { name: (name) => name.startsWith(item) }));
};

const chooseInRow = async (row: string, item: string | RegExp): Promise<void> => {
  fireEvent.contextMenu(within(screen.getByLabelText('Files')).getByRole('button', { name: row }));
  await userEvent.click(await screen.findByRole('menuitem', { name: item }));
};

const finishesWith =
  (failure: RunnerFailure): WorkerFactory =>
  () => {
    const fake: RunnerWorker = {
      onmessage: null,
      terminate: () => undefined,
      postMessage: (request) => {
        if (request.type === 'start') {
          const data: RunnerEvent = { type: 'finished', files: request.files, variables: [], failure };
          fake.onmessage?.({ data } as MessageEvent<RunnerEvent>);
        }
      },
    };

    return fake;
  };

const failure: RunnerFailure = { message: 'Falhou', line: 1, file: MAIN, example: null, missingName: null };

describe('EditorScreen', () => {
  beforeEach(() => {
    localStorage.clear();
    Object.defineProperty(navigator, 'language', { value: 'en-US', configurable: true });
  });

  afterEach(() => {
    vi.restoreAllMocks();
    vi.unstubAllGlobals();
    vi.mocked(downloadFile).mockClear();
    vi.mocked(downloadProject).mockClear();
  });

  describe('opening', () => {
    it('falls back to the first file of a project without the main script', () => {
      openProject({ 'a.txt': 'texto' });

      expect(tabs()[0]).toContain('a.txt');
      expect(shownText()).toBe('texto');
    });

    it('opens an empty main script in a project without files', () => {
      openProject({});

      expect(tabs()[0]).toContain(MAIN);
      expect(shownText()).toBe('');
    });

    it('opens a tab for a file that arrives through the address', async () => {
      openProject({ [MAIN]: '', 'a.txt': 'texto' });

      act(() => {
        window.history.pushState(null, '', '#/projects/1/a.txt');
        window.dispatchEvent(new HashChangeEvent('hashchange'));
      });

      await waitFor(() => {
        expect(activeTab()).toHaveTextContent('a.txt');
      });
      expect(tabs()).toHaveLength(2);
      expect(shownText()).toBe('texto');
    });
  });

  describe('tabs', () => {
    it('goes to a tab when it is pressed', async () => {
      openProject({ [MAIN]: '', 'a.txt': 'texto' });
      await userEvent.click(screen.getByRole('button', { name: 'a.txt' }));
      await userEvent.click(
        within(document.querySelector('.tab-bar') as HTMLElement).getByRole('button', { name: MAIN }),
      );

      expect(window.location.hash).toContain(encodeURIComponent(MAIN));
      expect(activeTab()).toHaveTextContent(MAIN);
    });

    it('moves to the next tab when the active one closes', async () => {
      openProject({ [MAIN]: 'a', 'a.txt': 'texto' });
      await userEvent.click(screen.getByRole('button', { name: 'a.txt' }));
      await userEvent.click(screen.getByRole('button', { name: 'Close tab a.txt' }));

      expect(tabs()).toHaveLength(1);
      expect(activeTab()).toHaveTextContent(MAIN);
      expect(window.location.hash).toContain(encodeURIComponent(MAIN));
    });

    it('stays where it is when another tab closes', async () => {
      openProject({ [MAIN]: 'a', 'a.txt': 'texto' });
      await userEvent.click(screen.getByRole('button', { name: 'a.txt' }));
      await userEvent.click(screen.getByRole('button', { name: `Close tab ${MAIN}` }));

      expect(tabs()).toHaveLength(1);
      expect(activeTab()).toHaveTextContent('a.txt');
    });

    it('leaves a blank script when the last tab closes, keeping what was typed', async () => {
      openProject({ [MAIN]: 'a' });
      replaceText('mostre 2');
      await userEvent.click(screen.getByRole('button', { name: `Close tab ${MAIN}` }));

      expect(activeTab()).toHaveTextContent('script-1.safira');
      expect(shownText()).toBe('');
      expect(savedProject().files[MAIN]).toContain('mostre 2');
    });

    it('creates a new tab with a free name from the menu and with Ctrl+N', async () => {
      openProject({ [MAIN]: '', 'script-1.safira': '' });
      await choose('File', 'New tab');

      expect(activeTab()).toHaveTextContent('script-2.safira');

      await userEvent.keyboard('{Control>}n{/Control}');

      expect(activeTab()).toHaveTextContent('script-3.safira');
    });

    it('opens an example in its own tab', async () => {
      openProject({ [MAIN]: '' });
      await choose('Learn', 'Lists');

      expect(activeTab()).toHaveTextContent('16-listas.safira');
      expect(shownText()).toContain('list of');
    });
  });

  describe('saving', () => {
    it('saves right away with Ctrl+S', async () => {
      openProject({ [MAIN]: 'a' });
      replaceText('mostre 2');

      expect(savedProject().files[MAIN]).not.toContain('mostre 2');

      await userEvent.keyboard('{Control>}s{/Control}');

      expect(savedProject().files[MAIN]).toContain('mostre 2');
    });

    it('does not lose text typed in a new tab when a program finishes before the autosave', async () => {
      openProject({ [MAIN]: '' });
      await userEvent.keyboard('{Control>}n{/Control}');
      replaceText('mostre 2');
      await userEvent.keyboard('{F5}');

      await waitFor(() => {
        expect(screen.getByRole('log')).toHaveTextContent('2');
      });
      await waitFor(() => {
        expect(savedProject().files['script-1.safira']).toContain('mostre 2');
      });
    });
  });

  describe('running', () => {
    const startedRuns = (): number => worker.requests.filter((request) => request.type === 'start').length;

    it.each([
      ['F5', 'run'],
      ['F7', 'debug'],
    ])('starts with %s in mode %s', async (key, mode) => {
      openProject({ [MAIN]: 'mostre 1' });
      await userEvent.keyboard(`{${key}}`);

      expect(worker.requests[0]).toMatchObject({ type: 'start', mode });
    });

    it('runs in debug mode when the project has breakpoints', async () => {
      openProject({ [MAIN]: 'mostre 1' }, { breakpoints: { 'b.safira': [1] } });
      await userEvent.keyboard('{F5}');

      expect(worker.requests[0]).toMatchObject({ mode: 'debug' });
    });

    it('continues a paused program from the debug bar', async () => {
      openProject({ [MAIN]: 'mostre 1' });
      await userEvent.keyboard('{F6}');
      const bar = await screen.findByText('Paused on line 1');
      await userEvent.click(within(bar.parentElement as HTMLElement).getByRole('button', { name: 'Continue' }));

      await waitFor(() => {
        expect(screen.getByRole('log')).toHaveTextContent('1');
      });
      expect(startedRuns()).toBe(1);
      expect(screen.queryByText('Paused on line 1')).not.toBeInTheDocument();
    });

    it('does not start again while a program runs', async () => {
      openProject({ [MAIN]: 'n = o que o usuario digitar' });
      await userEvent.keyboard('{F5}');
      await screen.findByLabelText('Type here and press Enter');
      await userEvent.keyboard('{Control>}{Enter}{/Control}');

      expect(startedRuns()).toBe(1);
    });

    it('explains a missing name', async () => {
      openProject({ [MAIN]: '' }, { createWorker: finishesWith({ ...failure, missingName: 'nome' }) });
      await userEvent.keyboard('{F5}');

      expect(await screen.findByRole('alert')).toHaveTextContent('looks for a variable called nome');
    });

    it('offers no example when the failure has none', async () => {
      openProject({ [MAIN]: '' }, { createWorker: finishesWith(failure) });
      await userEvent.keyboard('{F5}');
      const alert = await screen.findByRole('alert');

      expect(alert).toHaveTextContent('Line 1: Falhou');
      expect(within(alert).queryByRole('button', { name: 'See an example' })).not.toBeInTheDocument();
    });

    it('closes the example of a failure', async () => {
      openProject({ [MAIN]: '' }, { createWorker: finishesWith({ ...failure, example: '02' }) });
      await userEvent.keyboard('{F5}');
      await userEvent.click(await screen.findByRole('button', { name: 'See an example' }));

      expect(screen.getByRole('dialog')).toBeInTheDocument();

      await userEvent.keyboard('{Escape}');

      expect(screen.queryByRole('dialog')).not.toBeInTheDocument();
    });
  });

  describe('breakpoints', () => {
    it('toggles the breakpoint of the cursor line with F10', async () => {
      openProject({ [MAIN]: 'a' });
      await userEvent.keyboard('{F10}');

      expect(savedProject().breakpoints).toEqual({ [MAIN]: [1] });

      await userEvent.keyboard('{F10}');

      expect(savedProject().breakpoints).toEqual({ [MAIN]: [] });
    });

    it('toggles from the menu, following the cursor', async () => {
      openProject({ [MAIN]: 'a\nb' });
      act(() => {
        editor().dispatch({ selection: { anchor: 2 } });
      });
      await choose('Run', 'Toggle breakpoint');

      expect(savedProject().breakpoints).toEqual({ [MAIN]: [2] });
    });

    it('clears them all, also in the program that is paused', async () => {
      openProject({ [MAIN]: 'a = 1\nb = 2' }, { breakpoints: { [MAIN]: [2] } });
      await userEvent.keyboard('{F7}');
      await screen.findByText('Paused on line 2');
      await choose('Run', 'Clear breakpoints');

      expect(savedProject().breakpoints).toEqual({});
      expect(worker.requests.at(-1)).toEqual({ type: 'breakpoints', breakpoints: {} });
    });
  });

  describe('files', () => {
    it('refuses a file name that leaves the project', async () => {
      openProject({ [MAIN]: '' });
      await userEvent.click(screen.getByRole('button', { name: 'New file' }));
      await userEvent.keyboard('..{Enter}');

      expect(Object.keys(savedProject().files)).toEqual([MAIN]);
    });

    it('refuses a folder name that leaves the project', async () => {
      openProject({ [MAIN]: '' });
      await userEvent.click(screen.getByRole('button', { name: 'New folder' }));
      await userEvent.keyboard('..{Enter}');

      expect(Object.keys(savedProject().files)).toEqual([MAIN]);
    });

    it('opens a file that already exists instead of overwriting it', async () => {
      openProject({ [MAIN]: '', 'a.txt': 'texto' });
      await userEvent.click(screen.getByRole('button', { name: 'New file' }));
      await userEvent.keyboard('a.txt{Enter}');

      expect(savedProject().files['a.txt']).toBe('texto');
      expect(activeTab()).toHaveTextContent('a.txt');
    });

    it('leaves a blank script after deleting the only open file', async () => {
      openProject({ [MAIN]: '', 'script-1.safira': '' });
      await chooseInRow(MAIN, 'Delete');
      await userEvent.click(screen.getByRole('button', { name: 'Delete' }));

      expect(activeTab()).toHaveTextContent('script-2.safira');
    });

    it('goes to another tab after deleting the active file', async () => {
      openProject({ [MAIN]: '', 'a.txt': 'texto' });
      await userEvent.click(within(screen.getByLabelText('Files')).getByRole('button', { name: 'a.txt' }));
      await chooseInRow('a.txt', 'Delete');
      await userEvent.click(screen.getByRole('button', { name: 'Delete' }));

      expect(Object.keys(savedProject().files)).toEqual([MAIN]);
      expect(activeTab()).toHaveTextContent(MAIN);
    });

    it('deletes a folder with what is inside it, staying on the active file', async () => {
      openProject({ [MAIN]: '', 'dados/a.txt': '', 'dados/b.txt': '' });
      await chooseInRow('dados', 'Delete');

      expect(screen.getByRole('dialog', { name: 'Delete this item?' })).toHaveTextContent('"dados" will be deleted');

      await userEvent.click(screen.getByRole('button', { name: 'Delete' }));

      expect(Object.keys(savedProject().files)).toEqual([MAIN]);
      expect(activeTab()).toHaveTextContent(MAIN);
    });

    it.each(['the cancel button', 'Escape'])('keeps the item when the deletion is refused by %s', async (way) => {
      openProject({ [MAIN]: '', 'a.txt': '' });
      await chooseInRow('a.txt', 'Delete');

      if (way === 'Escape') {
        await userEvent.keyboard('{Escape}');
      } else {
        await userEvent.click(screen.getByRole('button', { name: 'Cancel' }));
      }

      expect(screen.queryByRole('dialog')).not.toBeInTheDocument();
      expect(Object.keys(savedProject().files)).toContain('a.txt');
    });

    it('keeps the marker of a folder emptied by a move, and follows the active file', async () => {
      const play = vi.spyOn(soundPlayer, 'play').mockResolvedValue(undefined);
      openProject({ [MAIN]: '', 'dados/a.txt': 'texto' }, { file: 'dados/a.txt', breakpoints: { 'dados/a.txt': [1] } });
      await chooseInRow('a.txt', /^Move to/);
      await userEvent.click(await screen.findByRole('button', { name: 'Project root' }));

      expect(new Set(Object.keys(savedProject().files))).toEqual(new Set(['a.txt', 'dados/.keep', MAIN]));
      expect(savedProject().breakpoints).toEqual({ 'a.txt': [1] });
      expect(activeTab()).toHaveTextContent('a.txt');
      expect(window.location.hash).toBe('#/projects/1/a.txt');
      expect(play).toHaveBeenCalledWith('move');
    });

    it('needs no marker when the folder keeps other files, and stays on the active file', async () => {
      openProject({ [MAIN]: '', 'dados/a.txt': '', 'dados/b.txt': '' });
      await chooseInRow('a.txt', /^Move to/);
      await userEvent.click(await screen.findByRole('button', { name: 'Project root' }));

      expect(new Set(Object.keys(savedProject().files))).toEqual(new Set(['a.txt', 'dados/b.txt', MAIN]));
      expect(activeTab()).toHaveTextContent(MAIN);
    });

    it('updates the saved order when a file is renamed', async () => {
      openProject({ [MAIN]: '', 'a.txt': '' }, { order: ['a.txt', MAIN] });
      await chooseInRow('a.txt', 'Rename');
      await userEvent.keyboard('novo{Enter}');

      expect(savedProject().order).toEqual(['novo.txt', MAIN]);
    });

    it('downloads a file with the text on screen', async () => {
      openProject({ 'a.txt': 'velho' });
      replaceText('novo');
      await chooseInRow('a.txt', 'Download');

      expect(downloadFile).toHaveBeenCalledExactlyOnceWith('a.txt', 'novo');
    });

    it('downloads a folder as a project with its inner paths', async () => {
      openProject({ [MAIN]: '', 'dados/a.txt': 'texto' });
      await chooseInRow('dados', 'Download');

      expect(downloadProject).toHaveBeenCalledExactlyOnceWith({ name: 'dados', files: { 'a.txt': 'texto' } });
    });

    it('exports the whole project from the menu', async () => {
      openProject({ 'a.txt': 'velho' });
      replaceText('novo');
      await choose('File', 'Export project');

      expect(downloadProject).toHaveBeenCalledExactlyOnceWith({ name: 'P', files: { 'a.txt': 'novo' } });
    });
  });

  describe('importing into the project', () => {
    const archiveInput = (): HTMLElement =>
      screen.getByLabelText('Import .zip into this project', { selector: 'input' });

    const zipFile = (bytes: Uint8Array): File => {
      const file = new File([bytes.slice()], 'pacote.zip', { type: 'application/zip' });
      file.arrayBuffer = () => Promise.resolve(bytes.slice().buffer);

      return file;
    };

    it('opens the file picker from the menu', async () => {
      openProject({ [MAIN]: '' });
      const click = vi.spyOn(archiveInput(), 'click');
      await choose('File', 'Import .zip');

      expect(click).toHaveBeenCalledOnce();
    });

    it('adds the files, refreshes the open tab and lets the notice be closed', async () => {
      openProject({ 'a.txt': 'velho' });
      await userEvent.upload(archiveInput(), zipFile(zipSync({ 'a.txt': strToU8('novo'), 'b.txt': strToU8('b') })));

      const notice = await screen.findByText('Imported 2 files.');

      expect(shownText()).toBe('novo');
      expect(new Set(Object.keys(savedProject().files))).toEqual(new Set(['a.txt', 'b.txt']));

      await userEvent.click(within(notice.parentElement as HTMLElement).getByRole('button', { name: 'Close' }));

      expect(screen.queryByText('Imported 2 files.')).not.toBeInTheDocument();
    });

    it('explains a broken file and changes nothing', async () => {
      openProject({ 'a.txt': 'velho' });
      await userEvent.upload(archiveInput(), zipFile(new Uint8Array([1, 2, 3])));

      expect(await screen.findByText('This file is not a valid .zip.')).toBeInTheDocument();
      expect(Object.keys(savedProject().files)).toEqual(['a.txt']);
    });
  });

  describe('interface', () => {
    it('formats the code', async () => {
      const play = vi.spyOn(soundPlayer, 'play').mockResolvedValue(undefined);
      openProject({ [MAIN]: 'repita 3 vezes {\nmostre 1\n}' });
      await choose('File', 'Format code');

      expect(shownText()).toBe('repita 3 vezes {\n    mostre 1\n}');
      expect(play).toHaveBeenCalledWith('format');
    });

    it('lists the commands and closes the list', async () => {
      openProject({ [MAIN]: '' });
      await choose('Help', 'Available commands');
      const dialog = screen.getByRole('dialog', { name: 'Available commands' });

      expect(within(dialog).getAllByRole('listitem').length).toBeGreaterThan(0);
      expect(dialog).toHaveTextContent('mostre');
      expect(dialog).toHaveTextContent('guarde a resposta em');
      expect(dialog).not.toHaveTextContent('anotar resposta');

      await userEvent.keyboard('{Escape}');

      expect(screen.queryByRole('dialog')).not.toBeInTheDocument();
    });

    it('changes the font size with its buttons', async () => {
      openProject({ [MAIN]: '' });
      await userEvent.click(screen.getByRole('button', { name: 'Increase font' }));

      expect(loadSettings().fontSize).toBe(DEFAULT_SETTINGS.fontSize + FONT_SIZE_STEP);

      await userEvent.click(screen.getByRole('button', { name: 'Decrease font' }));

      expect(loadSettings().fontSize).toBe(DEFAULT_SETTINGS.fontSize);
    });

    it('lets the code get a little smaller on a phone, down to a readable size', async () => {
      vi.stubGlobal('innerWidth', 400);
      openProject({ [MAIN]: '' });

      for (let press = 0; press < 5; press += 1) {
        await userEvent.click(screen.getByRole('button', { name: 'Decrease font' }));
      }

      expect(loadSettings().fontSize).toBe(12);
    });

    it('turns the suggestions off and on, each with its sound', async () => {
      const play = vi.spyOn(soundPlayer, 'play').mockResolvedValue(undefined);
      openProject({ [MAIN]: '' });
      const toggle = screen.getByRole('checkbox', { name: 'Smart suggestions' });
      await userEvent.click(toggle);

      expect(loadSettings().suggestions).toBe(false);
      expect(play).toHaveBeenCalledWith('suggestionsOff');

      await userEvent.click(toggle);

      expect(loadSettings().suggestions).toBe(true);
      expect(play).toHaveBeenCalledWith('suggestionsOn');
    });

    it.each([
      ['Resize the files panel', 'ArrowRight', 'sidebar', 16],
      ['Resize the output panel', 'ArrowLeft', 'output', 16],
      ['Resize the variables panel', 'ArrowUp', 'inspector', 16],
    ] as const)('%s saves its size', (label, key, panel, change) => {
      openProject({ [MAIN]: '' });
      fireEvent.keyDown(screen.getByRole('separator', { name: label }), { key });

      expect(loadSettings().panels[panel]).toBe(DEFAULT_SETTINGS.panels[panel] + change);
    });

    it('switches the panel shown on a phone', async () => {
      openProject({ [MAIN]: '' });
      const panels = screen.getByRole('navigation', { name: 'Safira IDE' });
      await userEvent.click(within(panels).getByRole('button', { name: 'Output' }));

      expect(document.getElementById('content')).toHaveClass('workspace-output');
      expect(within(panels).getByRole('button', { name: 'Output' })).toHaveAttribute('aria-pressed', 'true');
    });

    it.each([
      [
        'an example of the menu',
        async () => {
          await choose('Learn', 'Lists');
        },
      ],
      [
        'a file of the tree',
        async () => {
          await userEvent.click(screen.getByRole('button', { name: 'outro.safira' }));
        },
      ],
      [
        'a new file',
        async () => {
          await userEvent.click(screen.getByRole('button', { name: 'New file' }));
          await userEvent.keyboard('{Enter}');
        },
      ],
    ])('goes to the code on a phone after opening %s', async (_name, open) => {
      openProject({ [MAIN]: '', 'outro.safira': '' });
      const panels = screen.getByRole('navigation', { name: 'Safira IDE' });
      await userEvent.click(within(panels).getByRole('button', { name: 'Output' }));
      await open();

      expect(within(panels).getByRole('button', { name: 'Code' })).toHaveAttribute('aria-pressed', 'true');
    });

    it('goes to the code on a phone after changing tabs', async () => {
      openProject({ [MAIN]: '', 'outro.safira': '' });
      await userEvent.click(screen.getByRole('button', { name: 'outro.safira' }));
      const panels = screen.getByRole('navigation', { name: 'Safira IDE' });
      await userEvent.click(within(panels).getByRole('button', { name: 'Output' }));
      const tabs = screen.getByRole('navigation', { name: 'Virtual files of this project' });
      await userEvent.click(within(tabs).getByRole('button', { name: MAIN }));

      expect(within(panels).getByRole('button', { name: 'Code' })).toHaveAttribute('aria-pressed', 'true');
    });

    describe('full screen', () => {
      const requestFullscreen = vi.fn();
      const exitFullscreen = vi.fn();

      const setFullScreenElement = (element: Element | null): void => {
        Object.defineProperty(document, 'fullscreenElement', { value: element, configurable: true });
      };

      beforeEach(() => {
        document.documentElement.requestFullscreen = requestFullscreen;
        document.exitFullscreen = exitFullscreen;
      });

      afterEach(() => {
        Reflect.deleteProperty(document, 'fullscreenElement');
        Reflect.deleteProperty(document.documentElement, 'requestFullscreen');
        Reflect.deleteProperty(document, 'exitFullscreen');
        vi.clearAllMocks();
      });

      it('enters with F11', async () => {
        setFullScreenElement(null);
        openProject({ [MAIN]: '' });
        await userEvent.keyboard('{F11}');

        expect(requestFullscreen).toHaveBeenCalledOnce();
        expect(exitFullscreen).not.toHaveBeenCalled();
      });

      it('ignores F11 in a browser without the Fullscreen API', async () => {
        Reflect.deleteProperty(document.documentElement, 'requestFullscreen');
        openProject({ [MAIN]: '' });
        await userEvent.keyboard('{F11}');

        expect(exitFullscreen).not.toHaveBeenCalled();
      });

      it('leaves with F11', async () => {
        setFullScreenElement(document.documentElement);
        openProject({ [MAIN]: '' });
        await userEvent.keyboard('{F11}');

        expect(exitFullscreen).toHaveBeenCalledOnce();
        expect(requestFullscreen).not.toHaveBeenCalled();
      });
    });
  });
});
