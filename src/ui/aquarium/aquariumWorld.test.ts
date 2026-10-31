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
});
