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

describe('lines that do not parse', () => {
  const messageKeyOf = (source: string): unknown => (first(source) as { messageKey?: unknown }).messageKey;

  it.each([
    ['repita 2 vezes', 'a block that never comes'],
    ['mostre (1', 'a parenthesis left open'],
    ['funcao 1 { }', 'a number as a name'],
  ])('rejects %s, %s', (source) => {
    expect(messageKeyOf(source)).toBe('comando_desconhecido');
  });

  it.each(['senao se 1 == 1 { }', 'senao se 1 == 1 entao { }', 'senao { }'])('rejects %s without an if', (source) => {
    expect(messageKeyOf(source)).toBe('precisa_def_p_cond_senao');
  });

  it('leaves "senao der erro" after an if for the try that is missing', () => {
    expect(parse('se 1 == 1 { } senao der erro { }').map((statement) => statement.kind)).toEqual(['if', 'invalid']);
  });

  it.each(['importe', 'toque'])('reads a lonely %s as a name', (word) => {
    expect(first(word)).toMatchObject({ kind: 'expression', value: { kind: 'variable', name: word } });
  });

  it('lets a failure that is not about the syntax go through', () => {
    expect(() => parse('('.repeat(5_000))).toThrow(RangeError);
  });
});

describe('keys', () => {
  const condition = (line: string) =>
    (first(`${line} {\n}`) as { branches: { condition: unknown }[] }).branches[0].condition;

  it.each([
    ['se o usuario apertar pra cima', 'press', 'pra cima'],
    ['se apertar ArrowUp', 'press', 'ArrowUp'],
    ['se apertar Cima', 'press', 'Cima'],
    ['se pressionar Enter', 'press', 'Enter'],
    ['se segurar Enter', 'hold', 'Enter'],
    ['se soltar a tecla Enter', 'release', 'Enter'],
    ['ao soltar tecla Enter', 'release', 'Enter'],
    ['ao apertar Enter', 'press', 'Enter'],
    ['if press Up', 'press', 'Up'],
    ['if the user holds Up', 'hold', 'Up'],
    ['on release Enter', 'release', 'Enter'],
    ['si presiona arriba', 'press', 'arriba'],
    ['如果 按下 上', 'press', '上'],
    ['もし 押した 上', 'press', '上'],
  ])('reads %s', (line, mode, text) => {
    expect(condition(line)).toEqual({ kind: 'keyState', mode, parts: [{ kind: 'name', text }] });
  });

  it('reads a combination', () => {
    expect(condition('se apertar Shift+Enter')).toMatchObject({
      parts: [
        { kind: 'name', text: 'Shift' },
        { kind: 'name', text: 'Enter' },
      ],
    });
  });

  it('reads a text and a variable as the key', () => {
    expect(condition('se apertar "a"')).toMatchObject({ parts: [{ kind: 'value' }] });
    expect(condition('se apertar tecla')).toMatchObject({
      parts: [{ kind: 'value', value: { kind: 'variable', name: 'tecla' } }],
    });
  });

  it('joins with other conditions', () => {
    expect(condition('se apertar E e vida > 0 entao')).toMatchObject({
      kind: 'binary',
      left: { kind: 'keyState' },
    });
  });

  it.each(['se hold for maior que 2 entao', 'se hold > 2', 'se press', 'se hold entao'])(
    'keeps a variable called like a key word in %s',
    (line) => {
      expect(first(`${line} {\n}`)).toMatchObject({ kind: 'if' });
    },
  );

  it('leaves a variable alone when the line is not a condition', () => {
    expect(first('wait hold seconds')).toMatchObject({ kind: 'wait', amount: { kind: 'variable', name: 'hold' } });
  });

  it('still reads ao as a name', () => {
    expect(first('ao = 1')).toMatchObject({ kind: 'assign', name: 'ao' });
  });
});

