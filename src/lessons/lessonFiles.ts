import { lessonsOf } from '@/content/content';
import { createTranslator, LOCALES } from '@/i18n/i18n';
import type { Locale } from '@/language/messages';
import { addScriptVersion } from '@/language/version';
import { legacyLessonFilePath, lessonFilePath } from '@/lessons/lessonPlace';

const lessonFolderOf = (locale: Locale): string => createTranslator(locale)('lessons');

const LESSON_FOLDERS = LOCALES.map(({ id }) => `${lessonFolderOf(id)}/`);

export const isLessonFile = (file: string): boolean => LESSON_FOLDERS.some((folder) => file.startsWith(folder));

/**
 * Steps nobody edited, left by another language or by the old file names.
 * Anything edited is the person's code, so it stays where it is.
 */
export const untouchedOldLessonFiles = (files: Record<string, string>, current: Locale): string[] =>
  LOCALES.flatMap(({ id: locale }) => {
    const folder = lessonFolderOf(locale);

    return lessonsOf(locale).flatMap((lesson) =>
      lesson.steps.flatMap(({ code }, step) => {
        const place = { lessonId: lesson.id, step };
        const paths = [legacyLessonFilePath(folder, place)];

        if (locale !== current) {
          paths.push(lessonFilePath(folder, place));
        }

        return paths.filter((path) => files[path] === addScriptVersion(code));
      }),
    );
  });
