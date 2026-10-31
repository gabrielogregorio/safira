import { useId } from 'react';

interface AeroOrbProps {
  size: number;
}

const BUBBLES = [
  { x: 34, radius: 2.6, delay: '0s' },
  { x: 52, radius: 1.7, delay: '1.1s' },
  { x: 68, radius: 3.1, delay: '2.3s' },
  { x: 84, radius: 2, delay: '0.6s' },
  { x: 44, radius: 1.5, delay: '3s' },
];

const WAVE = 'M-120 0 q15 -7 30 0 t30 0 t30 0 t30 0 t30 0 t30 0 t30 0 t30 0 V70 H-120 Z';

// A glass globe with an aquarium inside, the most Frutiger Aero object there is: water, bubbles, a fish and a sprout.
export const AeroOrb = ({ size }: AeroOrbProps) => {
  const id = useId();

  return (
    <svg className="aero-orb" width={size} height={size} viewBox="0 0 120 120" aria-hidden="true">
      <defs>
        <radialGradient id={`${id}-sky`} cx="42%" cy="28%" r="80%">
          <stop offset="0%" stopColor="#f2fdff" />
          <stop offset="55%" stopColor="#8fdcfa" />
          <stop offset="100%" stopColor="#2a93dc" />
        </radialGradient>
        <linearGradient id={`${id}-water`} x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stopColor="#35c6f0" stopOpacity="0.9" />
          <stop offset="100%" stopColor="#0a4fa8" />
        </linearGradient>
        <linearGradient id={`${id}-gloss`} x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stopColor="#ffffff" stopOpacity="0.95" />
          <stop offset="100%" stopColor="#ffffff" stopOpacity="0.04" />
        </linearGradient>
        <radialGradient id={`${id}-rim`} cx="50%" cy="50%" r="50%">
          <stop offset="78%" stopColor="#ffffff" stopOpacity="0" />
          <stop offset="96%" stopColor="#d9f6ff" stopOpacity="0.75" />
          <stop offset="100%" stopColor="#ffffff" />
        </radialGradient>
        <linearGradient id={`${id}-leaf`} x1="0" y1="0" x2="1" y2="1">
          <stop offset="0%" stopColor="#c8f76a" />
          <stop offset="100%" stopColor="#35a82f" />
        </linearGradient>
        <clipPath id={`${id}-globe`}>
          <circle cx="60" cy="60" r="50" />
        </clipPath>
      </defs>
      <g className="aero-orb-float">
        <circle cx="60" cy="60" r="50" fill={`url(#${id}-sky)`} />
        <g clipPath={`url(#${id}-globe)`}>
          <g className="aero-orb-sway" style={{ transformOrigin: '60px 66px' }}>
            <path d="M60 66 Q58 50 62 38" fill="none" stroke="#4cae34" strokeWidth="3" strokeLinecap="round" />
            <path d="M62 40 C72 26 88 28 92 32 C86 44 72 48 62 40 Z" fill={`url(#${id}-leaf)`} />
            <path d="M60 50 C50 38 36 40 32 44 C38 54 52 58 60 50 Z" fill={`url(#${id}-leaf)`} />
          </g>
          <g transform="translate(0 64)">
            <path className="aero-orb-wave aero-orb-wave-back" d={WAVE} fill="#7fe0f7" fillOpacity="0.6" />
            <path className="aero-orb-wave" d={WAVE} fill={`url(#${id}-water)`} />
          </g>
          <g className="aero-orb-fish">
            <path d="M0 88 C8 80 20 80 26 88 C20 96 8 96 0 88 Z" fill="#ffb347" />
            <path d="M0 88 L-9 81 L-7 88 L-9 95 Z" fill="#ff8a2a" />
            <circle cx="20" cy="86.5" r="1.5" fill="#123" />
          </g>
          {BUBBLES.map((bubble) => (
            <circle
              key={bubble.x}
              className="aero-orb-bubble"
              cx={bubble.x}
              cy="108"
              r={bubble.radius}
              style={{ animationDelay: bubble.delay }}
            />
          ))}
        </g>
        <circle cx="60" cy="60" r="50" fill={`url(#${id}-rim)`} />
        <ellipse cx="60" cy="31" rx="35" ry="19" fill={`url(#${id}-gloss)`} />
        <path className="aero-orb-sparkle" d="M92 22 l2.4 6.6 6.6 2.4 -6.6 2.4 -2.4 6.6 -2.4 -6.6 -6.6 -2.4 6.6 -2.4 Z" />
      </g>
    </svg>
  );
};
