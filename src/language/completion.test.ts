import { STARTER_LINES, suggestCompletion } from './completion';
import { parse } from './parser';

const suggest = (before: string, document = before, after = '') => suggestCompletion(before, after, document, 'pt-br');

describe('suggestCompletion', () => {
  it('finishes a command for a beginner', () => {
    expect(suggest('mos')).toBe('tre "Olá!"');
    expect(suggest('rep')).toBe('ita 3 vezes {');
  });

  it('follows the language of the interface', () => {
    expect(suggestCompletion('sh', '', 'sh', 'en-us')).toBe('ow "Hello!"');
    expect(suggestCompletion('mu', '', 'mu', 'es')).toBe('estra "¡Hola!"');
    expect(suggestCompletion('显示', '', '显示', 'zh-cn')).toBe(' "你好!"');
    expect(suggestCompletion('表示', '', '表示', 'ja')).toBe(' 「こんにちは」');
  });

  it('keeps working with indentation', () => {
    expect(suggest('    mos')).toBe('tre "Olá!"');
  });

  it('completes phrases in the middle of a line', () => {
    expect(suggest('mostre "a" na c')).toBe('or');
  });

  it('ignores accents and capitals', () => {
    expect(suggest('MOS')).toBe('tre "Olá!"');
  });

  it('suggests names already used in the file', () => {
    expect(suggest('mostre tot', 'total = 1\nmostre tot')).toBe('al');
  });

  it('prefers the most used name', () => {
    expect(suggest('mostre tot', 'totem = 1\ntotal = 1\nmostre total\nmostre total\nmostre tot')).toBe('al');
  });

  it('waits for two letters', () => {
    expect(suggest('m')).toBeNull();
  });

  it('stays quiet inside a string', () => {
    expect(suggest('mostre "mos')).toBeNull();
  });

  it('stays quiet inside a comment', () => {
    expect(suggest('# mos')).toBeNull();
  });

  it('stays quiet in the middle of a word', () => {
    expect(suggest('mos', 'mostrei', 'trei')).toBeNull();
  });

  it('stays quiet after a space', () => {
    expect(suggest('mostre ')).toBeNull();
  });

  it('stays quiet when nothing matches', () => {
    expect(suggest('zzz')).toBeNull();
  });
});

describe('STARTER_LINES', () => {
  it.each(Object.values(STARTER_LINES).flat())('%s is valid Safira', (line) => {
    const complete = line.endsWith('{') ? `${line}\n}` : line;

    expect(parse(complete).map((statement) => statement.kind)).not.toContain('invalid');
  });
});

describe('suggestCompletion in imports', () => {
  const scripts = { 'here/main.safira': '', 'lib.safira': '' };
  const suggest = (before: string, after = ''): string | null => suggestCompletion(before, after, '', 'pt-br', scripts);

  it('offers a whole path right after the command', () => {
    expect(suggest('importe ')).toBe('"./here/main"');
  });

  it.each([
    ['importe "', './here/main"'],
    ['importe "./he', 're/main"'],
    ['importe "./here/ma', 'in"'],
    ['importe "./here/main', '.safira"'],
    ['importe "./here/main.saf', 'ira"'],
    ['importe li', 'b'],
    ['import "li', 'b"'],
  ])('completes %s', (before, expected) => {
    expect(suggest(before)).toBe(expected);
  });

  it('does not repeat a closing quote', () => {
    expect(suggest('importe "./li', '"')).toBe('b');
  });

  it('stops after the path is closed or unknown', () => {
    expect(suggest('importe "lib"')).toBeNull();
    expect(suggest('importe "./nada')).toBeNull();
  });
});

describe('suggestCompletion of functions', () => {
  const document = 'funcao soma recebe parametros a, b {\n}\nfuncao logo {\n}\n';
  const suggest = (before: string, after = '', source = document, scripts = {}): string | null =>
    suggestCompletion(before, after, source, 'pt-br', scripts);

  it('completes the name and shows the parameters', () => {
    expect(suggest('so')).toBe('ma(a, b)');
  });

  it('shows the parameters when the whole name is typed', () => {
    expect(suggest('soma')).toBe('(a, b)');
  });

  it('closes the call of a function without parameters', () => {
    expect(suggest('lo')).toBe('go()');
  });

  it('works inside an expression', () => {
    expect(suggest('x = so')).toBe('ma(a, b)');
  });

  it('adds nothing when the parentheses are already there', () => {
    expect(suggest('soma', '(1, 2)')).toBeNull();
  });

  it('does not suggest a call while declaring', () => {
    expect(suggest('funcao so')).not.toContain('(');
  });

  it('knows the functions of imported files, and only those', () => {
    const scripts = { 'here/lib.safira': 'funcao dobra recebe parametros n {\n}' };

    expect(suggest('do', '', 'importe "./here/lib"\n', scripts)).toBe('bra(n)');
    expect(suggest('do', '', '', scripts)).not.toContain('(');
  });
});
