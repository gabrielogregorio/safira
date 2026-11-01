import { prefersMotion } from '@/ui/motion';

export interface DustGrain {
  x: number;
  y: number;
  speedX: number;
  speedY: number;
  size: number;
  startsAt: number;
  lasts: number;
  color: string;
}

export interface Crumbling {
  left: number;
  top: number;
  width: number;
  height: number;
  color: string;
  delay: number;
}

const MOST_ELEMENTS = 160;
const MOST_GRAINS = 3200;
const GRAINS_PER_SQUARE_PIXEL = 0.012;
const FEWEST_GRAINS = 6;
const LONGEST_DELAY_MILLISECONDS = 1700;
const FADE_MILLISECONDS = 800;
const DARK_FADE_MILLISECONDS = 300;
const DUST_MILLISECONDS = 4200;
const MILLISECONDS_PER_SECOND = 1000;
const RETURN_KEY = 'safira.snap.return';
const CELL_PIXELS = 18;
const DEVOUR_MILLISECONDS = 2600;
const HOLE_COUNT = 16;
const DELAY_NOISE = 0.14;
const GRAINS_PER_CELL = 0.5;

const CONTAINERS = '.home-hero, .home-section, .modal, .scenery';

const isPainted = (color: string): boolean => color !== 'transparent' && color !== 'rgba(0, 0, 0, 0)';

/**
 * When each cell of the screen goes black. Holes open at random places and grow until they meet,
 * so the whole screen is eaten in parts and nothing is left. Values go from 0 to 1.
 */
export const planDevour = (columns: number, rows: number, random: () => number = Math.random): number[] => {
  const holes = Array.from({ length: HOLE_COUNT }, () => ({ x: random() * columns, y: random() * rows }));
  const distances = Array.from({ length: columns * rows }, (_cell, index) => {
    const x = index % columns;
    const y = Math.floor(index / columns);

    return Math.min(...holes.map((hole) => Math.hypot(hole.x - x, hole.y - y))) + random() * DELAY_NOISE * columns;
  });
  const farthest = Math.max(...distances, 1);

  return distances.map((distance) => distance / farthest);
};

/** Grains for one part of the page. Pure, so the amounts can be tested without a canvas. */
export const planGrains = (part: Crumbling, room: number, random: () => number = Math.random): DustGrain[] => {
  const wanted = Math.max(FEWEST_GRAINS, Math.round(part.width * part.height * GRAINS_PER_SQUARE_PIXEL));

  return Array.from({ length: Math.min(wanted, room) }, () => ({
    x: part.left + random() * part.width,
    y: part.top + random() * part.height,
    speedX: 30 + random() * 120,
    speedY: -30 - random() * 70,
    size: 1 + random() * 2.4,
    startsAt: part.delay + random() * FADE_MILLISECONDS,
    lasts: 800 + random() * 900,
    color: part.color,
  }));
};

const isVisible = (box: DOMRect): boolean =>
  box.width > 0 && box.height > 0 && box.bottom > 0 && box.top < window.innerHeight;

const shuffled = <Item>(items: Item[]): Item[] =>
  items
    .map((item) => ({ item, order: Math.random() }))
    .sort((first, second) => first.order - second.order)
    .map(({ item }) => item);

// Small pieces go first, in a random order, and the panels that hold them go last.
const pickParts = (): { element: Element; part: Crumbling }[] => {
  const leaves = [...document.querySelectorAll('#root *, .modal *')].filter(
    (element) => element.children.length === 0 && element.closest('svg') === null,
  );
  const whole = [...document.querySelectorAll('svg')].filter((svg) => svg.closest('.scenery') === null);
  const panels = [...document.querySelectorAll(CONTAINERS)];
  const toPart = (element: Element, firstDelay: number, spread: number) => {
    const box = element.getBoundingClientRect();
    const style = getComputedStyle(element);

    return {
      element,
      box,
      part: {
        left: box.left,
        top: box.top,
        width: box.width,
        height: box.height,
        color: isPainted(style.backgroundColor) ? style.backgroundColor : style.color,
        delay: firstDelay + Math.random() * spread,
      },
    };
  };

  return [
    ...shuffled([...leaves, ...whole])
      .slice(0, MOST_ELEMENTS)
      .map((element) => toPart(element, 0, LONGEST_DELAY_MILLISECONDS)),
    ...panels.map((element) => toPart(element, LONGEST_DELAY_MILLISECONDS / 2, LONGEST_DELAY_MILLISECONDS / 2)),
  ].filter(({ box }) => isVisible(box));
};

