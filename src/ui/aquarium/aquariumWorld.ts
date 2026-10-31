export interface Species {
  body: string;
  fin: string;
  length: number;
  speed: number;
  voice: number;
}

export const SPECIES: Species[] = [
  { body: '#ffb347', fin: '#ff8a2a', length: 46, speed: 62, voice: 1 },
  { body: '#ffe066', fin: '#f2b705', length: 34, speed: 78, voice: 1.25 },
  { body: '#ff8fb1', fin: '#f0507f', length: 58, speed: 50, voice: 0.85 },
  { body: '#7fe3ff', fin: '#1f9fe0', length: 40, speed: 70, voice: 1.12 },
  { body: '#b6f27a', fin: '#56b92e', length: 50, speed: 56, voice: 0.95 },
  { body: '#d3a6ff', fin: '#9a5ff0', length: 30, speed: 84, voice: 1.4 },
  { body: '#ffffff', fin: '#ff7a3c', length: 44, speed: 60, voice: 1.05 },
  { body: '#ff9d7a', fin: '#d9542b', length: 66, speed: 44, voice: 0.72 },
];

export const FISH_COUNT = 24;
export const MINIMUM_MASS = 1;
const MAXIMUM_MASS = 8;
export const MASS_LOST_PER_SECOND = 0.0008;
const MASS_PER_FOOD = 0.28;
const PREY_MASS_SHARE = 0.3;
const PREDATOR_MASS = 4;
const PREDATOR_ADVANTAGE = 2.2;
const SECONDS_BETWEEN_PREY = 25;
const FOOD_VISION = 230;
const PREY_VISION = 280;
const FOOD_LIFETIME_SECONDS = 45;
const FOOD_SINK_SPEED = 7;
const FLEE_SECONDS = 1.6;
const FLEE_SPEED = 3.6;
const HUNT_SPEED = 1.5;
const TURN_RATE = 2.4;
const FOOD_PER_CLICK = 3;
const FOOD_PER_RIGHT_CLICK = 6;
const FOOD_PER_BOTH_BUTTONS = 18;
const FOOD_SPREAD = 18;
const WIDE_FOOD_SPREAD = 60;
const RIGHT_BUTTON = 2;
const BOTH_BUTTONS = 3;
const APPETITE_VISION = 0.35;
const APPETITE_SPEED = 0.12;
const SURFACE_MARGIN = 30;
const BOTTOM_MARGIN = 50;
const MAXIMUM_BUBBLES = 70;
const BUBBLES_PER_SECOND = 1.6;
const PLANT_BUBBLES = 14;
const PLANT_SHAKE = 1;
const PLANT_WIDTH = 26;
const HOLD_SECONDS = 0.28;
const HOLD_RADIUS = 280;
const HOLD_PULL = 150;
const HOLD_BUBBLES_PER_SECOND = 12;
const DRAG_RADIUS = 170;
const DRAG_PUSH = 0.7;
const CLICK_DISTANCE = 12;
const RIPPLE_SECONDS = 1.4;
const RIPPLE_GAP = 26;
const PLANT_SPACING = 130;
const POP_SECONDS = 0.35;
const BUBBLE_REACH = 1.5;
const BUBBLE_MARGIN = 10;
const PERSONAL_SPACE = 0.38;
const SEPARATION_SPEED = 120;
const FLAT_BODY = 2;

export interface StoredFish {
  id: number;
  species: number;
  mass: number;
}

export interface Fish extends StoredFish {
  x: number;
  y: number;
  vx: number;
  vy: number;
  targetX: number;
  targetY: number;
  targetUntil: number;
  fleeUntil: number;
  fleeX: number;
  fleeY: number;
  preyAt: number;
  swim: number;
}

export interface Food {
  x: number;
  y: number;
  age: number;
  sway: number;
}

export interface Bubble {
  x: number;
  y: number;
  radius: number;
  speed: number;
  sway: number;
}

export interface Ripple {
  x: number;
  y: number;
  age: number;
}

export interface Pop {
  x: number;
  y: number;
  radius: number;
  age: number;
}

export interface Plant {
  x: number;
  height: number;
  sway: number;
  shake: number;
}

export interface Pointer {
  x: number;
  y: number;
  dragX: number;
  dragY: number;
  startX: number;
  startY: number;
  heldFor: number;
  hasMoved: boolean;
  buttons: number;
}

