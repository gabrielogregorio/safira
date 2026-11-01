import type { CommandKey } from './phrases';
import { getAllCommands, getPhrases, isContinuationWord } from './phrases';

describe('phrases', () => {
  it('lists the commands of every language', () => {
    const phrases = getPhrases('mostre').map((words) => words.join(' '));

    expect(phrases).toEqual(expect.arrayContaining(['mostre', 'show', 'muestra']));
  });

  it('tries the longest phrase first', () => {
    const lengths = getPhrases('declara_variaveis').map((words) => words.length);

    expect(lengths).toEqual([...lengths].sort((first, second) => second - first));
  });

  it('gives each command with phrases a syntax color', () => {
    const uncolored = getAllCommands().filter(
      ([, definition]) => definition.phrases.length > 0 && definition.color === '',
    );

    expect(uncolored).toEqual([]);
  });

  it('knows the words that continue a command', () => {
    expect(isContinuationWord('inserindo')).toBe(true);
    expect(isContinuationWord('senao')).toBe(true);
    expect(isContinuationWord('banana')).toBe(false);
  });
});

describe('getPhrases', () => {
  it('has nothing for a command that does not exist', () => {
    expect(getPhrases('nada' as CommandKey)).toEqual([]);
  });
});
