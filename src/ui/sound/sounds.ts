import acceptUrl from './files/accept.wav';
import alertUrl from './files/alert.wav';
import breakpointUrl from './files/breakpoint.wav';
import clickUrl from './files/click.wav';
import createUrl from './files/create.wav';
import deleteUrl from './files/delete.wav';
import errorUrl from './files/error.wav';
import fileCreateUrl from './files/file-create.wav';
import folderCreateUrl from './files/folder-create.wav';
import formatUrl from './files/format.wav';
import homeOpenUrl from './files/home-open.wav';
import hoverUrl from './files/hover.wav';
import ideOpenUrl from './files/ide-open.wav';
import importUrl from './files/import.wav';
import languageUrl from './files/language.wav';
import modalCloseUrl from './files/modal-close.wav';
import modalOpenUrl from './files/modal-open.wav';
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
import toggleUrl from './files/toggle.wav';
import typingUrl from './files/typing.wav';
import weatherUrl from './files/weather.wav';

export type SoundName =
  | 'click'
  | 'hover'
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
  | 'weather'
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
  | 'language'
  | 'error';

// Recorded sounds from Kenney's Interface Sounds pack, which is CC0. See files/LICENSE-kenney.txt.
export const SOUND_FILES: Record<SoundName, string> = {
  click: clickUrl,
  hover: hoverUrl,
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
  weather: weatherUrl,
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
  language: languageUrl,
  error: errorUrl,
};

// One gesture can ask for several sounds: a click on a button that also closes a modal, for example.
// Waiting a little lets the most meaningful one play first, and the others step aside.
const WAIT_MILLISECONDS: Partial<Record<SoundName, number>> = { modalClose: 10, click: 20 };
const STEPS_ASIDE: SoundName[] = ['click', 'modalClose'];
const SAME_GESTURE_MILLISECONDS = 80;
const HOVER_GAP_MILLISECONDS = 40;

const NOT_A_GESTURE: SoundName[] = ['typing', 'searchTyping'];

// These happen without a press: on a reload or a passing mouse, the browser would hold them until the first click.
const NEEDS_EARLIER_PRESS: SoundName[] = ['hover', 'ideOpen'];

const wait = (milliseconds: number): Promise<void> =>
  new Promise((resolve) => {
    setTimeout(resolve, milliseconds);
  });

const SOUND_NAMES = Object.keys(SOUND_FILES) as SoundName[];
const MASTER_GAIN = 0.5;
const LOOP_GAIN = 0.35;
const LOOP_FADE_IN_SECONDS = 0.04;
const LOOP_FADE_SECONDS = 0.06;
const LOOP_STOP_SECONDS = 0.3;
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
  let loopTimer: ReturnType<typeof setTimeout> | undefined;
  let isLoopStarting = false;
  const buffers = new Map<SoundName, Promise<AudioBuffer>>();

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

      try {
        const source = audio.createBufferSource();
        source.buffer = await bufferOf(audio, name);
        source.playbackRate.value = rate;
        source.connect(output);
        source.start();
      } catch {
        // A sound that fails to load must never get in the way of the interface.
        buffers.delete(name);
      }
    },
    // Keeps a looping sound alive for this long from now. Every call pushes the end further away.
    sustain: async (name: SoundName, milliseconds: number, rate: number): Promise<void> => {
      const audio = isEnabled ? start() : null;

      if (audio === null || output === null) {
        return;
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
          gain.gain.setTargetAtTime(LOOP_GAIN, audio.currentTime, LOOP_FADE_IN_SECONDS);
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
      clearTimeout(loopTimer);
      loopTimer = setTimeout(fadeLoop, milliseconds);
    },
  };
};

export const soundPlayer = createSoundPlayer(() =>
  typeof window.AudioContext === 'function' ? new window.AudioContext() : null,
);

const MENU_ITEMS = '[role="menuitem"], [role="menuitemradio"], [role="menuitemcheckbox"], [role="menubaritem"]';
const CLICKABLE = `button, a, summary, input[type="checkbox"], input[data-sound], ${MENU_ITEMS}`;

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

  return isSoundName(named) ? named : 'click';
};