export interface World {
  width: number;
  height: number;
  time: number;
  fishes: Fish[];
  food: Food[];
  bubbles: Bubble[];
  ripples: Ripple[];
  pops: Pop[];
  plants: Plant[];
  pointer: Pointer | null;
  random: () => number;
}

export type WorldEvent =
  | { kind: 'eat'; voice: number }
  | { kind: 'chomp'; voice: number }
  | { kind: 'flee'; voice: number }
  | { kind: 'pop'; voice: number }
  | { kind: 'plant' }
  | { kind: 'food' }
  | { kind: 'hold' }
  | { kind: 'swish' };

export const createPopulation = (): StoredFish[] =>
  Array.from({ length: FISH_COUNT }, (_, id) => ({ id, species: id % SPECIES.length, mass: MINIMUM_MASS }));

export const fatnessOf = (mass: number): number => Math.min(1.4, (mass - MINIMUM_MASS) * 0.16);

// Eating opens the appetite: the fatter the fish, the farther it sees food and the faster it goes after it.
export const appetiteOf = (mass: number): number => mass - MINIMUM_MASS;

export const lengthOf = (fish: Pick<StoredFish, 'species' | 'mass'>): number =>
  SPECIES[fish.species].length * (1 + 0.32 * Math.sqrt(fish.mass - MINIMUM_MASS));

const distance = (firstX: number, firstY: number, secondX: number, secondY: number): number =>
  Math.hypot(firstX - secondX, firstY - secondY);

const between = (random: () => number, minimum: number, maximum: number): number =>
  minimum + random() * (maximum - minimum);

const placeFish = (stored: StoredFish, world: Pick<World, 'width' | 'height' | 'random'>): Fish => {
  const { width, height, random } = world;
  const x = between(random, 0, width);
  const y = between(random, SURFACE_MARGIN, height - BOTTOM_MARGIN);

  return {
    ...stored,
    x,
    y,
    vx: 0,
    vy: 0,
    targetX: x,
    targetY: y,
    targetUntil: 0,
    fleeUntil: 0,
    fleeX: 0,
    fleeY: 0,
    preyAt: 0,
    swim: random() * Math.PI * 2,
  };
};

const placePlants = (width: number, height: number, random: () => number): Plant[] => {
  const count = Math.max(3, Math.round(width / PLANT_SPACING));

  return Array.from({ length: count }, (_, index) => ({
    x: ((index + 0.5) / count) * width + between(random, -30, 30),
    height: Math.min(height * 0.45, between(random, 90, 220)),
    sway: random() * Math.PI * 2,
    shake: 0,
  }));
};

export const createWorld = (
  stored: StoredFish[],
  width: number,
  height: number,
  random: () => number = Math.random,
): World => ({
  width,
  height,
  time: 0,
  fishes: stored.map((fish) => placeFish(fish, { width, height, random })),
  food: [],
  bubbles: [],
  ripples: [],
  pops: [],
  plants: placePlants(width, height, random),
  pointer: null,
  random,
});

export const resizeWorld = (world: World, width: number, height: number): void => {
  world.width = width;
  world.height = height;
  world.plants = placePlants(width, height, world.random);
};

const spawnBubble = (world: World, x: number, y: number): void => {
  if (world.bubbles.length < MAXIMUM_BUBBLES) {
    world.bubbles.push({
      x,
      y,
      radius: between(world.random, 3, 12),
      speed: between(world.random, 36, 80),
      sway: world.random() * Math.PI * 2,
    });
  }
};

const nearestFood = (world: World, fish: Fish): Food | null => {
  const vision = FOOD_VISION * (1 + appetiteOf(fish.mass) * APPETITE_VISION) + lengthOf(fish);
  let nearest: Food | null = null;
  let nearestDistance = vision;

  for (const food of world.food) {
    const away = distance(fish.x, fish.y, food.x, food.y);

    if (away < nearestDistance) {
      nearest = food;
      nearestDistance = away;
    }
  }

  return nearest;
};

const nearestPrey = (world: World, fish: Fish): Fish | null => {
  if (fish.mass < PREDATOR_MASS || world.time < fish.preyAt) {
    return null;
  }

  let nearest: Fish | null = null;
  let nearestDistance = PREY_VISION;

  for (const other of world.fishes) {
    const away = distance(fish.x, fish.y, other.x, other.y);

    if (other !== fish && fish.mass >= other.mass * PREDATOR_ADVANTAGE && away < nearestDistance) {
      nearest = other;
      nearestDistance = away;
    }
  }

  return nearest;
};

