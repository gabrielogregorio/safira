import { driveExecution } from '@/language/driver';
import { Interpreter } from '@/language/interpreter';
import { VirtualFileSystem } from '@/language/virtualFileSystem';
import type { ShownText } from './aboutPages';
import { ABOUT_PAGES, aboutHtml, aboutSitemapUrls, highlighted } from './aboutPages';
import { SEO_LOCALES, SEO_PAGES, SITE_URL } from './seoPages';

const read = (html: string): Document => new DOMParser().parseFromString(html, 'text/html');

// Builds the lines the terminal shows: a plain show ends its line, a show on the same line keeps it open.
const run = async (source: string): Promise<ShownText[][]> => {
  const lines: ShownText[][] = [];
  let line: ShownText[] = [];
  const files = new VirtualFileSystem({ 'main.safira': `#safira 1.1\n${source}` });
  await driveExecution(
    new Interpreter({ files, locale: 'en-us', random: (minimum: number) => minimum }).run('main.safira'),
    {
      onOutput: (inline: boolean, text: string, color: string) => {
        if (text !== '') {
          line.push(color === '' ? { text } : { text, color });
        }

        if (!inline) {
          lines.push(line);
          line = [];
        }
      },
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
    expect(japanese.querySelector('link[rel="apple-touch-icon"]')?.getAttribute('href')).toBe(
      '../../apple-touch-icon.png',
    );
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

  it('tells the history in paragraphs and shows how to help on GitHub', () => {
    const document = read(aboutHtml('pt-br', []));
    const help = [...document.querySelectorAll('#contribute ~ ul a')].map((link) => [
      link.textContent,
      link.getAttribute('href'),
    ]);

    expect(document.querySelectorAll('#history ~ p')).toHaveLength(ABOUT_PAGES['pt-br'].history.length);
    expect(help).toEqual([
      ['Sugerir uma ideia', 'https://github.com/gabrielogregorio/safira/issues/new?template=feature_request.yml'],
      ['Reportar um problema', 'https://github.com/gabrielogregorio/safira/issues/new?template=bug_report.yml'],
      [
        'Contribuir com código: por onde começar',
        'https://github.com/gabrielogregorio/safira/blob/main/CONTRIBUTING.md',
      ],
    ]);
  });

  it('paints what the example shows with the colors it asked for', () => {
    const terminal = read(aboutHtml('pt-br', [])).querySelector('pre.terminal');
    const painted = [...(terminal?.querySelectorAll('span') ?? [])].map((span) => [span.textContent, span.style.color]);

    expect(terminal?.textContent?.split('\n')[0]).toBe('Olá, Ana!');
    expect(painted[0]).toEqual(['Olá, Ana!', 'rgb(77, 163, 255)']);
    expect(terminal?.textContent).toContain('Você tem 12 anos.');
  });

  it('paints the code with the categories of the IDE and keeps the text intact', () => {
    const code = read(aboutHtml('pt-br', [])).querySelector('pre.editor code');

    expect(code?.textContent).toBe(ABOUT_PAGES['pt-br'].example);
    expect(code?.querySelector('.syntax-comentario')?.textContent).toBe(
      '# Várias formas de dizer a mesma coisa, com cor.',
    );
    expect(code?.querySelector('.syntax-exibicao')?.textContent).toBe('mostre');
    expect(highlighted('x = "<b>"')).toBe(
      'x <span class="syntax-atribuicao">=</span> <span class="syntax-string">&quot;&lt;b&gt;&quot;</span>',
    );
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
