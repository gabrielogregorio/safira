import type { Locale } from '@/language/messages';
import type { ThemeId } from '@/settings/settings';
import acceptUrl from './files/accept.wav';
import popUrl from './files/pop.wav';
import fishFleeUrl from './files/fish-flee.wav';
import fishEatUrl from './files/fish-eat.wav';
import fishBurstUrl from './files/fish-burst.wav';
import fishChompUrl from './files/fish-chomp.wav';
import foodDropUrl from './files/food-drop.wav';
import plantUrl from './files/plant.wav';
import waterHoldUrl from './files/water-hold.wav';
import seaLightUrl from './files/sea-light.wav';
import seaDarkUrl from './files/sea-dark.wav';
import seaSimpleUrl from './files/sea-simple.wav';
import aquariumCloseUrl from './files/aquarium-close.wav';
import aquariumUrl from './files/aquarium.wav';
import alertUrl from './files/alert.wav';
import breakpointUrl from './files/breakpoint.wav';
import clickUrl from './files/click.wav';
import createUrl from './files/create.wav';
import deleteUrl from './files/delete.wav';
import errorUrl from './files/error.wav';
import exportUrl from './files/export.wav';
import fileCreateUrl from './files/file-create.wav';
import folderCreateUrl from './files/folder-create.wav';
import formatUrl from './files/format.wav';
import homeOpenUrl from './files/home-open.wav';
import hoverSpecialUrl from './files/hover-special.wav';
import hoverUrl from './files/hover.wav';
import ideOpenUrl from './files/ide-open.wav';
import importUrl from './files/import.wav';
import languageEnUsUrl from './files/language-en-us.wav';
import languageEsUrl from './files/language-es.wav';
import languageJaUrl from './files/language-ja.wav';
import languagePtBrUrl from './files/language-pt-br.wav';
import languageZhCnUrl from './files/language-zh-cn.wav';
import lineDeleteUrl from './files/line-delete.wav';
import modalCloseUrl from './files/modal-close.wav';
import modalOpenUrl from './files/modal-open.wav';
import moveUrl from './files/move.wav';
import openUrl from './files/open.wav';
import renameStartUrl from './files/rename-start.wav';
import renameUrl from './files/rename.wav';
import runUrl from './files/run.wav';
import searchTypingUrl from './files/search-typing.wav';
import searchUrl from './files/search.wav';
import selectionUrl from './files/selection.wav';
import stopUrl from './files/stop.wav';
import suggestionsOffUrl from './files/suggestions-off.wav';
import suggestionsOnUrl from './files/suggestions-on.wav';
import tabUrl from './files/tab.wav';
import terminalFocusUrl from './files/terminal-focus.wav';
import terminalSendUrl from './files/terminal-send.wav';
import terminalTypingUrl from './files/terminal-typing.wav';
import toggleUrl from './files/toggle.wav';
import typingUrl from './files/typing.wav';
import weatherDarkUrl from './files/weather-dark.wav';
import weatherLightUrl from './files/weather-light.wav';
import weatherSimpleUrl from './files/weather-simple.wav';

export type SoundName =
  | 'click'
  | 'hover'
  | 'hoverSpecial'
  | 'toggle'
  | 'open'
  | 'tab'
  | 'homeOpen'
  | 'ideOpen'
  | 'create'
  | 'renameStart'
  | 'rename'
  | 'delete'
  | 'alert'
  | 'modalOpen'
  | 'modalClose'
  | 'breakpoint'
  | 'run'
  | 'stop'
  | 'format'
  | 'weatherLight'
  | 'weatherDark'
  | 'weatherSimple'
  | 'fileCreate'
  | 'folderCreate'
  | 'suggestionsOn'
  | 'suggestionsOff'
  | 'search'
  | 'searchTyping'
  | 'typing'
  | 'accept'
  | 'selection'
  | 'import'
  | 'languagePtBr'
  | 'languageEnUs'
  | 'languageEs'
  | 'languageZhCn'
  | 'languageJa'
  | 'error'
  | 'export'
  | 'lineDelete'
  | 'aquarium'
  | 'aquariumClose'
  | 'pop'
  | 'fishFlee'
  | 'fishEat'
  | 'fishChomp'
  | 'fishBurst'
  | 'foodDrop'
  | 'plant'
  | 'waterHold'
  | 'seaLight'
  | 'seaDark'
  | 'seaSimple'
  | 'move'
  | 'terminalFocus'
  | 'terminalTyping'
  | 'terminalSend';

