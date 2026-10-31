import messages from './messages.json';

export type Locale = 'pt-br' | 'en-us' | 'es';
export type MessageKey = keyof typeof messages;

const FALLBACK_LOCALE: Locale = 'pt-br';

const catalog: Record<string, Partial<Record<Locale, string>>> = messages;

export const translateMessage = (locale: Locale, key: string, ...values: (string | number)[]): string => {
  const template = catalog[key]?.[locale] ?? catalog[key]?.[FALLBACK_LOCALE] ?? key;
  let index = 0;

  return template.replace(/\{\}/g, () => {
    const value = values[index] ?? '';
    index += 1;

    return String(value);
  });
};