const steerTo = (fish: Fish, x: number, y: number, speed: number, seconds: number): void => {
  const away = distance(fish.x, fish.y, x, y) || 1;
  const blend = Math.min(1, TURN_RATE * seconds);
  fish.vx += (((x - fish.x) / away) * speed - fish.vx) * blend;
  fish.vy += (((y - fish.y) / away) * speed - fish.vy) * blend;
};

const applyPointer = (world: World, fish: Fish, seconds: number): void => {
  const { pointer } = world;

  if (pointer === null) {
    return;
  }

  const away = distance(fish.x, fish.y, pointer.x, pointer.y) || 1;

  if (pointer.heldFor > HOLD_SECONDS && !pointer.hasMoved && away < HOLD_RADIUS) {
    const pull = HOLD_PULL * (1 - away / HOLD_RADIUS) * seconds;
    fish.x += ((pointer.x - fish.x) / away) * pull - ((pointer.y - fish.y) / away) * pull;
    fish.y += ((pointer.y - fish.y) / away) * pull + ((pointer.x - fish.x) / away) * pull;
  } else if (pointer.hasMoved && away < DRAG_RADIUS) {
    const push = DRAG_PUSH * (1 - away / DRAG_RADIUS);
    fish.x += pointer.dragX * push;
    fish.y += pointer.dragY * push;
  }
};

const eatFood = (world: World, fish: Fish, events: WorldEvent[]): void => {
  const reach = Math.max(14, lengthOf(fish) * 0.5);
  const eaten = world.food.findIndex((food) => distance(fish.x, fish.y, food.x, food.y) < reach);

  if (eaten !== -1) {
    world.food.splice(eaten, 1);
    fish.mass = Math.min(MAXIMUM_MASS, fish.mass + MASS_PER_FOOD);
    events.push({ kind: 'eat', voice: SPECIES[fish.species].voice });
  }
};

const eatPrey = (world: World, fish: Fish, prey: Fish, events: WorldEvent[]): void => {
  if (distance(fish.x, fish.y, prey.x, prey.y) < lengthOf(fish) * 0.45) {
    world.fishes = world.fishes.filter((other) => other !== prey);
    fish.mass = Math.min(MAXIMUM_MASS, fish.mass + Math.min(1, prey.mass * PREY_MASS_SHARE));
    fish.preyAt = world.time + SECONDS_BETWEEN_PREY;
    events.push({ kind: 'chomp', voice: SPECIES[fish.species].voice });
  }
};

const moveFish = (world: World, fish: Fish, seconds: number, events: WorldEvent[]): void => {
  const species = SPECIES[fish.species];
  const speed = species.speed / (1 + fatnessOf(fish.mass) * 0.4);
  const prey = nearestPrey(world, fish);
  const food = nearestFood(world, fish);

  if (world.time < fish.fleeUntil) {
    steerTo(fish, fish.x + fish.fleeX, fish.y + fish.fleeY, speed * FLEE_SPEED, seconds * 2);
  } else if (prey !== null) {
    steerTo(fish, prey.x, prey.y, speed * HUNT_SPEED, seconds);
    eatPrey(world, fish, prey, events);
  } else if (food === null) {
    if (world.time > fish.targetUntil || distance(fish.x, fish.y, fish.targetX, fish.targetY) < 20) {
      fish.targetX = between(world.random, 0, world.width);
      fish.targetY = between(world.random, SURFACE_MARGIN, world.height - BOTTOM_MARGIN);
      fish.targetUntil = world.time + between(world.random, 4, 10);
    }

    steerTo(fish, fish.targetX, fish.targetY, speed, seconds);
  } else {
    steerTo(fish, food.x, food.y, speed * HUNT_SPEED * (1 + appetiteOf(fish.mass) * APPETITE_SPEED), seconds);
  }

  eatFood(world, fish, events);
  applyPointer(world, fish, seconds);
  fish.x = Math.min(world.width + 40, Math.max(-40, fish.x + fish.vx * seconds));
  fish.y = Math.min(world.height - BOTTOM_MARGIN / 2, Math.max(SURFACE_MARGIN / 2, fish.y + fish.vy * seconds));
  fish.swim += seconds * (4 + Math.hypot(fish.vx, fish.vy) * 0.08);
  fish.mass = Math.max(MINIMUM_MASS, fish.mass - MASS_LOST_PER_SECOND * seconds);
};

