import { pageHtml, SEO_LOCALES, SEO_PAGES, SITE_URL, sitemapXml } from './seoPages';

const BUILT = `<!doctype html>
<html lang="en">
  <head>
    <meta name="description" content="Safira, a programming language in natural language, with a web IDE" />
    <link rel="icon" type="image/png" href="./icone.png" />
    <link rel="apple-touch-icon" href="./apple-touch-icon.png" />
    <title>Safira</title>
    <script type="module" crossorigin src="./assets/index.js"></script>
    <link rel="stylesheet" crossorigin href="./assets/index.css">
  </head>
  <body>
    <div id="root"></div>
  </body>
</html>`;

const read = (html: string): Document => new DOMParser().parseFromString(html, 'text/html');

describe('SEO pages', () => {
  it.each(SEO_LOCALES)('writes the head of %s in its own language', (locale) => {
    const page = SEO_PAGES[locale];
    const document = read(pageHtml(BUILT, locale));
    const content = (selector: string): string | null =>
      document.querySelector(selector)?.getAttribute('content') ?? null;

    expect(document.documentElement.lang).toBe(page.htmlLang);
    expect(document.title).toBe(page.title);
    expect(content('meta[name="description"]')).toBe(page.description);
    expect(content('meta[property="og:title"]')).toBe(page.title);
    expect(content('meta[property="og:description"]')).toBe(page.description);
    expect(content('meta[property="og:locale"]')).toBe(page.ogLocale);
    expect(content('meta[property="og:image"]')).toBe(`${SITE_URL}og/${locale}.jpg`);
    expect(document.querySelector('link[rel="canonical"]')?.getAttribute('href')).toBe(SITE_URL + page.folder);
  });

  it.each(SEO_LOCALES)('links %s to every language and to a default', (locale) => {
    const links = [...read(pageHtml(BUILT, locale)).querySelectorAll('link[rel="alternate"]')].map((link) => [
      link.getAttribute('hreflang'),
      link.getAttribute('href'),
    ]);

    expect(links).toEqual([
      ['en', SITE_URL],
      ['pt-BR', `${SITE_URL}pt-br/`],
      ['es', `${SITE_URL}es/`],
      ['zh-CN', `${SITE_URL}zh-cn/`],
      ['ja', `${SITE_URL}ja/`],
      ['x-default', SITE_URL],
    ]);
  });

  it('says what Safira is before the app starts', () => {
    const intro = read(pageHtml(BUILT, 'pt-br')).querySelector('#root .seo-intro');

    expect(intro?.querySelector('h1')?.textContent).toBe(SEO_PAGES['pt-br'].title);
    expect(intro?.querySelector('code')?.textContent).toBe('mostre "Olá, mundo!"');
    expect(intro?.querySelectorAll('nav a')).toHaveLength(5);
    expect(intro?.querySelector('p a')?.getAttribute('href')).toBe(`${SITE_URL}pt-br/about/`);
    expect(intro?.querySelector('p a')?.textContent).toBe('Sobre a Safira');
  });

  it('keeps the files of the English page beside it and reaches them from the folder of every other language', () => {
    expect(pageHtml(BUILT, 'en-us')).toContain('src="./assets/index.js"');
    expect(pageHtml(BUILT, 'ja')).toContain('src="../assets/index.js"');
    expect(pageHtml(BUILT, 'ja')).toContain('href="../assets/index.css"');
    expect(pageHtml(BUILT, 'ja')).toContain('href="../icone.png"');
    expect(pageHtml(BUILT, 'ja')).toContain('href="../apple-touch-icon.png"');
    expect(pageHtml(BUILT, 'ja')).not.toContain('"./');
  });

  it('escapes text that would break the HTML', () => {
    expect(pageHtml(BUILT, 'en-us')).toContain('<code>show &quot;Hello, world!&quot;</code>');
  });

  it('keeps titles short and descriptions the size search engines show', () => {
    for (const locale of ['en-us', 'pt-br', 'es'] as const) {
      expect(SEO_PAGES[locale].title.length).toBeLessThanOrEqual(65);
      expect(SEO_PAGES[locale].description.length).toBeGreaterThanOrEqual(140);
      expect(SEO_PAGES[locale].description.length).toBeLessThanOrEqual(165);
    }
  });

  it('lists every language in the sitemap, each with its alternates, and then the other pages', () => {
    const other = '  <url>\n    <loc>https://example.com/other/</loc>\n  </url>';
    const sitemap = new DOMParser().parseFromString(sitemapXml([other]), 'application/xml');
    const urls = [...sitemap.getElementsByTagName('loc')].map((loc) => loc.textContent);

    expect(urls).toEqual([
      ...SEO_LOCALES.map((locale) => SITE_URL + SEO_PAGES[locale].folder),
      'https://example.com/other/',
    ]);
    expect(sitemap.getElementsByTagName('xhtml:link')).toHaveLength(25);
  });
});
