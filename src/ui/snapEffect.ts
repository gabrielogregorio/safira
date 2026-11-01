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
const DARK_FADE_MILLISECONDS = 700;
const DUST_MILLISECONDS = 3000;
const MILLISECONDS_PER_SECOND = 1000;
const RETURN_KEY = 'safira.snap.return';

const CONTAINERS = '.home-hero, .home-section, .modal, .scenery';

const isPainted = (color: string): boolean => color !== 'transparent' && color !== 'rgba(0, 0, 0, 0)';

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

/** Half of everything turns to dust, then the other half, and the screen goes dark. */
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
    blowDust(grains);
    await wait(LONGEST_DELAY_MILLISECONDS + FADE_MILLISECONDS);
  }

  await fallIntoTheDark();
};

/** The reload comes back in the dark, and `index.html` reads this before anything is painted. */
export const markReturnFromSnap = (): void => {
  try {
    sessionStorage.setItem(RETURN_KEY, 'true');
  } catch {
    // Without storage the page only skips the fade in.
  }
};
