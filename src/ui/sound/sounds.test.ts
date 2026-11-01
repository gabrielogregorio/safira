import { clickableAt, createSoundPlayer, isPlainTextField, SOUND_FILES, soundForClick, soundPlayer } from './sounds';

const SLOW_RENDER_MILLISECONDS = 40;

const fakeNode = () => ({
  connect: vi.fn(),
  start: vi.fn(),
  stop: vi.fn(),
  buffer: null as unknown,
  loop: false,
  onended: null as (() => void) | null,
  gain: { value: 0, setTargetAtTime: vi.fn(), setValueAtTime: vi.fn(), linearRampToValueAtTime: vi.fn() },
  playbackRate: { value: 1, setTargetAtTime: vi.fn() },
});

const fakeWave = () => {
  let finish = (): void => undefined;

  return {
    connect: vi.fn(),
    start: vi.fn(),
    stop: vi.fn(),
    type: '',
    frequency: { value: 0 },
    addEventListener: (_name: string, listener: () => void): void => {
      finish = listener;
    },
    end: (): void => {
      finish();
    },
  };
};

const fakeContext = (state = 'running') => {
  const sources: ReturnType<typeof fakeNode>[] = [];
  const gains: ReturnType<typeof fakeNode>[] = [];
  const waves: ReturnType<typeof fakeWave>[] = [];

  return {
    state,
    sources,
    gains,
    waves,
    currentTime: 5,
    destination: {},
    resume: vi.fn(() => Promise.resolve()),
    createGain: vi.fn(() => {
      const gain = fakeNode();
      gains.push(gain);

      return gain;
    }),
    createOscillator: vi.fn(() => {
      const wave = fakeWave();
      waves.push(wave);

      return wave;
    }),
    createBufferSource: vi.fn(() => {
      const source = fakeNode();
      sources.push(source);

      return source;
    }),
    decodeAudioData: vi.fn((data: ArrayBuffer) => Promise.resolve({ decoded: data })),
  };
};

const asContext = (context: ReturnType<typeof fakeContext>): AudioContext => context as unknown as AudioContext;

