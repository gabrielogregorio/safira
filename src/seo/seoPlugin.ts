import { readdirSync, readFileSync } from 'node:fs';
import { join } from 'node:path';
import type { Plugin } from 'vite';
import type { Locale } from '../language/messages.ts';
import { ABOUT_FOLDER, aboutHtml, aboutSitemapUrls } from './aboutPages.ts';
import { pageHtml, SEO_LOCALES, SEO_PAGES, sitemapXml } from './seoPages.ts';

// The build and the tests both run from the root of the repository.
const CONTENT = join(process.cwd(), 'src', 'content');

/** The titles of the lessons of one language, in their order, read from the lesson files. */
export const lessonTitles = (locale: Locale): string[] => {
  const folder = join(CONTENT, locale, 'lessons');

  return (
    readdirSync(folder)
      .filter((name) => name.endsWith('.md'))
      .sort((first, second) => first.localeCompare(second))
      // Every lesson starts with its title: "# Talk to me".
      .map((name) => readFileSync(join(folder, name), 'utf8').split('\n')[0].replace(/^# /, '').trim())
  );
};

/** After the build, index.html becomes the English page and each other language gets its folder, an about page and a sitemap. */
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
      const folder = SEO_PAGES[locale].folder;
      const html = pageHtml(built, locale);

      if (locale === 'en-us') {
        index.source = html;
      } else {
        this.emitFile({ type: 'asset', fileName: `${folder}index.html`, source: html });
      }

      this.emitFile({
        type: 'asset',
        fileName: `${folder}${ABOUT_FOLDER}index.html`,
        source: aboutHtml(locale, lessonTitles(locale)),
      });
    }

    this.emitFile({ type: 'asset', fileName: 'sitemap.xml', source: sitemapXml(aboutSitemapUrls()) });
  },
});
