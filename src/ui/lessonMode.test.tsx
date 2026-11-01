import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { lessonsOf } from '@/content/content';
import { loadProjects } from '@/projects/projectStore';
import { loadSettings } from '@/settings/settings';
import { App } from './App';
import { createFakeCheckWorker, FakeWorker } from './fakeWorker';

const lessons = lessonsOf('en-us');
const firstLesson = lessons[0];

const renderApp = (): ReturnType<typeof render> =>
  render(<App createWorker={() => new FakeWorker()} createLessonCheckWorker={createFakeCheckWorker} />);

const openProject = async (): Promise<void> => {
  renderApp();
  await userEvent.click(screen.getByRole('button', { name: 'Create project' }));
  await userEvent.click(screen.getByRole('button', { name: 'Go ahead' }));
};

const pressHelpItem = async (): Promise<void> => {
  await userEvent.click(screen.getByRole('menuitem', { name: 'Help' }));
  await userEvent.click(await screen.findByRole('menuitem', { name: 'Lesson mode' }));
};

const enterLessonMode = async (): Promise<void> => {
  await openProject();
  await pressHelpItem();
};

const run = async (): Promise<void> => {
  await userEvent.click(screen.getByRole('button', { name: 'Run' }));
};

const nextButton = (): Promise<HTMLElement> => screen.findByRole('button', { name: 'Next' });

const finishExample = async (): Promise<void> => {
  await run();
  await userEvent.click(await nextButton());
};

const solveChallenge = async (): Promise<void> => {
  await run();
  await userEvent.click(await screen.findByRole('button', { name: 'Show the solution' }));
  await run();
};

