import { act, renderHook } from '@testing-library/react';
import { lessonsOf } from '@/content/content';
import type * as content from '@/content/content';
import type { CheckRequest } from '@/lessons/lessonCheck';
import { lessonFilePath, stepKey } from '@/lessons/lessonPlace';
import type { RunnerFailure } from '@/runtime/protocol';
import type { LessonPlace, Settings } from '@/settings/settings';
import { DEFAULT_SETTINGS } from '@/settings/settings';
import type { CheckWorker, LessonRun } from './useLessonMode';
import { createCheckWorker, useLessonMode } from './useLessonMode';

const course = vi.hoisted(() => ({ isEmpty: false }));

vi.mock('@/content/content', async (importOriginal) => {
  const actual = await importOriginal<typeof content>();
  const noLessons: ReturnType<typeof actual.lessonsOf> = [];

  return {
    ...actual,
    lessonsOf: (locale: Parameters<typeof actual.lessonsOf>[0]) =>
      course.isEmpty ? noLessons : actual.lessonsOf(locale),
  };
});

const FOLDER = 'lessons';
const lessons = lessonsOf('en-us');
const lessonId = lessons[0].id;
const example: LessonPlace = { lessonId, step: 0 };
const challenge: LessonPlace = { lessonId, step: 1 };

const silentWorker = (): CheckWorker => ({
  postMessage: vi.fn<(request: CheckRequest) => void>(),
  terminate: vi.fn(),
  onmessage: null,
});

const setup = (activeFile = 'main.safira', settings: Partial<Settings> = {}, worker = silentWorker()) => {
  const pendingRunRef: { current: LessonRun | null } = { current: null };
  const finishListenerRef: { current: ((failure: RunnerFailure | null) => void) | null } = { current: null };
  const onChangeSettings = vi.fn();
  const onOpenFile = vi.fn();
  const onReplaceCode = vi.fn();
  const { result } = renderHook(() =>
    useLessonMode({
      settings: { ...DEFAULT_SETTINGS, lessonMode: true, ...settings },
      locale: 'en-us',
      folder: FOLDER,
      activeFile,
      pendingRunRef,
      finishListenerRef,
      createWorker: () => worker,
      onChangeSettings,
      onOpenFile,
      onReplaceCode,
    }),
  );
  onChangeSettings.mockClear();
  onOpenFile.mockClear();

  const finishRun = (file: string | null): void => {
    pendingRunRef.current = file === null ? null : { file, files: {} };
    act(() => {
      finishListenerRef.current?.(null);
    });
  };

  return { result, pendingRunRef, onChangeSettings, onOpenFile, onReplaceCode, finishRun };
};

describe('createCheckWorker', () => {
  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it('starts the check in a module worker', () => {
    const created: unknown[][] = [];
    vi.stubGlobal(
      'Worker',
      class {
        public constructor(...options: unknown[]) {
          created.push(options);
        }
      },
    );
    createCheckWorker();

    expect(String(created[0][0])).toContain('lessonCheck.worker');
    expect(created[0][1]).toEqual({ type: 'module' });
  });
});

describe('useLessonMode', () => {
  afterEach(() => {
    course.isEmpty = false;
    vi.useRealTimers();
  });

  it('gives up on a check that never answers', async () => {
    vi.useFakeTimers();
    const worker = silentWorker();
    const file = lessonFilePath(FOLDER, challenge);
    const { result, finishRun } = setup(file, {}, worker);

    finishRun(file);

    expect(result.current.verdict).toEqual({ status: 'checking' });

    await act(() => vi.advanceTimersByTimeAsync(4000));

    expect(result.current.verdict).toMatchObject({ status: 'failed', result: { reason: 'limit' } });
    expect(worker.terminate).toHaveBeenCalledTimes(1);
  });

  it('forgets the failure when the solution is written, until the step starts over', async () => {
    vi.useFakeTimers();
    const file = lessonFilePath(FOLDER, challenge);
    const { result, finishRun, onReplaceCode } = setup(file, {}, silentWorker());

    finishRun(file);
    await act(() => vi.advanceTimersByTimeAsync(4000));
    expect(result.current.hasRun).toBe(true);

    act(() => {
      result.current.showSolution();
    });

    expect(result.current).toMatchObject({ verdict: { status: 'idle' }, hasRun: false, isSolutionShown: true });
    expect(onReplaceCode).toHaveBeenLastCalledWith(lessons[0].steps[1].solution);

    act(() => {
      result.current.startOver();
    });

    expect(result.current.isSolutionShown).toBe(false);
  });

  it('opens nothing for a place that does not exist', () => {
    const { result, onChangeSettings, onOpenFile } = setup();

    act(() => {
      result.current.open({ lessonId: 'gone', step: 0 });
    });

    expect(onChangeSettings).not.toHaveBeenCalled();
    expect(onOpenFile).not.toHaveBeenCalled();
  });

  it('does not count a step twice', () => {
    const file = lessonFilePath(FOLDER, example);
    const { result, onChangeSettings, finishRun } = setup(file, { lessonProgress: [stepKey(example)] });

    finishRun(file);

    expect(result.current.hasRun).toBe(true);
    expect(onChangeSettings).not.toHaveBeenCalled();
  });

  it('ignores a program that ends with nothing pending', () => {
    const { result, finishRun } = setup();

    finishRun(null);

    expect(result.current.hasRun).toBe(false);
  });

  it('ignores a run of a file outside the lesson', () => {
    const { result, pendingRunRef, finishRun } = setup();

    finishRun('main.safira');

    expect(result.current.hasRun).toBe(false);
    expect(pendingRunRef.current).toBeNull();
  });

  it('stops at the last step', () => {
    const lastLesson = lessons[lessons.length - 1];
    const last = { lessonId: lastLesson.id, step: lastLesson.steps.length - 1 };
    const { result, onOpenFile } = setup(lessonFilePath(FOLDER, last));

    act(() => {
      result.current.goToNext();
    });

    expect(result.current.isLastStep).toBe(true);
    expect(onOpenFile).not.toHaveBeenCalled();
  });

  it('goes back to the step from another file', () => {
    const { result, onChangeSettings, onOpenFile } = setup('main.safira', { lessonPlace: challenge });

    act(() => {
      result.current.backToStep();
    });

    expect(onChangeSettings).toHaveBeenCalledExactlyOnceWith({ lessonPlace: challenge });
    expect(onOpenFile).toHaveBeenCalledExactlyOnceWith(lessonFilePath(FOLDER, challenge), lessons[0].steps[1].code);
  });

  it('writes an empty program when there are no lessons at all', () => {
    course.isEmpty = true;
    const { result, onReplaceCode } = setup('main.safira', { lessonMode: false });

    act(() => {
      result.current.startOver();
      result.current.showSolution();
    });

    expect(result.current.step).toBeUndefined();
    expect(onReplaceCode.mock.calls).toEqual([[''], ['']]);
  });
});
