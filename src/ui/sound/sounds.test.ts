import { createSoundPlayer, SOUND_RECIPES, soundForClick } from './sounds';

const fakeParam = () => ({
  value: 0,
  setValueAtTime: vi.fn(),
  exponentialRampToValueAtTime: vi.fn(),
});

const fakeNode = () => ({
  connect: vi.fn((next: unknown) => next),
  start: vi.fn(),
  stop: vi.fn(),
  type: '',
  buffer: null,
  frequency: fakeParam(),
  gain: fakeParam(),
});

const fakeContext = (state = 'running') => ({
  state,
  currentTime: 2,
  sampleRate: 100,
  destination: fakeNode(),
  resume: vi.fn(() => Promise.resolve()),
  createGain: vi.fn(fakeNode),
  createOscillator: vi.fn(fakeNode),
  createBufferSource: vi.fn(fakeNode),
  createBiquadFilter: vi.fn(fakeNode),
  createBuffer: vi.fn(() => ({ getChannelData: () => new Float32Array(30) })),
});

const asContext = (context: ReturnType<typeof fakeContext>): AudioContext => context as unknown as AudioContext;

describe('createSoundPlayer', () => {
  it('plays every tone and noise burst of a sound', () => {
    const context = fakeContext();
    createSoundPlayer(() => asContext(context)).play('delete');

    expect(context.createOscillator).toHaveBeenCalledTimes(SOUND_RECIPES.delete.tones.length);
    expect(context.createBufferSource).toHaveBeenCalledTimes(SOUND_RECIPES.delete.noise.length);
  });

  it('does not create the audio context until the first sound', () => {
    const create = vi.fn(() => asContext(fakeContext()));
    const player = createSoundPlayer(create);

    expect(create).not.toHaveBeenCalled();

    player.play('click');
    player.play('click');

    expect(create).toHaveBeenCalledTimes(1);
  });

  it('stays silent when disabled and speaks again when enabled', () => {
    const context = fakeContext();
    const player = createSoundPlayer(() => asContext(context));
    player.setEnabled(false);
    player.play('click');

    expect(context.createOscillator).not.toHaveBeenCalled();

    player.setEnabled(true);
    player.play('click');

    expect(context.createOscillator).toHaveBeenCalled();
  });

  it('wakes a suspended context', () => {
    const context = fakeContext('suspended');
    createSoundPlayer(() => asContext(context)).play('toggle');

    expect(context.resume).toHaveBeenCalled();
  });

  it('does nothing in a browser without audio', () => {
    expect(() => {
      createSoundPlayer(() => null).play('create');
    }).not.toThrow();
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
