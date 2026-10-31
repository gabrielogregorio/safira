import { runScript } from './testHarness';

describe('behavior fixed from the legacy interpreter', () => {
  it('keeps a line break in the printed text', async () => {
    expect((await runScript('mostre "a\\nb"')).texts).toEqual(['a\nb']);
  });

  it('allows parentheses in a condition', async () => {
    expect((await runScript('x = 5\nse (x > 9 ou x < 6) e x == 5 { mostre "c" }')).texts).toEqual(['c']);
  });

  it('allows a function to call itself', async () => {
    const source = 'funcao f recebe n {\nse n == 0 { retorne 0 }\nretorne f(n - 1) + 1\n}\nmostre f(3)';

    expect((await runScript(source)).texts).toEqual(['3']);
  });

  it('runs commands separated by a semicolon and keeps it inside strings', async () => {
    expect((await runScript('mostre "a;b"; mostre "c"')).texts).toEqual(['a;b', 'c']);
  });

  it('runs senao after a condition that was false, even if an earlier one was true', async () => {
    expect((await runScript('se 1 == 1 { mostre "a" }\nse 1 == 2 { } senao { mostre "b" }')).texts).toEqual(['a', 'b']);
  });

  it('replaces the text in a variable', async () => {
    expect((await runScript('t = "banana"\nsubstitua "a" por "o" na variavel t\nmostre t')).texts).toEqual(['bonono']);
  });

  it('reports a division by zero with its own message', async () => {
    expect((await runScript('mostre 1 / 0')).error?.message).toBe('Não é possível dividir por zero');
  });

  it('prints whole numbers without a decimal part', async () => {
    expect((await runScript('mostre 1 + 2')).texts).toEqual(['3']);
  });
});

describe('errors', () => {
  it('stops at the failing line and keeps what was already printed', async () => {
    const result = await runScript('mostre "a"\n\nmostre nada\nmostre "b"');

    expect(result.texts).toEqual(['a']);
    expect(result.error?.message).toBe("Você precisa definir a variável  'nada'");
    expect(result.error?.line).toBe(3);
    expect(result.error?.file).toBe('main.safira');
  });

  it('points to the example of the failing command', async () => {
    expect((await runScript('incremente 1 em nada')).error?.example).toBe('09');
  });

  it('stops a recursion that never ends', async () => {
    expect((await runScript('funcao f { f() }\nf()')).error?.message).toBe('A função chamou a si mesma vezes demais');
  });

  it('rejects a format with the wrong number of values', async () => {
    expect((await runScript('mostre "% %" inserindo 1')).error?.message).toBe(
      'O texto tem 2 marcadores %, mas foram informados 1 valores',
    );
  });

  it('does not run python code', async () => {
    expect((await runScript('x = __import__("os").getcwd()')).error?.message).toContain('Um comando desconhecido');
  });
});

describe('virtual files', () => {
  it('reads a file that came with the project', async () => {
    expect((await runScript('mostre leia o arquivo "dados.txt"', [], { 'dados.txt': 'oi' })).texts).toEqual(['oi']);
  });

  it('imports another virtual file', async () => {
    expect((await runScript('importe lib\nmostre v', [], { 'lib.safira': 'v = 7' })).texts).toEqual(['7']);
  });

  it('keeps what the program saved', async () => {
    const result = await runScript('crie o arquivo "a.txt"\nadicione "oi" no arquivo "a.txt"');

    expect(result.files.read('a.txt')).toBe('oi');
  });

  it('reports the line of the imported file', async () => {
    const result = await runScript('importe lib', [], { 'lib.safira': '\nmostre nada' });

    expect(result.error).toMatchObject({ file: 'lib.safira', line: 2 });
  });

  it('ignores the hidden version line of an imported file', async () => {
    expect((await runScript('importe lib\nmostre v', [], { 'lib.safira': '#safira 1.0\nv = 1' })).texts).toEqual(['1']);
  });
});

describe('waiting', () => {
  it.each([
    ['espere 2 segundos', 2000],
    ['espere 500 milisegundos', 500],
    ['wait 1 ms', 1],
  ])('%s waits the right time', async (source, milliseconds) => {
    expect((await runScript(source)).sleeps).toEqual([milliseconds]);
  });
});

describe('commands on the same line as a condition', () => {
  const greet = 'nome = o que o usuario digitar\nse nome for igual a "gabriel" entao mostre na tela "obaaaaaa"';

  it('runs the command when the condition is true', async () => {
    expect((await runScript(greet, ['gabriel'])).texts).toEqual(['obaaaaaa']);
  });

  it('skips the command when the condition is false', async () => {
    expect((await runScript(greet, ['ana'])).texts).toEqual([]);
  });

  it.each([
    ['se 1 == 2 entao mostre "a" senao mostre "b"', ['b']],
    ['se 1 == 1 entao mostre "a" senao mostre "b"', ['a']],
    ['se 1 == 2 mostre "a"\nsenao mostre "b"', ['b']],
    ['se 1 == 2 entao mostre "a"\nsenao se 2 == 2 entao mostre "b"\nsenao mostre "c"', ['b']],
    ['se 1 == 1 entao se 2 == 3 entao mostre "a" senao mostre "b"', ['b']],
    ['if 1 == 1 then show "a"', ['a']],
    ['si 1 == 1 entonces muestra "a"', ['a']],
    ['repita 2 vezes mostre "a"', ['a', 'a']],
    ['para cada i de 1 ate 2 mostre i', ['1', '2']],
    ['x = 0\nenquanto x < 2 entao x = x + 1\nmostre x', ['2']],
  ])('%s', async (source, expected) => {
    expect((await runScript(source)).texts).toEqual(expected);
  });

  it('keeps running the next line after the inline command', async () => {
    expect((await runScript('se 1 == 1 entao mostre "a"\nmostre "b"')).texts).toEqual(['a', 'b']);
  });

  it('stops a loop from an inline break', async () => {
    expect((await runScript('repita 5 vezes {\nmostre "a"\nse 1 == 1 entao pare\n}')).texts).toEqual(['a']);
  });

  it('reports an unknown inline command when it runs', async () => {
    expect((await runScript('se 1 == 1 entao nada nada')).error?.message).toContain('Um comando desconhecido');
  });
});
