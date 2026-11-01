import { act, render, screen, waitFor, within, fireEvent } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { strToU8, zipSync } from 'fflate';
import { loadProjects } from '@/projects/projectStore';
import { loadSettings } from '@/settings/settings';
import { App } from './App';
import { FakeWorker } from './fakeWorker';
import { snapAway } from './snapEffect';
import { soundPlayer } from './sound/sounds';
import { scrambleDocument } from './textScramble';

vi.mock('./snapEffect', () => ({
  hidePointer: vi.fn(),
  markReturnFromSnap: vi.fn(),
  snapAway: vi.fn(() => Promise.resolve()),
}));

vi.mock('./textScramble', () => ({ scrambleDocument: vi.fn(() => vi.fn()) }));

let worker: FakeWorker;

const renderApp = (): ReturnType<typeof render> =>
  render(
    <App
      createWorker={() => {
        worker = new FakeWorker();

        return worker;
      }}
    />,
  );

const openExample = async (name: string): Promise<void> => {
  await userEvent.click(screen.getByRole('button', { name: 'Create project' }));
  await userEvent.click(screen.getByRole('button', { name }));
  await userEvent.click(screen.getByRole('button', { name: 'Go ahead' }));
};

const allowMotion = (): void => {
  vi.stubGlobal('matchMedia', () => ({
    matches: true,
    addListener: vi.fn(),
    removeListener: vi.fn(),
    addEventListener: vi.fn(),
    removeEventListener: vi.fn(),
  }));
};

