import { Interpreter } from './interpreter';
import { noteFrequency } from './notes';
import { runScript } from './testHarness';
import { VirtualFileSystem } from './virtualFileSystem';

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

  it.each(['here/main', 'here/main.safira', './here/main', './here/main.safira'])(
    'imports "%s", with quotes',
    async (path) => {
      const result = await runScript(`importe "${path}"\nmostre v`, [], { 'here/main.safira': 'v = 7' });

      expect(result.texts).toEqual(['7']);
    },
  );

  it('imports beside the file that is importing, and from the root', async () => {
    const files = {
      'a/um.safira': 'importe "./dois"\nimporte "../raiz"',
      'a/dois.safira': 'x = 2',
      'raiz.safira': 'y = 3',
    };

    expect((await runScript('importe "a/um"\nmostre x + y', [], files)).texts).toEqual(['5']);
  });

  it('names the missing file with its extension once', async () => {
    const { error } = await runScript('importe "./nada.safira"');

    expect(error?.message).toContain('nada.safira');
    expect(error?.message).not.toContain('.safira.safira');
  });

  it('reports the line of the imported file', async () => {
    const result = await runScript('importe lib', [], { 'lib.safira': '\nmostre nada' });

    expect(result.error).toMatchObject({ file: 'lib.safira', line: 2 });
  });

  it('ignores the hidden version line of an imported file', async () => {
    expect((await runScript('importe lib\nmostre v', [], { 'lib.safira': '#safira 0.9\nv = 1' })).texts).toEqual(['1']);
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

describe('leaving a loop', () => {
  it.each([
    ['while', 'enquanto 1 == 1 { retorne "x" }'],
    ['repeat', 'repita 3 vezes { retorne "x" }'],
    ['for range', 'para cada i de 1 ate 3 { retorne "x" }'],
    ['for each', 'lista de l = 1, 2\npercorra a lista de lista l atribuindo cada valor em i { retorne "x" }'],
  ])('returns from a function inside a %s', async (_name, loop) => {
    expect((await runScript(`funcao f {\n${loop}\n}\nmostre f()`)).texts).toEqual(['x']);
  });

  it('ends a for each with a break', async () => {
    const source = 'percorra a lista de "abc" atribuindo cada valor em letra {\nmostre letra\npare\n}\nmostre "fim"';

    expect((await runScript(source)).texts).toEqual(['a', 'fim']);
  });
});

describe('return and print without a value', () => {
  it('returns an empty text', async () => {
    expect((await runScript('funcao f { retorne }\nmostre "[" + f() + "]"')).texts).toEqual(['[]']);
  });

  it('prints an empty line', async () => {
    expect((await runScript('mostre')).texts).toEqual(['']);
  });
});

describe('errors of commands', () => {
  it.each([
    ['percorra a lista de 5 atribuindo cada valor em x { }', "A variável '5' não é numérica!"],
    ['repita "a" vezes { }', "A variável 'a' não é numérica!"],
    ['espere "a" segundos', 'O tempo de espera precisa ser um número'],
    ['toque C por "a" segundos', 'O tempo de espera precisa ser um número'],
    ['crie o arquivo ""', 'Você precisa informar o nome de um arquivo'],
    ['adicione "x" no arquivo "nada.txt"', "O arquivo 'nada.txt' não existe!"],
    ['x = 1\nincremente "a" em x', "A variável 'a' não é numérica!"],
    [
      'x = 1\nsubstitua "a" por "b" na variavel x',
      'Para usar o recurso substituição, é necessário informar uma variável string',
    ],
    ['mostre "a" - 1', 'Não foi possivel realizar a conta  |a|'],
    ['mostre "a" > 1', 'Não foi possível realizar a condição:  |a 1|'],
    ['lista de l = 1\nmostre lista l > 1', 'Não foi possível realizar a condição:  |[1] 1|'],
    ['mostre 5 formatando 1', 'O comando inserindo precisa de um texto'],
    ['mostre 5 em maiusculo', 'Para converter entre maiúsculas e minúsculas, é necessário informar uma string'],
    ['mostre um numero aleatorio entre "a" e 2', 'O valor 1 não é numérico'],
    ['mostre um numero aleatorio entre 1 e "a"', 'O valor 2 não é numérico'],
    ['x = 1\nmostre x[1:2]', 'Só é possível fatiar um texto'],
    ['x = "abc"\nmostre x[0:2]', 'A posição 0 está fora do texto, que tem 3 letras'],
    ['x = "abc"\nmostre x[1:9]', 'A posição 9 está fora do texto, que tem 3 letras'],
  ])('%s', async (source, message) => {
    expect((await runScript(source)).error?.message).toBe(message);
  });
});

describe('values', () => {
  it('counts a boolean as a number in a sum', async () => {
    expect((await runScript('mostre verdade + 1')).texts).toEqual(['2']);
  });

  it('joins two lists with a plus', async () => {
    const source = 'lista de a = 1\nlista de b = 2\nc = lista a + lista b\nmostre c';

    expect((await runScript(source)).texts).toEqual(['[1, 2]']);
  });

  it('rejects a list plus a number', async () => {
    const { error } = await runScript('lista de a = 1\nmostre lista a + 1');

    expect(error?.message).toBe('Não foi possivel realizar a conta  |[1]|');
  });

  it('compares two texts', async () => {
    expect((await runScript('se "a" < "b" { mostre "antes" }')).texts).toEqual(['antes']);
  });

  it.each([
    ['1 == 1 ou nada', 'True'],
    ['1 == 2 e nada', 'False'],
  ])('stops at the left side of %s', async (condition, expected) => {
    expect((await runScript(`mostre ${condition}`)).texts).toEqual([expected]);
  });

  it('keeps a color it does not know as it was written', async () => {
    expect((await runScript('mostre "a" na cor "nada"')).events[0].color).toBe('nada');
  });

  it('prefers a variable to a question for the person', async () => {
    expect((await runScript('entrada = "guardado"\nx = entrada\nmostre x', ['digitado'])).texts).toEqual(['guardado']);
  });
});

describe('try', () => {
  it('runs without any clause', async () => {
    expect((await runScript('tente { mostre "a" }\nmostre "b"')).texts).toEqual(['a', 'b']);
  });

  it('leaves the loop from inside a clause', async () => {
    const source = 'repita 3 vezes {\nmostre "a"\ntente { mostre nada }\nse der erro { pare }\n}';

    expect((await runScript(source)).texts).toEqual(['a']);
  });
});

describe('import', () => {
  it('stops the whole program when the imported file halts', async () => {
    expect((await runScript('importe lib\nmostre "b"', [], { 'lib.safira': 'interrompa' })).texts).toEqual([]);
  });
});

describe('running by hand', () => {
  const effectsOf = (source: string, random?: () => number) => {
    const interpreter = new Interpreter({
      files: new VirtualFileSystem({ 'main.safira': source }),
      locale: 'pt-br',
      random,
    });

    return [...interpreter.run('main.safira')];
  };

  it('does nothing for a file that does not exist', () => {
    const interpreter = new Interpreter({ files: new VirtualFileSystem(), locale: 'pt-br' });

    expect([...interpreter.run('nada.safira')]).toEqual([]);
  });

  describe('keys', () => {
    const run = (source: string, pressed: string[]) =>
      runScript(source, [], {}, (_mode, keys) => pressed.includes(keys.join('+')));

    it.each(['Enter', 'enter', 'ENTER', '"Enter"', '"enter"'])('treats %s as the same key', async (name) => {
      expect((await run(`se apertar ${name} entao mostre "sim"`, ['enter'])).texts).toEqual(['sim']);
    });

    it('takes the key from a variable', async () => {
      expect((await run('tecla = "W"\nse apertar tecla entao mostre "sim"', ['w'])).texts).toEqual(['sim']);
    });

    it('prefers a variable with text over the name of a key', async () => {
      expect((await run('cima = "w"\nse apertar cima entao mostre "sim"', ['w'])).texts).toEqual(['sim']);
    });

    it('reads a combination from a text', async () => {
      expect((await run('se segurar "Shift+Enter" entao mostre "sim"', ['shift+enter'])).texts).toEqual(['sim']);
    });

    it('asks for the mode of the condition', async () => {
      const modes: string[] = [];
      await runScript('se segurar A { }\nse soltar A { }\nse apertar A { }', [], {}, (mode) => {
        modes.push(mode);

        return false;
      });

      expect(modes).toEqual(['hold', 'release', 'press']);
    });

    it('fails on a key that does not exist', async () => {
      const { error } = await run('tecla = "banana"\nse apertar tecla entao mostre "x"', []);

      expect(error?.message).toContain('banana');
    });

    it('takes a number as the name of a key', async () => {
      expect((await run('se apertar 7 entao mostre "sim"', ['7'])).texts).toEqual(['sim']);
    });
  });

  it('repeats forever until told to stop', async () => {
    const source = 'c = 0\nrepita pra sempre {\n  c = c + 1\n  se c == 3 entao pare\n  mostre c\n}\nmostre "fim"';

    expect((await runScript(source)).texts).toEqual(['1', '2', 'fim']);
  });

  it('skips a turn of a loop that never ends', async () => {
    const source = 'c = 0\nrepeat forever {\n  c = c + 1\n  if c == 1 then continue\n  show c\n  interrupt\n}';

    expect((await runScript(source)).texts).toEqual(['2']);
  });

  it('goes on after doing nothing', async () => {
    const { texts, error } = await runScript(
      'se 1 == 2 entao mostre "a" senao não faça nada\nnão faça nada\nmostre "b"',
    );

    expect(error).toBeNull();
    expect(texts).toEqual(['b']);
  });

  it.each(['guarde a resposta em nota', 'salve o que o usuario digitar na nota', 'save the answer to nota'])(
    'saves the answer with %s',
    async (line) => {
      expect((await runScript(`${line}\nmostre "Nota: " + nota`, ['7'])).texts).toEqual(['Nota: 7']);
    },
  );

  it('reads an empty text when no answer arrives', () => {
    const effects = effectsOf('x = o que o usuario digitar\nmostre "[" + x + "]"');

    expect(effects.at(-1)).toMatchObject({ type: 'output', text: '[]' });
  });

  it('does not hide an error that is not from the script', () => {
    const fail = () => {
      throw new RangeError('quebrou');
    };

    expect(() => effectsOf('tente { x = um numero aleatorio entre 1 e 2 }\nse der erro { }', fail)).toThrow(RangeError);
  });
});

describe('tone', () => {
  it('plays each note of a chord for the same time', async () => {
    const [low, high] = [noteFrequency('C'), noteFrequency('E')];

    expect((await runScript('toque C, E por 2 segundos')).tones).toEqual([
      { frequency: low, milliseconds: 2000 },
      { frequency: high, milliseconds: 2000 },
    ]);
  });

  it.each([-1, 1_000_001])('refuses a list with %s positions, and tente catches it', async (size) => {
    const { texts, error } = await runScript(
      `tente {\n  lista x com ${String(size)} posicoes\n} se der erro {\n  mostre "pegou"\n}`,
    );

    expect(error).toBeNull();
    expect(texts).toEqual(['pegou']);
  });

  it('keeps a success clause of tente on the line after a closing if', async () => {
    const source = 'tente {\n  se 1 for igual a 1 entao {\n    mostre "a"\n  }\n}\nsenao der erro {\n  mostre "b"\n}';

    expect((await runScript(source)).texts).toEqual(['a', 'b']);
  });

  it('accepts senao der erro on the line after an if inside tente', async () => {
    const source =
      'tente {\n  mostre 1\n} se der erro {\n  se 1 for igual a 1 entao {\n    mostre "e"\n  }\n}\nsenao der erro {\n  mostre "b"\n}';

    expect((await runScript(source)).error).toBeNull();
  });
});
