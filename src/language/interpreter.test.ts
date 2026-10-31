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
