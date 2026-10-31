import { useState } from 'react';
import { tutorials } from '@/content/content';
import { useTranslation } from '@/i18n/i18n';
import { parseMarkdown } from '@/ui/markdown';

interface LessonsScreenProps {
  readLessons: string[];
  onMarkRead: (id: string) => void;
  onBack: () => void;
}

export const LessonsScreen = ({ readLessons, onMarkRead, onBack }: LessonsScreenProps) => {
  const t = useTranslation();
  const [index, setIndex] = useState(0);
  const lesson = tutorials[index] ?? tutorials[0];

  if (lesson === undefined) {
    return null;
  }

  const goTo = (nextIndex: number): void => {
    onMarkRead(lesson.id);
    setIndex(nextIndex);
  };

  return (
    <main id="content" className="lessons">
      <nav className="lessons-nav" aria-label={t('Lessons')}>
        <button type="button" className="button" onClick={onBack}>
          {t('Back to projects')}
        </button>
        <ul>
          {tutorials.map((tutorial, tutorialIndex) => (
            <li key={tutorial.id}>
              <button
                type="button"
                className="menu-item"
                aria-current={tutorialIndex === index ? 'page' : undefined}
                onClick={() => {
                  goTo(tutorialIndex);
                }}>
                {tutorial.title}
                {readLessons.includes(tutorial.id) ? ` (${t('Read')})` : ''}
              </button>
            </li>
          ))}
        </ul>
      </nav>
      <article className="lesson">
        <h1>{lesson.title}</h1>
        {parseMarkdown(lesson.text).map((block, blockIndex) => {
          if (block.kind === 'code') {
            return <pre key={blockIndex}>{block.text}</pre>;
          }

          return block.kind === 'heading' ? (
            <h2 key={blockIndex}>{block.text}</h2>
          ) : (
            <p key={blockIndex}>{block.text}</p>
          );
        })}
        <div className="form-row">
          <button
            type="button"
            className="button"
            disabled={index === 0}
            onClick={() => {
              goTo(index - 1);
            }}>
            {t('Previous')}
          </button>
          <button
            type="button"
            className="button button-primary"
            disabled={index === tutorials.length - 1}
            onClick={() => {
              goTo(index + 1);
            }}>
            {t('Next')}
          </button>
        </div>
      </article>
    </main>
  );
};
