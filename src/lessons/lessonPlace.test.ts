import type { Lesson } from '@/content/lessons';
import {
  firstPlace,
  isLessonDone,
  isStepDone,
  lessonFilePath,
  nextPlace,
  placeOfFile,
  previousPlace,
  resolvePlace,
  resumePlace,
  stepAt,
  stepKey,
} from './lessonPlace';

const step = { title: 'Passo', text: 'Texto', code: '', solution: null, check: null };
const lessons: Lesson[] = [
  { id: 'aula-01-um', title: 'Um', steps: [step, step] },
  { id: 'aula-02-dois', title: 'Dois', steps: [step] },
];

describe('lesson places', () => {
  it('names the file of a step', () => {
    expect(lessonFilePath('aulas', { lessonId: 'aula-01-um', step: 1 })).toBe('aulas/01-um-2.safira');
  });

  it('finds the step of a file', () => {
    expect(placeOfFile(lessons, 'aulas', 'aulas/02-dois-1.safira')).toEqual({ lessonId: 'aula-02-dois', step: 0 });
    expect(placeOfFile(lessons, 'aulas', 'main.safira')).toBeNull();
  });

  it('walks across lessons', () => {
    const last = { lessonId: 'aula-01-um', step: 1 };

    expect(nextPlace(lessons, last)).toEqual({ lessonId: 'aula-02-dois', step: 0 });
    expect(previousPlace(lessons, { lessonId: 'aula-02-dois', step: 0 })).toEqual(last);
    expect(previousPlace(lessons, firstPlace(lessons))).toBeNull();
    expect(nextPlace(lessons, { lessonId: 'aula-02-dois', step: 0 })).toBeNull();
  });

  it('falls back to the start when the saved place is gone', () => {
    expect(resolvePlace(lessons, { lessonId: 'sumiu', step: 0 })).toEqual(firstPlace(lessons));
    expect(resolvePlace(lessons, null)).toEqual(firstPlace(lessons));
    expect(resolvePlace(lessons, { lessonId: 'aula-01-um', step: 1 })).toEqual({ lessonId: 'aula-01-um', step: 1 });
  });

  it('remembers what is done', () => {
    const done = [stepKey({ lessonId: 'aula-01-um', step: 0 })];

    expect(isStepDone(done, { lessonId: 'aula-01-um', step: 0 })).toBe(true);
    expect(isLessonDone(done, lessons[0])).toBe(false);
    expect(isLessonDone([...done, 'aula-01-um:1'], lessons[0])).toBe(true);
  });

  it('opens a lesson on the first step not done', () => {
    expect(resumePlace(lessons[0], ['aula-01-um:0'])).toEqual({ lessonId: 'aula-01-um', step: 1 });
    expect(resumePlace(lessons[0], ['aula-01-um:0', 'aula-01-um:1'])).toEqual({ lessonId: 'aula-01-um', step: 0 });
  });

  it('reads a step', () => {
    expect(stepAt(lessons, { lessonId: 'aula-01-um', step: 0 })).toBe(step);
    expect(stepAt(lessons, { lessonId: 'aula-01-um', step: 9 })).toBeUndefined();
  });
});
