import { createSoundPlayer, SOUND_FILES, soundForClick } from './sounds';

const fakeNode = () => ({
  connect: vi.fn(),
  start: vi.fn(),
  buffer: null as unknown,
  gain: { value: 0 },
});

const fakeContext = (state = 'running') => {
  const sources: ReturnType<typeof fakeNode>[] = [];

  return {
    state,
    sources,
    destination: {},
    resume: vi.fn(() => Promise.resolve()),
    createGain: vi.fn(fakeNode),
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

  it('uses the sound named by the button', () => {
    expect(clickOn('<button data-sound="delete">Delete</button>', 'button')).toBe('delete');
  });

  it('falls back to the click for an unknown name', () => {
    expect(clickOn('<button data-sound="nada">x</button>', 'button')).toBe('click');
  });

  it('stays silent on plain text', () => {
    expect(clickOn('<p>text</p>', 'p')).toBeNull();
    expect(soundForClick(null)).toBeNull();
  });
});