const crumble = ({ element, part }: { element: Element; part: Crumbling }): void => {
  element.animate(
    [
      { opacity: 1, filter: 'blur(0)', transform: 'translate(0, 0)' },
      { opacity: 0, filter: 'blur(5px)', transform: 'translate(26px, -16px)' },
    ],
    { duration: FADE_MILLISECONDS, delay: part.delay, easing: 'ease-in', fill: 'forwards' },
  );
};

const blowDust = (grains: DustGrain[]): void => {
  const canvas = document.createElement('canvas');
  canvas.className = 'snap-dust';
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;
  document.body.append(canvas);
  const context = canvas.getContext('2d');
  const startedAt = performance.now();

  const draw = (now: number): void => {
    const elapsed = now - startedAt;

    if (context === null || elapsed > DUST_MILLISECONDS) {
      return;
    }

    context.clearRect(0, 0, canvas.width, canvas.height);

    for (const grain of grains) {
      const age = elapsed - grain.startsAt;

      if (age > 0 && age < grain.lasts) {
        const seconds = age / MILLISECONDS_PER_SECOND;
        context.globalAlpha = 1 - age / grain.lasts;
        context.fillStyle = grain.color;
        context.fillRect(grain.x + grain.speedX * seconds, grain.y + grain.speedY * seconds, grain.size, grain.size);
      }
    }

    requestAnimationFrame(draw);
  };

  requestAnimationFrame(draw);
};

const skyGrainColors = (): string[] => {
  const style = getComputedStyle(document.documentElement);

  return ['--color-accent', '--color-border', '--color-text'].map((name) => style.getPropertyValue(name).trim());
};

// The sky and everything else behind the panels goes too: a black canvas eats the screen cell by cell.
const devourScreen = (): DustGrain[] => {
  const canvas = document.createElement('canvas');
  canvas.className = 'snap-devour';
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;
  document.body.append(canvas);
  const context = canvas.getContext('2d');
  const columns = Math.ceil(canvas.width / CELL_PIXELS);
  const rows = Math.ceil(canvas.height / CELL_PIXELS);
  const delays = planDevour(columns, rows).map((delay) => delay * DEVOUR_MILLISECONDS);
  const cells = delays
    .map((delay, index) => ({
      delay,
      x: (index % columns) * CELL_PIXELS,
      y: Math.floor(index / columns) * CELL_PIXELS,
    }))
    .sort((first, second) => first.delay - second.delay);
  const startedAt = performance.now();
  let next = 0;

  const draw = (now: number): void => {
    if (context === null) {
      return;
    }

    context.fillStyle = '#000000';

    while (next < cells.length && cells[next].delay <= now - startedAt) {
      context.fillRect(cells[next].x, cells[next].y, CELL_PIXELS, CELL_PIXELS);
      next += 1;
    }

    if (next < cells.length) {
      requestAnimationFrame(draw);
    }
  };

  requestAnimationFrame(draw);
  const colors = skyGrainColors();

  return cells
    .filter(() => Math.random() < GRAINS_PER_CELL)
    .flatMap((cell, index) =>
      planGrains(
        {
          left: cell.x,
          top: cell.y,
          width: CELL_PIXELS,
          height: CELL_PIXELS,
          color: colors[index % colors.length],
          delay: cell.delay,
        },
        1,
      ),
    );
};

const wait = (milliseconds: number): Promise<void> =>
  new Promise((resolve) => {
    setTimeout(resolve, milliseconds);
  });

const fallIntoTheDark = async (): Promise<void> => {
  const dark = document.createElement('div');
  dark.className = 'snap-dark';
  document.body.append(dark);
  await wait(DARK_FADE_MILLISECONDS);
};

/** Everything on the screen turns to dust in parts, and only black is left. */
export const snapAway = async (): Promise<void> => {
  if (prefersMotion()) {
    const parts = pickParts();
    let room = MOST_GRAINS;
    const grains = parts.flatMap(({ part }) => {
      const planned = planGrains(part, room);
      room -= planned.length;

      return planned;
    });

    parts.forEach(crumble);
    blowDust([...grains, ...devourScreen()]);
    await wait(DEVOUR_MILLISECONDS);
  }

  await fallIntoTheDark();
};

/** The pointer goes with everything else, and comes back when the new screen starts to appear. */
export const hidePointer = (): void => {
  document.documentElement.classList.add('snap-running');
};

/** The reload comes back in the dark, and `index.html` reads this before anything is painted. */
export const markReturnFromSnap = (): void => {
  try {
    sessionStorage.setItem(RETURN_KEY, 'true');
  } catch {
    // Without storage the page only skips the fade in.
  }
};
