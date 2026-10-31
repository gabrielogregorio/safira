import { removeAccents } from './tokenizer';

const DEFAULT_OCTAVE = 4;
const SEMITONES_PER_OCTAVE = 12;
const REFERENCE_FREQUENCY = 440;
const REFERENCE_NOTE = 69;
const FIRST_MIDI_OCTAVE = 1;

const SEMITONES: Record<string, number> = {
  c: 0,
  do: 0,
  d: 2,
  re: 2,
  e: 4,
  mi: 4,
  f: 5,
  fa: 5,
  g: 7,
  sol: 7,
  a: 9,
  la: 9,
  b: 11,
  si: 11,
};

const NOTE_PATTERN = /^(do|re|mi|fa|sol|la|si|[a-g])([#b]?)(\d?)([#b]?)$/;
const REST = 'r';

const accidentalOf = (mark: string): number => {
  if (mark === '#') {
    return 1;
  }

  return mark === 'b' ? -1 : 0;
};

// Accepts C, C#, Db, C2, C2#, Dó, Ré, Sol#... An R is a rest, which gives 0. Returns null for anything else.
export const noteFrequency = (name: string): number | null => {
  const text = removeAccents(name).toLowerCase();

  if (text === REST) {
    return 0;
  }

  const match = NOTE_PATTERN.exec(text);

  if (match === null) {
    return null;
  }

  const [, note, markBefore, octave, markAfter] = match;
  const semitone = SEMITONES[note] + accidentalOf(markBefore) + accidentalOf(markAfter);
  const midi = (Number(octave || DEFAULT_OCTAVE) + FIRST_MIDI_OCTAVE) * SEMITONES_PER_OCTAVE + semitone;

  return REFERENCE_FREQUENCY * 2 ** ((midi - REFERENCE_NOTE) / SEMITONES_PER_OCTAVE);
};
