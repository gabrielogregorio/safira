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

  it('keeps drawing on each frame', () => {
    const drawArrays = vi.fn();
    const frames: FrameRequestCallback[] = [];
    vi.spyOn(window, 'requestAnimationFrame').mockImplementation((callback) => frames.push(callback));
    const stop = startGem(canvasWith(fakeContext({ drawArrays })), { size: 40, animate: true, onLost: vi.fn() });
    frames[0]?.(performance.now() + 16);

    expect(drawArrays).toHaveBeenCalledTimes(2);

    stop?.();
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
