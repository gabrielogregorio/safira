import { useId } from 'react';

interface SafiraLogoProps {
  size: number;
}

export const SafiraLogo = ({ size }: SafiraLogoProps) => {
  const id = useId();

  return (
    <svg className="safira-logo" width={size} height={size} viewBox="0 0 64 64" aria-hidden="true">
      <defs>
        <radialGradient id={`${id}-orb`} cx="35%" cy="28%" r="75%">
          <stop offset="0%" stopColor="#c8f2ff" />
          <stop offset="38%" stopColor="#2fa8f0" />
          <stop offset="100%" stopColor="#07307e" />
        </radialGradient>
        <linearGradient id={`${id}-gloss`} x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stopColor="#ffffff" stopOpacity="0.95" />
          <stop offset="100%" stopColor="#ffffff" stopOpacity="0.05" />
        </linearGradient>
      </defs>
      <circle cx="32" cy="32" r="29" fill={`url(#${id}-orb)`} stroke="#ffffff" strokeOpacity="0.7" strokeWidth="1.5" />
      <path d="M32 15 L46 27 L32 50 L18 27 Z" fill="#ffffff" fillOpacity="0.22" stroke="#ffffff" strokeOpacity="0.75" />
      <path d="M18 27 H46 M25 27 L32 15 L39 27 L32 50 Z" fill="none" stroke="#ffffff" strokeOpacity="0.55" />
      <ellipse cx="32" cy="16" rx="21" ry="11.5" fill={`url(#${id}-gloss)`} />
    </svg>
  );
};
