import type { RefObject } from 'react';
import { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { lessonsOf } from '@/content/content';
import type { Lesson, LessonStep } from '@/content/lessons';
import type { Locale } from '@/language/messages';
import type { CheckRequest, CheckResult } from '@/lessons/lessonCheck';
import {
  isStepDone,
  lessonFilePath,
  nextPlace,
  placeOfFile,
  resolvePlace,
  stepAt,
  stepKey,
} from '@/lessons/lessonPlace';
import type { RunnerFailure } from '@/runtime/protocol';
import type { LessonPlace, Settings } from '@/settings/settings';
import { soundPlayer } from '@/ui/sound/sounds';

export interface CheckWorker {
  postMessage: (request: CheckRequest) => void;
  terminate: () => void;
  onmessage: ((message: MessageEvent<CheckResult>) => void) | null;
}

export type CheckWorkerFactory = () => CheckWorker;

export const createCheckWorker: CheckWorkerFactory = () =>
  new Worker(new URL('../../lessons/lessonCheck.worker.ts', import.meta.url), { type: 'module' });

/** What was run: the check needs the files of that moment, not of when the program ended. */
export interface LessonRun {
  file: string;
  files: Record<string, string>;
}

export type LessonVerdict = { status: 'idle' } | { status: 'checking' } | { status: 'failed'; result: CheckResult };

const CHECK_LIMIT_MILLISECONDS = 4000;
const IDLE: LessonVerdict = { status: 'idle' };

const checkInWorker = (createWorker: CheckWorkerFactory, request: CheckRequest): Promise<CheckResult> =>
  new Promise((resolve) => {
    const worker = createWorker();
    const finish = (result: CheckResult): void => {
      clearTimeout(timer);
      worker.terminate();
      resolve(result);
    };
    const timer = setTimeout(() => {
      finish({ passed: false, reason: 'limit', text: '', inputs: [] });
    }, CHECK_LIMIT_MILLISECONDS);

    worker.onmessage = (message) => {
      finish(message.data);
    };
    worker.postMessage(request);
  });

interface LessonModeOptions {
  settings: Settings;
  locale: Locale;
  folder: string;
  activeFile: string;
  pendingRunRef: RefObject<LessonRun | null>;
  finishListenerRef: RefObject<((failure: RunnerFailure | null) => void) | null>;
  createWorker: CheckWorkerFactory;
  onChangeSettings: (changes: Partial<Settings>) => void;
  onOpenFile: (path: string, code: string) => void;
  onReplaceCode: (code: string) => void;
}

export interface LessonMode {
  lessons: Lesson[];
  place: LessonPlace;
  step: LessonStep | undefined;
  isOnStepFile: boolean;
  isDone: boolean;
  isLastStep: boolean;
  verdict: LessonVerdict;
  /** This step already ran without an error since it was opened. */
  hasRun: boolean;
  open: (place: LessonPlace) => void;
  toggle: () => void;
  goToNext: () => void;
  backToStep: () => void;
  startOver: () => void;
  showSolution: () => void;
}

export const useLessonMode = ({
  settings,
  locale,
  folder,
  activeFile,
  pendingRunRef,
  finishListenerRef,
  createWorker,
  onChangeSettings,
  onOpenFile,
  onReplaceCode,
}: LessonModeOptions): LessonMode => {
  const lessons = lessonsOf(locale);
  const [verdict, setVerdict] = useState<LessonVerdict>(IDLE);
  const [hasRun, setHasRun] = useState(false);
  const filePlace = useMemo(() => placeOfFile(lessons, folder, activeFile), [activeFile, folder, lessons]);
  const place = filePlace ?? resolvePlace(lessons, settings.lessonPlace);
  const step = stepAt(lessons, place);

  const open = useCallback(
    (target: LessonPlace) => {
      const targetStep = stepAt(lessons, target);

      if (targetStep !== undefined) {
        setVerdict(IDLE);
        setHasRun(false);
        onChangeSettings({ lessonPlace: target });
        onOpenFile(lessonFilePath(folder, target), targetStep.code);
      }
    },
    [folder, lessons, onChangeSettings, onOpenFile],
  );

  const toggle = useCallback(() => {
    void soundPlayer.play(settings.lessonMode ? 'modalClose' : 'open');
    onChangeSettings({ lessonMode: !settings.lessonMode });
  }, [onChangeSettings, settings.lessonMode]);

  // Runs when the mode starts, after a reload and when the language changes, since each language has its own scripts.
  const openedLocale = useRef<Locale | null>(null);

  useEffect(() => {
    if (!settings.lessonMode) {
      openedLocale.current = null;
    } else if (openedLocale.current !== locale) {
      openedLocale.current = locale;
      open(place);
    }
  }, [locale, open, place, settings.lessonMode]);

  const complete = useCallback(
    (done: LessonPlace) => {
      void soundPlayer.play('lessonPass');
      setVerdict(IDLE);

      if (!isStepDone(settings.lessonProgress, done)) {
        onChangeSettings({ lessonProgress: [...settings.lessonProgress, stepKey(done)] });
      }
    },
    [onChangeSettings, settings.lessonProgress],
  );

  const judge = useCallback(
    async (run: LessonRun, done: LessonPlace) => {
      const check = stepAt(lessons, done)?.check ?? null;
      setHasRun(true);

      if (check === null) {
        complete(done);

        return;
      }

      setVerdict({ status: 'checking' });
      const result = await checkInWorker(createWorker, { ...run, locale, check });

      if (result.passed) {
        complete(done);
      } else {
        void soundPlayer.play('lessonFail');
        setVerdict({ status: 'failed', result });
      }
    },
    [complete, createWorker, lessons, locale],
  );

  useEffect(() => {
    finishListenerRef.current = (failure) => {
      const run = pendingRunRef.current;
      pendingRunRef.current = null;
      const done = run === null ? null : placeOfFile(lessons, folder, run.file);

      if (run !== null && done !== null && settings.lessonMode && failure === null) {
        void judge(run, done);
      }
    };
  }, [finishListenerRef, folder, judge, lessons, pendingRunRef, settings.lessonMode]);

  const isDone = isStepDone(settings.lessonProgress, place);
  const following = nextPlace(lessons, place);

  return {
    lessons,
    place,
    step,
    isOnStepFile: filePlace !== null,
    isDone,
    isLastStep: following === null,
    verdict,
    hasRun,
    open,
    toggle,
    goToNext: () => {
      if (following !== null) {
        open(following);
      }
    },
    backToStep: () => {
      open(place);
    },
    startOver: () => {
      setVerdict(IDLE);
      setHasRun(false);
      onReplaceCode(step?.code ?? '');
    },
    showSolution: () => {
      onReplaceCode(step?.solution ?? '');
    },
  };
};
