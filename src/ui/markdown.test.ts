import { parseMarkdown } from './markdown';

describe('parseMarkdown', () => {
  it('reads headings, paragraphs and code', () => {
    expect(parseMarkdown('## Título\n**forte** texto\n\n```\nmostre 1\n\nmostre 2\n```')).toEqual([
      { kind: 'heading', level: 2, text: 'Título' },
      { kind: 'paragraph', text: 'forte texto' },
      { kind: 'code', text: 'mostre 1\n\nmostre 2' },
    ]);
  });

  it('does not read a comment inside code as a heading', () => {
    expect(parseMarkdown('```\n# nota\n```')).toEqual([{ kind: 'code', text: '# nota' }]);
  });
});
