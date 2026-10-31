import {
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
} from './aquariumWorld';
import type { StoredFish, World } from './aquariumWorld';

const steady = (): number => 0.5;
const oneFish = (mass = MINIMUM_MASS): StoredFish[] => [{ id: 0, species: 0, mass }];
const click = (world: World, x: number, y: number) => {
  pressPointer(world, x, y);

  return releasePointer(world);
};

describe('aquariumWorld', () => {
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

    expect(movePointer(world, 200, 100)).toEqual([{ kind: 'swish' }]);
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
      world.food.push({ x: 600, y: 300, age: 0, sway: 0 });
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
});