describe('lesson mode', () => {
  beforeEach(() => {
    localStorage.clear();
    sessionStorage.setItem('safira.cat.met', 'true');
    window.history.replaceState(null, '', '#/');
  });

  it('shows a switch while it is on, and turning the switch off removes it', async () => {
    await openProject();
    await pressHelpItem();
    const lessonSwitch = await screen.findByRole('checkbox', { name: 'Lesson mode' });

    expect(lessonSwitch).toBeChecked();

    await userEvent.click(lessonSwitch);

    expect(screen.queryByRole('checkbox', { name: 'Lesson mode' })).not.toBeInTheDocument();
    expect(document.querySelector('.cat')).toBeNull();
    expect(loadSettings().lessonMode).toBe(false);
  });

  it('only starts from the Help menu', async () => {
    await openProject();

    expect(screen.queryByRole('checkbox', { name: 'Lesson mode' })).not.toBeInTheDocument();

    await pressHelpItem();

    expect(document.querySelector('.cat')).not.toBeNull();
  });

  it('shows the first step in the IDE and swaps the tabs for the lesson bar', async () => {
    await enterLessonMode();

    expect(document.querySelector('.cm-content')).toHaveTextContent('show');
    expect(screen.getByRole('combobox', { name: 'Choose a lesson' })).toHaveValue(firstLesson.id);
    expect(document.querySelector('.tab')).toBeNull();
    expect(Object.keys(loadProjects()[0].files)).toContain('lessons/01-1.safira');
  });

  it('shows a program to run before the challenge', async () => {
    await enterLessonMode();

    expect(document.querySelector('.cm-content')).toHaveTextContent('show');
    expect(screen.getByText('Read this code.')).toBeInTheDocument();

    await userEvent.click(screen.getByRole('button', { name: 'Continue' }));

    expect(screen.getByText('Press ▶')).toBeInTheDocument();

    await run();

    expect(await screen.findByText('Well done! You can move on.')).toBeInTheDocument();
    expect(loadSettings().lessonProgress).toEqual([`${firstLesson.id}:0`]);
  });

  it('refuses a wrong answer, explains it, and accepts the solution', async () => {
    await enterLessonMode();
    await finishExample();
    expect(screen.getByText('Write your answer and press ▶ Run.')).toBeInTheDocument();

    await run();

    expect(await screen.findByText(/^Tip: /)).toBeInTheDocument();
    expect(await nextButton()).toBeDisabled();

    await userEvent.click(screen.getByRole('button', { name: 'Show the solution' }));

    expect(await screen.findByText('Press ▶')).toBeInTheDocument();
    expect(screen.queryByText(/^Tip: /)).not.toBeInTheDocument();
    expect(screen.queryByRole('button', { name: 'Show the solution' })).not.toBeInTheDocument();

    await run();

    expect(await screen.findByText('Correct! Challenge complete.')).toBeInTheDocument();
    expect(await nextButton()).toBeEnabled();
    expect(loadSettings().lessonProgress).toContain(`${firstLesson.id}:1`);
  });

  it('counts the steps done at the bottom', async () => {
    await enterLessonMode();
    const total = String(lessons.reduce((sum, lesson) => sum + lesson.steps.length, 0));

    expect(screen.getByRole('progressbar')).toHaveAttribute('aria-valuetext', `0 of ${total} steps`);

    await run();
    await nextButton();

    expect(screen.getByRole('progressbar')).toHaveAttribute('aria-valuetext', `1 of ${total} steps`);
  });

  it('goes to the next lesson after the challenge', async () => {
    await enterLessonMode();
    await finishExample();
    await solveChallenge();
    await userEvent.click(await nextButton());

    expect(screen.getByRole('combobox', { name: 'Choose a lesson' })).toHaveValue(lessons[1].id);
    expect(screen.getByRole('button', { name: 'Next step' })).toBeDisabled();
  });

  it('puts the starting code back', async () => {
    await enterLessonMode();
    await finishExample();
    await run();
    await userEvent.click(await screen.findByRole('button', { name: 'Show the solution' }));
    await run();
    await userEvent.click(await screen.findByRole('button', { name: 'Start over' }));

    expect(document.querySelector('.cm-content')).not.toHaveTextContent('show "');
  });

  it('changes lessons in the bar', async () => {
    await enterLessonMode();
    await userEvent.selectOptions(screen.getByRole('combobox', { name: 'Choose a lesson' }), lessons[2].id);

    expect(await screen.findByRole('combobox', { name: 'Choose a lesson' })).toHaveValue(lessons[2].id);
    expect(Object.keys(loadProjects()[0].files)).toContain('lessons/03-1.safira');
  });

  it('keeps the place after a reload', async () => {
    await enterLessonMode();
    await finishExample();
    document.body.replaceChildren();
    renderApp();

    expect(await screen.findByRole('button', { name: /^Step 1: .* \(done\)$/ })).toBeInTheDocument();
  });

  it('gives the tabs back when the mode ends', async () => {
    await enterLessonMode();
    await pressHelpItem();

    expect(document.querySelector('.cat')).toBeNull();
    expect(document.querySelector('.tab')).not.toBeNull();
    expect(loadSettings().lessonMode).toBe(false);
  });

  it('moves to the scripts of the new language', async () => {
    await enterLessonMode();
    await userEvent.click(screen.getByRole('menuitem', { name: 'Interface' }));
    await userEvent.click(await screen.findByRole('menuitem', { name: 'Language' }));
    await userEvent.click(await screen.findByRole('menuitemradio', { name: 'Español' }));

    expect(await screen.findByRole('option', { name: /^1\. Háblame/ })).toBeInTheDocument();
    expect(Object.keys(loadProjects()[0].files)).toContain('clases/01-1.safira');
    expect(Object.keys(loadProjects()[0].files)).not.toContain('lessons/01-1.safira');
  });

  it('offers the way back from another file', async () => {
    await enterLessonMode();
    await userEvent.click(screen.getByRole('button', { name: /^main\.safira/ }));

    expect(screen.getByRole('button', { name: 'Back to the lesson' })).toBeInTheDocument();
  });

  it('loses the cat for good after the last challenge', async () => {
    await enterLessonMode();
    const last = lessons[lessons.length - 1];
    await userEvent.selectOptions(screen.getByRole('combobox', { name: 'Choose a lesson' }), last.id);
    await finishExample();
    await solveChallenge();

    await vi.waitFor(() => {
      expect(loadSettings().catLeft).toBe(true);
    });

    expect(document.querySelector('.cat')).toBeNull();

    await userEvent.click(screen.getByRole('menuitem', { name: 'Help' }));

    expect(await screen.findByRole('menuitem', { name: 'Available commands' })).toBeInTheDocument();
    expect(screen.queryByRole('menuitem', { name: 'Lesson mode' })).not.toBeInTheDocument();
  });
});