// Recorded sounds from Kenney's Interface Sounds pack, which is CC0. See files/LICENSE-kenney.txt.
export const SOUND_FILES: Record<SoundName, string> = {
  click: clickUrl,
  hover: hoverUrl,
  hoverSpecial: hoverSpecialUrl,
  toggle: toggleUrl,
  open: openUrl,
  tab: tabUrl,
  homeOpen: homeOpenUrl,
  ideOpen: ideOpenUrl,
  create: createUrl,
  renameStart: renameStartUrl,
  rename: renameUrl,
  delete: deleteUrl,
  alert: alertUrl,
  modalOpen: modalOpenUrl,
  modalClose: modalCloseUrl,
  breakpoint: breakpointUrl,
  run: runUrl,
  stop: stopUrl,
  format: formatUrl,
  weatherLight: weatherLightUrl,
  weatherDark: weatherDarkUrl,
  weatherSimple: weatherSimpleUrl,
  fileCreate: fileCreateUrl,
  folderCreate: folderCreateUrl,
  suggestionsOn: suggestionsOnUrl,
  suggestionsOff: suggestionsOffUrl,
  search: searchUrl,
  searchTyping: searchTypingUrl,
  typing: typingUrl,
  accept: acceptUrl,
  selection: selectionUrl,
  import: importUrl,
  languagePtBr: languagePtBrUrl,
  languageEnUs: languageEnUsUrl,
  languageEs: languageEsUrl,
  languageZhCn: languageZhCnUrl,
  languageJa: languageJaUrl,
  error: errorUrl,
  export: exportUrl,
  lineDelete: lineDeleteUrl,
  aquarium: aquariumUrl,
  aquariumClose: aquariumCloseUrl,
  pop: popUrl,
  fishFlee: fishFleeUrl,
  fishEat: fishEatUrl,
  fishChomp: fishChompUrl,
  fishBurst: fishBurstUrl,
  foodDrop: foodDropUrl,
  plant: plantUrl,
  waterHold: waterHoldUrl,
  seaLight: seaLightUrl,
  seaDark: seaDarkUrl,
  seaSimple: seaSimpleUrl,
  move: moveUrl,
  terminalFocus: terminalFocusUrl,
  terminalTyping: terminalTypingUrl,
  terminalSend: terminalSendUrl,
};

// Each language lands with something of its region, and each sky with its own weather.
export const LANGUAGE_SOUNDS: Record<Locale, SoundName> = {
  'pt-br': 'languagePtBr',
  'en-us': 'languageEnUs',
  es: 'languageEs',
  'zh-cn': 'languageZhCn',
  ja: 'languageJa',
};

export const WEATHER_SOUNDS: Record<ThemeId, SoundName> = {
  light: 'weatherLight',
  dark: 'weatherDark',
  simple: 'weatherSimple',
};

export const SEA_SOUNDS: Record<ThemeId, SoundName> = { light: 'seaLight', dark: 'seaDark', simple: 'seaSimple' };

// One gesture can ask for several sounds: a click on a button that also closes a modal, for example.
// Waiting a little lets the most meaningful one play first, and the others step aside.
const WAIT_MILLISECONDS: Partial<Record<SoundName, number>> = { modalClose: 10, click: 20 };
const STEPS_ASIDE: SoundName[] = ['click', 'modalClose'];
const SAME_GESTURE_MILLISECONDS = 80;
const HOVER_GAP_MILLISECONDS = 40;

const NOT_A_GESTURE: SoundName[] = ['hoverSpecial', 'typing', 'searchTyping', 'terminalTyping', 'fishEat', 'pop'];

// These happen without a press: on a reload or a passing mouse, the browser would hold them until the first click.
const NEEDS_EARLIER_PRESS: SoundName[] = ['hover', 'hoverSpecial', 'ideOpen'];

const wait = (milliseconds: number): Promise<void> =>
  new Promise((resolve) => {
    setTimeout(resolve, milliseconds);
  });

const SOUND_NAMES = Object.keys(SOUND_FILES) as SoundName[];
const LANGUAGE_SOUND_NAMES: SoundName[] = Object.values(LANGUAGE_SOUNDS);
const LANGUAGE_FADE_SECONDS = 0.012;
const LANGUAGE_STOP_SECONDS = 0.06;
const MASTER_GAIN = 0.5;
const LOOP_GAIN = 0.35;
const MUTE_SECONDS = 0.01;
const MILLISECONDS_PER_SECOND = 1000;
const TONE_GAIN = 0.5;
const TONE_SUSTAIN = 0.45;
const TONE_ATTACK_SECONDS = 0.008;
const TONE_DECAY_SECONDS = 0.18;
const TONE_RELEASE_SECONDS = 0.06;
const TONE_WAVES: [OscillatorType, number][] = [
  ['triangle', 1],
  ['sine', 2],
];
const LOOP_FADE_IN_SECONDS = 0.04;
const LOOP_FADE_SECONDS = 0.02;
const LOOP_STOP_SECONDS = 0.1;
const RATE_GLIDE_SECONDS = 0.05;

