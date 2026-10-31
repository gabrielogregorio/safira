import { render, screen, waitFor, within } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { loadProjects } from '@/projects/projectStore';
import { App } from './App';
import { FakeWorker } from './fakeWorker';

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

describe('App', () => {
  beforeEach(() => {
    localStorage.clear();
    Range.prototype.getClientRects = () => [] as unknown as DOMRectList;
    Range.prototype.getBoundingClientRect = () => ({ left: 0, right: 0, top: 0, bottom: 0 }) as DOMRect;
    Object.defineProperty(navigator, 'language', { value: 'en-US', configurable: true });
    Element.prototype.scrollTo = vi.fn();
    document.documentElement.removeAttribute('data-theme');
  });

  it('shows the home screen without projects', () => {
    renderApp();

    expect(screen.getByRole('heading', { name: 'Safira', level: 1 })).toBeInTheDocument();
    expect(screen.getByText('You have no projects yet.')).toBeInTheDocument();
    expect(screen.queryByRole('button', { name: 'Variaveis' })).not.toBeInTheDocument();
  });

  it('only shows the examples after pressing create', async () => {
    renderApp();
    await userEvent.click(screen.getByRole('button', { name: 'Create project' }));

    expect(screen.getByRole('button', { name: 'Variaveis' })).toBeInTheDocument();
  });

  it('creates a project without choosing anything', async () => {
    renderApp();
    await userEvent.click(screen.getByRole('button', { name: 'Create project' }));
    await userEvent.click(screen.getByRole('button', { name: 'Go ahead' }));

    expect(screen.getByRole('heading', { name: 'New project' })).toBeInTheDocument();
    expect(loadProjects().map((project) => project.files['main.safira'])).toEqual(['#safira 1.0\n']);
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
    const example = screen.getByRole('button', { name: 'Pare' });
    await userEvent.click(example);

    expect(example).toHaveAttribute('aria-pressed', 'true');

    await userEvent.click(example);

    expect(example).toHaveAttribute('aria-pressed', 'false');
  });

  it('runs an example and shows its output in the terminal', async () => {
    renderApp();
    await openExample('Pare');
    await userEvent.click(screen.getByRole('button', { name: 'Run' }));

    const terminal = screen.getByRole('log');
    await waitFor(() => {
      expect(terminal).toHaveTextContent('soma: 4');
    });
    expect(worker.requests[0]).toMatchObject({ type: 'start', mode: 'run', file: 'main.safira' });
  });

  it('does not show the hidden version line in the editor', async () => {
    renderApp();
    await openExample('Pare');

    expect(document.querySelector('.cm-content')).not.toHaveTextContent('#safira');
  });

  it('shows an error with its line and a link to the example', async () => {
    localStorage.setItem(
      'safira.projects.v1',
      JSON.stringify([{ id: '1', name: 'Erro', files: { 'main.safira': 'x recebe nada' }, breakpoints: {} }]),
    );
    renderApp();
    await userEvent.click(screen.getByRole('button', { name: 'Open Erro' }));
    await userEvent.click(screen.getByRole('button', { name: 'Run' }));

    const alert = await screen.findByRole('alert');
    expect(alert).toHaveTextContent('Line 1');

    await userEvent.click(within(alert).getByRole('button', { name: 'See an example' }));

    expect(screen.getByRole('button', { name: '01-variaveis.safira' })).toHaveAttribute('aria-current', 'page');
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
    await userEvent.click(screen.getByRole('button', { name: 'Open Atual' }));

    expect(screen.queryByRole('alert')).not.toBeInTheDocument();

    await userEvent.click(screen.getByRole('button', { name: 'Back to projects' }));
    await userEvent.click(screen.getByRole('button', { name: 'Open Futuro' }));

    expect(screen.getByRole('alert')).toHaveTextContent('declares Safira 9.0');
    expect(screen.getByRole('alert')).toHaveTextContent('0.38, 1.0');
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
    await userEvent.click(screen.getByRole('button', { name: 'Open Entrada' }));
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
    await userEvent.click(screen.getByRole('button', { name: 'Open Debug' }));
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
    await userEvent.click(screen.getByRole('button', { name: 'Open Loop' }));
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
    await userEvent.click(screen.getByRole('button', { name: 'Open Arq' }));
    await userEvent.click(screen.getByRole('button', { name: 'Run' }));

    await waitFor(() => {
      expect(Object.keys(loadProjects()[0]?.files ?? {})).toContain('a.txt');
    });
  });

  it('runs with Ctrl+Enter', async () => {
    renderApp();
    await openExample('Pare');
    await userEvent.keyboard('{Control>}{Enter}{/Control}');

    await waitFor(() => {
      expect(screen.getByRole('log')).toHaveTextContent('soma: 4');
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
    await userEvent.click(screen.getByRole('button', { name: 'Open Pausa' }));
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
    await userEvent.click(screen.getByRole('button', { name: 'Open Vars' }));

    expect(screen.getByText('Run your program to see its variables here.')).toBeInTheDocument();

    await userEvent.click(screen.getByRole('button', { name: 'Run' }));
    await screen.findByRole('cell', { name: 'idade' });
    await userEvent.type(screen.getByLabelText('Search variables'), 'no');

    expect(screen.queryByRole('cell', { name: 'idade' })).not.toBeInTheDocument();
    expect(screen.getByRole('cell', { name: 'nome' })).toBeInTheDocument();
  });

  it('renames and deletes a project', async () => {
    localStorage.setItem(
      'safira.projects.v1',
      JSON.stringify([{ id: '1', name: 'Velho', files: {}, breakpoints: {} }]),
    );
    renderApp();
    await userEvent.click(screen.getByRole('button', { name: 'Rename Velho' }));
    const field = screen.getByLabelText('Project name', { selector: '[role=dialog] input' });
    await userEvent.clear(field);
    await userEvent.type(field, 'Novo{Enter}');

    expect(screen.getByText('Novo')).toBeInTheDocument();

    await userEvent.click(screen.getByRole('button', { name: 'Delete Novo' }));
    await userEvent.click(screen.getByRole('button', { name: 'Delete' }));

    expect(screen.getByText('You have no projects yet.')).toBeInTheDocument();
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

  it('changes the language and the theme from the home screen', async () => {
    renderApp();
    await userEvent.click(screen.getByRole('button', { name: 'Theme and language' }));
    await userEvent.click(screen.getByRole('radio', { name: 'Português (Brasil)' }));

    expect(screen.getByRole('dialog', { name: 'Tema e idioma' })).toBeInTheDocument();
    expect(document.documentElement.lang).toBe('pt-br');

    await userEvent.click(screen.getByRole('radio', { name: 'Escuro' }));

    expect(document.documentElement.dataset['theme']).toBe('dark');
  });

  it('offers theme and language in the editor and in the lessons', async () => {
    renderApp();
    await userEvent.click(screen.getByRole('button', { name: 'Lessons' }));

    expect(screen.getByRole('button', { name: 'Theme and language' })).toBeInTheDocument();

    await userEvent.click(screen.getByRole('button', { name: 'Back to projects' }));
    await openExample('Pare');

    expect(screen.getByRole('button', { name: 'Theme and language' })).toBeInTheDocument();
  });

  it('opens the lessons and walks through them', async () => {
    renderApp();
    await userEvent.click(screen.getByRole('button', { name: 'Lessons' }));
    await userEvent.click(screen.getByRole('button', { name: 'Next' }));

    expect(screen.getByRole('heading', { name: 'Exibicao', level: 1 })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Apresentacao (Read)' })).toBeInTheDocument();
  });
});
