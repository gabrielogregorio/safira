import { act, fireEvent, render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { lessonsOf } from '@/content/content';
import type * as i18n from '@/i18n/i18n';
import type { Translate } from '@/i18n/i18n';
import type { LessonMode } from '@/ui/hooks/useLessonMode';
import { planTrip, ProfessorCat } from './ProfessorCat';

const WRITE_SPEECH = 'Write your answer and press ▶ Run.';

// No translated speech has code in it today, so the backtick handling needs its own line of text.
const translation = vi.hoisted(() => ({ writeSpeech: null as string | null }));

vi.mock('@/i18n/i18n', async (importOriginal) => {
  const actual = await importOriginal<typeof i18n>();

  return {
    ...actual,
    useTranslation: (): Translate => {
      const t = actual.useTranslation();

      return (text, values) => (text === WRITE_SPEECH ? (translation.writeSpeech ?? t(text, values)) : t(text, values));
    },
  };
});

const lessons = lessonsOf('en-us');

const lessonMode = (changes: Partial<LessonMode> = {}): LessonMode => ({
  lessons,
  place: { lessonId: lessons[0].id, step: 0 },
  step: lessons[0].steps[1],
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

const renderCat = (changes: Partial<LessonMode> = {}, onAbandon = vi.fn()) =>
  render(<ProfessorCat lesson={lessonMode(changes)} hasError={false} isWaitingInput={false} onAbandon={onAbandon} />);

const farewell = { isLastStep: true, isDone: true, hasRun: true };

const withMotion = (): void => {
  vi.stubGlobal('matchMedia', vi.fn().mockReturnValue({ matches: true }));
  vi.useFakeTimers();
};

const advance = (milliseconds: number): void => {
  act(() => {
    vi.advanceTimersByTime(milliseconds);
  });
};

const catElement = (container: HTMLElement): HTMLElement => container.querySelector<HTMLElement>('.cat') as HTMLElement;

describe('ProfessorCat', () => {
  const boxes: HTMLElement[] = [];

  const addBox = (className: string, box: DOMRect): void => {
    const element = document.createElement('div');
    element.className = className;
    element.getBoundingClientRect = () => box;
    document.body.append(element);
    boxes.push(element);
  };

  beforeEach(() => {
    sessionStorage.clear();
  });

  afterEach(() => {
    vi.useRealTimers();
    vi.unstubAllGlobals();
    vi.restoreAllMocks();
    translation.writeSpeech = null;
    boxes.splice(0).forEach((element) => {
      element.remove();
    });
  });

  it('introduces himself once per session', async () => {
    const { unmount } = render(
      <ProfessorCat lesson={lessonMode()} hasError={false} isWaitingInput={false} onAbandon={vi.fn()} />,
    );

    expect(screen.getByText(/I am a therian/)).toBeInTheDocument();

    await press('Continue');
    unmount();
    render(<ProfessorCat lesson={lessonMode()} hasError={false} isWaitingInput={false} onAbandon={vi.fn()} />);

    expect(screen.queryByText(/I am a therian/)).not.toBeInTheDocument();
  });

  it('only points: no title and no explanation in the balloon', () => {
    sessionStorage.setItem('safira.cat.met', 'true');
    render(<ProfessorCat lesson={lessonMode()} hasError={false} isWaitingInput={false} onAbandon={vi.fn()} />);

    expect(screen.getByText('Write your answer and press ▶ Run.')).toBeInTheDocument();
    expect(screen.queryByRole('heading')).not.toBeInTheDocument();
    expect(screen.queryByRole('button', { name: 'Continue' })).not.toBeInTheDocument();
  });

  it('shows the code before asking for a run, and only then lights the button', async () => {
    sessionStorage.setItem('safira.cat.met', 'true');
    const step = { ...lessons[0].steps[0], check: null };
    const { unmount } = render(
      <ProfessorCat lesson={lessonMode({ step })} hasError={false} isWaitingInput={false} onAbandon={vi.fn()} />,
    );

    expect(screen.getByText('Read this code.')).toBeInTheDocument();
    expect(document.documentElement.dataset['spotlight']).toBeUndefined();

    await press('Continue');

    expect(screen.getByText('Press ▶')).toBeInTheDocument();
    expect(document.documentElement.dataset['spotlight']).toBe('run');

    unmount();

    expect(document.documentElement.dataset['spotlight']).toBeUndefined();
  });

  it('shows the result after a run, with the way forward', async () => {
    const lesson = lessonMode({ hasRun: true, isDone: true });
    sessionStorage.setItem('safira.cat.met', 'true');
    render(<ProfessorCat lesson={lesson} hasError={false} isWaitingInput={false} onAbandon={vi.fn()} />);

    expect(screen.getByText('Look at the result over there.')).toBeInTheDocument();

    await press('Next');

    expect(lesson.goToNext).toHaveBeenCalledTimes(1);
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

    const { container } = render(
      <ProfessorCat lesson={lessonMode(changes)} hasError={hasError} isWaitingInput={false} onAbandon={vi.fn()} />,
    );

    expect(container.querySelector('.cat')).toHaveAttribute('data-pose', pose);
  });

  it('asks for the answer when the program waits for one', () => {
    sessionStorage.setItem('safira.cat.met', 'true');
    const { container } = render(
      <ProfessorCat lesson={lessonMode()} hasError={false} isWaitingInput onAbandon={vi.fn()} />,
    );

    expect(screen.getByText('Type your answer here and press Enter.')).toBeInTheDocument();
    expect(container.querySelector('.cat')).toHaveAttribute('data-pose', 'point');
    expect(document.documentElement.dataset['spotlight']).toBeUndefined();
  });

  it('tells you off at the end and leaves for good', async () => {
    const onAbandon = vi.fn();
    render(
      <ProfessorCat
        lesson={lessonMode({ isLastStep: true, isDone: true, hasRun: true })}
        hasError={false}
        isWaitingInput={false}
        onAbandon={onAbandon}
      />,
    );

    await vi.waitFor(() => {
      expect(onAbandon).toHaveBeenCalledTimes(1);
    });
  });

  it('draws nothing when there is no step', () => {
    const { container } = renderCat({ step: undefined });

    expect(container).toBeEmptyDOMElement();
  });

  it('still introduces himself when the browser blocks the storage', async () => {
    vi.spyOn(Storage.prototype, 'getItem').mockImplementation(() => {
      throw new Error('blocked');
    });
    vi.spyOn(Storage.prototype, 'setItem').mockImplementation(() => {
      throw new Error('blocked');
    });
    renderCat();

    expect(screen.getByText(/I am a therian/)).toBeInTheDocument();

    await press('Continue');

    expect(screen.queryByText(/I am a therian/)).not.toBeInTheDocument();
  });

  it('stays in the corner on a phone', () => {
    vi.stubGlobal('innerWidth', 500);
    vi.stubGlobal('innerHeight', 800);
    const { container } = renderCat();

    expect(catElement(container).style.transform).toBe('translate(392px, 588px)');
  });

  it.each([
    ['right', new DOMRect(1000, 400, 400, 20), '23deg'],
    ['left', new DOMRect(100, 400, 100, 20), '12deg'],
  ])('turns %s and aims the arm at the target', (facing, target, angle) => {
    sessionStorage.setItem('safira.cat.met', 'true');
    vi.spyOn(Math, 'random').mockReturnValue(0.5);
    addBox('code-editor', new DOMRect(100, 100, 800, 600));
    addBox('cm-line', target);
    const { container } = renderCat();
    const cat = catElement(container);

    expect(cat.style.transform).toBe('translate(769px, 208px)');
    expect(cat.dataset['facing']).toBe(facing);
    expect(cat.style.getPropertyValue('--point-angle')).toBe(angle);
  });

  it('keeps quiet until the saucer arrives', () => {
    sessionStorage.setItem('safira.cat.met', 'true');
    vi.spyOn(Math, 'random').mockReturnValue(0.5);
    withMotion();
    const lesson = lessonMode();
    const { container, rerender } = render(
      <ProfessorCat lesson={lesson} hasError={false} isWaitingInput={false} onAbandon={vi.fn()} />,
    );

    rerender(<ProfessorCat lesson={lesson} hasError={false} isWaitingInput onAbandon={vi.fn()} />);

    expect(container.querySelector('.cat-bubble')).toBeNull();

    advance(1874);

    expect(container.querySelector('.cat-bubble')).toBeNull();

    advance(1);

    expect(container.querySelector('.cat-bubble')).not.toBeNull();
  });

  it('types his speech, with a way to show it all at once', () => {
    sessionStorage.setItem('safira.cat.met', 'true');
    withMotion();
    const { container } = renderCat();
    const typed = container.querySelector('.lesson-brief-text');

    expect(typed).toHaveAttribute('aria-hidden', 'true');
    expect(container.querySelector('.visually-hidden')).toHaveTextContent(WRITE_SPEECH);

    fireEvent.click(screen.getByRole('button', { name: 'Show it all' }));

    expect(typed).not.toHaveAttribute('aria-hidden');
    expect(typed).toHaveTextContent(WRITE_SPEECH);
    expect(screen.queryByRole('button', { name: 'Show it all' })).not.toBeInTheDocument();
  });

  it('hides a backtick until its pair is typed', () => {
    sessionStorage.setItem('safira.cat.met', 'true');
    translation.writeSpeech = 'Use `show` now';
    withMotion();
    const { container } = renderCat();
    const typed = container.querySelector('.lesson-brief-text');

    advance(7 * 24);

    expect(typed).toHaveTextContent(/^Use sh$/);

    advance(7 * 24);

    expect(typed?.querySelector('code')).toHaveTextContent('show');
  });

  it('takes his time to say goodbye and to fly away', () => {
    withMotion();
    const onAbandon = vi.fn();
    const { container } = renderCat(farewell, onAbandon);

    advance(3000);
    advance(2499);

    expect(catElement(container)).not.toHaveClass('cat-leaving');

    advance(1);

    expect(catElement(container)).toHaveClass('cat-leaving');
    expect(catElement(container).style.transform).toBe('translate(1120px, -96px)');
    expect(onAbandon).not.toHaveBeenCalled();

    advance(900);

    expect(onAbandon).toHaveBeenCalledTimes(1);
  });

  it('still leaves when the step disappears on the way out', () => {
    vi.useFakeTimers();
    const firstAbandon = vi.fn();
    const lastAbandon = vi.fn();
    const { rerender } = renderCat(farewell, firstAbandon);

    advance(0);
    rerender(
      <ProfessorCat
        lesson={lessonMode({ ...farewell, step: undefined })}
        hasError={false}
        isWaitingInput={false}
        onAbandon={lastAbandon}
      />,
    );
    advance(0);

    expect(firstAbandon).not.toHaveBeenCalled();
    expect(lastAbandon).toHaveBeenCalledTimes(1);
  });

  it('points at the code in a challenge', () => {
    sessionStorage.setItem('safira.cat.met', 'true');
    const { container } = render(
      <ProfessorCat lesson={lessonMode()} hasError={false} isWaitingInput={false} onAbandon={vi.fn()} />,
    );

    expect(container.querySelector('.cat')).toHaveAttribute('data-pose', 'point');
  });
});

describe('planTrip', () => {
  it('varies a little between the shortest and the longest trip', () => {
    expect(planTrip(() => 0)).toMatchObject({ milliseconds: 1500, driftX: -0 });
    expect(planTrip(() => 1)).toMatchObject({ milliseconds: 2250, driftX: -46, driftY: 18 });
  });
});
