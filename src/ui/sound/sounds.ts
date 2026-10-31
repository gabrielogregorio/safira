export type SoundName = 'click' | 'toggle' | 'open' | 'create' | 'delete';

interface Tone {
  wave: OscillatorType;
  fromHertz: number;
  toHertz: number;
  startSeconds: number;
  seconds: number;
  gain: number;
}

interface NoiseBurst {
  bandHertz: number;
  startSeconds: number;
  seconds: number;
  gain: number;
}

interface SoundRecipe {
  tones: Tone[];
  noise: NoiseBurst[];
}

const MASTER_GAIN = 0.2;
const SILENCE = 0.0001;
const NOISE_SECONDS = 0.3;

const note = (hertz: number, startSeconds: number, seconds: number, gain: number): Tone => ({
  wave: 'sine',
  fromHertz: hertz,
  toHertz: hertz,
  startSeconds,
  seconds,
  gain,
});

// Short glassy notes, in the spirit of the desktop sounds from the Frutiger Aero years.
export const SOUND_RECIPES: Record<SoundName, SoundRecipe> = {
  click: {
    tones: [
      { wave: 'sine', fromHertz: 1900, toHertz: 1200, startSeconds: 0, seconds: 0.035, gain: 0.5 },
      { wave: 'triangle', fromHertz: 3800, toHertz: 3000, startSeconds: 0, seconds: 0.02, gain: 0.12 },
    ],
    noise: [],
  },
  toggle: {
    tones: [note(660, 0, 0.09, 0.5), note(990, 0.065, 0.13, 0.5)],
    noise: [],
  },
  // A soft glass swoosh rising into one clear note.
  open: {
    tones: [
      { wave: 'triangle', fromHertz: 380, toHertz: 1500, startSeconds: 0, seconds: 0.16, gain: 0.3 },
      note(1319, 0.11, 0.22, 0.4),
      note(1976, 0.15, 0.2, 0.18),
    ],
    noise: [],
  },
  create: {
    tones: [note(523, 0, 0.3, 0.4), note(659, 0.07, 0.3, 0.4), note(784, 0.14, 0.3, 0.4), note(1047, 0.21, 0.45, 0.4)],
    noise: [],
  },
  // Paper crumpling, then falling into the recycle bin.
  delete: {
    tones: [{ wave: 'triangle', fromHertz: 320, toHertz: 80, startSeconds: 0.14, seconds: 0.2, gain: 0.7 }],
    noise: [
      { bandHertz: 3200, startSeconds: 0, seconds: 0.05, gain: 0.7 },
      { bandHertz: 2400, startSeconds: 0.05, seconds: 0.045, gain: 0.6 },
      { bandHertz: 3600, startSeconds: 0.095, seconds: 0.05, gain: 0.5 },
      { bandHertz: 1800, startSeconds: 0.15, seconds: 0.09, gain: 0.45 },
    ],
  },
};

const noiseBuffer = (context: BaseAudioContext): AudioBuffer => {
  const buffer = context.createBuffer(1, Math.ceil(context.sampleRate * NOISE_SECONDS), context.sampleRate);
  const samples = buffer.getChannelData(0);

  for (let index = 0; index < samples.length; index += 1) {
    samples[index] = Math.random() * 2 - 1;
  }

  return buffer;
};

const envelope = (context: BaseAudioContext, start: number, seconds: number, gain: number): GainNode => {
  const node = context.createGain();
  node.gain.setValueAtTime(SILENCE, start);
  node.gain.exponentialRampToValueAtTime(gain, start + Math.min(0.006, seconds / 3));
  node.gain.exponentialRampToValueAtTime(SILENCE, start + seconds);

  return node;
};

export const scheduleSound = (context: BaseAudioContext, output: AudioNode, name: SoundName, when: number): void => {
  const { tones, noise } = SOUND_RECIPES[name];

  for (const tone of tones) {
    const start = when + tone.startSeconds;
    const oscillator = context.createOscillator();
    oscillator.type = tone.wave;
    oscillator.frequency.setValueAtTime(tone.fromHertz, start);
    oscillator.frequency.exponentialRampToValueAtTime(tone.toHertz, start + tone.seconds);
    oscillator.connect(envelope(context, start, tone.seconds, tone.gain)).connect(output);
    oscillator.start(start);
    oscillator.stop(start + tone.seconds);
  }

  for (const burst of noise) {
    const start = when + burst.startSeconds;
    const source = context.createBufferSource();
    const filter = context.createBiquadFilter();
    source.buffer = noiseBuffer(context);
    filter.type = 'bandpass';
    filter.frequency.value = burst.bandHertz;
    source
      .connect(filter)
      .connect(envelope(context, start, burst.seconds, burst.gain))
      .connect(output);
    source.start(start);
    source.stop(start + burst.seconds);
  }
};

export const createSoundPlayer = (createContext: () => AudioContext | null) => {
  let context: AudioContext | null = null;
  let output: GainNode | null = null;
  let isEnabled = true;

  return {
    setEnabled: (enabled: boolean): void => {
      isEnabled = enabled;
    },
    // The context only starts on the first sound, which always comes from a click, as browsers demand.
    play: (name: SoundName): void => {
      if (!isEnabled) {
        return;
      }

      if (context === null) {
        context = createContext();
      }

      if (context === null) {
        return;
      }

      if (output === null) {
        output = context.createGain();
        output.gain.value = MASTER_GAIN;
        output.connect(context.destination);
      }

      if (context.state === 'suspended') {
        void context.resume();
      }

      scheduleSound(context, output, name, context.currentTime);
    },
  };
};

export const soundPlayer = createSoundPlayer(() =>
  typeof window.AudioContext === 'function' ? new window.AudioContext() : null,
);

const CLICKABLE =
  'button, a, summary, [role="menuitem"], [role="menuitemradio"], [role="menuitemcheckbox"], [role="menubaritem"], .breakpoint-dot';
const SOUND_NAMES = Object.keys(SOUND_RECIPES);

const isSoundName = (value: string | undefined): value is SoundName =>
  value !== undefined && SOUND_NAMES.includes(value);

export const soundForClick = (target: EventTarget | null): SoundName | null => {
  if (!(target instanceof Element)) {
    return null;
  }

  const clicked = target.closest<HTMLElement>(CLICKABLE);

  if (clicked === null) {
    return null;
  }

  const named = clicked.dataset['sound'];

  return isSoundName(named) ? named : 'click';
};
