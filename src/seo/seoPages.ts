import type { Locale } from '../language/messages.ts';

/** Search engines and link previews need full addresses: previews point to the site too, so only it gets listed. */
export const SITE_URL = 'https://gabrielogregorio.github.io/safira/';

interface SeoPage {
  folder: string;
  htmlLang: string;
  ogLocale: string;
  title: string;
  description: string;
  example: string;
  label: string;
  about: string;
}

// Each page is read before the app runs: by a search engine, or by a chat app building a link preview.
export const SEO_PAGES: Record<Locale, SeoPage> = {
  'en-us': {
    folder: '',
    htmlLang: 'en',
    ogLocale: 'en_US',
    title: 'Safira: a programming language in plain words for beginners',
    description:
      'Learn to code from zero with Safira: a free programming language in plain words, in the browser and on the phone, with no install, no account and 14 short lessons.',
    example: 'show "Hello, world!"',
    label: 'English',
    about: 'About Safira',
  },
  'pt-br': {
    folder: 'pt-br/',
    htmlLang: 'pt-BR',
    ogLocale: 'pt_BR',
    title: 'Safira: linguagem de programação em português para iniciantes',
    description:
      'Aprenda lógica de programação do zero com a Safira: linguagem em português, grátis, no navegador e no celular, sem instalar, sem conta e com 14 aulas curtas.',
    example: 'mostre "Olá, mundo!"',
    label: 'Português (Brasil)',
    about: 'Sobre a Safira',
  },
  es: {
    folder: 'es/',
    htmlLang: 'es',
    ogLocale: 'es_ES',
    title: 'Safira: lenguaje de programación en español para principiantes',
    description:
      'Aprende a programar desde cero con Safira: un lenguaje en español, gratis, en el navegador y en el móvil, sin instalar nada, sin cuenta y con 14 lecciones cortas.',
    example: 'muestra "¡Hola, mundo!"',
    label: 'Español',
    about: 'Sobre Safira',
  },
  'zh-cn': {
    folder: 'zh-cn/',
    htmlLang: 'zh-CN',
    ogLocale: 'zh_CN',
    title: 'Safira：面向初学者的中文编程语言',
    description:
      '用 Safira 从零开始学编程：免费的中文编程语言，直接在浏览器和手机上运行，无需安装，无需注册，附带 14 节简短课程。',
    example: '显示 "你好，世界！"',
    label: '简体中文',
    about: '关于 Safira',
  },
  ja: {
    folder: 'ja/',
    htmlLang: 'ja',
    ogLocale: 'ja_JP',
    title: 'Safira：初心者のための日本語プログラミング言語',
    description:
      'Safira でゼロからプログラミングを学ぼう。日本語で書ける無料のプログラミング言語で、ブラウザやスマホでそのまま動き、インストールも登録も不要。14 の短いレッスン付き。',
    example: '表示 "こんにちは、世界！"',
    label: '日本語',
    about: 'Safira について',
  },
};

export const SEO_LOCALES = Object.keys(SEO_PAGES) as Locale[];

const pageUrl = (locale: Locale): string => SITE_URL + SEO_PAGES[locale].folder;

const escapeHtml = (text: string): string =>
  text.replaceAll('&', '&amp;').replaceAll('"', '&quot;').replaceAll('<', '&lt;').replaceAll('>', '&gt;');

const alternateLinks = (): string =>
  [
    ...SEO_LOCALES.map(
      (locale) => `<link rel="alternate" hreflang="${SEO_PAGES[locale].htmlLang}" href="${pageUrl(locale)}" />`,
    ),
    `<link rel="alternate" hreflang="x-default" href="${pageUrl('en-us')}" />`,
  ].join('\n    ');

const headTags = (locale: Locale): string => {
  const page = SEO_PAGES[locale];
  const title = escapeHtml(page.title);
  const description = escapeHtml(page.description);

  return `<link rel="canonical" href="${pageUrl(locale)}" />
    ${alternateLinks()}
    <meta property="og:type" content="website" />
    <meta property="og:site_name" content="Safira" />
    <meta property="og:url" content="${pageUrl(locale)}" />
    <meta property="og:title" content="${title}" />
    <meta property="og:description" content="${description}" />
    <meta property="og:image" content="${SITE_URL}og/${locale}.jpg" />
    <meta property="og:image:alt" content="${title}" />
    <meta property="og:image:width" content="1200" />
    <meta property="og:image:height" content="630" />
    <meta property="og:locale" content="${page.ogLocale}" />
    <meta name="twitter:card" content="summary_large_image" />
  </head>`;
};

// The app replaces this when it starts: until then, and for readers that do not run scripts, it says what Safira is.
const introduction = (locale: Locale): string => {
  const page = SEO_PAGES[locale];
  const languages = SEO_LOCALES.map(
    (other) => `<a href="${pageUrl(other)}" hreflang="${SEO_PAGES[other].htmlLang}">${SEO_PAGES[other].label}</a>`,
  ).join(' · ');

  return `<div id="root"><main class="seo-intro">
      <h1>${escapeHtml(page.title)}</h1>
      <p>${escapeHtml(page.description)}</p>
      <pre><code>${escapeHtml(page.example)}</code></pre>
      <p><a href="${pageUrl(locale)}about/">${escapeHtml(page.about)}</a></p>
      <nav>${languages}</nav>
    </main></div>`;
};

/** Turns the built index.html into the page of one language, in its own folder. */
export const pageHtml = (html: string, locale: Locale): string => {
  const page = SEO_PAGES[locale];
  const inFolder = page.folder === '' ? html : html.replaceAll(/(src|href)="\.\//g, '$1="../');

  return inFolder
    .replace('<html lang="en">', `<html lang="${page.htmlLang}">`)
    .replace(/<title>[^<]*<\/title>/, `<title>${escapeHtml(page.title)}</title>`)
    .replace(
      /<meta name="description" content="[^"]*" \/>/,
      `<meta name="description" content="${escapeHtml(page.description)}" />`,
    )
    .replace('</head>', headTags(locale))
    .replace('<div id="root"></div>', introduction(locale));
};

/** Each page of the app in every language, plus the other pages the build adds. */
export const sitemapXml = (otherUrls: string[]): string => {
  const alternates = SEO_LOCALES.map(
    (locale) => `    <xhtml:link rel="alternate" hreflang="${SEO_PAGES[locale].htmlLang}" href="${pageUrl(locale)}" />`,
  ).join('\n');
  const urls = SEO_LOCALES.map((locale) => `  <url>\n    <loc>${pageUrl(locale)}</loc>\n${alternates}\n  </url>`);

  return `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">
${[...urls, ...otherUrls].join('\n')}
</urlset>
`;
};