describe('repeating forever', () => {
  it.each([
    'repita pra sempre',
    'repita para sempre',
    'repita sempre',
    'repetir para sempre',
    'repita infinitamente',
    'pra sempre',
    'para sempre',
    'repeat forever',
    'loop forever',
    'forever',
    'repetir para siempre',
    'para siempre',
    '永远重复',
    'ずっと繰り返す',
  ])('reads %s', (line) => {
    expect(first(`${line} {\n}`)).toMatchObject({ kind: 'while', condition: { kind: 'literal', value: true } });
  });

  it('accepts a command on the same line', () => {
    expect(first('repita pra sempre pare')).toMatchObject({ kind: 'while', body: [{ kind: 'break' }] });
  });

  it('keeps a loop with a number of times', () => {
    expect(first('repita 2 vezes {\n}')).toMatchObject({ kind: 'repeat' });
  });

  it('keeps para cada working', () => {
    expect(first('para cada x de 1 ate 2 {\n}')).toMatchObject({ kind: 'forRange' });
  });

  it('keeps a variable called sempre', () => {
    expect(first('sempre = 1')).toMatchObject({ kind: 'assign', name: 'sempre' });
  });
});

describe('doing nothing', () => {
  it.each([
    'não faça nada',
    'nao faca nada',
    'não fazer nada',
    'não faz nada',
    'do nothing',
    'no hagas nada',
    'no hacer nada',
    '什么都不做',
    '何もしない',
  ])('reads %s', (line) => {
    expect(first(line)).toMatchObject({ kind: 'noop' });
  });

  it('works as the only command of a condition', () => {
    expect(first('se 1 == 1 entao não faça nada senao mostre "x"')).toMatchObject({
      kind: 'if',
      branches: [{ body: [{ kind: 'noop' }] }],
      otherwise: [{ kind: 'print' }],
    });
  });

  it('leaves a variable called nada alone', () => {
    expect(first('nada = 1')).toMatchObject({ kind: 'assign', name: 'nada' });
  });
});

describe('saving the answer', () => {
  it.each([
    'guarde a resposta em nota',
    'guarde a resposta na nota',
    'guarde a resposta no nota',
    'guardar a resposta em nota',
    'guarda a resposta em nota',
    'guarde resposta em nota',
    'guarde a resposta na variavel nota',
    'guarde a resposta na variável nota',
    'guarde a resposta do usuario em nota',
    'guarde a resposta do usuário em nota',
    'guarde o que o usuario digitar em nota',
    'guarde o que for digitado em nota',
    'salve a resposta em nota',
    'salvar a resposta em nota',
    'armazene a resposta em nota',
    'coloque a resposta em nota',
    'anote a resposta em nota',
    'save the answer in nota',
    'store the answer in nota',
    'keep the answer in nota',
    'save the answer to nota',
    'save the answer as nota',
    'save the answer in the variable nota',
    'save the response in nota',
    'save answer in nota',
    'save what the user types in nota',
    'put the answer into nota',
    'guarda la respuesta en nota',
    'guarda la respuesta en la nota',
    'guardar la respuesta en nota',
    'guarda lo que escribe el usuario en nota',
    '保存回答到 nota',
    '保存答案到 nota',
    '回答を保存 nota',
    '回答を保存する nota',
  ])('reads %s', (line) => {
    expect(first(line)).toMatchObject({
      kind: 'assign',
      name: 'nota',
      value: { kind: 'input', numeric: false, variableName: null },
    });
  });

  it('needs the name of a variable', () => {
    expect(first('guarde a resposta em')).toMatchObject({ kind: 'invalid' });
  });

  it.each(['guarde', 'salve', 'save', 'store', 'keep', 'put', 'anote', 'coloque'])(
    'leaves a variable called %s alone',
    (word) => {
      expect(first(`${word} = 1`)).toMatchObject({ kind: 'assign', name: word });
    },
  );
});

describe('lists', () => {
  it('sets a position with the word that gives a value', () => {
    expect(first('lista x na posicao 1 recebe 5')).toMatchObject({ kind: 'listSet', name: 'x' });
  });

  it('reads a list alone in a line as a value', () => {
    expect(first('lista x')).toMatchObject({ kind: 'expression', value: { kind: 'listValue', name: 'x' } });
  });

  it('rejects a position without a value', () => {
    expect(first('lista x na posicao 1 5')).toMatchObject({ kind: 'invalid' });
  });
});

describe('expressions', () => {
  it('ignores a plus sign before a value', () => {
    expect(first('x = +1')).toMatchObject({ value: { kind: 'literal', value: 1 } });
  });

  it('reads the spanish question about a file', () => {
    expect(first('x = existe el archivo "a"')).toMatchObject({
      value: { kind: 'fileExists', path: { value: 'a' }, negated: false },
    });
  });
});
