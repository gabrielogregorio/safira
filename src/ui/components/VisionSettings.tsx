import { useId, useState } from 'react';
import { useTranslation } from '@/i18n/i18n';
import type { VisionMode } from '@/settings/vision';
import { VISION_MODES } from '@/settings/vision';
import { soundPlayer } from '@/ui/sound/sounds';
import { visionHint, visionLabel } from '@/ui/visionLabels';
import { Modal } from './Modal';

interface VisionSettingsProps {
  vision: VisionMode;
  onChange: (vision: VisionMode) => void;
}

const GEAR_TEETH = [0, 45, 90, 135];

const GearOrb = () => {
  const id = useId();

  return (
    <svg viewBox="0 0 48 48" aria-hidden="true">
      <defs>
        <radialGradient id={`${id}-sky`} cx="50%" cy="28%" r="80%">
          <stop offset="0%" stopColor="#e6f8ff" />
          <stop offset="55%" stopColor="#6cc8f5" />
          <stop offset="100%" stopColor="#0f6fc6" />
        </radialGradient>
        <linearGradient id={`${id}-metal`} x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stopColor="#ffffff" />
          <stop offset="55%" stopColor="#d3ecfb" />
          <stop offset="100%" stopColor="#7fb8de" />
        </linearGradient>
        <linearGradient id={`${id}-gloss`} x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stopColor="#ffffff" stopOpacity="0.85" />
          <stop offset="100%" stopColor="#ffffff" stopOpacity="0.05" />
        </linearGradient>
      </defs>
      <circle cx="24" cy="24" r="23" fill={`url(#${id}-sky)`} />
      <g className="settings-gear" fill={`url(#${id}-metal)`} stroke="#0d4f8c" strokeWidth="1">
        {GEAR_TEETH.map((angle) => (
          <rect key={angle} x="20.5" y="8" width="7" height="32" rx="1.5" transform={`rotate(${angle} 24 24)`} />
        ))}
        <circle cx="24" cy="24" r="12" stroke="none" />
        <circle cx="24" cy="24" r="5" fill="#2a8fdc" />
      </g>
      <ellipse cx="24" cy="13" rx="16" ry="9" fill={`url(#${id}-gloss)`} />
      <circle cx="24" cy="24" r="23" fill="none" stroke="#ffffff" strokeOpacity="0.9" strokeWidth="1.5" />
    </svg>
  );
};

export const VisionSettings = ({ vision, onChange }: VisionSettingsProps) => {
  const t = useTranslation();
  const id = useId();
  const [isOpen, setIsOpen] = useState(false);
  const label = t('Accessibility');

  return (
    <>
      <button
        type="button"
        className="orb-toggle settings-orb"
        aria-label={label}
        title={`${label}: ${visionLabel(t, vision)}`}
        aria-haspopup="dialog"
        onClick={() => {
          setIsOpen(true);
        }}>
        <GearOrb />
      </button>
      {isOpen ? (
        <Modal
          title={label}
          onClose={() => {
            setIsOpen(false);
          }}>
          <div className="vision-options" role="radiogroup" aria-label={label}>
            {VISION_MODES.map((mode) => (
              <label key={mode} className="vision-option">
                <input
                  type="radio"
                  name="vision"
                  aria-labelledby={`${id}-${mode}`}
                  aria-describedby={`${id}-${mode}-hint`}
                  data-autofocus={mode === vision ? true : undefined}
                  checked={mode === vision}
                  onChange={() => {
                    void soundPlayer.play('toggle');
                    onChange(mode);
                  }}
                />
                <span className="vision-option-text">
                  <span id={`${id}-${mode}`} className="vision-option-name">
                    {visionLabel(t, mode)}
                  </span>
                  <span id={`${id}-${mode}-hint`} className="vision-option-hint">
                    {visionHint(t, mode)}
                  </span>
                </span>
              </label>
            ))}
          </div>
        </Modal>
      ) : null}
    </>
  );
};
