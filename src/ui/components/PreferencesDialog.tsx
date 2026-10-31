import { LOCALES, useTranslation } from '@/i18n/i18n';
import type { Locale } from '@/language/messages';
import type { Settings, ThemeId } from '@/settings/settings';
import { LanguageOrb } from './LanguageOrb';
import { Modal } from './Modal';
import { ThemeScene } from './ThemeScene';

interface PreferencesDialogProps {
  settings: Settings;
  locale: Locale;
  onChange: (changes: Partial<Settings>) => void;
  onClose: () => void;
}

const THEME_IDS: ThemeId[] = ['light', 'dark', 'simple'];

export const PreferencesDialog = ({ settings, locale, onChange, onClose }: PreferencesDialogProps) => {
  const t = useTranslation();
  const themeLabels: Record<ThemeId, string> = { light: t('Light'), dark: t('Dark'), simple: t('Simple') };

  return (
    <Modal title={t('Theme and language')} onClose={onClose}>
      <fieldset className="choice-group">
        <legend>{t('Theme')}</legend>
        <div className="choice-row">
          {THEME_IDS.map((theme) => (
            <label key={theme} className="choice-card">
              <input
                type="radio"
                name="theme"
                checked={settings.theme === theme}
                onChange={() => {
                  onChange({ theme, syntax: theme });
                }}
              />
              <ThemeScene theme={theme} />
              <span>{themeLabels[theme]}</span>
            </label>
          ))}
        </div>
      </fieldset>
      <fieldset className="choice-group">
        <legend>{t('Language')}</legend>
        <div className="choice-row">
          {LOCALES.map((option) => (
            <label key={option.id} className="choice-card">
              <input
                type="radio"
                name="language"
                checked={locale === option.id}
                onChange={() => {
                  onChange({ locale: option.id });
                }}
              />
              <LanguageOrb locale={option.id} />
              <span>{option.label}</span>
            </label>
          ))}
        </div>
      </fieldset>
    </Modal>
  );
};
