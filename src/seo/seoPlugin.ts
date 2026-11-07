import type { Plugin } from 'vite';
import { pageHtml, SEO_LOCALES, SEO_PAGES, sitemapXml } from './seoPages.ts';

/** After the build, index.html becomes the English page and each other language gets its folder and a sitemap. */
export const seoPages = (): Plugin => ({
  name: 'safira-seo-pages',
  apply: 'build',
  // After Vite's own HTML plugin, which is the one that puts index.html in the bundle.
  enforce: 'post',
  generateBundle(_options, bundle) {
    const index = bundle['index.html'];

    if (index?.type !== 'asset' || typeof index.source !== 'string') {
      throw new Error('index.html is missing from the build');
    }

    const built = index.source;

    for (const locale of SEO_LOCALES) {
      const html = pageHtml(built, locale);

      if (locale === 'en-us') {
        index.source = html;
      } else {
        this.emitFile({ type: 'asset', fileName: `${SEO_PAGES[locale].folder}index.html`, source: html });
      }
    }

    this.emitFile({ type: 'asset', fileName: 'sitemap.xml', source: sitemapXml() });
  },
});
