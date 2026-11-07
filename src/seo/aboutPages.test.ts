import { driveExecution } from '@/language/driver';
import { Interpreter } from '@/language/interpreter';
import { VirtualFileSystem } from '@/language/virtualFileSystem';
import { ABOUT_PAGES, aboutHtml, aboutSitemapUrls } from './aboutPages';
import { SEO_LOCALES, SEO_PAGES, SITE_URL } from './seoPages';

const read = (html: string): Document => new DOMParser().parseFromString(html, 'text/html');

const run = async (source: string): Promise<string[]> => {
  const lines: string[] = [];
  const files = new VirtualFileSystem({ 'main.safira': `#safira 1.1\n${source}` });
  await driveExecution(
    new Interpreter({ files, locale: 'en-us', random: (minimum: number) => minimum }).run('main.safira'),
    {
      onOutput: (_inline: boolean, text: string) => lines.push(text),
    } as unknown as Parameters<typeof driveExecution>[1],
  );

  return lines;
};

describe('about pages', () => {
  it.each(SEO_LOCALES)('shows in %s what its example really prints', async (locale) => {
    const copy = ABOUT_PAGES[locale];

    expect(await run(copy.example)).toEqual(copy.output);
  });

  it.each(SEO_LOCALES)('writes the page of %s in its own language, with the lessons', (locale) => {
    const copy = ABOUT_PAGES[locale];
    const document = read(aboutHtml(locale, ['Lesson one', 'Lesson <two>']));
    const url = `${SITE_URL}${SEO_PAGES[locale].folder}about/`;

    expect(document.documentElement.lang).toBe(SEO_PAGES[locale].htmlLang);
    expect(document.title).toBe(copy.title);
    expect(document.querySelector('meta[name="description"]')?.getAttribute('content')).toBe(copy.description);
    expect(document.querySelector('link[rel="canonical"]')?.getAttribute('href')).toBe(url);
    expect(document.querySelector('h1')?.textContent).toBe(copy.heading);
    expect(document.querySelector('pre code')?.textContent).toBe(copy.example);
    expect([...document.querySelectorAll('ol li')].map((item) => item.textContent)).toEqual([
      'Lesson one',
      'Lesson <two>',
    ]);
    expect(document.querySelectorAll('dt')).toHaveLength(copy.questions.length);
    expect(document.querySelector('a.open')?.getAttribute('href')).toBe('../');
  });

  it('reaches the icon and the other languages from one or two folders deep', () => {
    const english = read(aboutHtml('en-us', []));
    const japanese = read(aboutHtml('ja', []));
    const languages = (document: Document): (string | null)[] =>
      [...document.querySelectorAll('footer a')].map((link) => link.getAttribute('href'));

    expect(english.querySelector('link[rel="icon"]')?.getAttribute('href')).toBe('../icone.png');
    expect(japanese.querySelector('link[rel="icon"]')?.getAttribute('href')).toBe('../../icone.png');
    expect(languages(english)).toEqual([
      '../about/',
      '../pt-br/about/',
      '../es/about/',
      '../zh-cn/about/',
      '../ja/about/',
    ]);
    expect(languages(japanese)[0]).toBe('../../about/');
    expect(japanese.querySelector('footer a[aria-current="page"]')?.textContent).toBe('日本語');
  });

  it('links each about page to every language and to a default', () => {
    const links = [...read(aboutHtml('es', [])).querySelectorAll('link[rel="alternate"]')].map((link) =>
      link.getAttribute('hreflang'),
    );

    expect(links).toEqual(['en', 'pt-BR', 'es', 'zh-CN', 'ja', 'x-default']);
  });

  it('lists every about page for the sitemap', () => {
    const urls = aboutSitemapUrls();

    expect(urls).toHaveLength(SEO_LOCALES.length);
    expect(urls[4]).toContain(`<loc>${SITE_URL}ja/about/</loc>`);
    expect(urls[0]).toContain(`hreflang="zh-CN" href="${SITE_URL}zh-cn/about/"`);
  });
});