describe('App', () => {
  beforeEach(() => {
    localStorage.clear();
    window.history.replaceState(null, '', '#/');
    Object.defineProperty(navigator, 'language', { value: 'en-US', configurable: true });
    document.documentElement.removeAttribute('data-theme');
    document.documentElement.removeAttribute('data-theme-changing');
  });

  afterEach(() => {
    vi.useRealTimers();
    vi.unstubAllGlobals();
    vi.restoreAllMocks();
    vi.mocked(scrambleDocument).mockClear();
  });

  it('shows the home screen without projects', () => {
    renderApp();

    expect(screen.getByRole('heading', { name: 'Safira', level: 1 })).toBeInTheDocument();
    expect(screen.getByText('You have no projects yet.')).toBeInTheDocument();
    expect(screen.queryByRole('button', { name: 'Variables' })).not.toBeInTheDocument();
  });

  it('only shows the examples after pressing create', async () => {
    renderApp();
    await userEvent.click(screen.getByRole('button', { name: 'Create project' }));

    expect(screen.getByRole('button', { name: 'Variables' })).toBeInTheDocument();
  });

  it('creates a project without choosing anything', async () => {
    renderApp();
    await userEvent.click(screen.getByRole('button', { name: 'Create project' }));
    await userEvent.click(screen.getByRole('button', { name: 'Go ahead' }));

    expect(screen.getByRole('heading', { name: 'New project' })).toBeInTheDocument();
    expect(loadProjects().map((project) => project.files['main.safira'])).toEqual(['#safira 1.1\n']);
  });

  it('creates a project with the typed name', async () => {
    renderApp();
    await userEvent.click(screen.getByRole('button', { name: 'Create project' }));
    await userEvent.type(screen.getByLabelText('Project name (optional)'), 'Meu jogo{Enter}');

    expect(screen.getByRole('heading', { name: 'Meu jogo' })).toBeInTheDocument();
    expect(loadProjects().map((project) => project.name)).toEqual(['Meu jogo']);
  });

  it('can undo the choice of an example', async () => {
    renderApp();
    await userEvent.click(screen.getByRole('button', { name: 'Create project' }));
    const example = screen.getByRole('button', { name: 'Break' });
    await userEvent.click(example);

    expect(example).toHaveAttribute('aria-pressed', 'true');

    await userEvent.click(example);

    expect(example).toHaveAttribute('aria-pressed', 'false');
  });

  it('runs an example and shows its output in the terminal', async () => {
    renderApp();
    await openExample('Break');
    await userEvent.click(screen.getByRole('button', { name: 'Run' }));

    const terminal = screen.getByRole('log');
    await waitFor(() => {
      expect(terminal).toHaveTextContent('1');
    });
    expect(worker.requests[0]).toMatchObject({ type: 'start', mode: 'run', file: 'main.safira' });
  });

  it('does not show the hidden version line in the editor', async () => {
    renderApp();
    await openExample('Break');

    expect(document.querySelector('.cm-content')).not.toHaveTextContent('#safira');
  });

  it('shows an error with its line and a link to the example', async () => {
    localStorage.setItem(
      'safira.projects.v1',
      JSON.stringify([{ id: '1', name: 'Erro', files: { 'main.safira': 'x recebe nada' }, breakpoints: {} }]),
    );
    renderApp();
    await userEvent.click(screen.getByRole('link', { name: 'Open Erro' }));
    await userEvent.click(screen.getByRole('button', { name: 'Run' }));

    const alert = await screen.findByRole('alert');
    expect(alert).toHaveTextContent('Line 1');

    await userEvent.click(within(alert).getByRole('button', { name: 'See an example' }));

    expect(screen.getByRole('dialog', { name: 'Variables' })).toHaveTextContent('name');
    expect(screen.queryByRole('button', { name: '01-variaveis.safira' })).not.toBeInTheDocument();
  });

  it('warns only when the script version is not supported', async () => {
    localStorage.setItem(
      'safira.projects.v1',
      JSON.stringify([
        { id: '1', name: 'Futuro', files: { 'main.safira': '#safira 9.0\nmostre 1' }, breakpoints: {} },
        { id: '2', name: 'Atual', files: { 'main.safira': '#safira 1.0\nmostre 1' }, breakpoints: {} },
      ]),
    );
    renderApp();
    await userEvent.click(screen.getByRole('link', { name: 'Open Atual' }));

    expect(screen.queryByRole('alert')).not.toBeInTheDocument();

    await userEvent.click(screen.getByRole('button', { name: 'Back to projects' }));
    await userEvent.click(screen.getByRole('link', { name: 'Open Futuro' }));

    expect(screen.getByRole('alert')).toHaveTextContent('declares Safira 9.0');
    expect(screen.getByRole('alert')).toHaveTextContent('0.38, 0.9, 1.0');
  });

  it('asks for input in the terminal and continues', async () => {
    localStorage.setItem(
      'safira.projects.v1',
      JSON.stringify([
        {
          id: '1',
          name: 'Entrada',
          files: { 'main.safira': 'n = o que o usuario digitar\nmostre "oi " + n' },
          breakpoints: {},
        },
      ]),
    );
    renderApp();
    await userEvent.click(screen.getByRole('link', { name: 'Open Entrada' }));
    await userEvent.click(screen.getByRole('button', { name: 'Run' }));
    await userEvent.type(await screen.findByLabelText('Type here and press Enter'), 'Ana{Enter}');

    await waitFor(() => {
      expect(screen.getByRole('log')).toHaveTextContent('oi Ana');
    });
  });

  it('pauses line by line and shows the variables', async () => {
    localStorage.setItem(
      'safira.projects.v1',
      JSON.stringify([{ id: '1', name: 'Debug', files: { 'main.safira': 'x = 1\nmostre x' }, breakpoints: {} }]),
    );
    renderApp();
    await userEvent.click(screen.getByRole('link', { name: 'Open Debug' }));
    await userEvent.keyboard('{F6}');
    await screen.findByRole('button', { name: 'Next line' });
    await userEvent.click(screen.getByRole('button', { name: 'Next line' }));

    expect(await screen.findByRole('cell', { name: 'x' })).toBeInTheDocument();
    expect(screen.getByRole('cell', { name: 'float' })).toBeInTheDocument();
  });

  it('stops a program that does not finish', async () => {
    localStorage.setItem(
      'safira.projects.v1',
      JSON.stringify([
        { id: '1', name: 'Loop', files: { 'main.safira': 'n = o que o usuario digitar' }, breakpoints: {} },
      ]),
    );
    renderApp();
    await userEvent.click(screen.getByRole('link', { name: 'Open Loop' }));
    await userEvent.click(screen.getByRole('button', { name: 'Run' }));
    await userEvent.click(screen.getByRole('button', { name: 'Stop' }));

    expect(worker.terminated).toBe(true);
    expect(screen.getByRole('log')).toHaveTextContent('Execution stopped');
  });

  it('saves files the program created in the project', async () => {
    localStorage.setItem(
      'safira.projects.v1',
      JSON.stringify([{ id: '1', name: 'Arq', files: { 'main.safira': 'crie o arquivo "a.txt"' }, breakpoints: {} }]),
    );
    renderApp();
    await userEvent.click(screen.getByRole('link', { name: 'Open Arq' }));
    await userEvent.click(screen.getByRole('button', { name: 'Run' }));

    await waitFor(() => {
      expect(Object.keys(loadProjects()[0]?.files ?? {})).toContain('a.txt');
    });
  });

  it('runs with Ctrl+Enter', async () => {
    renderApp();
    await openExample('Break');
    await userEvent.keyboard('{Control>}{Enter}{/Control}');

    await waitFor(() => {
      expect(screen.getByRole('log')).toHaveTextContent('1');
    });
  });

  it('stops at a breakpoint when running and shows the inspector', async () => {
    localStorage.setItem(
      'safira.projects.v1',
      JSON.stringify([
        { id: '1', name: 'Pausa', files: { 'main.safira': 'x = 1\nmostre x' }, breakpoints: { 'main.safira': [2] } },
      ]),
    );
    renderApp();
    await userEvent.click(screen.getByRole('link', { name: 'Open Pausa' }));
    await userEvent.click(screen.getByRole('button', { name: 'Run' }));

    expect(await screen.findByText('Paused on line 2')).toBeInTheDocument();
    expect(screen.getByRole('cell', { name: 'x' })).toBeInTheDocument();
  });

  it('filters the variables in the inspector', async () => {
    localStorage.setItem(
      'safira.projects.v1',
      JSON.stringify([{ id: '1', name: 'Vars', files: { 'main.safira': 'idade = 1\nnome = "a"' }, breakpoints: {} }]),
    );
    renderApp();
    await userEvent.click(screen.getByRole('link', { name: 'Open Vars' }));

    expect(screen.getByText('Run your program to see its variables here.')).toBeInTheDocument();

    await userEvent.click(screen.getByRole('button', { name: 'Run' }));
    await screen.findByRole('cell', { name: 'idade' });
    await userEvent.type(screen.getByLabelText('Search variables'), 'no');

    expect(screen.queryByRole('cell', { name: 'idade' })).not.toBeInTheDocument();
    expect(screen.getByRole('cell', { name: 'nome' })).toBeInTheDocument();
  });

  it('opens a project from its address', () => {
    localStorage.setItem(
      'safira.projects.v1',
      JSON.stringify([{ id: '1', name: 'Link', files: { 'main.safira': 'x', 'a.txt': 'y' }, breakpoints: {} }]),
    );
    window.history.replaceState(null, '', '#/projects/1/a.txt');
    renderApp();

    expect(screen.getByRole('heading', { name: 'Link' })).toBeInTheDocument();
    expect(document.querySelector('.cm-content')).toHaveTextContent('y');
  });

  it('goes home when the project of the address does not exist', () => {
    window.history.replaceState(null, '', '#/projects/nada');
    renderApp();

    expect(screen.getByRole('heading', { name: 'Safira', level: 1 })).toBeInTheDocument();
  });

  it('creates files and folders from the sidebar', async () => {
    renderApp();
    await userEvent.click(screen.getByRole('button', { name: 'Create project' }));
    await userEvent.click(screen.getByRole('button', { name: 'Go ahead' }));
    await userEvent.click(screen.getByRole('button', { name: 'New folder' }));
    await userEvent.keyboard('dados{Enter}');
    fireEvent.contextMenu(screen.getByRole('button', { name: 'dados', expanded: true }));
    await userEvent.click(await screen.findByRole('menuitem', { name: 'New file' }));
    await userEvent.keyboard('lib{Enter}');

    expect(Object.keys(loadProjects()[0]?.files ?? {})).toEqual(
      expect.arrayContaining(['dados/.keep', 'dados/lib.safira']),
    );
    expect(window.location.hash).toBe('#/projects/' + loadProjects()[0]?.id + '/dados%2Flib.safira');
  });

  it('asks before deleting a file and closes its tab', async () => {
    localStorage.setItem(
      'safira.projects.v1',
      JSON.stringify([{ id: '1', name: 'P', files: { 'main.safira': 'a', 'b.txt': 'c' }, breakpoints: {} }]),
    );
    renderApp();
    await userEvent.click(screen.getByRole('link', { name: 'Open P' }));
    fireEvent.contextMenu(screen.getByRole('button', { name: 'b.txt' }));
    await userEvent.click(await screen.findByRole('menuitem', { name: 'Delete' }));

    expect(Object.keys(loadProjects()[0]?.files ?? {})).toContain('b.txt');

    await userEvent.click(screen.getByRole('button', { name: 'Delete' }));

    expect(Object.keys(loadProjects()[0]?.files ?? {})).toEqual(['main.safira']);
  });

  it('removes from the project a file the program deleted', async () => {
    localStorage.setItem(
      'safira.projects.v1',
      JSON.stringify([
        { id: '1', name: 'P', files: { 'main.safira': 'delete o arquivo "b.txt"', 'b.txt': 'c' }, breakpoints: {} },
      ]),
    );
    renderApp();
    await userEvent.click(screen.getByRole('link', { name: 'Open P' }));
    await userEvent.click(screen.getByRole('button', { name: 'Run' }));

    await waitFor(() => {
      expect(Object.keys(loadProjects()[0]?.files ?? {})).toEqual(['main.safira']);
    });
  });

  it('imports a project from a zip file', async () => {
    const archive = zipSync({ 'main.safira': strToU8('mostre 1') });
    const file = new File([archive.slice()], 'jogo.zip', { type: 'application/zip' });
    file.arrayBuffer = () => Promise.resolve(archive.buffer);
    renderApp();
    await userEvent.upload(screen.getByLabelText('Import project (.zip)', { selector: 'input' }), file);

    expect(await screen.findByText('Imported 1 files.')).toBeInTheDocument();
    expect(loadProjects().map((project) => project.name)).toEqual(['jogo']);
  });

  it('explains a broken zip file and creates nothing', async () => {
    const file = new File(['nada'], 'quebrado.zip', { type: 'application/zip' });
    file.arrayBuffer = () => Promise.resolve(new Uint8Array([1, 2, 3]).buffer);
    renderApp();
    await userEvent.upload(screen.getByLabelText('Import project (.zip)', { selector: 'input' }), file);

    expect(await screen.findByText('This file is not a valid .zip.')).toBeInTheDocument();
    expect(loadProjects()).toEqual([]);
  });

  it('renames and deletes a project', async () => {
    localStorage.setItem(
      'safira.projects.v1',
      JSON.stringify([{ id: '1', name: 'Velho', files: {}, breakpoints: {} }]),
    );
    renderApp();
    await userEvent.click(screen.getByRole('button', { name: 'Velho' }));
    await userEvent.keyboard('Novo{Enter}');

    expect(screen.getByText('Novo')).toBeInTheDocument();

    await userEvent.click(screen.getByRole('button', { name: 'Delete Novo' }));
    await userEvent.click(screen.getByRole('button', { name: 'Delete' }));

    expect(screen.getByText('You have no projects yet.')).toBeInTheDocument();
  });

  it('renames the project by clicking its name in the IDE, without the gem', async () => {
    localStorage.setItem(
      'safira.projects.v1',
      JSON.stringify([{ id: '1', name: 'Velho', files: { 'main.safira': '' }, breakpoints: {} }]),
    );
    window.history.replaceState(null, '', '#/projects/1/main.safira');
    renderApp();
    await userEvent.click(within(screen.getByRole('heading', { level: 1 })).getByRole('button', { name: 'Velho' }));
    await userEvent.keyboard('Novo{Enter}');

    expect(loadProjects().map((project) => project.name)).toEqual(['Novo']);
    expect(screen.getByRole('heading', { name: 'Novo', level: 1 })).toBeInTheDocument();
    expect(document.querySelector('.safira-logo')).toBeNull();
  });

  it('renames a project by clicking its name on the home screen', async () => {
    localStorage.setItem(
      'safira.projects.v1',
      JSON.stringify([{ id: '1', name: 'Velho', files: {}, breakpoints: {} }]),
    );
    renderApp();
    await userEvent.click(screen.getByRole('button', { name: 'Velho' }));
    await userEvent.keyboard('Novo');
    await userEvent.click(document.body);

    expect(loadProjects().map((project) => project.name)).toEqual(['Novo']);
  });

  it('moves files, breakpoints, tabs and unsaved text when a folder is renamed', async () => {
    localStorage.setItem(
      'safira.projects.v1',
      JSON.stringify([
        {
          id: '1',
          name: 'P',
          files: { 'dados/a.safira': 'mostre 2\n', 'dados/b.txt': 'x', 'main.safira': '' },
          breakpoints: { 'dados/a.safira': [1] },
        },
      ]),
    );
    window.history.replaceState(null, '', '#/projects/1/dados%2Fa.safira');
    renderApp();
    fireEvent.contextMenu(screen.getByRole('button', { name: 'dados', expanded: true }));
    await userEvent.click(await screen.findByRole('menuitem', { name: 'Rename' }));
    await userEvent.keyboard('info{Enter}');

    const [project] = loadProjects();

    expect(Object.keys(project.files)).toEqual(['info/a.safira', 'info/b.txt', 'main.safira']);
    expect(project.files['info/a.safira']).toContain('mostre 2');
    expect(project.breakpoints).toEqual({ 'info/a.safira': [1] });
    expect(window.location.hash).toContain('info');
    expect(document.querySelector('.tab-active')).toHaveTextContent('info/a.safira');
    expect(document.querySelector('.cm-content')).toHaveTextContent('mostre 2');
  });

  it('keeps the project when the delete confirmation is cancelled', async () => {
    localStorage.setItem('safira.projects.v1', JSON.stringify([{ id: '1', name: 'Fica', files: {}, breakpoints: {} }]));
    renderApp();
    await userEvent.click(screen.getByRole('button', { name: 'Delete Fica' }));

    expect(screen.getByRole('dialog', { name: 'Delete project?' })).toHaveTextContent('"Fica" and all its files');
    expect(screen.getByRole('button', { name: 'Cancel' })).toHaveFocus();

    await userEvent.click(screen.getByRole('button', { name: 'Cancel' }));

    expect(screen.queryByRole('dialog')).not.toBeInTheDocument();
    expect(loadProjects().map((project) => project.name)).toEqual(['Fica']);
  });

  it('closes a modal with Escape', async () => {
    renderApp();
    await userEvent.click(screen.getByRole('button', { name: 'Create project' }));

    expect(screen.getByLabelText('Project name (optional)')).toHaveFocus();

    await userEvent.keyboard('{Escape}');

    expect(screen.queryByRole('dialog')).not.toBeInTheDocument();
  });

  it('changes the language and the theme by clicking the icons on the home screen', async () => {
    renderApp();
    await userEvent.click(screen.getByRole('button', { name: /^Language: / }));

    expect(screen.queryByRole('dialog')).not.toBeInTheDocument();
    expect(document.documentElement.lang).toBe('pt-br');

    await userEvent.click(screen.getByRole('button', { name: /^Tema: / }));

    expect(document.documentElement.dataset['theme']).toBe('dark');
  });

  it('offers the icons at home and leaves them to the menu in the editor', async () => {
    renderApp();

    expect(screen.getByRole('button', { name: /^Theme: / })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /^Language: / })).toBeInTheDocument();

    await openExample('Break');

    expect(screen.queryByRole('button', { name: /^Language: / })).not.toBeInTheDocument();
    expect(screen.queryByRole('button', { name: /^Sound: / })).not.toBeInTheDocument();
    expect(screen.queryByRole('button', { name: /^Theme: / })).not.toBeInTheDocument();
  });

  it('highlights the screen while a file is dragged and imports the dropped .zip', async () => {
    renderApp();
    const dataTransfer = {
      types: ['Files'],
      files: [new File([zipSync({ 'main.safira': strToU8('mostre 1') })], 'arrastado.zip')],
    };

    fireEvent.dragEnter(document, { dataTransfer });

    expect(screen.getByText('Drop the .zip to create a project')).toBeInTheDocument();

    fireEvent.drop(document, { dataTransfer });

    expect(screen.queryByText('Drop the .zip to create a project')).not.toBeInTheDocument();
    await waitFor(() => {
      expect(loadProjects().map((project) => project.name)).toContain('arrastado');
    });
  });

  it('ignores something dragged that is not a file', () => {
    renderApp();
    fireEvent.dragEnter(document, { dataTransfer: { types: ['text/plain'], files: [] } });

    expect(screen.queryByText('Drop the .zip to create a project')).not.toBeInTheDocument();
  });

  it('removes the highlight when the file leaves the window', () => {
    renderApp();
    fireEvent.dragEnter(document, { dataTransfer: { types: ['Files'], files: [] } });
    fireEvent(document, Object.assign(new Event('dragleave'), { relatedTarget: null }));

    expect(screen.queryByText('Drop the .zip to create a project')).not.toBeInTheDocument();
  });

  describe('theme animation', () => {
    const THEME_CHANGE_MILLISECONDS = 1700;
    const root = document.documentElement;

    const pressTheme = (): void => {
      fireEvent.click(screen.getByRole('button', { name: /^Theme: / }));
    };

    const wait = (milliseconds: number): void => {
      act(() => {
        vi.advanceTimersByTime(milliseconds);
      });
    };

    beforeEach(() => {
      allowMotion();
      vi.useFakeTimers({ toFake: ['setTimeout', 'clearTimeout'] });
    });

    it('marks the page during the change and clears the mark afterwards', () => {
      renderApp();
      pressTheme();

      expect(root.dataset['themeChanging']).toBe('true');

      wait(THEME_CHANGE_MILLISECONDS);

      expect(root.dataset['themeChanging']).toBeUndefined();
    });

    it('counts the time again when the theme changes during the animation', () => {
      renderApp();
      pressTheme();
      wait(THEME_CHANGE_MILLISECONDS - 1);
      pressTheme();
      wait(THEME_CHANGE_MILLISECONDS - 1);

      expect(root.dataset['themeChanging']).toBe('true');

      wait(1);

      expect(root.dataset['themeChanging']).toBeUndefined();
    });

    it('cancels the pending cleanup when it leaves the screen', () => {
      const { unmount } = renderApp();
      pressTheme();
      unmount();
      wait(THEME_CHANGE_MILLISECONDS);

      expect(root.dataset['themeChanging']).toBe('true');
    });
  });

  it('never marks the theme change without motion', async () => {
    renderApp();
    await userEvent.click(screen.getByRole('button', { name: /^Theme: / }));

    expect(document.documentElement.dataset['themeChanging']).toBeUndefined();
  });

  it('scrambles the texts when the language changes, if motion is allowed', async () => {
    allowMotion();
    renderApp();
    await userEvent.click(screen.getByRole('button', { name: /^Language: / }));

    expect(scrambleDocument).toHaveBeenCalledExactlyOnceWith(document.body);
  });

  it('plays the note of an item that has one when hovered', async () => {
    const play = vi.spyOn(soundPlayer, 'play').mockResolvedValue(undefined);
    renderApp();
    await openExample('Break');
    await userEvent.click(screen.getByRole('menuitem', { name: 'Examples' }));
    await userEvent.hover(await screen.findByRole('menuitem', { name: '💎 Introduction' }));

    expect(play).toHaveBeenCalledWith('hoverSpecial', 0.5);
  });

  it('applies the sound choice before saving it', async () => {
    const setEnabled = vi.spyOn(soundPlayer, 'setEnabled');
    renderApp();
    await userEvent.click(screen.getByRole('button', { name: /^Sound: / }));

    expect(setEnabled).toHaveBeenLastCalledWith(false);
    expect(loadSettings().sound).toBe(false);
  });

  it('jumps to the content from the skip link', async () => {
    renderApp();
    await userEvent.click(screen.getByRole('link', { name: 'Skip to content' }));

    expect(document.getElementById('content')).toHaveFocus();
  });

  it('warns when the browser refuses to save the projects', async () => {
    vi.spyOn(Storage.prototype, 'setItem').mockImplementation(() => {
      throw new DOMException('full', 'QuotaExceededError');
    });
    renderApp();
    await userEvent.click(screen.getByRole('button', { name: 'Create project' }));
    await userEvent.click(screen.getByRole('button', { name: 'Go ahead' }));

    expect(screen.getByRole('alert')).toHaveTextContent('The browser refused to save your projects.');
  });

  it('closes the notice of an import', async () => {
    const file = new File(['nada'], 'quebrado.zip', { type: 'application/zip' });
    file.arrayBuffer = () => Promise.resolve(new Uint8Array([1, 2, 3]).buffer);
    renderApp();
    await userEvent.upload(screen.getByLabelText('Import project (.zip)', { selector: 'input' }), file);
    const status = await screen.findByRole('status');
    await userEvent.click(within(status).getByRole('button', { name: 'Close' }));

    expect(screen.queryByText('This file is not a valid .zip.')).not.toBeInTheDocument();
  });

  it('keeps the other projects when one is renamed', async () => {
    localStorage.setItem(
      'safira.projects.v1',
      JSON.stringify([
        { id: '1', name: 'Velho', files: {}, breakpoints: {} },
        { id: '2', name: 'Outro', files: {}, breakpoints: {} },
      ]),
    );
    renderApp();
    await userEvent.click(screen.getByRole('button', { name: 'Velho' }));
    await userEvent.keyboard('Novo{Enter}');

    expect(loadProjects().map((project) => project.name)).toEqual(['Novo', 'Outro']);
  });

  it('opens the aquarium from the orb and goes back home', async () => {
    renderApp();
    await userEvent.click(screen.getByRole('button', { name: 'Open the aquarium' }));

    expect(window.location.hash).toBe('#/aquarium');
    expect(await screen.findByRole('img', { name: 'Aquarium' })).toBeInTheDocument();

    await userEvent.click(within(screen.getByRole('dialog')).getByRole('button', { name: 'Close' }));

    await waitFor(() => {
      expect(window.location.hash).toBe('#/');
    });
  });

  it('shows the globe alone on its address and goes back home', async () => {
    window.history.replaceState(null, '', '#/globe');
    renderApp();

    expect(screen.queryByRole('heading', { name: 'Safira', level: 1 })).not.toBeInTheDocument();
    expect(document.querySelector('.wallpaper')).not.toBeNull();

    await userEvent.click(screen.getByRole('button', { name: 'Close' }));

    expect(screen.getByRole('heading', { name: 'Safira', level: 1 })).toBeInTheDocument();
  });

  it('crumbles the screen after erasing everything and starts over', async () => {
    const reload = vi.fn();
    const location = { hash: '', search: '', reload };
    localStorage.setItem('safira.projects.v1', JSON.stringify([{ id: '1', name: 'P', files: {}, breakpoints: {} }]));
    renderApp();
    await userEvent.click(screen.getByRole('button', { name: 'Settings' }));
    await userEvent.click(screen.getByRole('button', { name: 'Delete everything' }));
    const confirmation = screen.getByRole('dialog', { name: 'Delete everything?' });
    await userEvent.click(within(confirmation).getByRole('button', { name: 'Delete everything' }));

    expect(loadProjects()).toEqual([]);

    vi.stubGlobal('location', location);

    await waitFor(() => {
      expect(reload).toHaveBeenCalledOnce();
    });
    expect(snapAway).toHaveBeenCalledOnce();
    expect(location.hash).toBe('#/');
  });

  it('changes the vision mode from the settings at home', async () => {
    renderApp();
    await userEvent.click(screen.getByRole('button', { name: 'Settings' }));
    await userEvent.click(screen.getByRole('radio', { name: 'Tritanopia (weak blue)' }));

    expect(loadSettings().vision).toBe('tritanopia');
  });
});
