import { createContext, useContext } from 'react';
import type { Locale } from '@/language/messages';
import type { TranslationKey } from './dictionaries';
import { dictionaries } from './dictionaries';

export const LOCALES: { id: Locale; label: string }[] = [
  { id: 'en-us', label: 'English' },
  { id: 'pt-br', label: 'Português (Brasil)' },
  { id: 'es', label: 'Español' },
  { id: 'zh-cn', label: '简体中文' },
  { id: 'ja', label: '日本語' },
];

export type Translate = (key: TranslationKey, values?: Record<string, string | number>) => string;

const fillValues = (text: string, values: Record<string, string | number>): string =>
  text.replace(/\{(\w+)\}/g, (marker, name: string) => String(values[name] ?? marker));

export const createTranslator =
  (locale: Locale): Translate =>
  (key, values = {}) => {
    const text = locale === 'en-us' ? key : dictionaries[locale][key];

    return fillValues(text, values);
  };

const isLocale = (value: string | null): value is Locale => LOCALES.some((locale) => locale.id === value);

const BROWSER_LANGUAGES: [string, Locale][] = [
  ['pt', 'pt-br'],
  ['es', 'es'],
  ['zh', 'zh-cn'],
  ['ja', 'ja'],
];

const fromBrowserLanguage = (language: string): Locale => {
  const lower = language.toLowerCase();

  const match = BROWSER_LANGUAGES.find(([prefix]) => lower.startsWith(prefix));

  return match === undefined ? 'en-us' : match[1];
};

export const detectLocale = (search: string, saved: string | null, browserLanguage: string): Locale => {
  const requested = new URLSearchParams(search).get('lang');

  if (isLocale(requested)) {
    return requested;
  }

  return isLocale(saved) ? saved : fromBrowserLanguage(browserLanguage);
};

export const TranslationContext = createContext<Translate>(createTranslator('en-us'));

export const useTranslation = (): Translate => useContext(TranslationContext);
