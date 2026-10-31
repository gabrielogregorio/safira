import { highlightCode } from './highlight';

const categories = (code: string): [string, string][] =>
  highlightCode(code).map(({ start, end, category }) => [code.slice(start, end), category]);

describe('highlightCode', () => {
  it('colors commands, strings and numbers', () => {
    expect(categories('mostre "oi"')).toEqual([
      ['mostre', 'exibicao'],
      ['"oi"', 'string'],
    ]);
    expect(categories('x = 1')).toEqual([
      ['=', 'atribuicao'],
      ['1', 'numerico'],
    ]);
  });

  it('colors a color code as a value, not as a comment', () => {
    expect(categories('mostre "a" na cor #331')).toContainEqual(['#331', 'string']);
  });

  it('colors a phrase of several words as a single range', () => {
    expect(categories('idade for maior que 3')).toEqual([
      ['for maior que', 'logico'],
      ['3', 'numerico'],
    ]);
  });

  it('colors commands of any language', () => {
    expect(categories('muestra 1')[0]).toEqual(['muestra', 'exibicao']);
    expect(categories('show 1')[0]).toEqual(['show', 'exibicao']);
  });

  it('colors comments and does not color what is inside them', () => {
    expect(categories('# mostre')).toEqual([['# mostre', 'comentario']]);
  });

  it('leaves names without color', () => {
    expect(categories('nome_qualquer')).toEqual([]);
  });
});
