export type SweepKind = 'theme' | 'language';

interface SceneSweepProps {
  kind: SweepKind;
  onFinished: () => void;
}

export const SCENE_SWEEP_MIDPOINT_MILLISECONDS = 450;

const MARKS: Record<SweepKind, string> = { theme: '☀', language: 'Aa' };

export const canAnimateScenes = (): boolean =>
  typeof window.matchMedia === 'function' && window.matchMedia('(prefers-reduced-motion: no-preference)').matches;

export const SceneSweep = ({ kind, onFinished }: SceneSweepProps) => (
  <div className={`scene-sweep scene-sweep-${kind}`} aria-hidden="true">
    <div
      className="scene-sweep-wave"
      onAnimationEnd={(event) => {
        if (event.target === event.currentTarget) {
          onFinished();
        }
      }}>
      <span className="scene-sweep-mark">{MARKS[kind]}</span>
    </div>
  </div>
);
