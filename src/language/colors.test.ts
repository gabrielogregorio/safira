import { runScript } from './testHarness';
import { resolveColor } from './colors';

const colorOf = async (source: string): Promise<string | undefined> => {
  const { events, error } = await runScript(source);

  expect(error).toBeNull();

  return events[0]?.color;
};

describe('resolveColor', () => {
  it.each([
    ['#ff1122', '#ff1122'],
    ['#FF1122', '#ff1122'],
    ['#331', '#331'],
    ['#ff112280', '#ff112280'],
    ['0xff1122', '#ff1122'],
    ['0xABC', '#abc'],
  ])('reads %s', (text, color) => {
    expect(resolveColor(text)).toBe(color);
  });

  it('knows names in every language, with or without accents', () => {
    expect(resolveColor('azul')).toBe(resolveColor('blue'));
    expect(resolveColor('vermelho')).toBe(resolveColor('rojo'));
    expect(resolveColor('lilás')).toBe(resolveColor('lilas'));
    expect(resolveColor('ROXO')).toBe(resolveColor('roxo'));
  });

  it.each(['nada', '#12', '#12345', '0x12', '#gggggg'])('refuses %s', (text) => {
    expect(resolveColor(text)).toBeNull();
  });
});

describe('showing text in a color', () => {
  it.each([
    ['mostrar "ola" na cor 0xff1122', '#ff1122'],
    ['mostrar "ola" na cor #ff1122', '#ff1122'],
    ['mostrar "ola" na cor #331', '#331'],
    ['mostrar "ola" na cor "#ff1122"', '#ff1122'],
    ['mostrar "ola" na cor "azul"', resolveColor('azul')],
    ['mostrar "ola" na cor roxo', resolveColor('roxo')],
    ['mostrar "ola" na cor pink', resolveColor('pink')],
    ['mostrar "ola" na cor azul', resolveColor('azul')],
    ['show "ola" in color red', resolveColor('red')],
    ['mostre "ola" na cor #ff1122 # comentario', '#ff1122'],
  ])('%s', async (source, color) => {
    expect(await colorOf(source)).toBe(color);
  });

  it.each([
    ['mostre na cor #331 "opa eae"', '#331'],
    ['mostrar na cor 0xff1122 "opa eae"', '#ff1122'],
    ['mostra na cor azul "opa eae"', resolveColor('azul')],
    ['mostre na cor "#123456" "opa eae"', '#123456'],
  ])('with the color first: %s', async (source, color) => {
    const { texts, events } = await runScript(source);

    expect(texts).toEqual(['opa eae']);
    expect(events[0]?.color).toBe(color);
  });

  it('keeps the color of the inline form', async () => {
    const { events } = await runScript('mostre nessa linha "a" na cor #331');

    expect(events[0]).toMatchObject({ type: 'inline', color: '#331' });
  });

  it('prefers a variable over a color with the same name', async () => {
    expect(await colorOf('azul vale "#123456"\nmostre "ola" na cor azul')).toBe('#123456');
  });

  it('reads the color from a variable', async () => {
    expect(await colorOf('tom vale "roxo"\nmostre "ola" na cor tom')).toBe(resolveColor('roxo'));
  });

  it('fails on a name that is neither a variable nor a color', async () => {
    const { error } = await runScript('mostre "ola" na cor nadinha');

    expect(error?.message).toContain('nadinha');
  });

  it('keeps a # after a finished line as a comment', async () => {
    const { texts } = await runScript('mostre "a" #ff1122 "b"\nmostre "c"');

    expect(texts).toEqual(['a', 'c']);
  });

  it('keeps a variable named like the word in', async () => {
    const { texts } = await runScript('en vale 3\nmostre en');

    expect(texts).toEqual(['3']);
  });
});

describe('show command spellings', () => {
  it.each(['mostre', 'mostra', 'mostrar'])('accepts %s', async (command) => {
    const { texts } = await runScript(`${command} "ola"`);

    expect(texts).toEqual(['ola']);
  });

  it.each(['mostra nessa linha', 'mostrar nessa linha', 'mostra na tela', 'mostrar na tela'])(
    'accepts %s',
    async (command) => {
      const { texts } = await runScript(`${command} "ola"`);

      expect(texts.join('')).toBe('ola');
    },
  );

  it('does not break names that start with the command', async () => {
    const { texts } = await runScript('funcao mostra_tudo { mostre "ok" }\nmostra_tudo()');

    expect(texts).toEqual(['ok']);
  });
});
