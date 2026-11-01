import { lessonsOf } from '@/content/content';
import { addScriptVersion } from '@/language/version';
import { isLessonFile, untouchedOldLessonFiles } from './lessonFiles';
import { lessonFilePath } from './lessonPlace';

const firstLesson = lessonsOf('pt-br')[0];
const place = { lessonId: firstLesson.id, step: 0 };
const untouched = addScriptVersion(firstLesson.steps[0].code);
const path = lessonFilePath('aulas', place);
const oldPath = `aulas/${firstLesson.id.replace('aula-', '')}-1.safira`;

describe('lesson files', () => {
  it('knows the lesson folder of every language', () => {
    expect(['aulas/a', 'lessons/a', 'clases/a', '课程/a', 'レッスン/a'].every(isLessonFile)).toBe(true);
    expect(isLessonFile('main.safira')).toBe(false);
  });

  it('finds an untouched step of another language', () => {
    expect(untouchedOldLessonFiles({ [path]: untouched, 'main.safira': '' }, 'en-us')).toEqual([path]);
  });

  it('keeps the steps of the current language', () => {
    expect(untouchedOldLessonFiles({ [path]: untouched }, 'pt-br')).toEqual([]);
  });

  it('finds the old file name even in the current language', () => {
    expect(untouchedOldLessonFiles({ [oldPath]: untouched }, 'pt-br')).toEqual([oldPath]);
  });

  it('keeps what the person edited', () => {
    expect(untouchedOldLessonFiles({ [path]: `${untouched}\nmostre 1` }, 'en-us')).toEqual([]);
  });
});
