import alertUrl from './files/alert.wav';
import breakpointUrl from './files/breakpoint.wav';
import clickUrl from './files/click.wav';
import createUrl from './files/create.wav';
import deleteUrl from './files/delete.wav';
import formatUrl from './files/format.wav';
import homeOpenUrl from './files/home-open.wav';
import hoverUrl from './files/hover.wav';
import ideOpenUrl from './files/ide-open.wav';
import modalCloseUrl from './files/modal-close.wav';
import modalOpenUrl from './files/modal-open.wav';
import openUrl from './files/open.wav';
import renameStartUrl from './files/rename-start.wav';
import renameUrl from './files/rename.wav';
import runUrl from './files/run.wav';
import stopUrl from './files/stop.wav';
import tabUrl from './files/tab.wav';
import toggleUrl from './files/toggle.wav';
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
  | 'weather';

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
};

// One gesture can ask for several sounds: a click on a button that also closes a modal, for example.
// Waiting a little lets the most meaningful one play first, and the others step aside.
const WAIT_MILLISECONDS: Partial<Record<SoundName, number>> = { modalClose: 10, click: 20 };
const STEPS_ASIDE: SoundName[] = ['click', 'modalClose'];
const SAME_GESTURE_MILLISECONDS = 80;
const HOVER_GAP_MILLISECONDS = 40;

// These happen without a press: on a reload or a passing mouse, the browser would hold them until the first click.
const NEEDS_EARLIER_PRESS: SoundName[] = ['hover', 'ideOpen'];

const wait = (milliseconds: number): Promise<void> =>
  new Promise((resolve) => {
    setTimeout(resolve, milliseconds);
  });

const SOUND_NAMES = Object.keys(SOUND_FILES) as SoundName[];
const MASTER_GAIN = 0.5;

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
  const buffers = new Map<SoundName, Promise<AudioBuffer>>();

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
    play: async (name: SoundName): Promise<void> => {
      await wait(WAIT_MILLISECONDS[name] ?? 0);

      if (NEEDS_EARLIER_PRESS.includes(name) && context === null) {
        return;
      }

      const audio = isEnabled ? start() : null;

      if (audio === null || output === null || isSameGesture(name)) {
        return;
      }

      // A hover never counts as a gesture, or the click that follows it would step aside.
      if (name === 'hover') {
        if (performance.now() - lastHover < HOVER_GAP_MILLISECONDS) {
          return;
        }

        lastHover = performance.now();
      } else {
        lastSound = { name, time: performance.now() };
      }

      if (audio.state === 'suspended') {
        void audio.resume();
      }

      try {
        const source = audio.createBufferSource();
        source.buffer = await bufferOf(audio, name);
        source.connect(output);
        source.start();
      } catch {
        // A sound that fails to load must never get in the way of the interface.
        buffers.delete(name);
      }
    },
  };
};

export const soundPlayer = createSoundPlayer(() =>
  typeof window.AudioContext === 'function' ? new window.AudioContext() : null,
);

const MENU_ITEMS = '[role="menuitem"], [role="menuitemradio"], [role="menuitemcheckbox"], [role="menubaritem"]';
const CLICKABLE = `button, a, summary, ${MENU_ITEMS}`;

export const menuItemAt = (target: EventTarget | null): Element | null =>
  target instanceof Element ? target.closest(MENU_ITEMS) : null;

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
