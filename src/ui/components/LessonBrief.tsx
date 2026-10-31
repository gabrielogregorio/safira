import type { Translate } from '@/i18n/i18n';
import { useTranslation } from '@/i18n/i18n';
import type { LessonStep } from '@/content/lessons';
import type { CheckResult } from '@/lessons/lessonCheck';
import type { LessonVerdict } from '@/ui/hooks/useLessonMode';

interface LessonBriefProps {
  step: LessonStep;
  verdict: LessonVerdict;
  isDone: boolean;
  isLastStep: boolean;
  isOnStepFile: boolean;
  onNext: () => void;
  onBack: () => void;
  onStartOver: () => void;
  onShowSolution: () => void;
}

export const describeFailure = (t: Translate, result: CheckResult): string => {
  if (result.passed) {
    return '';
  }

  switch (result.reason) {
    case 'command':
      return '';
    case 'missing':
      return result.inputs.length === 0
        ? t('Almost! "{text}" did not appear in the output.', { text: result.text })
        : t('Almost! When the answer is {inputs}, "{text}" should appear.', {
            text: result.text,
            inputs: result.inputs.join(', '),
          });
    case 'spacing':
      return t('Almost! The words came out glued together. Leave a space before the closing quote: "text " + variable');
    case 'unexpected':
      return t('Almost! "{text}" should not appear here.', { text: result.text });
    case 'error':
      return `${t('Line {line}', { line: result.line ?? 0 })}: ${result.text}`;
    case 'limit':
      return t('Your program never ends. Check your repetition.');
  }
};

const describeStatus = (t: Translate, props: LessonBriefProps): string => {
  const { step, verdict, isDone, isLastStep } = props;
  const isChallenge = step.check !== null;

  if (verdict.status === 'checking') {
    return t('Checking your answer...');
  }

  if (verdict.status === 'failed') {
    return describeFailure(t, verdict.result);
  }

  if (isDone) {
    if (isLastStep) {
      return t('You finished every lesson! 🎉');
    }

    return isChallenge ? t('Correct! Challenge complete.') : t('Well done! You can move on.');
  }

  return isChallenge ? t('Write your answer and press ▶ Run.') : t('Press ▶ Run to see it work.');
};

export const LessonBrief = (props: LessonBriefProps) => {
  const t = useTranslation();
  const { step, verdict, isDone, isLastStep, isOnStepFile } = props;
  const { onNext, onBack, onStartOver, onShowSolution } = props;
  const hasFailed = verdict.status === 'failed';
  const hint = hasFailed ? (step.check?.hint ?? null) : null;

  return (
    <div className="lesson-brief-bubble">
      <div className="lesson-brief-side">
        <p
          className={`lesson-status${isDone ? ' lesson-status-done' : ''}${hasFailed ? ' lesson-status-failed' : ''}`}
          role="status">
          {isDone ? <span aria-hidden="true">✓ </span> : null}
          {describeStatus(t, props)}
          {hint === null ? null : <span className="lesson-hint">{t('Tip: {hint}', { hint })}</span>}
        </p>
        <div className="lesson-actions">
          {isOnStepFile ? (
            <button type="button" className="button" data-sound="format" onClick={onStartOver}>
              {t('Start over')}
            </button>
          ) : (
            <button type="button" className="button" data-sound="open" onClick={onBack}>
              {t('Back to the lesson')}
            </button>
          )}
          {hasFailed && isOnStepFile ? (
            <button type="button" className="button" data-sound="accept" onClick={onShowSolution}>
              {t('Show the solution')}
            </button>
          ) : null}
          {isLastStep ? null : (
            <button
              type="button"
              className={`button button-primary${isDone ? ' lesson-next-ready' : ''}`}
              data-sound="open"
              disabled={!isDone}
              onClick={onNext}>
              {t('Next')}
            </button>
          )}
        </div>
      </div>
    </div>
  );
};
