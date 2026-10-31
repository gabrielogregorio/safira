import type { ReactNode } from 'react';
import { useEffect, useRef } from 'react';
import { tutorials } from '@/content/content';
import { useTranslation } from '@/i18n/i18n';
import { routeToHash } from '@/routing/routes';
import { LessonMarkdown } from '@/ui/components/LessonMarkdown';

interface LessonsScreenProps {
  lessonId: string | null;
  section: string | null;
  readLessons: string[];
  onMarkRead: (id: string) => void;
  onOpenCode: (lessonTitle: string, code: string) => void;
  onBack: () => void;
  preferenceToggles: ReactNode;
}

const lessonHash = (lessonId: string): string => routeToHash({ name: 'lessons', lessonId, section: null });

export const LessonsScreen = ({
  lessonId,
  section,
  readLessons,
  onMarkRead,
  onOpenCode,
  onBack,
  preferenceToggles,
}: LessonsScreenProps) => {
  const t = useTranslation();
  const articleRef = useRef<HTMLElement>(null);
  const foundIndex = tutorials.findIndex((tutorial) => tutorial.id === lessonId);
  const index = Math.max(foundIndex, 0);
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

  if (lesson === undefined) {
    return null;
  }

  return (
    <div className="lessons">
      <nav className="lessons-nav" aria-label={t('Lessons')}>
        <div className="lessons-actions">
          <button type="button" className="button" onClick={onBack}>
            {t('Back to projects')}
          </button>
          {preferenceToggles}
        </div>
        <ul className="lessons-list">
          {tutorials.map((tutorial, tutorialIndex) => (
            <li key={tutorial.id}>
              <a
                className="lesson-link"
                href={lessonHash(tutorial.id)}
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
      <main id="content" tabIndex={-1} className="lesson-page">
        <article ref={articleRef} className="lesson" key={lesson.id}>
          <h1 data-fixed-text>{lesson.title}</h1>
          <LessonMarkdown
            lessonId={lesson.id}
            text={lesson.text}
            onOpenCode={(code) => {
              onOpenCode(lesson.title, code);
            }}
          />
          <nav className="lesson-pager" aria-label={t('Lessons')}>
            {previous === undefined ? null : (
              <a className="button" href={lessonHash(previous.id)}>
                {t('Previous')}
              </a>
            )}
            {next === undefined ? null : (
              <a
                className="button button-primary"
                href={lessonHash(next.id)}
                onClick={() => {
                  onMarkRead(lesson.id);
                }}>
                {t('Next')}
              </a>
            )}
          </nav>
        </article>
      </main>
    </div>
  );
};
