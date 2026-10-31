import type { Statement } from './ast';
import { parse } from './parser';

const first = (source: string): Statement => parse(source)[0];

describe('parse', () => {
  it('records the line of each statement', () => {
    expect(parse('mostre 1\n\nmostre 2').map((statement) => statement.line)).toEqual([1, 3]);
  });

  it('turns an unknown line into an invalid statement so that it only fails when it runs', () => {
    expect(first('isso nao existe')).toMatchObject({
      kind: 'invalid',
      messageKey: 'comando_desconhecido',
      detail: "'isso nao existe'",
    });
  });

  it('keeps parsing after an invalid line', () => {
    expect(parse('isso nao\nmostre 1').map((statement) => statement.kind)).toEqual(['invalid', 'print']);
  });

  it('accepts accents in commands', () => {
    expect(first('função f { mostre 1 }').kind).toBe('functionDeclaration');
    expect(parse('se 1 == 1 { } senão { }')).toHaveLength(1);
  });

  it.each([
    ['se 1 == 1 { }', 'if'],
    ['if 1 == 1 { }', 'if'],
    ['si 1 == 1 { }', 'if'],
    ['mostre 1', 'print'],
    ['show 1', 'print'],
    ['muestra 1', 'print'],
    ['repita 2 vezes { }', 'repeat'],
    ['repeat 2 veces { }', 'repeat'],
  ])('reads %s in any language', (source, kind) => {
    expect(first(source).kind).toBe(kind);
  });

  it('attaches else if and else branches to the same statement', () => {
    expect(first('se 1 == 1 {\n}\nsenao se 2 == 2 {\n}\nsenao {\n}')).toMatchObject({
      kind: 'if',
      branches: [{}, {}],
      otherwise: [],
    });
  });

  it('collects the clauses of tente', () => {
    expect(first('tente { } se der erro { } senao der erro { } em qualquer caso { }')).toMatchObject({
      kind: 'try',
      onError: [],
      onSuccess: [],
      always: [],
    });
  });

  it('reports a block that never closes', () => {
    expect(first('repita 2 vezes {\nmostre 1')).toMatchObject({
      kind: 'repeat',
      body: [{ kind: 'print' }, { kind: 'invalid', messageKey: 'nao_fechou_chave' }],
    });
  });

  it('reports a closing brace without a block', () => {
    expect(first('}')).toMatchObject({ kind: 'invalid', messageKey: 'nao_abriu_chave' });
  });

  it('reports a string that never closes as an invalid line', () => {
    expect(first('mostre "abc').kind).toBe('invalid');
  });

  it('gives multiplication priority over addition', () => {
    expect(first('x = 1 + 2 * 3')).toMatchObject({
      value: { operator: 'add', right: { operator: 'multiply' } },
    });
  });

  it('skips an invalid line that opens a block', () => {
    expect(parse('nada nada {\nmostre 1\n}\nmostre 2').map((statement) => statement.kind)).toEqual([
      'invalid',
      'print',
    ]);
  });
});
