import { removeAccents, tokenize } from './tokenizer';

const kinds = (source: string): string[] => tokenize(source).tokens.map((token) => token.kind);
const texts = (source: string): string[] => tokenize(source).tokens.map((token) => token.text);

describe('tokenize', () => {
  it('splits words, numbers, strings and symbols', () => {
    expect(texts('mostre "oi" + 1.5')).toEqual(['mostre', '"oi"', '+', '1.5', '']);
    expect(kinds('mostre "oi" + 1.5')).toEqual(['word', 'string', 'symbol', 'number', 'end']);
  });

  it('keeps two character symbols together', () => {
    expect(texts('a ** b <= c')).toEqual(['a', '**', 'b', '<=', 'c', '']);
  });

  it('treats a semicolon as a statement separator outside of strings', () => {
    expect(kinds('a;b')).toEqual(['word', 'newline', 'word', 'end']);
    expect(texts('"a;b"')).toEqual(['"a;b"', '']);
  });

  it.each(['# nota', '// nota'])('ignores the comment %s', (comment) => {
    const result = tokenize(`mostre 1 ${comment}`);

    expect(result.tokens.map((token) => token.text)).toEqual(['mostre', '1', '']);
    expect(result.comments).toEqual([{ start: 9, end: 9 + comment.length }]);
  });

  it('keeps comment markers that are inside strings', () => {
    expect(texts('"a # b // c"')).toEqual(['"a # b // c"', '']);
  });

  it('tracks the line of each token', () => {
    expect(tokenize('a\n\nb').tokens.map((token) => token.line)).toEqual([1, 1, 2, 3, 3]);
  });

  it('flags a string that never closes', () => {
    expect(tokenize('"abc\nmostre').tokens[0]).toMatchObject({ text: '"abc', terminated: false });
  });

  it('reads a word that starts with a digit as a word', () => {
    expect(kinds('3d')).toEqual(['word', 'end']);
  });

  it('normalizes accents for phrase matching but preserves the text', () => {
    expect(tokenize('função').tokens[0]).toMatchObject({ text: 'função', normalized: 'funcao' });
    expect(removeAccents('posição')).toBe('posicao');
  });
});