describe('createSoundPlayer', () => {
  beforeEach(() => {
    vi.stubGlobal(
      'fetch',
      vi.fn(() => Promise.resolve({ arrayBuffer: () => Promise.resolve(new ArrayBuffer(1)) })),
    );
  });

  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it('plays the recorded file of the sound', async () => {
    const context = fakeContext();
    await createSoundPlayer(() => asContext(context)).play('delete');

    expect(fetch).toHaveBeenCalledWith(SOUND_FILES.delete);
    expect(context.sources[0]?.start).toHaveBeenCalled();
    expect(context.sources[0]?.buffer).toBeTruthy();
  });

  it('downloads each file only once', async () => {
    const player = createSoundPlayer(() => asContext(fakeContext()));
    await player.play('click');
    await player.play('click');

    expect(fetch).toHaveBeenCalledTimes(1);
  });

  it('prepares every file on the first press', () => {
    createSoundPlayer(() => asContext(fakeContext())).prepare();

    expect(fetch).toHaveBeenCalledTimes(Object.keys(SOUND_FILES).length);
  });

  it('prepares nothing when disabled', () => {
    const player = createSoundPlayer(() => asContext(fakeContext()));
    player.setEnabled(false);
    player.prepare();

    expect(fetch).not.toHaveBeenCalled();
  });

  it('does not create the audio context until it is needed', () => {
    const create = vi.fn(() => asContext(fakeContext()));
    createSoundPlayer(create);

    expect(create).not.toHaveBeenCalled();
  });

  it('stays silent when disabled and speaks again when enabled', async () => {
    const context = fakeContext();
    const player = createSoundPlayer(() => asContext(context));
    player.setEnabled(false);
    await player.play('click');

    expect(context.sources).toHaveLength(0);

    player.setEnabled(true);
    await player.play('click');

    expect(context.sources).toHaveLength(1);
  });

  it('wakes a suspended context', async () => {
    const context = fakeContext('suspended');
    await createSoundPlayer(() => asContext(context)).play('toggle');

    expect(context.resume).toHaveBeenCalled();
  });

  it('does nothing in a browser without audio', async () => {
    await expect(createSoundPlayer(() => null).play('create')).resolves.toBeUndefined();
  });

  it('lets the click step aside for the modal that it opens', async () => {
    const context = fakeContext();
    const player = createSoundPlayer(() => asContext(context));
    await Promise.all([player.play('click'), player.play('modalOpen')]);

    expect(fetch).toHaveBeenCalledExactlyOnceWith(SOUND_FILES.modalOpen);
    expect(context.sources).toHaveLength(1);
  });

  it('lets the click step aside even when the modal takes long to render', async () => {
    const context = fakeContext();
    const player = createSoundPlayer(() => asContext(context));
    const click = player.play('click');
    const renderStart = performance.now();

    // A render blocks the page, so the timer of the click runs late, right before the sound of the modal.
    while (performance.now() - renderStart < SLOW_RENDER_MILLISECONDS) {
      // Holds the thread, as a slow render does.
    }

    await Promise.all([click, player.play('modalOpen')]);

    expect(fetch).toHaveBeenCalledExactlyOnceWith(SOUND_FILES.modalOpen);
    expect(context.sources).toHaveLength(1);
  });

  it('lets the sound of the menu step aside for the modal that an item opens', async () => {
    const context = fakeContext();
    const player = createSoundPlayer(() => asContext(context));
    await Promise.all([player.play('menuClick'), player.play('modalOpen')]);

    expect(fetch).toHaveBeenCalledExactlyOnceWith(SOUND_FILES.modalOpen);
  });

  it('plays the closing sound, not the click, on the button that closes a modal', async () => {
    const context = fakeContext();
    const player = createSoundPlayer(() => asContext(context));
    await Promise.all([player.play('click'), player.play('modalClose')]);

    expect(fetch).toHaveBeenCalledExactlyOnceWith(SOUND_FILES.modalClose);
  });

  it('keeps only the delete sound when deleting also closes the modal', async () => {
    const context = fakeContext();
    const player = createSoundPlayer(() => asContext(context));
    await Promise.all([player.play('modalClose'), player.play('delete'), player.play('click')]);

    expect(fetch).toHaveBeenCalledExactlyOnceWith(SOUND_FILES.delete);
  });

  it('plays the same sound once per gesture', async () => {
    const context = fakeContext();
    const player = createSoundPlayer(() => asContext(context));
    await Promise.all([player.play('modalOpen'), player.play('modalOpen')]);

    expect(context.sources).toHaveLength(1);
  });

  it('plays again on the next gesture', async () => {
    const context = fakeContext();
    const player = createSoundPlayer(() => asContext(context));
    const now = vi.spyOn(performance, 'now').mockReturnValue(1000);
    await player.play('click');
    now.mockReturnValue(2000);
    await player.play('click');
    now.mockRestore();

    expect(context.sources).toHaveLength(2);
  });

  it('cuts the previous language when the next one starts', async () => {
    const context = fakeContext();
    const player = createSoundPlayer(() => asContext(context));
    await player.play('languageEnUs');
    await player.play('languagePtBr');

    expect(context.sources[0]?.stop).toHaveBeenCalled();
    expect(context.sources[1]?.start).toHaveBeenCalled();
    expect(context.sources[1]?.stop).not.toHaveBeenCalled();
  });

  it('tells the page while a language sound plays', async () => {
    const player = createSoundPlayer(() => asContext(fakeContext()));
    await player.play('languagePtBr');

    expect(document.documentElement.dataset['languageSound']).toBe('playing');
  });

  it('skips a language that is overtaken while its file loads', async () => {
    const context = fakeContext();
    const player = createSoundPlayer(() => asContext(context));
    let finishFirstLoad = (): void => undefined;
    vi.mocked(fetch).mockImplementationOnce(
      () =>
        new Promise((resolve) => {
          finishFirstLoad = () => {
            resolve({ arrayBuffer: () => Promise.resolve(new ArrayBuffer(1)) } as Response);
          };
        }),
    );
    const first = player.play('languageEnUs');
    await vi.waitFor(() => {
      expect(fetch).toHaveBeenCalled();
    });
    await player.play('languagePtBr');
    finishFirstLoad();
    await first;

    expect(context.sources[0]?.start).not.toHaveBeenCalled();
    expect(context.sources[1]?.start).toHaveBeenCalled();
  });

  it('survives a file that fails to load and tries again later', async () => {
    const context = fakeContext();
    const player = createSoundPlayer(() => asContext(context));
    const now = vi.spyOn(performance, 'now').mockReturnValue(1000);
    vi.mocked(fetch).mockRejectedValueOnce(new Error('offline'));

    await expect(player.play('click')).resolves.toBeUndefined();
    now.mockReturnValue(2000);
    await player.play('click');
    now.mockRestore();

    expect(context.sources[1]?.start).toHaveBeenCalled();
  });

  it('tries again later a file that failed while preparing', async () => {
    const player = createSoundPlayer(() => asContext(fakeContext()));
    const fileCount = Object.keys(SOUND_FILES).length;
    vi.mocked(fetch).mockRejectedValueOnce(new Error('offline'));
    player.prepare();
    await new Promise((resolve) => {
      setTimeout(resolve);
    });
    player.prepare();

    expect(fetch).toHaveBeenCalledTimes(fileCount + 1);
  });

  it('ends the signal of the language sound when it ends', async () => {
    const context = fakeContext();
    await createSoundPlayer(() => asContext(context)).play('languagePtBr');
    context.sources[0]?.onended?.();

    expect(document.documentElement.dataset['languageSound']).toBeUndefined();
  });

  it('keeps the signal when an older language ends after a newer one took over', async () => {
    const context = fakeContext();
    const player = createSoundPlayer(() => asContext(context));
    await player.play('languageEnUs');
    await player.play('languagePtBr');
    context.sources[0]?.onended?.();

    expect(document.documentElement.dataset['languageSound']).toBe('playing');

    context.sources[1]?.onended?.();

    expect(document.documentElement.dataset['languageSound']).toBeUndefined();
  });

  it('cuts what is already playing when muted, and brings it back when enabled', async () => {
    const context = fakeContext();
    const player = createSoundPlayer(() => asContext(context));
    await player.play('click');
    const [output] = context.gains;
    player.setEnabled(false);

    expect(output?.gain.setTargetAtTime).toHaveBeenLastCalledWith(0, 5, 0.01);

    player.setEnabled(true);

    expect(output?.gain.setTargetAtTime).toHaveBeenLastCalledWith(0.5, 5, 0.01);
  });

  it.each(['hover', 'hoverSpecial', 'ideOpen'] as const)('holds back %s until a first press', async (name) => {
    const create = vi.fn(() => asContext(fakeContext()));
    await createSoundPlayer(create).play(name);

    expect(create).not.toHaveBeenCalled();
    expect(fetch).not.toHaveBeenCalled();
  });

  it('keeps a small gap between hovers once the audio is awake', async () => {
    const context = fakeContext();
    const player = createSoundPlayer(() => asContext(context));
    const now = vi.spyOn(performance, 'now').mockReturnValue(1000);
    await player.play('click');
    await player.play('hover');
    await player.play('hover');

    expect(context.sources).toHaveLength(2);

    now.mockReturnValue(1100);
    await player.play('hover');
    now.mockRestore();

    expect(context.sources).toHaveLength(3);
  });

  it('does not count typing as a gesture, so the click that follows still sounds', async () => {
    const context = fakeContext();
    const player = createSoundPlayer(() => asContext(context));
    const now = vi.spyOn(performance, 'now').mockReturnValue(1000);
    await player.play('typing');
    await player.play('click');
    now.mockRestore();

    expect(context.sources).toHaveLength(2);
  });

  describe('hold', () => {
    it('loops the sound at the rate asked, fading in', async () => {
      const context = fakeContext();
      await createSoundPlayer(() => asContext(context)).hold('waterHold', 1.2);
      const [source] = context.sources;

      expect(source?.loop).toBe(true);
      expect(source?.start).toHaveBeenCalledTimes(1);
      expect(source?.playbackRate.setTargetAtTime).toHaveBeenCalledWith(1.2, 5, 0.05);
      expect(context.gains[1]?.gain.setTargetAtTime).toHaveBeenCalledWith(0.35, 5, 0.04);
    });

    it('takes a volume of its own', async () => {
      const context = fakeContext();
      await createSoundPlayer(() => asContext(context)).hold('seaLight', 1, 0.48);

      expect(context.gains[1]?.gain.setTargetAtTime).toHaveBeenCalledWith(0.48, 5, 0.04);
    });

    it('moves the sound that is playing instead of starting another', async () => {
      const context = fakeContext();
      const player = createSoundPlayer(() => asContext(context));
      await player.hold('waterHold', 1);
      await player.hold('waterHold', 2);

      expect(context.sources).toHaveLength(1);
      expect(context.sources[0]?.playbackRate.setTargetAtTime).toHaveBeenLastCalledWith(2, 5, 0.05);
    });

    it('starts only one sound while the file is still loading', async () => {
      const context = fakeContext();
      const player = createSoundPlayer(() => asContext(context));
      await Promise.all([player.hold('waterHold', 1), player.hold('waterHold', 1)]);

      expect(context.sources).toHaveLength(1);
      expect(fetch).toHaveBeenCalledTimes(1);
    });

    it('fades out and stops on release', async () => {
      const context = fakeContext();
      const player = createSoundPlayer(() => asContext(context));
      await player.hold('waterHold', 1);
      player.release();

      expect(context.gains[1]?.gain.setTargetAtTime).toHaveBeenLastCalledWith(0, 5, 0.02);
      expect(context.sources[0]?.stop).toHaveBeenCalledExactlyOnceWith(5.1);
    });

    it('stops when the sound is turned off', async () => {
      const context = fakeContext();
      const player = createSoundPlayer(() => asContext(context));
      await player.hold('waterHold', 1);
      player.setEnabled(false);

      expect(context.sources[0]?.stop).toHaveBeenCalled();
    });

    it('stops at once when the press ends while the file loads', async () => {
      const context = fakeContext();
      const player = createSoundPlayer(() => asContext(context));
      const holding = player.hold('waterHold', 1);
      player.release();
      await holding;

      expect(context.sources[0]?.start).toHaveBeenCalled();
      expect(context.sources[0]?.stop).toHaveBeenCalled();
    });

    it('stops at once when the sound is turned off while the file loads', async () => {
      const context = fakeContext();
      const player = createSoundPlayer(() => asContext(context));
      const holding = player.hold('waterHold', 1);
      player.setEnabled(false);
      await holding;

      expect(context.sources[0]?.stop).toHaveBeenCalled();
    });

    it('wakes a suspended context', async () => {
      const context = fakeContext('suspended');
      await createSoundPlayer(() => asContext(context)).hold('waterHold', 1);

      expect(context.resume).toHaveBeenCalled();
    });

    it('stays silent when disabled and in a browser without audio', async () => {
      const context = fakeContext();
      const player = createSoundPlayer(() => asContext(context));
      player.setEnabled(false);
      await player.hold('waterHold', 1);

      expect(context.sources).toHaveLength(0);
      await expect(createSoundPlayer(() => null).hold('waterHold', 1)).resolves.toBeUndefined();
    });

    it('survives a file that fails to load and tries again later', async () => {
      const context = fakeContext();
      const player = createSoundPlayer(() => asContext(context));
      vi.mocked(fetch).mockRejectedValueOnce(new Error('offline'));

      await expect(player.hold('waterHold', 1)).resolves.toBeUndefined();
      expect(context.sources[0]?.start).not.toHaveBeenCalled();

      await player.hold('waterHold', 1);

      expect(context.sources[1]?.start).toHaveBeenCalled();
    });
  });

  describe('tone', () => {
    it('rings two waves an octave apart, through the master volume', () => {
      const context = fakeContext();
      createSoundPlayer(() => asContext(context)).tone(440, 1000);
      const [output, envelope] = context.gains;

      expect(context.waves.map((wave) => [wave.type, wave.frequency.value])).toEqual([
        ['triangle', 440],
        ['sine', 880],
      ]);
      expect(envelope?.connect).toHaveBeenCalledWith(output);
      expect(context.waves[0]?.connect).toHaveBeenCalledWith(envelope);
      expect(context.waves[0]?.start).toHaveBeenCalledWith(5);
      expect(context.waves[0]?.stop).toHaveBeenCalledWith(6.06);
    });

    it.each([
      [0, 100],
      [-1, 100],
      [440, 0],
      [440, -1],
    ])('ignores a note of frequency %d and length %d', (frequency, milliseconds) => {
      const context = fakeContext();
      createSoundPlayer(() => asContext(context)).tone(frequency, milliseconds);

      expect(context.waves).toEqual([]);
    });

    it('stays silent when disabled and in a browser without audio', () => {
      const context = fakeContext();
      const player = createSoundPlayer(() => asContext(context));
      player.setEnabled(false);
      player.tone(440, 100);

      expect(context.waves).toEqual([]);
      expect(() => {
        createSoundPlayer(() => null).tone(440, 100);
      }).not.toThrow();
    });

    it('stops the notes still ringing, but not the ones that already ended', () => {
      const context = fakeContext();
      const player = createSoundPlayer(() => asContext(context));
      player.tone(440, 100);
      const [ended, ringing] = context.waves;
      ended?.end();
      player.stopTones();

      expect(ended?.stop).toHaveBeenCalledTimes(1);
      expect(ringing?.stop).toHaveBeenCalledTimes(2);
    });
  });

  it('uses the audio of the browser in the shared player', () => {
    const context = fakeContext();
    vi.stubGlobal(
      'AudioContext',
      vi.fn(function fakeAudioContext() {
        return context;
      }),
    );
    soundPlayer.tone(440, 100);

    expect(context.waves).toHaveLength(2);
  });
});

