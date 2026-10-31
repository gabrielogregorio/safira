import type { ThemeId } from '@/settings/settings';

interface SceneBackdropProps {
  theme: ThemeId;
}

const THEME_IDS: ThemeId[] = ['light', 'dark', 'simple'];

export const SceneBackdrop = ({ theme }: SceneBackdropProps) => (
  <div className="scenery" aria-hidden="true">
    {THEME_IDS.map((id) => (
      <div key={id} className={`scenery-layer scenery-${id}`} data-active={id === theme}>
        <span className="scenery-star" />
      </div>
    ))}
  </div>
);