const moveWater = (world: World, seconds: number): void => {
  const { height, pointer, random } = world;

  world.food = world.food.filter((food) => {
    food.age += seconds;
    food.y = Math.min(height - 20, food.y + FOOD_SINK_SPEED * seconds);

    return food.age < FOOD_LIFETIME_SECONDS;
  });
  world.bubbles = world.bubbles.filter((bubble) => {
    bubble.y -= bubble.speed * seconds;
    bubble.sway += seconds * 2;

    if (pointer?.hasMoved === true && distance(bubble.x, bubble.y, pointer.x, pointer.y) < DRAG_RADIUS) {
      bubble.x += pointer.dragX;
      bubble.y += pointer.dragY;
    }

    return bubble.y > -bubble.radius;
  });
  world.ripples = world.ripples.filter((ripple) => {
    ripple.age += seconds;

    return ripple.age < RIPPLE_SECONDS;
  });
  world.pops = world.pops.filter((pop) => {
    pop.age += seconds;

    return pop.age < POP_SECONDS;
  });

  for (const plant of world.plants) {
    plant.sway += seconds * 1.1;
    plant.shake = Math.max(0, plant.shake - seconds * 0.9);
  }

  if (random() < BUBBLES_PER_SECOND * seconds) {
    spawnBubble(world, between(random, 0, world.width), height + 10);
  }
};

const movePointerEffects = (world: World, seconds: number, events: WorldEvent[]): void => {
  const { pointer } = world;

  if (pointer === null) {
    return;
  }

  const wasHolding = pointer.heldFor > HOLD_SECONDS;
  pointer.heldFor += seconds;

  if (pointer.hasMoved) {
    pointer.dragX *= 0.8;
    pointer.dragY *= 0.8;
  } else if (pointer.heldFor > HOLD_SECONDS) {
    if (!wasHolding) {
      events.push({ kind: 'hold' });
      world.ripples.push({ x: pointer.x, y: pointer.y, age: 0 });
    }

    if (world.random() < HOLD_BUBBLES_PER_SECOND * seconds) {
      spawnBubble(world, pointer.x + between(world.random, -50, 50), pointer.y + between(world.random, -50, 50));
    }

    if (world.random() < 2 * seconds) {
      world.ripples.push({ x: pointer.x, y: pointer.y, age: 0 });
    }
  }
};

const canEat = (hunter: Fish, prey: Fish): boolean =>
  hunter.mass >= PREDATOR_MASS && hunter.mass >= prey.mass * PREDATOR_ADVANTAGE;

// A soft push, stronger the more they overlap. They can swim close, but never pile up on the same spot.
const separatePair = (first: Fish, second: Fish, seconds: number): void => {
  const offsetX = second.x - first.x;
  const offsetY = (second.y - first.y) * FLAT_BODY;
  const away = Math.hypot(offsetX, offsetY);
  const space = (lengthOf(first) + lengthOf(second)) * PERSONAL_SPACE;

  if (away >= space) {
    return;
  }

  const push = (SEPARATION_SPEED * seconds * (1 - away / space)) / 2;
  const directionX = away === 0 ? 0 : offsetX / away;
  const directionY = away === 0 ? 1 : offsetY / away;
  first.x -= directionX * push;
  first.y -= directionY * push;
  second.x += directionX * push;
  second.y += directionY * push;
};

const separateFishes = (world: World, seconds: number): void => {
  world.fishes.forEach((first, index) => {
    for (const second of world.fishes.slice(index + 1)) {
      if (!canEat(first, second) && !canEat(second, first)) {
        separatePair(first, second, seconds);
      }
    }
  });
};

export const stepWorld = (world: World, seconds: number): WorldEvent[] => {
  const events: WorldEvent[] = [];
  world.time += seconds;

  for (const fish of [...world.fishes]) {
    if (world.fishes.includes(fish)) {
      moveFish(world, fish, seconds, events);
    }
  }

  separateFishes(world, seconds);
  moveWater(world, seconds);
  movePointerEffects(world, seconds, events);

  return events;
};

const pressedFish = (world: World, x: number, y: number): Fish | undefined =>
  world.fishes.find((fish) => distance(fish.x, fish.y, x, y) < Math.max(26, lengthOf(fish) * 0.6));

