import { useTranslation } from '@/i18n/i18n';
import type { OrbSlot } from './OrbToggle';
import { OrbToggle } from './OrbToggle';

interface SoundToggleProps {
  isOn: boolean;
  onChange: (isOn: boolean) => void;
}

const Speaker = () => <path d="M10 19 H17 L26 11 V37 L17 29 H10 Z" fill="#ffffff" stroke="#0b4f9c" strokeWidth="1.2" />;

const SpeakerOn = () => (
  <>
    <Speaker />
    <g fill="none" stroke="#ffffff" strokeWidth="2.6" strokeLinecap="round">
      <path className="orb-star" d="M30 19 Q33.5 24 30 29" />
      <path className="orb-star orb-star-late" d="M34 15 Q40 24 34 33" />
    </g>
  </>
);

const SpeakerOff = () => (
  <>
    <Speaker />
    <path d="M31 19 L40 29 M40 19 L31 29" stroke="#ffd7dd" strokeWidth="3" strokeLinecap="round" />
  </>
);

const SLOTS: OrbSlot[] = [
  { id: 'on', art: <SpeakerOn /> },
  { id: 'off', art: <SpeakerOff /> },
];

export const SoundToggle = ({ isOn, onChange }: SoundToggleProps) => {
  const t = useTranslation();

  return (
    <OrbToggle
      label={t('Sound: {name}', { name: isOn ? t('On') : t('Off') })}
      slots={SLOTS}
      activeIndex={isOn ? 0 : 1}
      backdrop={<rect width="48" height="48" fill={isOn ? '#1f8fe0' : '#6d7f92'} />}
      onClick={() => {
        onChange(!isOn);
      }}
    />
  );
};
