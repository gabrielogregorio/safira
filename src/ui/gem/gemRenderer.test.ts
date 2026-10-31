import { startGem } from './gemRenderer';

const fakeContext = (overrides: Record<string, unknown> = {}): WebGL2RenderingContext =>
  new Proxy(overrides, {
    get: (target, name: string) => {
      if (name in target) {
        return target[name];
      }

      return name === name.toUpperCase() ? name : () => true;
    },
  }) as unknown as WebGL2RenderingContext;

const canvasWith = (context: WebGL2RenderingContext | null): HTMLCanvasElement => {
  const canvas = document.createElement('canvas');
  vi.spyOn(canvas, 'getContext').mockReturnValue(context);

  return canvas;
};

describe('startGem', () => {
  beforeEach(() => {
    vi.spyOn(window, 'requestAnimationFrame').mockReturnValue(1);
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  it('gives up without WebGL 2', () => {
    expect(startGem(canvasWith(null), { size: 40, animate: true, onLost: vi.fn() })).toBeNull();
  });

  it('gives up when a shader does not compile', () => {
    const context = fakeContext({ getShaderParameter: () => false });

    expect(startGem(canvasWith(context), { size: 40, animate: true, onLost: vi.fn() })).toBeNull();
  });

  it('gives up when the program does not link', () => {
    const context = fakeContext({ getProgramParameter: () => false });

    expect(startGem(canvasWith(context), { size: 40, animate: true, onLost: vi.fn() })).toBeNull();
  });

  it('draws one still frame when animation is off', () => {
    const drawArrays = vi.fn();
    const stop = startGem(canvasWith(fakeContext({ drawArrays })), { size: 40, animate: false, onLost: vi.fn() });

    expect(drawArrays).toHaveBeenCalledTimes(2);
    expect(window.requestAnimationFrame).not.toHaveBeenCalled();

    stop?.();
  });

  it('follows the mouse only while running', () => {
    const add = vi.spyOn(window, 'addEventListener');
    const remove = vi.spyOn(window, 'removeEventListener');
    const stop = startGem(canvasWith(fakeContext()), { size: 40, animate: true, onLost: vi.fn() });
    window.dispatchEvent(new MouseEvent('pointermove', { clientX: 10, clientY: 10 }));

    expect(add).toHaveBeenCalledWith('pointermove', expect.any(Function), { passive: true });

    stop?.();

    expect(remove).toHaveBeenCalledWith('pointermove', expect.any(Function));
  });

  describe('frame rate', () => {
    const NOW = 1_000_000;
    let frames: FrameRequestCallback[];
    let drawArrays: ReturnType<typeof vi.fn>;
    let stop: (() => void) | null;

    const passes = (): number => drawArrays.mock.calls.length / 2;

    beforeEach(() => {
      frames = [];
      drawArrays = vi.fn();
      vi.spyOn(window, 'requestAnimationFrame').mockImplementation((callback) => frames.push(callback));
      vi.spyOn(performance, 'now').mockReturnValue(NOW);
      vi.spyOn(document, 'hasFocus').mockReturnValue(true);
      stop = startGem(canvasWith(fakeContext({ drawArrays })), { size: 40, animate: true, onLost: vi.fn() });
    });

    afterEach(() => {
      stop?.();
    });

    it('draws at about 15 frames per second when nobody moves the mouse', () => {
      frames.at(-1)?.(NOW + 16);
      frames.at(-1)?.(NOW + 50);

      expect(passes()).toBe(0);

      frames.at(-1)?.(NOW + 70);

      expect(passes()).toBe(1);
    });

    it('draws at about 30 frames per second while following the mouse', () => {
      window.dispatchEvent(new MouseEvent('pointermove', { clientX: 10, clientY: 10 }));
      frames.at(-1)?.(NOW + 16);

      expect(passes()).toBe(0);

      frames.at(-1)?.(NOW + 34);

      expect(passes()).toBe(1);
    });

    it('rests when the window loses the focus, and keeps checking', () => {
      vi.mocked(document.hasFocus).mockReturnValue(false);
      const waiting = frames.length;
      frames.at(-1)?.(NOW + 1000);

      expect(passes()).toBe(0);
      expect(frames).toHaveLength(waiting + 1);
    });
  });

  it('reports a lost context', () => {
    const onLost = vi.fn();
    const canvas = canvasWith(fakeContext());
    const stop = startGem(canvas, { size: 40, animate: true, onLost });
    canvas.dispatchEvent(new Event('webglcontextlost'));

    expect(onLost).toHaveBeenCalled();

    stop?.();
  });
});
