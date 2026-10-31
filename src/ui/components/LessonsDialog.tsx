import { useEffect, useRef } from 'react';
import { lessonsOf } from '@/content/content';
import { useLocale, useTranslation } from '@/i18n/i18n';
import { LessonMarkdown } from './LessonMarkdown';
import { Modal } from './Modal';

interface LessonsDialogProps {
  lessonId: string | null;
  section: string | null;
  readLessons: string[];
  lessonHref: (lessonId: string, section: string | null) => string;
  onMarkRead: (id: string) => void;
  onOpenCode: (lessonId: string, code: string) => void;
  onClose: () => void;
}

export const LessonsDialog = ({
  lessonId,
  section,
  readLessons,
  lessonHref,
  onMarkRead,
  onOpenCode,
  onClose,
}: LessonsDialogProps) => {
  const t = useTranslation();
  const tutorials = lessonsOf(useLocale());
  const articleRef = useRef<HTMLElement>(null);
  const index = Math.max(
    tutorials.findIndex((tutorial) => tutorial.id === lessonId),
    0,
  );
  const lesson = tutorials[index];
  const previous = tutorials[index - 1];
  const next = tutorials[index + 1];

  useEffect(() => {
    const target = section === null ? null : document.getElementById(section);

    if (target === null) {
      articleRef.current?.scrollTo({ top: 0 });
    } else {
      target.scrollIntoView();
    }
  }, [index, section]);

  return (
    <Modal title={t('Lessons')} isWide onClose={onClose}>
      <div className="lessons">
        <nav className="lessons-nav" aria-label={t('Lessons')}>
          <ul className="lessons-list">
            {tutorials.map((tutorial, tutorialIndex) => (
              <li key={tutorial.id}>
                <a
                  className="lesson-link"
                  href={lessonHref(tutorial.id, null)}
                  aria-current={tutorialIndex === index ? 'page' : undefined}
                  onClick={() => {
                    onMarkRead(lesson.id);
                  }}>
                  <span data-fixed-text>{tutorial.title}</span>
                  {readLessons.includes(tutorial.id) ? ` (${t('Read')})` : ''}
                </a>
              </li>
            ))}
          </ul>
        </nav>
        <article ref={articleRef} className="lesson" key={lesson.id}>
          <h2 data-fixed-text>{lesson.title}</h2>
          <LessonMarkdown
            sectionHref={(sectionId) => lessonHref(lesson.id, sectionId)}
            text={lesson.text}
            onOpenCode={(code) => {
              onOpenCode(lesson.id, code);
            }}
          />
          <nav className="lesson-pager" aria-label={t('Lessons')}>
            {previous === undefined ? null : (
              <a className="button" href={lessonHref(previous.id, null)}>
                {t('Previous')}
              </a>
            )}
            {next === undefined ? null : (
              <a
                className="button button-primary"
                href={lessonHref(next.id, null)}
                onClick={() => {
                  onMarkRead(lesson.id);
                }}>
                {t('Next')}
              </a>
            )}
          </nav>
        </article>
      </div>
    </Modal>
  );
};