const fetchSound = async (context: AudioContext, url: string): Promise<AudioBuffer> => {
  const response = await fetch(url);

  return context.decodeAudioData(await response.arrayBuffer());
};

export const createSoundPlayer = (createContext: () => AudioContext | null) => {
  let context: AudioContext | null = null;
  let output: GainNode | null = null;
  let isEnabled = true;
  let lastSound: { name: SoundName; time: number } | null = null;
  let lastHover = -HOVER_GAP_MILLISECONDS;
  let loop: { source: AudioBufferSourceNode; gain: GainNode } | null = null;
  let languageVoice: { source: AudioBufferSourceNode; gain: GainNode } | null = null;
  let languageTurn = 0;
  let isLoopHeld = false;
  let isLoopStarting = false;
  const buffers = new Map<SoundName, Promise<AudioBuffer>>();
  const tones = new Set<OscillatorNode>();

  const fadeLoop = (): void => {
    if (context !== null && loop !== null) {
      loop.gain.gain.setTargetAtTime(0, context.currentTime, LOOP_FADE_SECONDS);
      loop.source.stop(context.currentTime + LOOP_STOP_SECONDS);
      loop = null;
    }
  };

  const start = (): AudioContext | null => {
    context ??= createContext();

    if (context !== null && output === null) {
      output = context.createGain();
      output.gain.value = MASTER_GAIN;
      output.connect(context.destination);
    }

    return context;
  };

  const isSameGesture = (name: SoundName): boolean => {
    if (lastSound === null || performance.now() - lastSound.time > SAME_GESTURE_MILLISECONDS) {
      return false;
    }

    return STEPS_ASIDE.includes(name) || lastSound.name === name;
  };

  const bufferOf = (audio: AudioContext, name: SoundName): Promise<AudioBuffer> => {
    const known = buffers.get(name);

    if (known !== undefined) {
      return known;
    }

    const loading = fetchSound(audio, SOUND_FILES[name]);
    buffers.set(name, loading);

    return loading;
  };

  return {
    setEnabled: (enabled: boolean): void => {
      isEnabled = enabled;

      // Muting also cuts what is already playing, such as the long tail of the weather sounds.
      if (context !== null && output !== null) {
        output.gain.setTargetAtTime(enabled ? MASTER_GAIN : 0, context.currentTime, MUTE_SECONDS);
      }

      if (!enabled) {
        fadeLoop();
      }
    },
    // Runs on the first press, so that the files are decoded before the click that follows it.
    prepare: (): void => {
      const audio = isEnabled ? start() : null;

      if (audio !== null) {
        for (const name of SOUND_NAMES) {
          bufferOf(audio, name).catch(() => {
            buffers.delete(name);
          });
        }
      }
    },
    play: async (name: SoundName, rate = 1): Promise<void> => {
      await wait(WAIT_MILLISECONDS[name] ?? 0);

      if (NEEDS_EARLIER_PRESS.includes(name) && context === null) {
        return;
      }

      const audio = isEnabled ? start() : null;

      if (audio === null || output === null || isSameGesture(name)) {
        return;
      }

      // Hovering and typing never count as a gesture, or the click that follows them would step aside.
      if (name === 'hover') {
        if (performance.now() - lastHover < HOVER_GAP_MILLISECONDS) {
          return;
        }

        lastHover = performance.now();
      } else if (!NOT_A_GESTURE.includes(name)) {
        lastSound = { name, time: performance.now() };
      }

      if (audio.state === 'suspended') {
        void audio.resume();
      }

      // A new language cuts the one before it, even when that one is still loading its file.
      const isLanguage = LANGUAGE_SOUND_NAMES.includes(name);

      if (isLanguage) {
        languageTurn += 1;
      }

      const turn = languageTurn;

      try {
        const source = audio.createBufferSource();
        source.buffer = await bufferOf(audio, name);

        if (!isEnabled || (isLanguage && turn !== languageTurn)) {
          return;
        }

        source.playbackRate.value = rate;

        if (isLanguage) {
          if (languageVoice !== null) {
            languageVoice.gain.gain.setTargetAtTime(0, audio.currentTime, LANGUAGE_FADE_SECONDS);
            languageVoice.source.stop(audio.currentTime + LANGUAGE_STOP_SECONDS);
          }

          const gain = audio.createGain();
          gain.gain.value = 1;
          source.connect(gain);
          gain.connect(output);
          languageVoice = { source, gain };
        } else {
          source.connect(output);
        }

        source.start();
      } catch {
        // A sound that fails to load must never get in the way of the interface.
        buffers.delete(name);
      }
    },
    // Starts a looping sound, or moves the one that is playing to this rate. It lasts until `release`.
    hold: async (name: SoundName, rate: number, volume = LOOP_GAIN): Promise<void> => {
      const audio = isEnabled ? start() : null;

      if (audio === null || output === null) {
        return;
      }

      isLoopHeld = true;

      if (audio.state === 'suspended') {
        void audio.resume();
      }

      if (loop === null) {
        if (isLoopStarting) {
          return;
        }

        isLoopStarting = true;

        try {
          const source = audio.createBufferSource();
          const gain = audio.createGain();
          source.buffer = await bufferOf(audio, name);
          source.loop = true;
          gain.gain.value = 0;
          gain.gain.setTargetAtTime(volume, audio.currentTime, LOOP_FADE_IN_SECONDS);
          source.connect(gain);
          gain.connect(output);
          source.start();
          loop = { source, gain };
        } catch {
          buffers.delete(name);

          return;
        } finally {
          isLoopStarting = false;
        }
      }

      loop.source.playbackRate.setTargetAtTime(rate, audio.currentTime, RATE_GLIDE_SECONDS);

      // The press can end while the file is still loading.
      if (!isLoopHeld) {
        fadeLoop();
      }
    },
    release: (): void => {
      isLoopHeld = false;
      fadeLoop();
    },
    // A note of a Safira program: a soft bell made of two waves, so that it never sounds like a test tone.
    tone: (frequency: number, milliseconds: number): void => {
      const audio = isEnabled ? start() : null;

      if (audio === null || output === null || frequency <= 0 || milliseconds <= 0) {
        return;
      }

      const now = audio.currentTime;
      const end = now + milliseconds / MILLISECONDS_PER_SECOND;
      const envelope = audio.createGain();
      envelope.gain.setValueAtTime(0, now);
      envelope.gain.linearRampToValueAtTime(TONE_GAIN, now + TONE_ATTACK_SECONDS);
      envelope.gain.setTargetAtTime(TONE_GAIN * TONE_SUSTAIN, now + TONE_ATTACK_SECONDS, TONE_DECAY_SECONDS);
      envelope.gain.setTargetAtTime(0, Math.max(now, end - TONE_RELEASE_SECONDS), TONE_RELEASE_SECONDS / 3);
      envelope.connect(output);

      for (const [type, multiple] of TONE_WAVES) {
        const wave = audio.createOscillator();
        wave.type = type;
        wave.frequency.value = frequency * multiple;
        wave.connect(envelope);
        wave.start(now);
        wave.stop(end + TONE_RELEASE_SECONDS);
        tones.add(wave);
        wave.addEventListener('ended', () => {
          tones.delete(wave);
        });
      }
    },
    stopTones: (): void => {
      for (const wave of tones) {
        wave.stop();
      }
    },
  };
};

