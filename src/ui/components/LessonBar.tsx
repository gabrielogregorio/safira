import { useTranslation } from '@/i18n/i18n';
import type { Lesson } from '@/content/lessons';
import { isLessonDone, isStepDone, nextPlace, previousPlace, resumePlace } from '@/lessons/lessonPlace';
import type { LessonPlace } from '@/settings/settings';

interface LessonBarProps {
  lessons: Lesson[];
  place: LessonPlace;
  progress: string[];
  onOpen: (place: LessonPlace) => void;
}

const DONE_MARK = '✓';

export const LessonBar = ({ lessons, place, progress, onOpen }: LessonBarProps) => {
  const t = useTranslation();
  const lesson = lessons.find((candidate) => candidate.id === place.lessonId);
  const previous = previousPlace(lessons, place);
  const next = nextPlace(lessons, place);
  const steps = lesson?.steps ?? [];
  const isDone = (step: number): boolean => isStepDone(progress, { lessonId: place.lessonId, step });
  const firstPending = steps.findIndex((_step, step) => !isDone(step));
  const canReach = (step: number): boolean => firstPending === -1 || step <= firstPending;

  return (
    <div className="lesson-bar" role="group" aria-label={t('Lesson mode')}>
      <button
        type="button"
        className="lesson-arrow"
        data-sound="tab"
        aria-label={t('Previous step')}
        title={t('Previous step')}
        disabled={previous === null}
        onClick={() => {
          onOpen(previous as LessonPlace);
        }}>
        ‹
      </button>
      <select
        className="lesson-select"
        aria-label={t('Choose a lesson')}
        data-fixed-text
        value={place.lessonId}
        onChange={(event) => {
          const chosen = lessons.find((candidate) => candidate.id === event.target.value);

          if (chosen !== undefined) {
            onOpen(resumePlace(chosen, progress));
          }
        }}>
        {lessons.map((candidate, index) => (
          <option key={candidate.id} value={candidate.id}>
            {[`${String(index + 1)}.`, candidate.title, isLessonDone(progress, candidate) ? DONE_MARK : '']
              .join(' ')
              .trim()}
          </option>
        ))}
      </select>
      <ol className="lesson-steps" aria-label={t('Lesson steps')}>
        {steps.map((step, index) => {
          const number = index + 1;
          const label = t(isDone(index) ? 'Step {number}: {title} (done)' : 'Step {number}: {title}', {
            number,
            title: step.title,
          });

          return (
            <li key={step.title}>
              <button
                type="button"
                className={isDone(index) ? 'lesson-dot lesson-dot-done' : 'lesson-dot'}
                data-sound="tab"
                aria-label={label}
                title={label}
                aria-current={index === place.step ? 'step' : undefined}
                disabled={!canReach(index)}
                onClick={() => {
                  onOpen({ lessonId: place.lessonId, step: index });
                }}>
                {isDone(index) ? DONE_MARK : number}
              </button>
            </li>
          );
        })}
      </ol>
      <button
        type="button"
        className="lesson-arrow"
        data-sound="tab"
        aria-label={t('Next step')}
        title={t('Next step')}
        disabled={next === null || !isStepDone(progress, place)}
        onClick={() => {
          onOpen(next as LessonPlace);
        }}>
        ›
      </button>
    </div>
  );
};
