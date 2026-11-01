import { hidePointer, markReturnFromSnap, planDevour, planGrains, snapAway } from './snapEffect';

const part = { left: 10, top: 20, width: 100, height: 50, color: '#123', delay: 300 };

describe('planDevour', () => {
  it('reaches every cell of the screen', () => {
    const delays = planDevour(40, 20);

    expect(delays).toHaveLength(800);
    expect(Math.max(...delays)).toBe(1);
    expect(delays.every((delay) => delay >= 0 && delay <= 1)).toBe(true);
  });

  it('eats in parts, not from one side to the other', () => {
    const delays = planDevour(40, 20);
    const leftColumn = delays.filter((_delay, index) => index % 40 === 0);
    const rightColumn = delays.filter((_delay, index) => index % 40 === 39);
    const average = (values: number[]): number => values.reduce((total, value) => total + value, 0) / values.length;

    expect(Math.abs(average(leftColumn) - average(rightColumn))).toBeLessThan(0.5);
  });
});

describe('planGrains', () => {
  it('gives bigger parts more dust, inside their own area', () => {
    const grains = planGrains(part, 1000, () => 0.5);

    expect(grains).toHaveLength(60);
    expect(grains[0]).toMatchObject({ x: 60, y: 45, color: '#123' });
    expect(grains[0].startsAt).toBeGreaterThanOrEqual(300);
  });

  it('never goes over the room left', () => {
    expect(planGrains(part, 7)).toHaveLength(7);
  });

  it('gives a tiny part a few grains, and blows them up and to the right', () => {
    const grains = planGrains({ ...part, width: 2, height: 2 }, 1000);

    expect(grains).toHaveLength(6);
    expect(grains.every((grain) => grain.speedX > 0 && grain.speedY < 0)).toBe(true);
  });
});

describe('snapAway', () => {
  const SNAP_MILLISECONDS = 6000;
  let painted: string[];
  let colors: string[];
  let crumbled: Keyframe[][];

  const fakeCanvasContext = (): CanvasRenderingContext2D =>
    new Proxy(
      {},
      {
        get: (_target, name: string) => () => {
          painted.push(name);
        },
        set: (_target, name: string, value: string) => {
          if (name === 'fillStyle') {
            colors.push(value);
          }

          return true;
        },
      },
    ) as CanvasRenderingContext2D;

  const withMotion = (hasMotion: boolean): void => {
    window.matchMedia = vi.fn().mockReturnValue({ matches: hasMotion });
  };

  const run = async (): Promise<void> => {
    const finished = snapAway();
    await vi.advanceTimersByTimeAsync(SNAP_MILLISECONDS);
    await finished;
  };

  beforeEach(() => {
    vi.useFakeTimers();
    painted = [];
    colors = [];
    crumbled = [];
    document.body.innerHTML =
      '<div id="root"><section class="home-hero"><p>oi</p><button>ok</button><svg></svg></section></div>';
    vi.spyOn(Element.prototype, 'getBoundingClientRect').mockReturnValue(new DOMRect(10, 10, 100, 40));
    vi.spyOn(HTMLCanvasElement.prototype, 'getContext').mockImplementation(() => fakeCanvasContext());
    Element.prototype.animate = vi.fn((frames: Keyframe[]) => {
      crumbled.push(frames);

      return {} as Animation;
    });
  });

  afterEach(() => {
    vi.useRealTimers();
    vi.restoreAllMocks();
    document.body.replaceChildren();
    document.documentElement.classList.remove('snap-running');
  });

  it('crumbles the page, eats the screen and ends in the dark', async () => {
    withMotion(true);
    await run();

    expect(crumbled.length).toBeGreaterThanOrEqual(4);
    expect(document.querySelector('.snap-devour')).not.toBeNull();
    expect(document.querySelector('.snap-dust')).not.toBeNull();
    expect(document.querySelector('.snap-dark')).not.toBeNull();
    expect(painted).toContain('fillRect');
  });

  it('skips the dust without motion and only goes dark', async () => {
    withMotion(false);
    await run();

    expect(crumbled).toEqual([]);
    expect(document.querySelector('.snap-dust')).toBeNull();
    expect(document.querySelector('.snap-dark')).not.toBeNull();
  });

  it('makes the dust of a painted part from its background', async () => {
    withMotion(true);
    document.querySelector<HTMLElement>('.home-hero p')?.style.setProperty('background-color', 'rgb(1, 2, 3)');
    await run();

    expect(colors).toContain('rgb(1, 2, 3)');
  });

  it('still ends in the dark on a browser with no canvas', async () => {
    withMotion(true);
    vi.mocked(HTMLCanvasElement.prototype.getContext).mockReturnValue(null);
    await run();

    expect(painted).toEqual([]);
    expect(document.querySelector('.snap-devour')).not.toBeNull();
    expect(document.querySelector('.snap-dark')).not.toBeNull();
  });

  it('ignores parts outside the screen', async () => {
    withMotion(true);
    vi.mocked(Element.prototype.getBoundingClientRect).mockReturnValue(new DOMRect(10, 99_999, 100, 40));
    await run();

    expect(crumbled).toEqual([]);
  });
});

describe('around the snap', () => {
  it('hides the pointer', () => {
    hidePointer();

    expect(document.documentElement).toHaveClass('snap-running');

    document.documentElement.classList.remove('snap-running');
  });

  it('leaves a note for the page that comes back', () => {
    markReturnFromSnap();

    expect(sessionStorage.getItem('safira.snap.return')).toBe('true');

    sessionStorage.clear();
  });
});
