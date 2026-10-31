import type { Locale } from '@/language/messages';
import type { Lesson } from './lessons';
import { parseLesson } from './lessons';

const exampleModules = import.meta.glob<string>('./*/examples/*.safira', {
  eager: true,
  query: '?raw',
  import: 'default',
});
const lessonModules = import.meta.glob<string>('./*/lessons/*.md', { eager: true, query: '?raw', import: 'default' });

export interface ContentEntry {
  id: string;
  title: string;
  text: string;
}

const NAME_OF_FILE = /^.*\/|\.[a-z]+$/g;
const VERSION_LINE = '#safira';
const COMMENT = '#';

const readTitle = (text: string): string | undefined =>
  text
    .split('\n')
    .find((line) => line.startsWith(COMMENT) && !line.startsWith(VERSION_LINE))
    ?.slice(COMMENT.length)
    .trim();

const toId = (path: string): string => path.replace(NAME_OF_FILE, '');

const isFromLocale = (path: string, locale: Locale): boolean => path.startsWith(`./${locale}/`);

const toExample = ([path, text]: [string, string]): ContentEntry => ({
  id: toId(path),
  title: readTitle(text) ?? toId(path),
  text,
});

const byId = (first: { id: string }, second: { id: string }): number => first.id.localeCompare(second.id);

const pickByLocale = <Entry extends { id: string }>(
  modules: Record<string, string>,
  build: (entry: [string, string]) => Entry,
): ((locale: Locale) => Entry[]) => {
  const cache = new Map<Locale, Entry[]>();

  return (locale) => {
    const entries =
      cache.get(locale) ??
      Object.entries(modules)
        .filter(([path]) => isFromLocale(path, locale))
        .map(build)
        .sort(byId);
    cache.set(locale, entries);

    return entries;
  };
};

export const examplesOf = pickByLocale(exampleModules, toExample);

export const lessonsOf = pickByLocale<Lesson>(lessonModules, ([path, text]) => parseLesson(toId(path), text));

export const findExampleByPrefix = (locale: Locale, prefix: string): ContentEntry | undefined =>
  examplesOf(locale).find((example) => example.id.startsWith(`${prefix}-`));
