import type { CSSProperties } from 'react';
import { THEME_IDS } from '@/settings/settings';
import { sceneOffset, sceneOpacity, themeAtPhase } from '@/ui/sky/skyClock';

interface SceneBackdropProps {
  phase: number;
}

const NIGHT_STARS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9];

export const SceneBackdrop = ({ phase }: SceneBackdropProps) => (
  <div className="scenery" aria-hidden="true">
    {THEME_IDS.map((id, index) => (
      <div
        key={id}
        className={`scenery-layer scenery-${id}`}
        data-active={id === themeAtPhase(phase)}
        style={{ opacity: sceneOpacity(index, phase), '--sky-offset': sceneOffset(index, phase) } as CSSProperties}>
        <span className="scenery-star" />
        {id === 'dark' ? NIGHT_STARS.map((star) => <span key={star} className="scenery-twinkle" />) : null}
      </div>
    ))}
  </div>
);
