import { parse } from './parser';
import { runScript } from './testHarness';

const invalidLines = (source: string): string[] =>
  parse(source).flatMap((statement) => (statement.kind === 'invalid' ? [statement.detail] : []));

describe('the same commands in each language', () => {
  it.each([
    ['for each x from 1 to 3 {\n  print x\n}', ['1', '2', '3']],
    ['para cada x desde 1 hasta 3 {\n  muestra x\n}', ['1', '2', '3']],
  ])('counts with %s', async (source, expected) => {
    expect((await runScript(source)).texts).toEqual(expected);
  });

  it.each([
    [
      'list of fruits receive "a", "b"\nadd "c" at the end of the list of fruits\nadd "z" at the start of the list of fruits\nremove "a" from the list of fruits\nprint fruits\nprint the size of the list of fruits\nif have "c" in the list of fruits then {\n  print "yes"\n}',
    ],
    [
      'lista de frutas recibe "a", "b"\nañadir "c" al final de la lista de frutas\nañadir "z" al inicio de la lista de frutas\neliminarlo "a" de la lista de frutas\nmuestra frutas\nmuestra el tamaño de la lista de frutas\nsi tener "c" en la lista de frutas entonces {\n  muestra "yes"\n}',
    ],
  ])('changes a list in %s', async (source) => {
    expect((await runScript(source)).texts).toEqual(["['z', 'b', 'c']", '3', 'yes']);
  });

  it.each([
    [
      'create the file "a.txt"\nadd "x" to the file "a.txt"\noverwrite "y" to the file "a.txt"\nprint read the file "a.txt"',
    ],
    [
      'crea el archivo "a.txt"\nagregue "x" al archivo "a.txt"\nsobrescribir "y" al archivo "a.txt"\nmuestra lea el archivo "a.txt"',
    ],
  ])('writes a file in %s', async (source) => {
    expect((await runScript(source)).texts).toEqual(['y']);
  });

  it.each([
    ['n = 1\nincrease 3 in n\ndecrease 1 in n\nprint n'],
    ['n = 1\nincrementar 3 en n\ndecrementar 1 en n\nmuestra n'],
  ])('moves a number in %s', async (source) => {
    expect((await runScript(source)).texts).toEqual(['3']);
  });

  it('reads accents in commands', () => {
    expect(invalidLines('n = 7\nse n for maior que 5 então {\n  mostre "a"\n} senão {\n  mostre "b"\n}')).toEqual([]);
  });

  it('keeps text in any alphabet', async () => {
    expect((await runScript('name = "世界"\nprint "你好," + name')).texts).toEqual(['你好,世界']);
  });
});
