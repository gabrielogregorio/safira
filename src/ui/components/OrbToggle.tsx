import type { ReactNode } from 'react';
import { useId, useState } from 'react';

export interface OrbSlot {
  id: string;
  art: ReactNode;
}

interface OrbToggleProps {
  label: string;
  slots: OrbSlot[];
  activeIndex: number;
  backdrop: ReactNode;
  onClick: () => void;
}

const FULL_TURN = 360;
const ORB_CENTER = 24;
const SLOT_SPACING = 52;

// Slots sit on a circle wide enough to keep only one of them inside the orb, however many there are.
const pivotHeight = (slotCount: number): number =>
  Math.round(ORB_CENTER + SLOT_SPACING / (2 * Math.sin(Math.PI / slotCount)));

export const OrbToggle = ({ label, slots, activeIndex, backdrop, onClick }: OrbToggleProps) => {
  const id = useId();
  const [turn, setTurn] = useState(activeIndex);
  const stepsAhead = (activeIndex - (turn % slots.length) + slots.length) % slots.length;

  // The wheel only moves forward, so the last choice rolls into the first instead of spinning back.
  if (stepsAhead > 0) {
    setTurn(turn + stepsAhead);
  }

  const slotAngle = FULL_TURN / slots.length;
  const pivotY = pivotHeight(slots.length);

  return (
    <button type="button" className="orb-toggle" aria-label={label} title={label} onClick={onClick}>
      <svg viewBox="0 0 48 48" aria-hidden="true">
        <defs>
          <clipPath id={`${id}-orb`}>
            <circle cx="24" cy="24" r="23" />
          </clipPath>
          <linearGradient id={`${id}-gloss`} x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stopColor="#ffffff" stopOpacity="0.85" />
            <stop offset="100%" stopColor="#ffffff" stopOpacity="0.05" />
          </linearGradient>
        </defs>
        <g clipPath={`url(#${id}-orb)`}>
          {backdrop}
          <g
            className="orb-wheel"
            style={{
              transform: `rotate(${-(turn + stepsAhead) * slotAngle}deg)`,
              transformOrigin: `${ORB_CENTER}px ${pivotY}px`,
            }}>
            {slots.map((slot, index) => (
              <g
                key={slot.id}
                className="orb-slot"
                data-active={index === activeIndex}
                transform={`rotate(${index * slotAngle} ${ORB_CENTER} ${pivotY})`}>
                {slot.art}
              </g>
            ))}
          </g>
        </g>
        <ellipse cx="24" cy="13" rx="16" ry="9" fill={`url(#${id}-gloss)`} />
        <circle cx="24" cy="24" r="23" fill="none" stroke="#ffffff" strokeOpacity="0.9" strokeWidth="1.5" />
      </svg>
    </button>
  );
};
