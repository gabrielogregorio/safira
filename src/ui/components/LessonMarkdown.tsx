import type { ComponentProps, ReactElement, ReactNode } from 'react';
import { Children, isValidElement } from 'react';
import Markdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { useTranslation } from '@/i18n/i18n';
import { SafiraCode } from './SafiraCode';

interface LessonMarkdownProps {
  sectionHref: (section: string) => string;
  text: string;
  onOpenCode: (code: string) => void;
}

const COMBINING_MARKS = /\p{M}/gu;
const NOT_SLUG_CHARACTER = /[^a-z0-9]+/g;
const REMARK_PLUGINS = [remarkGfm];

export const toSlug = (text: string): string =>
  text
    .normalize('NFD')
    .replace(COMBINING_MARKS, '')
    .toLowerCase()
    .replace(NOT_SLUG_CHARACTER, '-')
    .replace(/^-|-$/g, '');

const readText = (node: ReactNode): string =>
  Children.toArray(node)
    .map((child) => {
      if (isValidElement(child)) {
        return readText((child as ReactElement<{ children?: ReactNode }>).props.children);
      }

      return typeof child === 'string' ? child : '';
    })
    .join('');

const trimFinalLineBreak = (text: string): string => text.replace(/\n$/, '');

export const LessonMarkdown = ({ sectionHref, text, onOpenCode }: LessonMarkdownProps) => {
  const t = useTranslation();

  const Heading = ({ children }: ComponentProps<'h2'>) => {
    const section = toSlug(readText(children));

    return (
      <h2 id={section}>
        {children}
        <a
          className="heading-link"
          href={sectionHref(section)}
          aria-label={`${t('Link to this section')}: ${readText(children)}`}>
          #
        </a>
      </h2>
    );
  };

  const CodeBlock = ({ children }: ComponentProps<'pre'>) => {
    const code = trimFinalLineBreak(readText(children));

    return (
      <figure className="lesson-code">
        <pre>
          <SafiraCode code={code} />
        </pre>
        <button
          type="button"
          className="button"
          data-translated
          data-sound="open"
          onClick={() => {
            onOpenCode(code);
          }}>
          {t('Open in the IDE')}
        </button>
      </figure>
    );
  };

  const Link = ({ href, children }: ComponentProps<'a'>) => (
    <a href={href} target={href?.startsWith('#') === true ? undefined : '_blank'} rel="noreferrer">
      {children}
    </a>
  );

  return (
    <div data-fixed-text>
      <Markdown remarkPlugins={REMARK_PLUGINS} components={{ h2: Heading, pre: CodeBlock, a: Link }}>
        {text}
      </Markdown>
    </div>
  );
};
