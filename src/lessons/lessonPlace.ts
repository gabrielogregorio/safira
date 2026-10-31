import type { Lesson, LessonStep } from '@/content/lessons';
import type { LessonPlace } from '@/settings/settings';

const SCRIPT_EXTENSION = '.safira';
const LESSON_PREFIX = /^aula-/;

export const stepKey = ({ lessonId, step }: LessonPlace): string => `${lessonId}:${String(step)}`;

export const isStepDone = (progress: string[], place: LessonPlace): boolean => progress.includes(stepKey(place));

export const isLessonDone = (progress: string[], lesson: Lesson): boolean =>
  lesson.steps.every((_step, step) => isStepDone(progress, { lessonId: lesson.id, step }));

/** The folder has the language in its name, so each language keeps its own scripts. */
export const lessonFilePath = (folder: string, { lessonId, step }: LessonPlace): string =>
  `${folder}/${lessonId.replace(LESSON_PREFIX, '')}-${String(step + 1)}${SCRIPT_EXTENSION}`;

const allPlaces = (lessons: Lesson[]): LessonPlace[] =>
  lessons.flatMap((lesson) => lesson.steps.map((_step, step) => ({ lessonId: lesson.id, step })));

export const placeOfFile = (lessons: Lesson[], folder: string, file: string): LessonPlace | null =>
  allPlaces(lessons).find((place) => lessonFilePath(folder, place) === file) ?? null;

export const stepAt = (lessons: Lesson[], { lessonId, step }: LessonPlace): LessonStep | undefined =>
  lessons.find((lesson) => lesson.id === lessonId)?.steps[step];

export const firstPlace = (lessons: Lesson[]): LessonPlace => ({ lessonId: lessons[0]?.id ?? '', step: 0 });

/** A saved place can point to a lesson that no longer exists. */
export const resolvePlace = (lessons: Lesson[], place: LessonPlace | null): LessonPlace =>
  place !== null && stepAt(lessons, place) !== undefined ? place : firstPlace(lessons);

const neighbor = (lessons: Lesson[], place: LessonPlace, offset: number): LessonPlace | null => {
  const places = allPlaces(lessons);

  return places[places.findIndex((candidate) => stepKey(candidate) === stepKey(place)) + offset] ?? null;
};

export const previousPlace = (lessons: Lesson[], place: LessonPlace): LessonPlace | null =>
  neighbor(lessons, place, -1);

export const nextPlace = (lessons: Lesson[], place: LessonPlace): LessonPlace | null => neighbor(lessons, place, 1);

/** Where a lesson picks up: the first step not done yet, or the start when everything is done. */
export const resumePlace = (lesson: Lesson, progress: string[]): LessonPlace => {
  const pending = lesson.steps.findIndex((_step, step) => !isStepDone(progress, { lessonId: lesson.id, step }));

  return { lessonId: lesson.id, step: Math.max(pending, 0) };
};
