import { dictionaries } from './dictionaries';
import { createTranslator, detectLocale } from './i18n';

const sources = import.meta.glob<string>('../ui/**/*.tsx', { eager: true, query: '?raw', import: 'default' });

const usedKeys = Object.entries(sources)
  .filter(([path]) => !path.includes('.test.'))
  .flatMap(([, text]) => [...text.matchAll(/\bt\(\s*(?:'([^']+)'|"([^"]+)")/g)].map((match) => match[1] ?? match[2]));

const byText = (first: string, second: string): number => first.localeCompare(second);

describe('i18n', () => {
  it('uses the English key as the English text', () => {
    expect(createTranslator('en-us')('Run')).toBe('Run');
  });

  it('translates and fills values', () => {
    expect(createTranslator('pt-br')('Line {line}', { line: 3 })).toBe('Linha 3');
  });

  it('keeps a marker without a value visible', () => {
    expect(createTranslator('en-us')('Line {line}')).toBe('Line {line}');
  });

  it.each([
    ['?lang=es', null, 'pt-BR', 'es'],
    ['', 'pt-br', 'en-US', 'pt-br'],
    ['', null, 'pt-BR', 'pt-br'],
    ['', null, 'es-AR', 'es'],
    ['', null, 'fr-FR', 'en-us'],
    ['?lang=xx', 'nada', 'en-US', 'en-us'],
  ])('detects the language for %s, saved %s, browser %s', (search, saved, browser, expected) => {
    expect(detectLocale(search, saved, browser)).toBe(expected);
  });

  it('has the same keys in every dictionary', () => {
    expect(Object.keys(dictionaries.es).sort(byText)).toEqual(Object.keys(dictionaries['pt-br']).sort(byText));
  });

  it('translates every key used by the interface', () => {
    const missing = usedKeys.filter((key) => !(key in dictionaries['pt-br']));

    expect(usedKeys.length).toBeGreaterThan(0);
    expect(missing).toEqual([]);
  });
});
