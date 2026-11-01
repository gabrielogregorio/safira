import { useId } from 'react';
import { LOCALES, useTranslation } from '@/i18n/i18n';
import type { Locale } from '@/language/messages';
import type { OrbSlot } from './OrbToggle';
import { OrbToggle } from './OrbToggle';

interface LanguageToggleProps {
  locale: Locale;
  onChange: (locale: Locale) => void;
}

const NEXT_LOCALE: Record<Locale, Locale> = {
  'en-us': 'pt-br',
  'pt-br': 'es',
  es: 'zh-cn',
  'zh-cn': 'ja',
  ja: 'en-us',
};

const BrazilFlag = () => (
  <>
    <rect width="48" height="48" fill="#1f9d4d" />
    <path d="M24 6 L46 24 L24 42 L2 24 Z" fill="#ffd93b" />
    <circle cx="24" cy="24" r="10" fill="#1a3f9c" />
    <path d="M14.5 22 Q24 19 33.5 27" stroke="#ffffff" strokeWidth="1.8" fill="none" />
  </>
);

const UnitedStatesFlag = () => (
  <>
    <rect width="48" height="48" fill="#ffffff" />
    <path d="M0 4 H48 M0 15 H48 M0 26 H48 M0 37 H48 M0 47 H48" stroke="#d0243c" strokeWidth="5.5" />
    <rect width="27" height="24" fill="#22407f" />
    <g fill="#ffffff">
      <circle cx="13" cy="9" r="1.5" />
      <circle cx="21" cy="9" r="1.5" />
      <circle cx="17" cy="15" r="1.5" />
      <circle cx="9" cy="15" r="1.5" />
      <circle cx="13" cy="20" r="1.5" />
      <circle cx="21" cy="20" r="1.5" />
    </g>
  </>
);

const SpainFlag = () => (
  <>
    <rect width="48" height="48" fill="#c9202c" />
    <rect y="12" width="48" height="24" fill="#ffc920" />
    <rect x="13" y="18" width="8" height="12" rx="2" fill="#a3262b" />
  </>
);

const ChinaFlag = () => (
  <>
    <rect width="48" height="48" fill="#de2910" />
    <path d="M17 12 L20 21 L29 21 L22 27 L25 36 L17 30 L9 36 L12 27 L5 21 L14 21 Z" fill="#ffde00" />
    <g fill="#ffde00">
      <circle cx="31" cy="11" r="2" />
      <circle cx="36" cy="17" r="2" />
      <circle cx="36" cy="25" r="2" />
      <circle cx="31" cy="31" r="2" />
    </g>
  </>
);

const JapanFlag = () => (
  <>
    <rect width="48" height="48" fill="#ffffff" />
    <circle cx="24" cy="24" r="13" fill="#d0243c" />
  </>
);

const FLAGS: Record<Locale, () => React.JSX.Element> = {
  'en-us': UnitedStatesFlag,
  'pt-br': BrazilFlag,
  es: SpainFlag,
  'zh-cn': ChinaFlag,
  ja: JapanFlag,
};

export const LanguageToggle = ({ locale, onChange }: LanguageToggleProps) => {
  const t = useTranslation();
  const id = useId();
  const clipId = `${id}-flag`;
  const slots: OrbSlot[] = LOCALES.map((option) => {
    const Flag = FLAGS[option.id];

    return {
      id: option.id,
      art: (
        <g clipPath={`url(#${clipId})`}>
          <Flag />
        </g>
      ),
    };
  });

  return (
    <OrbToggle
      className="language-orb"
      sound="click"
      label={t('Language: {name}', { name: LOCALES.find((option) => option.id === locale)?.label ?? locale })}
      slots={slots}
      activeIndex={LOCALES.findIndex((option) => option.id === locale)}
      backdrop={
        <>
          <clipPath id={clipId}>
            <circle cx="24" cy="24" r="24" />
          </clipPath>
          <rect width="48" height="48" fill="#58b8f2" />
        </>
      }
      onClick={() => {
        onChange(NEXT_LOCALE[locale]);
      }}
    />
  );
};
