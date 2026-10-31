import { useTranslation } from '@/i18n/i18n';
import type { ThemeId } from '@/settings/settings';
import { THEME_IDS } from '@/settings/settings';
import type { OrbSlot } from './OrbToggle';
import { OrbToggle } from './OrbToggle';

interface ThemeToggleProps {
  theme: ThemeId;
  onChange: (theme: ThemeId) => void;
}

const NEXT_THEME: Record<ThemeId, ThemeId> = { light: 'dark', dark: 'simple', simple: 'light' };

const SKY_COLORS: Record<ThemeId, { top: string; bottom: string; ground: string }> = {
  light: { top: '#1f8fe0', bottom: '#bdeeff', ground: '#6fd64a' },
  dark: { top: '#030d26', bottom: '#0a4a6e', ground: '#06302f' },
  simple: { top: '#3f7f94', bottom: '#a4e3df', ground: '#14958f' },
};

const Sun = () => (
  <>
    <g className="orb-sun-rays" stroke="#fff3a8" strokeWidth="2.4" strokeLinecap="round">
      <path d="M24 5 V9 M24 31 V35 M9 20 H13 M35 20 H39 M13.4 9.4 L16.2 12.2 M31.8 27.8 L34.6 30.6 M13.4 30.6 L16.2 27.8 M31.8 12.2 L34.6 9.4" />
    </g>
    <circle cx="24" cy="20" r="8.5" fill="#ffe34d" stroke="#fffbe0" strokeWidth="1.5" />
  </>
);

const Moon = () => (
  <>
    <path d="M27 8 A13 13 0 1 0 37 28 A11 11 0 0 1 27 8 Z" fill="#fdf6d3" />
    <g fill="#ffffff">
      <circle className="orb-star" cx="33" cy="11" r="1.3" />
      <circle className="orb-star orb-star-late" cx="39" cy="19" r="1" />
      <circle className="orb-star orb-star-later" cx="10" cy="10" r="1" />
    </g>
  </>
);

const RainCloud = () => (
  <>
    <g fill="#ffffff">
      <ellipse cx="24" cy="19" rx="13" ry="6.5" />
      <circle cx="18" cy="15" r="6" />
      <circle cx="28" cy="13" r="7.5" />
    </g>
    <path
      className="orb-rain"
      d="M16 27 l-2 6 M24 27 l-2 6 M32 27 l-2 6"
      stroke="#e6fbff"
      strokeWidth="2"
      strokeLinecap="round"
    />
  </>
);

const SLOTS: OrbSlot[] = [
  { id: 'light', art: <Sun /> },
  { id: 'dark', art: <Moon /> },
  { id: 'simple', art: <RainCloud /> },
];

const Sky = ({ theme, isActive }: { theme: ThemeId; isActive: boolean }) => {
  const { top, bottom, ground } = SKY_COLORS[theme];
  const gradientId = `orb-sky-${theme}`;

  return (
    <g className="orb-sky" data-active={isActive}>
      <linearGradient id={gradientId} x1="0" y1="0" x2="0" y2="1">
        <stop offset="0%" stopColor={top} />
        <stop offset="100%" stopColor={bottom} />
      </linearGradient>
      <rect width="48" height="48" fill={`url(#${gradientId})`} />
      <path d="M0 40 Q16 32 48 41 V48 H0 Z" fill={ground} />
    </g>
  );
};

export const ThemeToggle = ({ theme, onChange }: ThemeToggleProps) => {
  const t = useTranslation();
  const names: Record<ThemeId, string> = { light: t('Light'), dark: t('Dark'), simple: t('Simple') };

  return (
    <OrbToggle
      label={t('Theme: {name}', { name: names[theme] })}
      slots={SLOTS}
      activeIndex={THEME_IDS.indexOf(theme)}
      backdrop={THEME_IDS.map((id) => (
        <Sky key={id} theme={id} isActive={id === theme} />
      ))}
      onClick={() => {
        onChange(NEXT_THEME[theme]);
      }}
    />
  );
};
