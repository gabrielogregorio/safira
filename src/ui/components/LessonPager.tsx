import { useState } from 'react';
import type { Lesson } from '@/content/lessons';
import { useTranslation } from '@/i18n/i18n';
import { isLessonDone, resumePlace } from '@/lessons/lessonPlace';
import type { LessonPlace } from '@/settings/settings';

interface LessonPagerProps {
  lessons: Lesson[];
  place: LessonPlace;
  progress: string[];
  onOpen: (place: LessonPlace) => void;
}

const PAGE_SIZE = 6;

/** The list of lessons on a phone, where a native list of every lesson does not fit. */
export const LessonPager = ({ lessons, place, progress, onOpen }: LessonPagerProps) => {
  const t = useTranslation();
  const current = lessons.findIndex((lesson) => lesson.id === place.lessonId);
  const [page, setPage] = useState(Math.floor(Math.max(current, 0) / PAGE_SIZE));
  const start = page * PAGE_SIZE;
  const visible = lessons.slice(start, start + PAGE_SIZE);

  return (
    <nav className="lesson-pager" aria-label={t('Choose a lesson')}>
      <button
        type="button"
        className="lesson-page lesson-page-arrow"
        data-sound="tab"
        aria-label={t('Previous lessons')}
        disabled={page === 0}
        onClick={() => {
          setPage(page - 1);
        }}>
        ‹
      </button>
      {visible.map((lesson, index) => {
        const number = start + index + 1;
        const isDone = isLessonDone(progress, lesson);
        const label = t(isDone ? 'Lesson {number}: {title} (done)' : 'Lesson {number}: {title}', {
          number,
          title: lesson.title,
        });

        return (
          <button
            key={lesson.id}
            type="button"
            className={isDone ? 'lesson-page lesson-page-done' : 'lesson-page'}
            data-sound="tab"
            aria-label={label}
            aria-current={lesson.id === place.lessonId ? 'true' : undefined}
            onClick={() => {
              onOpen(resumePlace(lesson, progress));
            }}>
            {number}
          </button>
        );
      })}
      <button
        type="button"
        className="lesson-page lesson-page-arrow"
        data-sound="tab"
        aria-label={t('Next lessons')}
        disabled={start + PAGE_SIZE >= lessons.length}
        onClick={() => {
          setPage(page + 1);
        }}>
        ›
      </button>
    </nav>
  );
};
