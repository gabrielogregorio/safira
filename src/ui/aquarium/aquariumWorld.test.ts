import {
  BURST_MASS,
  colorsOf,
  createPopulation,
  createWorld,
  FISH_COUNT,
  fatnessOf,
  lengthOf,
  MINIMUM_MASS,
  movePointer,
  pressPointer,
  releasePointer,
  scrollPointer,
  stepWorld,
  warmUpWorld,
} from './aquariumWorld';
import type { StoredFish, World } from './aquariumWorld';

const steady = (): number => 0.5;
const distance2 = (point: { x: number; y: number }, x: number, y: number): number =>
  Math.hypot(point.x - x, point.y - y);
const oneFish = (mass = MINIMUM_MASS): StoredFish[] => [{ id: 0, species: 0, mass }];
const click = (world: World, x: number, y: number) => {
  pressPointer(world, x, y);

  return releasePointer(world);
};

// Fish start at random places, so one run says little about who can reach whom.
const WARM_UP_ATTEMPTS = 300;

describe('aquariumWorld', () => {
  it('gives every fish a color of its own', () => {
    const colors = createPopulation().map((fish) => colorsOf(fish.id).body);

    expect(new Set(colors).size).toBe(FISH_COUNT);
  });

  it('starts with a closed population', () => {
    expect(createPopulation()).toHaveLength(FISH_COUNT);
  });

  it('makes a fish longer and fatter as it gains mass', () => {
    expect(lengthOf({ species: 0, mass: 3 })).toBeGreaterThan(lengthOf({ species: 0, mass: 1 }));
    expect(fatnessOf(3)).toBeGreaterThan(fatnessOf(1));
  });

  it('feeds in open water, and the fish in sight eats and grows', () => {
    const world = createWorld(oneFish(), 800, 600, steady);
    const [fish] = world.fishes;
    fish.x = 100;
    fish.y = 300;

    expect(click(world, 180, 300)).toEqual([{ kind: 'food' }]);

    const events = Array.from({ length: 300 }, () => stepWorld(world, 1 / 30)).flat();

    expect(events.some((event) => event.kind === 'eat')).toBe(true);
    expect(fish.mass).toBeGreaterThan(MINIMUM_MASS);
  });

  it('leaves food alone when it is out of sight', () => {
    const world = createWorld(oneFish(), 2000, 600, steady);
    const [fish] = world.fishes;
    fish.x = 10;
    click(world, 1900, 300);
    stepWorld(world, 1 / 30);

    expect(fish.mass).toBe(MINIMUM_MASS);
  });

  it('scares a clicked fish instead of feeding', () => {
    const world = createWorld(oneFish(), 800, 600, steady);
    const [fish] = world.fishes;

    expect(click(world, fish.x, fish.y)).toEqual([expect.objectContaining({ kind: 'flee' })]);
    expect(world.food).toEqual([]);
  });

  it('pops a clicked bubble', () => {
    const world = createWorld(oneFish(), 800, 600, steady);
    world.fishes = [];
    world.bubbles.push({ x: 50, y: 50, radius: 8, speed: 1, sway: 0 });

    expect(click(world, 50, 50)).toEqual([expect.objectContaining({ kind: 'pop' })]);
    expect(world.bubbles).toEqual([]);
    expect(world.pops).toHaveLength(1);
  });

  it('shakes a clicked plant, which lets bubbles go', () => {
    const world = createWorld([], 800, 600, steady);
    const [plant] = world.plants;

    expect(click(world, plant.x, 590)).toEqual([{ kind: 'plant' }]);
    expect(plant.shake).toBeGreaterThan(0);
    expect(world.bubbles.length).toBeGreaterThan(5);
  });

  it('shrinks slowly and stops at the base size', () => {
    const world = createWorld(oneFish(1.01), 800, 600, steady);
    const [fish] = world.fishes;

    stepWorld(world, 1);

    expect(fish.mass).toBeLessThan(1.01);
    expect(fish.mass).toBeGreaterThan(1);

    stepWorld(world, 100);

    expect(fish.mass).toBe(MINIMUM_MASS);
  });

  it('lets a very big fish eat a much smaller one, for good', () => {
    const world = createWorld(
      [
        { id: 0, species: 0, mass: 6 },
        { id: 1, species: 1, mass: 1 },
      ],
      800,
      600,
      steady,
    );
    const [big, small] = world.fishes;
    big.x = 100;
    small.x = 110;
    big.y = 300;
    small.y = 300;

    expect(stepWorld(world, 1 / 30)).toContainEqual(expect.objectContaining({ kind: 'chomp' }));
    expect(world.fishes).toEqual([big]);
    expect(big.mass).toBeGreaterThan(6);
  });

  it('does not let equals eat each other', () => {
    const world = createWorld(
      [
        { id: 0, species: 0, mass: 6 },
        { id: 1, species: 1, mass: 5 },
      ],
      800,
      600,
      steady,
    );
    world.fishes[1].x = world.fishes[0].x;
    stepWorld(world, 1 / 30);

    expect(world.fishes).toHaveLength(2);
  });

  it('tells a hold from a click', () => {
    const world = createWorld([], 800, 300, steady);
    pressPointer(world, 100, 100);

    const events = Array.from({ length: 30 }, () => stepWorld(world, 1 / 30)).flat();

    expect(events).toContainEqual({ kind: 'hold' });
    expect(releasePointer(world)).toEqual([]);
    expect(world.food).toEqual([]);
  });

  it('draws ripples along a drag and feeds nothing', () => {
    const world = createWorld([], 800, 300, steady);
    pressPointer(world, 100, 100);

    movePointer(world, 200, 100);

    expect(world.ripples.length).toBeGreaterThan(0);
    expect(releasePointer(world)).toEqual([]);
  });

  it('gives more food with the right button, and much more with both', () => {
    const world = createWorld([], 800, 600, steady);
    pressPointer(world, 100, 100, 2);
    releasePointer(world);
    const afterRight = world.food.length;
    pressPointer(world, 100, 100, 1);
    movePointer(world, 100, 100, 3);
    releasePointer(world);

    expect(afterRight).toBeGreaterThan(3);
    expect(world.food.length - afterRight).toBeGreaterThan(afterRight);
  });

  it('feeds with the right button even over a fish', () => {
    const world = createWorld(oneFish(), 800, 600, steady);
    const [fish] = world.fishes;
    pressPointer(world, fish.x, fish.y, 2);

    expect(releasePointer(world)).toEqual([{ kind: 'food' }]);
  });

  it('sees food from farther as it gets fatter', () => {
    const near = createWorld(oneFish(), 3000, 600, steady);
    const fat = createWorld(oneFish(5), 3000, 600, steady);

    for (const world of [near, fat]) {
      world.fishes[0].x = 100;
      world.fishes[0].y = 300;
      world.fishes[0].targetX = 100;
      world.food.push({ x: 320, y: 300, age: 0, sway: 0 });
      stepWorld(world, 1);
    }

    expect(fat.fishes[0].vx).toBeGreaterThan(near.fishes[0].vx);
  });

  it('drops one piece per wheel tick, only while a button is held', () => {
    const world = createWorld([], 800, 600, steady);

    expect(scrollPointer(world)).toEqual([]);

    pressPointer(world, 100, 100);
    scrollPointer(world);
    scrollPointer(world);

    expect(world.food).toHaveLength(2);
  });

  it('keeps fish apart, softly', () => {
    const world = createWorld(
      [
        { id: 0, species: 0, mass: 1 },
        { id: 1, species: 0, mass: 1 },
      ],
      800,
      600,
      steady,
    );
    const [first, second] = world.fishes;
    first.x = 400;
    second.x = 400;
    first.y = 300;
    second.y = 300;
    first.targetUntil = 99;
    second.targetUntil = 99;
    first.targetX = 400;
    second.targetX = 400;
    first.targetY = 300;
    second.targetY = 300;

    for (let frame = 0; frame < 30; frame += 1) {
      stepWorld(world, 1 / 30);
    }

    expect(Math.abs(first.y - second.y)).toBeGreaterThan(2);
  });

  it('pops a bubble from a little outside of it', () => {
    const world = createWorld([], 800, 600, steady);
    world.bubbles.push({ x: 50, y: 50, radius: 8, speed: 1, sway: 0 });

    expect(click(world, 50 + 25, 50)).toEqual([expect.objectContaining({ kind: 'pop' })]);
  });

  it('keeps eating while there is food around it', () => {
    const world = createWorld(oneFish(), 800, 600, steady);
    const [fish] = world.fishes;
    fish.x = 400;
    fish.y = 300;

    for (let piece = 0; piece < 8; piece += 1) {
      world.food.push({ x: 360 + piece * 12, y: 290 + (piece % 3) * 10, age: 0, sway: 0 });
    }

    for (let frame = 0; frame < 150; frame += 1) {
      stepWorld(world, 1 / 30);
    }

    expect(world.food).toEqual([]);
    expect(distance2(fish, 400, 300)).toBeLessThan(120);
  });

  it('prefers the nearer food to a far prey', () => {
    const world = createWorld(
      [
        { id: 0, species: 0, mass: 6 },
        { id: 1, species: 1, mass: 1 },
      ],
      800,
      600,
      steady,
    );
    const [big, small] = world.fishes;
    big.x = 100;
    big.y = 300;
    small.x = 300;
    small.y = 300;
    world.food.push({ x: 140, y: 300, age: 0, sway: 0 });

    expect(stepWorld(world, 1 / 30)).not.toContainEqual(expect.objectContaining({ kind: 'chomp' }));
    expect(big.isFeeding).toBe(true);
  });

  it('makes a big fish catch a small one that swims away', () => {
    const world = createWorld(
      [
        { id: 0, species: 7, mass: 8 },
        { id: 1, species: 5, mass: 1 },
      ],
      1000,
      600,
      Math.random,
    );
    const [big, small] = world.fishes;
    big.x = 200;
    big.y = 300;
    small.x = 500;
    small.y = 300;

    const events = Array.from({ length: 450 }, () => stepWorld(world, 1 / 30)).flat();

    expect(events).toContainEqual(expect.objectContaining({ kind: 'chomp' }));
    expect(world.fishes).toEqual([big]);
    expect(world.bubbles.length).toBeGreaterThan(0);
  });

  it('does not hunt fish of a similar size', () => {
    const world = createWorld(
      [
        { id: 0, species: 0, mass: 5 },
        { id: 1, species: 0, mass: 4 },
      ],
      800,
      600,
      Math.random,
    );

    const events = Array.from({ length: 300 }, () => stepWorld(world, 1 / 30)).flat();

    expect(events).not.toContainEqual(expect.objectContaining({ kind: 'chomp' }));
  });

  it('drops 1.5 times more food for each popped bubble, on top of the last value', () => {
    const world = createWorld([], 800, 600, steady);

    for (let popped = 0; popped < 2; popped += 1) {
      world.bubbles.push({ x: 50, y: 50, radius: 8, speed: 1, sway: 0 });
      click(world, 50, 50);
    }

    expect(world.foodGrowth).toBeCloseTo(2.25);

    click(world, 400, 300);

    expect(world.food).toHaveLength(7);
  });

  it('never fills the water past its limit', () => {
    const world = createWorld([], 800, 600, steady);
    world.foodGrowth = 1e12;

    for (let drop = 0; drop < 10; drop += 1) {
      click(world, 400, 300);
    }

    expect(world.food).toHaveLength(800);
  });

  it('lets a fish get fat until it pops like a bubble, for good', () => {
    const world = createWorld(oneFish(BURST_MASS - 0.01), 800, 600, steady);
    const [fish] = world.fishes;
    world.food.push({ x: fish.x, y: fish.y, age: 0, sway: 0 });

    expect(stepWorld(world, 1 / 30)).toContainEqual(expect.objectContaining({ kind: 'burst' }));
    expect(world.fishes).toEqual([]);
    expect(world.pops).toHaveLength(1);
    expect(world.bubbles.length).toBeGreaterThan(5);
  });

  it('pops a fish only at 30% over the old largest size', () => {
    const oldLimit = lengthOf({ species: 0, mass: 16 });

    expect(lengthOf({ species: 0, mass: BURST_MASS }) / oldLimit).toBeCloseTo(1.3, 2);
  });

  it('keeps a fat fish alive below the limit', () => {
    const world = createWorld(oneFish(BURST_MASS - 2), 800, 600, steady);
    const [fish] = world.fishes;
    world.food.push({ x: fish.x, y: fish.y, age: 0, sway: 0 });
    stepWorld(world, 1 / 30);

    expect(world.fishes).toEqual([fish]);
    expect(fish.mass).toBeGreaterThan(BURST_MASS - 2);
  });

  it('drops food as an irregular handful, not as a square', () => {
    const world = createWorld([], 800, 600, Math.random);

    for (let drop = 0; drop < 40; drop += 1) {
      pressPointer(world, 400, 300);
      releasePointer(world);
    }

    const distances = world.food.map((food) => Math.hypot(food.x - 400, food.y - 300));
    const middle = distances.filter((value) => value < Math.max(...distances) / 2).length;

    expect(world.food.length).toBeGreaterThan(10);
    expect(middle / distances.length).toBeGreaterThan(0.5);
  });

  it('opens with every fish already swimming and nobody eaten', () => {
    for (let attempt = 0; attempt < WARM_UP_ATTEMPTS; attempt += 1) {
      const fishes = [...oneFish(10), { id: 1, species: 1, mass: MINIMUM_MASS }];
      const world = createWorld(fishes, 240, 180);
      warmUpWorld(world);

      expect(world.fishes).toHaveLength(2);
      expect(world.fishes.every((fish) => Math.hypot(fish.vx, fish.vy) > 0)).toBe(true);
    }
  });
});
