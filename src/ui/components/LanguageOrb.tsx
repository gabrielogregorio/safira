import { useId } from 'react';
import type { Locale } from '@/language/messages';

interface LanguageOrbProps {
  locale: Locale;
}

const BrazilFlag = () => (
  <>
    <rect x="10" y="26" width="140" height="88" fill="#1f9d4d" />
    <path d="M80 34 L138 70 L80 106 L22 70 Z" fill="#ffd93b" />
    <circle cx="80" cy="70" r="20" fill="#1a3f9c" />
    <path d="M60 66 Q80 60 100 74" stroke="#ffffff" strokeWidth="3" fill="none" />
  </>
);

const UnitedStatesFlag = () => (
  <>
    <rect x="10" y="26" width="140" height="88" fill="#ffffff" />
    <path
      d="M10 32 H150 M10 46 H150 M10 60 H150 M10 74 H150 M10 88 H150 M10 102 H150"
      stroke="#d0243c"
      strokeWidth="7"
    />
    <rect x="10" y="26" width="66" height="50" fill="#22407f" />
    <g fill="#ffffff">
      <circle cx="28" cy="40" r="3" />
      <circle cx="50" cy="40" r="3" />
      <circle cx="39" cy="52" r="3" />
      <circle cx="61" cy="52" r="3" />
      <circle cx="28" cy="64" r="3" />
      <circle cx="50" cy="64" r="3" />
    </g>
  </>
);

const SpainFlag = () => (
  <>
    <rect x="10" y="26" width="140" height="88" fill="#c9202c" />
    <rect x="10" y="48" width="140" height="44" fill="#ffc920" />
    <rect x="50" y="58" width="16" height="24" rx="3" fill="#a3262b" />
  </>
);

const FLAGS: Record<Locale, () => React.JSX.Element> = {
  'pt-br': BrazilFlag,
  'en-us': UnitedStatesFlag,
  es: SpainFlag,
};

export const LanguageOrb = ({ locale }: LanguageOrbProps) => {
  const id = useId();
  const Flag = FLAGS[locale];

  return (
    <svg className="choice-art" viewBox="0 0 160 96" aria-hidden="true">
      <defs>
        <linearGradient id={`${id}-sky`} x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stopColor="#58b8f2" />
          <stop offset="100%" stopColor="#d5f5ff" />
        </linearGradient>
        <clipPath id={`${id}-orb`}>
          <circle cx="80" cy="46" r="38" />
        </clipPath>
        <linearGradient id={`${id}-gloss`} x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stopColor="#ffffff" stopOpacity="0.9" />
          <stop offset="100%" stopColor="#ffffff" stopOpacity="0.05" />
        </linearGradient>
      </defs>
      <rect width="160" height="96" fill={`url(#${id}-sky)`} />
      <path d="M0 80 Q60 68 160 84 V96 H0 Z" fill="#7fdc55" />
      <g clipPath={`url(#${id}-orb)`}>
        <Flag />
      </g>
      <circle cx="80" cy="46" r="38" fill="none" stroke="#ffffff" strokeOpacity="0.85" strokeWidth="2" />
      <ellipse cx="80" cy="26" rx="28" ry="15" fill={`url(#${id}-gloss)`} />
    </svg>
  );
};