export const soundPlayer = createSoundPlayer(() =>
  typeof window.AudioContext === 'function' ? new window.AudioContext() : null,
);

const MENU_ITEMS = '[role="menuitem"], [role="menuitemradio"], [role="menuitemcheckbox"], [role="menubaritem"]';
const TEXT_FIELDS = 'input:not([type]), input[type="text"], input[type="search"]';
const CLICKABLE = `button, a, summary, input[type="checkbox"], ${TEXT_FIELDS}, ${MENU_ITEMS}`;

// Fields with their own typing sound name it, and every other text field shares this one.
export const isPlainTextField = (target: EventTarget | null): boolean =>
  target instanceof HTMLInputElement && target.matches(TEXT_FIELDS) && target.dataset['sound'] === undefined;

export const clickableAt = (target: EventTarget | null): Element | null => {
  const clickable = target instanceof Element ? target.closest(CLICKABLE) : null;

  return clickable === null || clickable.matches(':disabled, [aria-disabled="true"]') ? null : clickable;
};

const isSoundName = (value: string | undefined): value is SoundName =>
  value !== undefined && (SOUND_NAMES as string[]).includes(value);

export const soundForClick = (target: EventTarget | null): SoundName | null => {
  if (!(target instanceof Element)) {
    return null;
  }

  const clicked = target.closest<HTMLElement>(CLICKABLE);

  if (clicked === null) {
    return null;
  }

  const named = clicked.dataset['sound'];

  if (isSoundName(named)) {
    return named;
  }

  return clicked.matches(TEXT_FIELDS) ? 'terminalFocus' : 'click';
};
