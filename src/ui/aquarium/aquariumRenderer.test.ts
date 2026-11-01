import { THEME_IDS } from '@/settings/settings';
import { createPopulation, createWorld, pressPointer, stepWorld, warmUpWorld } from './aquariumWorld';
import { drawWorld, easePalette, startingPalette } from './aquariumRenderer';

const WIDTH = 800;
const HEIGHT = 500;
const STEP_SECONDS = 1 / 30;
const STEPS = 90;

interface FakeCanvas {
  context: CanvasRenderingContext2D;
  calls: string[];
  styles: string[];
}

const fakeCanvas = (): FakeCanvas => {
  const calls: string[] = [];
  const styles: string[] = [];
  const gradient = { addColorStop: (_offset: number, color: string) => styles.push(color) };
  const context = new Proxy(
    {},
    {
      get:
        (_target, name: string) =>
        (...values: unknown[]) => {
          calls.push(name);

          return name.startsWith('create') ? gradient : values[0];
        },
      set: (_target, name: string, value: unknown) => {
        if (typeof value === 'string' && name.endsWith('Style')) {
          styles.push(value);
        }

        return true;
      },
    },
  ) as CanvasRenderingContext2D;

  return { context, calls, styles };
};

const busyWorld = () => {
  const world = createWorld(createPopulation(), WIDTH, HEIGHT);
  warmUpWorld(world);
  pressPointer(world, WIDTH / 2, HEIGHT / 2);

  for (let step = 0; step < STEPS; step += 1) {
    stepWorld(world, STEP_SECONDS);
  }

  return world;
};

describe('aquarium drawing', () => {
  it('draws the water, the plants and every fish', () => {
    const { context, calls } = fakeCanvas();
    const world = busyWorld();
    drawWorld(context, world, startingPalette('light'));

    expect(calls).toContain('fillRect');
    expect(calls).toContain('quadraticCurveTo');
    expect(calls.filter((name) => name === 'save').length).toBeGreaterThanOrEqual(world.fishes.length);
    expect(calls.filter((name) => name === 'save')).toHaveLength(calls.filter((name) => name === 'restore').length);
  });

  it.each(THEME_IDS)('paints valid colors in the %s theme', (theme) => {
    const { context, styles } = fakeCanvas();
    drawWorld(context, busyWorld(), startingPalette(theme));

    expect(styles.length).toBeGreaterThan(0);
    expect(styles.filter((style) => style.includes('NaN') || style.includes('undefined'))).toEqual([]);
  });

  it('draws each piece of food and six fading sparks for each pop', () => {
    const { context, calls, styles } = fakeCanvas();
    const world = createWorld([], WIDTH, HEIGHT);
    world.plants = [];
    world.food.push({ x: 100, y: 100, age: 0, sway: 0 }, { x: 200, y: 100, age: 0, sway: 0 });
    world.pops.push({ x: 300, y: 300, radius: 8, age: 0.175 });
    drawWorld(context, world, startingPalette('light'));

    expect(calls.filter((name) => name === 'arc')).toHaveLength(2);
    expect(calls.filter((name) => name === 'stroke')).toHaveLength(6);
    expect(styles).toContain('#e8a23c');
    expect(styles).toContain('rgb(255 255 255 / 0.5)');
  });

  it('moves the colors toward the theme little by little', () => {
    const palette = startingPalette('light');
    const start = [...palette.deep];
    easePalette(palette, 'dark', 1 / 60);

    expect(palette.deep).not.toEqual(start);
    expect(palette.deep).not.toEqual(startingPalette('dark').deep);

    for (let step = 0; step < 3000; step += 1) {
      easePalette(palette, 'dark', 1 / 60);
    }

    palette.deep.forEach((channel, index) => {
      expect(channel).toBeCloseTo(startingPalette('dark').deep[index]);
    });
  });
});