describe('isPlainTextField', () => {
  const fieldOf = (html: string): Element | null => {
    document.body.innerHTML = html;

    return document.body.firstElementChild;
  };

  it('accepts the text inputs with no sound of their own', () => {
    expect(isPlainTextField(fieldOf('<input>'))).toBe(true);
    expect(isPlainTextField(fieldOf('<input type="text">'))).toBe(true);
    expect(isPlainTextField(fieldOf('<input type="search">'))).toBe(true);
  });

  it('refuses the rest', () => {
    expect(isPlainTextField(fieldOf('<input type="checkbox">'))).toBe(false);
    expect(isPlainTextField(fieldOf('<input data-sound="terminalTyping">'))).toBe(false);
    expect(isPlainTextField(fieldOf('<textarea></textarea>'))).toBe(false);
    expect(isPlainTextField(null)).toBe(false);
  });
});

describe('clickableAt', () => {
  const clickableIn = (html: string, selector: string) => {
    document.body.innerHTML = html;

    return clickableAt(document.querySelector(selector));
  };

  it('finds the clickable around the target', () => {
    expect(clickableIn('<button id="run"><span>Run</span></button>', 'span')?.id).toBe('run');
  });

  it('finds nothing on plain text or without a target', () => {
    expect(clickableIn('<p>text</p>', 'p')).toBeNull();
    expect(clickableAt(null)).toBeNull();
  });

  it('skips what is disabled', () => {
    expect(clickableIn('<button disabled>Run</button>', 'button')).toBeNull();
    expect(clickableIn('<div role="menuitem" aria-disabled="true">Save</div>', 'div')).toBeNull();
  });
});

describe('soundForClick', () => {
  const clickOn = (html: string, selector: string) => {
    document.body.innerHTML = html;

    return soundForClick(document.querySelector(selector));
  };

  it('clicks on buttons, links and menu items, also from inside them', () => {
    expect(clickOn('<button><span>Run</span></button>', 'span')).toBe('click');
    expect(clickOn('<a href="#/">Home</a>', 'a')).toBe('click');
    expect(clickOn('<div role="menuitem">Save</div>', 'div')).toBe('click');
  });

  it('stays quiet on a button whose result has its own sound', () => {
    expect(clickOn('<button data-sound="none">Create</button>', 'button')).toBeNull();
  });

  it('uses the sound named by the button', () => {
    expect(clickOn('<button data-sound="delete">Delete</button>', 'button')).toBe('delete');
  });

  it('falls back to the click for an unknown name', () => {
    expect(clickOn('<button data-sound="nada">x</button>', 'button')).toBe('click');
  });

  it('sounds like the terminal on a text field', () => {
    expect(clickOn('<input type="text">', 'input')).toBe('terminalFocus');
  });

  it('stays silent on plain text', () => {
    expect(clickOn('<p>text</p>', 'p')).toBeNull();
    expect(soundForClick(null)).toBeNull();
  });
});
