import { dictionaries } from './dictionaries';
import { createTranslator, detectLocale, localePath } from './i18n';

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
    ['', null, 'zh-TW', 'zh-cn'],
    ['', null, 'ja-JP', 'ja'],
    ['?lang=ja', 'es', 'pt-BR', 'ja'],
    ['', null, 'fr-FR', 'en-us'],
    ['?lang=xx', 'nada', 'en-US', 'en-us'],
  ])('detects the language for %s, saved %s, browser %s', (search, saved, browser, expected) => {
    expect(detectLocale(search, '/safira/', saved, browser)).toBe(expected);
  });

  it.each([
    ['/safira/pt-br/', null, 'en-US', 'pt-br'],
    ['/safira/ja/index.html', null, 'pt-BR', 'ja'],
    ['/safira/preview/fix/zh-cn/', null, 'en-US', 'zh-cn'],
    ['/safira/es/', 'pt-br', 'en-US', 'es'],
    ['/safira/', 'ja', 'en-US', 'ja'],
    ['/safira/en-us/', null, 'pt-BR', 'pt-br'],
    ['/safira/fr/', null, 'ja-JP', 'ja'],
    ['/safira/pt-br/assets/', null, 'en-US', 'en-us'],
  ])('opens the page of %s, saved %s, browser %s, in its language', (pathname, saved, browser, expected) => {
    expect(detectLocale('', pathname, saved, browser)).toBe(expected);
  });

  it.each([
    ['/safira/', 'pt-br', '/safira/pt-br/'],
    ['/safira/ja/', 'es', '/safira/es/'],
    ['/safira/ja/', 'en-us', '/safira/'],
    ['/safira/zh-cn/index.html', 'ja', '/safira/ja/'],
    ['/safira/index.html', 'en-us', '/safira/'],
    ['/safira/preview/fix/es/', 'zh-cn', '/safira/preview/fix/zh-cn/'],
    ['/', 'ja', '/ja/'],
    ['/ja/', 'en-us', '/'],
  ])('moves %s to the page of %s at %s', (pathname, locale, expected) => {
    expect(localePath(pathname, locale as Parameters<typeof localePath>[1])).toBe(expected);
  });

  it('lets ?lang= win over the page that was opened', () => {
    expect(detectLocale('?lang=es', '/safira/pt-br/', null, 'en-US')).toBe('es');
  });

  it('has the same keys in every dictionary', () => {
    expect(Object.keys(dictionaries.es).sort(byText)).toEqual(Object.keys(dictionaries['pt-br']).sort(byText));
    expect(Object.keys(dictionaries['zh-cn']).sort(byText)).toEqual(Object.keys(dictionaries['pt-br']).sort(byText));
    expect(Object.keys(dictionaries.ja).sort(byText)).toEqual(Object.keys(dictionaries['pt-br']).sort(byText));
  });

  it('translates every key used by the interface', () => {
    const missing = usedKeys.filter((key) => !(key in dictionaries['pt-br']));

    expect(usedKeys.length).toBeGreaterThan(0);
    expect(missing).toEqual([]);
  });
});
