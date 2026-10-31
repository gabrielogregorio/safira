import { useTranslation } from '@/i18n/i18n';
import type { VisionMode } from '@/settings/vision';
import { VISION_MODES } from '@/settings/vision';
import { visionLabel } from '@/ui/visionLabels';
import type { OrbSlot } from './OrbToggle';
import { OrbToggle } from './OrbToggle';

interface VisionToggleProps {
  vision: VisionMode;
  onChange: (vision: VisionMode) => void;
}

const IRIS_COLORS: Record<VisionMode, string> = {
  default: '#1f8fe0',
  protanopia: '#1a66c2',
  deuteranopia: '#d98324',
  tritanopia: '#d6246e',
  achromatopsia: '#6e6e6e',
  lowVision: '#000000',
  lightSensitivity: '#a8814a',
  calm: '#3f9c7a',
};

const Eye = ({ vision }: { vision: VisionMode }) => (
  <>
    <path d="M6 20 Q24 5 42 20 Q24 35 6 20 Z" fill="#ffffff" stroke="#0b2a4a" strokeWidth="1.6" />
    <circle cx="24" cy="20" r="7.5" fill={IRIS_COLORS[vision]} />
    <circle cx="24" cy="20" r="3" fill="#0b2a4a" />
    <circle cx="26.5" cy="17.5" r="1.4" fill="#ffffff" />
  </>
);

const SLOTS: OrbSlot[] = VISION_MODES.map((vision) => ({ id: vision, art: <Eye vision={vision} /> }));

export const VisionToggle = ({ vision, onChange }: VisionToggleProps) => {
  const t = useTranslation();
  const activeIndex = VISION_MODES.indexOf(vision);

  return (
    <OrbToggle
      label={`${t('Accessibility')}: ${visionLabel(t, vision)}`}
      slots={SLOTS}
      activeIndex={activeIndex}
      backdrop={<rect width="48" height="48" fill="#d6efff" />}
      onClick={() => {
        onChange(VISION_MODES[(activeIndex + 1) % VISION_MODES.length]);
      }}
    />
  );
};
