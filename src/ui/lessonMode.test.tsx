import { render, screen, within } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { lessonsOf } from '@/content/content';
import { loadProjects } from '@/projects/projectStore';
import { loadSettings } from '@/settings/settings';
import { App } from './App';
import { createFakeCheckWorker, FakeWorker } from './fakeWorker';

const lessons = lessonsOf('en-us');
const firstLesson = lessons[0];
const STEPS_BEFORE_CHALLENGE = firstLesson.steps.length - 1;

const renderApp = (): ReturnType<typeof render> =>
  render(<App createWorker={() => new FakeWorker()} createLessonCheckWorker={createFakeCheckWorker} />);

const openProject = async (): Promise<void> => {
  renderApp();
  await userEvent.click(screen.getByRole('button', { name: 'Create project' }));
  await userEvent.click(screen.getByRole('button', { name: 'Go ahead' }));
};

const lessonSwitch = (): HTMLElement => screen.getByRole('checkbox', { name: 'Lesson mode' });

const enterLessonMode = async (): Promise<void> => {
  await openProject();
  await userEvent.click(lessonSwitch());
};

const run = async (): Promise<void> => {
  await userEvent.click(screen.getByRole('button', { name: 'Run' }));
};

const nextButton = (): HTMLElement => screen.getByRole('button', { name: 'Next' });

const continueButton = (): HTMLElement =>
  within(document.querySelector<HTMLElement>('.cat-bubble') as HTMLElement).getByRole('button', { name: 'Continue' });

const finishStep = async (): Promise<void> => {
  await run();
  await userEvent.click(await screen.findByRole('button', { name: 'Next' }));
};

const goToChallenge = async (): Promise<void> => {
  await enterLessonMode();

  for (let step = 0; step < STEPS_BEFORE_CHALLENGE; step += 1) {
    await finishStep();
  }
};

describe('lesson mode', () => {
  beforeEach(() => {
    localStorage.clear();
    sessionStorage.setItem('safira.cat.met', 'true');
    window.history.replaceState(null, '', '#/');
  });

  it('shows the first step in the IDE and swaps the tabs for the lesson bar', async () => {
    await enterLessonMode();

    expect(screen.getByRole('heading', { name: firstLesson.steps[0].title })).toBeInTheDocument();
    expect(screen.getByRole('combobox', { name: 'Choose a lesson' })).toHaveValue(firstLesson.id);
    expect(document.querySelector('.tab')).toBeNull();
    expect(document.querySelector('.cm-content')).toHaveTextContent('show');
    expect(Object.keys(loadProjects()[0].files)).toContain('lessons/01-apresentacao-1.safira');
  });

  it('asks for a run before moving on, and gives the check after it', async () => {
    await enterLessonMode();

    await userEvent.click(continueButton());

    expect(screen.getByText('Press ▶ Run to see it work.')).toBeInTheDocument();
    expect(screen.queryByRole('button', { name: 'Next' })).not.toBeInTheDocument();

    await run();

    expect(await screen.findByText('Well done! You can move on.')).toBeInTheDocument();
    expect(nextButton()).toBeEnabled();
    expect(loadSettings().lessonProgress).toEqual([`${firstLesson.id}:0`]);
    expect(screen.getByRole('button', { name: /^Step 1: .* \(done\)$/ })).toHaveTextContent('✓');
  });

  it('counts the steps done at the bottom', async () => {
    await enterLessonMode();
    const steps = lessons.reduce((total, lesson) => total + lesson.steps.length, 0);

    expect(screen.getByRole('progressbar')).toHaveAttribute('aria-valuetext', `0 of ${String(steps)} steps`);

    await run();
    await screen.findByText('Well done! You can move on.');

    expect(screen.getByRole('progressbar')).toHaveAttribute('aria-valuetext', `1 of ${String(steps)} steps`);
  });

  it('walks to the next step, which starts locked', async () => {
    await enterLessonMode();
    await finishStep();

    expect(screen.getByRole('heading', { name: firstLesson.steps[1].title })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Next step' })).toBeDisabled();
    expect(screen.getByRole('button', { name: 'Previous step' })).toBeEnabled();
  });

  it('refuses a wrong challenge, explains it, and accepts the solution', async () => {
    await goToChallenge();

    await userEvent.click(continueButton());

    expect(screen.getByText('Write your answer and press ▶ Run.')).toBeInTheDocument();

    await run();

    expect(await screen.findByText(/^Tip: /)).toBeInTheDocument();
    expect(nextButton()).toBeDisabled();

    await userEvent.click(screen.getByRole('button', { name: 'Show the solution' }));
    await run();

    expect(await screen.findByText('Correct! Challenge complete.')).toBeInTheDocument();
    expect(nextButton()).toBeEnabled();
    expect(loadSettings().lessonProgress).toContain(`${firstLesson.id}:${String(STEPS_BEFORE_CHALLENGE)}`);
  });

  it('puts the starting code back', async () => {
    await goToChallenge();
    await run();
    await userEvent.click(await screen.findByRole('button', { name: 'Show the solution' }));
    await userEvent.click(screen.getByRole('button', { name: 'Start over' }));

    expect(document.querySelector('.cm-content')).not.toHaveTextContent('show');
  });

  it('changes lessons in the bar', async () => {
    await enterLessonMode();
    await userEvent.selectOptions(screen.getByRole('combobox', { name: 'Choose a lesson' }), lessons[2].id);

    expect(await screen.findByRole('heading', { name: lessons[2].steps[0].title })).toBeInTheDocument();
    expect(Object.keys(loadProjects()[0].files)).toContain('lessons/03-variaveis-1.safira');
  });

  it('keeps the place after a reload', async () => {
    await enterLessonMode();
    await finishStep();
    document.body.replaceChildren();
    renderApp();

    expect(await screen.findByRole('heading', { name: firstLesson.steps[1].title })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /^Step 1: .* \(done\)$/ })).toBeInTheDocument();
  });

  it('gives the tabs back when the mode ends', async () => {
    await enterLessonMode();
    await userEvent.click(lessonSwitch());

    expect(document.querySelector('.cat')).toBeNull();
    expect(document.querySelector('.tab')).not.toBeNull();
    expect(loadSettings().lessonMode).toBe(false);
  });

  it('moves to the scripts of the new language', async () => {
    await enterLessonMode();
    await finishStep();
    await userEvent.click(screen.getByRole('menuitem', { name: 'Interface' }));
    await userEvent.click(await screen.findByRole('menuitem', { name: 'Language' }));
    await userEvent.click(await screen.findByRole('menuitemradio', { name: 'Español' }));

    const spanish = lessonsOf('es')[0];

    expect(await screen.findByRole('heading', { name: spanish.steps[1].title })).toBeInTheDocument();
    expect(Object.keys(loadProjects()[0].files)).toContain('clases/01-apresentacao-2.safira');
    expect(screen.getByRole('button', { name: /^Paso 1: .* \(hecho\)$/ })).toBeInTheDocument();
  });

  it('opens from the Help menu too', async () => {
    await openProject();
    await userEvent.click(screen.getByRole('menuitem', { name: 'Help' }));
    await userEvent.click(await screen.findByRole('menuitem', { name: 'Lesson mode' }));

    expect(lessonSwitch()).toBeChecked();
  });

  it('offers the way back from another file', async () => {
    await enterLessonMode();
    await userEvent.click(screen.getByRole('button', { name: /^main\.safira/ }));

    expect(screen.getByRole('button', { name: 'Back to the lesson' })).toBeInTheDocument();
    expect(screen.queryByRole('button', { name: 'Start over' })).not.toBeInTheDocument();
  });
});
