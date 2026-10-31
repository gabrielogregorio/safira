import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { LessonMarkdown, toSlug } from './LessonMarkdown';

const setup = (text: string) => {
  const onOpenCode = vi.fn();
  render(<LessonMarkdown lessonId="aula-01" text={text} onOpenCode={onOpenCode} />);

  return onOpenCode;
};

describe('LessonMarkdown', () => {
  it('renders the usual markdown', () => {
    setup('Texto **forte** e *leve*\n\n- item');

    expect(screen.getByText('forte').tagName).toBe('STRONG');
    expect(screen.getByText('leve').tagName).toBe('EM');
    expect(screen.getByRole('listitem')).toHaveTextContent('item');
  });

  it('renders tables', () => {
    setup('| a |\n|---|\n| b |');

    expect(screen.getByRole('table')).toBeInTheDocument();
  });

  it('gives each section a link', () => {
    setup('## Comando de exibição');

    expect(screen.getByRole('link', { name: /Link to this section/ })).toHaveAttribute(
      'href',
      '#/lessons/aula-01/comando-de-exibicao',
    );
    expect(screen.getByRole('heading', { level: 2 })).toHaveAttribute('id', 'comando-de-exibicao');
  });

  it('colors the code', () => {
    setup('```\nmostre 1\n```');

    expect(screen.getByText('mostre')).toHaveClass('syntax-exibicao');
  });

  it('opens the example in the IDE', async () => {
    const onOpenCode = setup('```\nmostre 1\n```');
    await userEvent.click(screen.getByRole('button', { name: 'Open in the IDE' }));

    expect(onOpenCode).toHaveBeenCalledWith('mostre 1');
  });

  it('opens external links in a new tab', () => {
    setup('[site](https://example.com)');

    expect(screen.getByRole('link', { name: 'site' })).toHaveAttribute('target', '_blank');
  });

  it('does not run HTML from the text', () => {
    setup('<img src=x onerror=alert(1)>');

    expect(document.querySelector('img')).toBeNull();
  });

  it('builds slugs without accents', () => {
    expect(toSlug('  Posição & Ação! ')).toBe('posicao-acao');
  });
});
