import type { Lesson } from '@/content/lessons';
import { useTranslation } from '@/i18n/i18n';
import { isStepDone } from '@/lessons/lessonPlace';

interface LessonProgressProps {
  lessons: Lesson[];
  progress: string[];
}

const FULL = 100;

export const LessonProgress = ({ lessons, progress }: LessonProgressProps) => {
  const t = useTranslation();
  const steps = lessons.flatMap((lesson) => lesson.steps.map((_step, step) => ({ lessonId: lesson.id, step })));
  const done = steps.filter((place) => isStepDone(progress, place)).length;
  const percent = Math.round((done / Math.max(steps.length, 1)) * FULL);
  const label = t('{done} of {total} steps', { done, total: steps.length });

  return (
    <div className="lesson-progress">
      <span>{label}</span>
      <div
        className="lesson-progress-track"
        role="progressbar"
        aria-label={t('Progress in the lessons')}
        aria-valuemin={0}
        aria-valuemax={FULL}
        aria-valuenow={percent}
        aria-valuetext={label}>
        <div className="lesson-progress-fill" style={{ width: `${String(percent)}%` }} />
      </div>
    </div>
  );
};
