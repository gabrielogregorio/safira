import { fireEvent, render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { lessonsOf } from '@/content/content';
import type { LessonMode } from '@/ui/hooks/useLessonMode';
import { ProfessorCat } from './ProfessorCat';

const lessons = lessonsOf('en-us');

const lessonMode = (changes: Partial<LessonMode> = {}): LessonMode => ({
  lessons,
  place: { lessonId: lessons[0].id, step: 0 },
  step: lessons[0].steps[0],
  isOnStepFile: true,
  isDone: false,
  isLastStep: false,
  verdict: { status: 'idle' },
  hasRun: false,
  open: vi.fn(),
  toggle: vi.fn(),
  goToNext: vi.fn(),
  backToStep: vi.fn(),
  startOver: vi.fn(),
  showSolution: vi.fn(),
  ...changes,
});

const press = (name: string) => userEvent.click(screen.getByRole('button', { name }));

describe('ProfessorCat', () => {
  beforeEach(() => {
    sessionStorage.clear();
  });

  it('introduces himself once per session', async () => {
    const { unmount } = render(<ProfessorCat lesson={lessonMode()} hasError={false} />);

    expect(screen.getByText(/I am Professor Cat/)).toBeInTheDocument();

    await press('Continue');
    unmount();
    render(<ProfessorCat lesson={lessonMode()} hasError={false} />);

    expect(screen.queryByText(/I am Professor Cat/)).not.toBeInTheDocument();
  });

  it('explains the step, then asks for a run', async () => {
    render(<ProfessorCat lesson={lessonMode()} hasError={false} />);
    await press('Continue');

    expect(screen.getByRole('heading', { name: lessons[0].steps[0].title })).toBeInTheDocument();

    await press('Continue');

    expect(screen.getByText('Press ▶ Run to see it work.')).toBeInTheDocument();
  });

  it('lights the Run button only while asking for a run', async () => {
    const { unmount } = render(<ProfessorCat lesson={lessonMode()} hasError={false} />);
    await press('Continue');

    expect(document.documentElement.dataset['spotlight']).toBeUndefined();

    await press('Continue');

    expect(document.documentElement.dataset['spotlight']).toBe('run');

    unmount();

    expect(document.documentElement.dataset['spotlight']).toBeUndefined();
  });

  it('shows the result after a run, with the way forward', async () => {
    const lesson = lessonMode({ hasRun: true, isDone: true });
    sessionStorage.setItem('safira.cat.met', 'true');
    render(<ProfessorCat lesson={lesson} hasError={false} />);

    expect(screen.getByText('Look at the result over there.')).toBeInTheDocument();

    await press('Next');

    expect(lesson.goToNext).toHaveBeenCalledTimes(1);
  });

  it('runs while the stone is held and continues when it drops', () => {
    sessionStorage.setItem('safira.cat.met', 'true');
    const { container } = render(<ProfessorCat lesson={lessonMode()} hasError={false} />);
    const stone = screen.getByRole('button', { name: 'Drag the stone' });
    stone.setPointerCapture = vi.fn();

    fireEvent.pointerDown(stone, { clientX: 100, clientY: 100, pointerId: 1 });
    fireEvent.pointerMove(stone, { clientX: 100, clientY: 60, pointerId: 1 });

    expect(container.querySelector('.cat-bubble')).toBeNull();
    expect(stone).toHaveAttribute('aria-pressed', 'true');

    fireEvent.pointerUp(stone, { pointerId: 1 });

    expect(screen.getByRole('heading', { name: lessons[0].steps[0].title })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Drag the stone' })).toHaveAttribute('aria-pressed', 'false');
  });

  it('does not run from a plain click', () => {
    const { container } = render(<ProfessorCat lesson={lessonMode()} hasError={false} />);
    const stone = screen.getByRole('button', { name: 'Drag the stone' });
    stone.setPointerCapture = vi.fn();
    fireEvent.pointerDown(stone, { clientX: 100, clientY: 100, pointerId: 1 });
    fireEvent.pointerUp(stone, { pointerId: 1 });

    expect(container.querySelector('.cat-bubble')).not.toBeNull();
  });

  it('also works from the keyboard', async () => {
    const { container } = render(<ProfessorCat lesson={lessonMode()} hasError={false} />);
    screen.getByRole('button', { name: 'Drag the stone' }).focus();
    await userEvent.keyboard('{Enter}');

    expect(container.querySelector('.cat-bubble')).toBeNull();

    await userEvent.keyboard('{Enter}');

    expect(container.querySelector('.cat-bubble')).not.toBeNull();
  });

  it.each<[string, Partial<LessonMode>, boolean, string]>([
    ['waves hello', {}, false, 'wave'],
    ['thumbs up on a right answer', { hasRun: true, isDone: true }, false, 'thumbs'],
    [
      'facepalms on a wrong answer',
      {
        hasRun: true,
        verdict: { status: 'failed', result: { passed: false, reason: 'command', text: '', inputs: [] } },
      },
      false,
      'facepalm',
    ],
    ['facepalms on a program error', {}, true, 'facepalm'],
  ])('%s', (name, changes, hasError, pose) => {
    if (name !== 'waves hello') {
      sessionStorage.setItem('safira.cat.met', 'true');
    }

    const { container } = render(<ProfessorCat lesson={lessonMode(changes)} hasError={hasError} />);

    expect(container.querySelector('.cat')).toHaveAttribute('data-pose', pose);
  });

  it('points while explaining', async () => {
    const { container } = render(<ProfessorCat lesson={lessonMode()} hasError={false} />);
    await press('Continue');

    expect(container.querySelector('.cat')).toHaveAttribute('data-pose', 'point');
  });
});