const pressedBubble = (world: World, x: number, y: number): Bubble | undefined =>
  world.bubbles.find((bubble) => distance(bubble.x, bubble.y, x, y) < (bubble.radius + BUBBLE_MARGIN) * BUBBLE_REACH);

const pressedPlant = (world: World, x: number, y: number): Plant | undefined =>
  world.plants.find(
    (plant) => Math.abs(plant.x - x) < PLANT_WIDTH && y > world.height - plant.height && y <= world.height,
  );

const scareFish = (world: World, fish: Fish, x: number, y: number): WorldEvent => {
  const away = distance(fish.x, fish.y, x, y) || 1;
  fish.fleeX = ((fish.x - x) / away) * 200;
  fish.fleeY = ((fish.y - y) / away) * 200;
  fish.fleeUntil = world.time + FLEE_SECONDS;

  return { kind: 'flee', voice: SPECIES[fish.species].voice };
};

const dropFood = (world: World, x: number, y: number, pieces = FOOD_PER_CLICK, spread = FOOD_SPREAD): WorldEvent => {
  for (let piece = 0; piece < pieces; piece += 1) {
    world.food.push({
      x: x + between(world.random, -spread, spread),
      y: y + between(world.random, -spread, spread),
      age: 0,
      sway: world.random() * Math.PI * 2,
    });
  }

  return { kind: 'food' };
};

// What a quick click does depends on what is under it, and only open water feeds the fish.
const clickAt = (world: World, x: number, y: number): WorldEvent => {
  const bubble = pressedBubble(world, x, y);
  const fish = pressedFish(world, x, y);
  const plant = pressedPlant(world, x, y);

  if (bubble !== undefined) {
    world.bubbles = world.bubbles.filter((other) => other !== bubble);
    world.pops.push({ x: bubble.x, y: bubble.y, radius: bubble.radius, age: 0 });

    return { kind: 'pop', voice: 1.5 - bubble.radius / 16 };
  }

  if (fish !== undefined) {
    return scareFish(world, fish, x, y);
  }

  if (plant !== undefined) {
    plant.shake = PLANT_SHAKE;

    for (let index = 0; index < PLANT_BUBBLES; index += 1) {
      spawnBubble(world, plant.x + between(world.random, -14, 14), world.height - world.random() * plant.height);
    }

    return { kind: 'plant' };
  }

  return dropFood(world, x, y);
};

export const pressPointer = (world: World, x: number, y: number, buttons = 1): void => {
  world.pointer = { x, y, dragX: 0, dragY: 0, startX: x, startY: y, heldFor: 0, hasMoved: false, buttons };
};

export const movePointer = (world: World, x: number, y: number, buttons = 1): WorldEvent[] => {
  const { pointer } = world;

  if (pointer === null) {
    return [];
  }

  // The second button of a chord only shows up here, because a press of it fires no event of its own.
  pointer.buttons |= buttons;

  const startedDragging = !pointer.hasMoved && distance(x, y, pointer.startX, pointer.startY) > CLICK_DISTANCE;
  pointer.hasMoved ||= startedDragging;

  if (pointer.hasMoved) {
    pointer.dragX = x - pointer.x;
    pointer.dragY = y - pointer.y;
    const last = world.ripples.at(-1);

    if (last === undefined || distance(last.x, last.y, x, y) > RIPPLE_GAP) {
      world.ripples.push({ x, y, age: 0 });
    }
  }

  pointer.x = x;
  pointer.y = y;

  return startedDragging ? [{ kind: 'swish' }] : [];
};

// Scrolling while holding a button drops one piece for each tick of the wheel.
export const scrollPointer = (world: World): WorldEvent[] => {
  const { pointer } = world;

  return pointer === null ? [] : [dropFood(world, pointer.x, pointer.y, 1)];
};

export const releasePointer = (world: World): WorldEvent[] => {
  const { pointer } = world;
  world.pointer = null;

  if (pointer?.buttons === BOTH_BUTTONS) {
    return [dropFood(world, pointer.x, pointer.y, FOOD_PER_BOTH_BUTTONS, WIDE_FOOD_SPREAD)];
  }

  if (pointer?.buttons === RIGHT_BUTTON) {
    return [dropFood(world, pointer.x, pointer.y, FOOD_PER_RIGHT_CLICK)];
  }

  return pointer === null || pointer.hasMoved || pointer.heldFor > HOLD_SECONDS
    ? []
    : [clickAt(world, pointer.x, pointer.y)];
};
