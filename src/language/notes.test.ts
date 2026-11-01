import { noteFrequency } from './notes';
import { runScript } from './testHarness';

describe('noteFrequency', () => {
  it.each([
    ['A', 440],
    ['La', 440],
    ['Lá', 440],
    ['A5', 880],
    ['a3', 220],
  ])('tunes %s', (name, frequency) => {
    expect(noteFrequency(name)).toBeCloseTo(frequency);
  });

  it('reads sharps and flats on either side of the octave', () => {
    expect(noteFrequency('C#')).toBeCloseTo(277.18, 1);
    expect(noteFrequency('C2#')).toBeCloseTo(noteFrequency('C#2') ?? 0);
    expect(noteFrequency('Db')).toBeCloseTo(noteFrequency('C#') ?? 0);
    expect(noteFrequency('Ré')).toBeCloseTo(noteFrequency('D') ?? 0);
  });

  it('treats R as a rest and refuses the rest', () => {
    expect(noteFrequency('R')).toBe(0);
    expect(noteFrequency('banana')).toBeNull();
    expect(noteFrequency('H')).toBeNull();
  });
});

describe('tone commands', () => {
  it('plays a note for a time in seconds', async () => {
    expect((await runScript('toque C por 1s')).tones).toEqual([
      { frequency: expect.closeTo(261.63, 1) as number, milliseconds: 1000 },
    ]);
  });

  it('keeps a sharp and still reads the comment after it', async () => {
    const { tones, error } = await runScript('play D# by 0.1 # second no caso');

    expect(error).toBeNull();
    expect(tones).toEqual([{ frequency: expect.closeTo(311.13, 1) as number, milliseconds: 100 }]);
  });

  it('plays a list, one note after the other', async () => {
    const { tones } = await runScript('toque C2#, D2, D, C, R, Ré,Mi,Fa,Sol por 1s');

    expect(tones).toHaveLength(9);
    expect(tones[4]).toEqual({ frequency: 0, milliseconds: 1000 });
    expect(tones.every((tone) => tone.milliseconds === 1000)).toBe(true);
  });

  it('accepts milliseconds, an expression and no time at all', async () => {
    expect((await runScript('toque C por 250ms')).tones[0].milliseconds).toBe(250);
    expect((await runScript('t = 2\ntoque C por t * 2 segundos')).tones[0].milliseconds).toBe(4000);
    expect((await runScript('toque C')).tones[0].milliseconds).toBe(500);
  });

  it('leaves names alone', async () => {
    expect((await runScript('play = 3\nmostre play')).texts).toEqual(['3']);
  });

  it('fails on something that is not a note', async () => {
    expect((await runScript('toque banana por 1s')).error).not.toBeNull();
  });

  it('keeps a # as a comment elsewhere', async () => {
    expect((await runScript('x = 1# nota\nmostre x')).texts).toEqual(['1']);
  });
});
