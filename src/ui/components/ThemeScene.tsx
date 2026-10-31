import { useId } from 'react';
import type { ThemeId } from '@/settings/settings';

interface ThemeSceneProps {
  theme: ThemeId;
}

interface SceneProps {
  id: string;
}

const Cloud = ({ x, y, scale }: { x: number; y: number; scale: number }) => (
  <g transform={`translate(${x} ${y}) scale(${scale})`} fill="#ffffff">
    <ellipse cx="0" cy="0" rx="18" ry="8" />
    <ellipse cx="-9" cy="-4" rx="9" ry="7" />
    <ellipse cx="7" cy="-6" rx="11" ry="9" />
  </g>
);

const SunnySky = ({ id }: SceneProps) => (
  <>
    <defs>
      <linearGradient id={`${id}-sky`} x1="0" y1="0" x2="0" y2="1">
        <stop offset="0%" stopColor="#1f8fe0" />
        <stop offset="70%" stopColor="#bdeeff" />
      </linearGradient>
      <radialGradient id={`${id}-sun`}>
        <stop offset="0%" stopColor="#fffbe0" />
        <stop offset="35%" stopColor="#ffe873" />
        <stop offset="100%" stopColor="#ffe873" stopOpacity="0" />
      </radialGradient>
      <linearGradient id={`${id}-hill`} x1="0" y1="0" x2="0" y2="1">
        <stop offset="0%" stopColor="#a6f06b" />
        <stop offset="100%" stopColor="#35a82a" />
      </linearGradient>
    </defs>
    <rect width="160" height="96" fill={`url(#${id}-sky)`} />
    <circle cx="122" cy="24" r="26" fill={`url(#${id}-sun)`} />
    <Cloud x={40} y={28} scale={1} />
    <Cloud x={92} y={44} scale={0.6} />
    <path d="M0 74 Q50 50 104 72 T160 66 V96 H0 Z" fill="#7fdc55" />
    <path d="M0 84 Q64 62 160 86 V96 H0 Z" fill={`url(#${id}-hill)`} />
  </>
);

const MoonlitAurora = ({ id }: SceneProps) => (
  <>
    <defs>
      <linearGradient id={`${id}-sky`} x1="0" y1="0" x2="0" y2="1">
        <stop offset="0%" stopColor="#030d26" />
        <stop offset="75%" stopColor="#0a4a6e" />
      </linearGradient>
      <linearGradient id={`${id}-aurora`} x1="0" y1="0" x2="1" y2="0">
        <stop offset="0%" stopColor="#3dffb0" stopOpacity="0" />
        <stop offset="50%" stopColor="#3dffb0" stopOpacity="0.75" />
        <stop offset="100%" stopColor="#7a8bff" stopOpacity="0.1" />
      </linearGradient>
    </defs>
    <rect width="160" height="96" fill={`url(#${id}-sky)`} />
    <path
      d="M-6 56 C30 10 66 62 100 28 S150 22 170 42 V62 C130 44 104 76 66 62 S20 62 -6 76 Z"
      fill={`url(#${id}-aurora)`}
    />
    <circle cx="122" cy="24" r="13" fill="#fdf6d3" />
    <circle cx="128" cy="20" r="11" fill="#04163a" />
    <g fill="#ffffff">
      <circle cx="24" cy="14" r="1" />
      <circle cx="52" cy="24" r="0.8" />
      <circle cx="84" cy="10" r="1.1" />
      <circle cx="146" cy="44" r="0.8" />
      <circle cx="104" cy="16" r="0.7" />
    </g>
    <path d="M0 80 Q56 60 160 82 V96 H0 Z" fill="#06302f" />
  </>
);

const RainyLagoon = ({ id }: SceneProps) => (
  <>
    <defs>
      <linearGradient id={`${id}-sky`} x1="0" y1="0" x2="0" y2="1">
        <stop offset="0%" stopColor="#3f7f94" />
        <stop offset="58%" stopColor="#a4e3df" />
      </linearGradient>
      <linearGradient id={`${id}-water`} x1="0" y1="0" x2="0" y2="1">
        <stop offset="0%" stopColor="#23c7b0" />
        <stop offset="100%" stopColor="#056a74" />
      </linearGradient>
    </defs>
    <rect width="160" height="96" fill={`url(#${id}-sky)`} />
    <Cloud x={52} y={24} scale={1.15} />
    <Cloud x={112} y={32} scale={0.9} />
    <g stroke="#e6fbff" strokeWidth="1.4" strokeLinecap="round">
      <path d="M34 38 l-3 9 M50 40 l-3 9 M66 38 l-3 9 M98 44 l-3 9 M114 46 l-3 9 M128 44 l-3 9" />
    </g>
    <path d="M0 64 Q20 58 40 64 T80 64 T120 64 T160 64 V96 H0 Z" fill={`url(#${id}-water)`} />
    <g fill="#ffffff" fillOpacity="0.5">
      <circle cx="34" cy="80" r="4" />
      <circle cx="44" cy="74" r="2.2" />
      <circle cx="118" cy="82" r="3" />
    </g>
  </>
);

const SCENES: Record<ThemeId, (props: SceneProps) => React.JSX.Element> = {
  light: SunnySky,
  dark: MoonlitAurora,
  simple: RainyLagoon,
};

export const ThemeScene = ({ theme }: ThemeSceneProps) => {
  const id = useId();
  const Scene = SCENES[theme];

  return (
    <svg className="choice-art" viewBox="0 0 160 96" aria-hidden="true">
      <Scene id={id} />
      <ellipse cx="80" cy="4" rx="96" ry="24" fill="#ffffff" fillOpacity="0.22" />
    </svg>
  );
};
