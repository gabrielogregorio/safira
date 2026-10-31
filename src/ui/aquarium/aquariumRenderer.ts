import type { ThemeId } from '@/settings/settings';
import type { Fish, World } from './aquariumWorld';
import { colorsOf, fatnessOf, lengthOf } from './aquariumWorld';

interface Palette {
  surface: number[];
  middle: number[];
  deep: number[];
  light: number[];
  plantTop: number[];
  plantBottom: number[];
}

const PALETTES: Record<ThemeId, Palette> = {
  light: {
    surface: [143, 228, 251],
    middle: [36, 150, 225],
    deep: [6, 58, 140],
    light: [255, 255, 255],
    plantTop: [168, 238, 106],
    plantBottom: [44, 143, 58],
  },
  dark: {
    surface: [14, 58, 110],
    middle: [6, 30, 74],
    deep: [2, 10, 34],
    light: [150, 190, 255],
    plantTop: [58, 120, 110],
    plantBottom: [12, 58, 66],
  },
  simple: {
    surface: [164, 227, 223],
    middle: [40, 150, 150],
    deep: [10, 70, 90],
    light: [214, 255, 240],
    plantTop: [140, 226, 170],
    plantBottom: [20, 120, 110],
  },
};

const PALETTE_EASE = 1.6;
const RIPPLE_SIZE = 90;
const RIPPLE_SECONDS = 1.4;
const POP_SECONDS = 0.35;

export type LivePalette = Palette;

export const startingPalette = (theme: ThemeId): LivePalette => structuredClone(PALETTES[theme]);

// The water moves toward the sky of the moment instead of jumping, so a theme change is seen in the aquarium too.
export const easePalette = (palette: LivePalette, theme: ThemeId, seconds: number): void => {
  const target = PALETTES[theme];
  const blend = Math.min(1, seconds * PALETTE_EASE);

  for (const key of Object.keys(target) as (keyof Palette)[]) {
    palette[key] = palette[key].map((value, index) => value + (target[key][index] - value) * blend);
  }
};

const rgb = ([red, green, blue]: number[], alpha = 1): string =>
  `rgb(${Math.round(red)} ${Math.round(green)} ${Math.round(blue)} / ${alpha})`;

const drawWater = (context: CanvasRenderingContext2D, world: World, palette: LivePalette): void => {
  const water = context.createLinearGradient(0, 0, 0, world.height);
  water.addColorStop(0, rgb(palette.surface));
  water.addColorStop(0.55, rgb(palette.middle));
  water.addColorStop(1, rgb(palette.deep));
  context.fillStyle = water;
  context.fillRect(0, 0, world.width, world.height);

  context.fillStyle = rgb(palette.light, 0.09);

  for (let ray = 0; ray < 4; ray += 1) {
    const x = world.width * (0.15 + ray * 0.24) + Math.sin(world.time * 0.3 + ray) * 40;
    context.beginPath();
    context.moveTo(x, 0);
    context.lineTo(x + 70, 0);
    context.lineTo(x - 90, world.height);
    context.lineTo(x - 240, world.height);
    context.fill();
  }
};

const drawPlants = (context: CanvasRenderingContext2D, world: World, palette: LivePalette): void => {
  for (const plant of world.plants) {
    const bend = Math.sin(plant.sway) * 14 + Math.sin(plant.sway * 7) * 34 * plant.shake;
    const base = world.height + 6;
    const top = base - plant.height;
    const leaf = context.createLinearGradient(0, top, 0, base);
    leaf.addColorStop(0, rgb(palette.plantTop));
    leaf.addColorStop(1, rgb(palette.plantBottom));
    context.fillStyle = leaf;
    context.beginPath();
    context.moveTo(plant.x - 13, base);
    context.quadraticCurveTo(plant.x - 16 + bend * 0.4, base - plant.height * 0.6, plant.x + bend, top);
    context.quadraticCurveTo(plant.x + 16 + bend * 0.4, base - plant.height * 0.6, plant.x + 13, base);
    context.fill();
  }
};

const drawFish = (context: CanvasRenderingContext2D, fish: Fish): void => {
  const { body, fin } = colorsOf(fish.id);
  const length = lengthOf(fish);
  const half = length / 2;
  const height = length * 0.24 * (1 + fatnessOf(fish.mass) * 0.45);
  const tail = Math.sin(fish.swim) * length * 0.09;

  context.save();
  context.translate(fish.x, fish.y);
  context.scale(fish.vx < 0 ? -1 : 1, 1);
  context.fillStyle = fin;
  context.beginPath();
  context.moveTo(-half * 0.8, 0);
  context.lineTo(-half * 1.35, -height * 0.9 + tail);
  context.lineTo(-half * 1.15, tail * 0.4);
  context.lineTo(-half * 1.35, height * 0.9 + tail);
  context.fill();
  context.beginPath();
  context.ellipse(-half * 0.1, -height * 0.85, half * 0.34, height * 0.42, 0, 0, Math.PI * 2);
  context.fill();
  context.fillStyle = body;
  context.beginPath();
  context.ellipse(0, 0, half, height, 0, 0, Math.PI * 2);
  context.fill();
  context.fillStyle = 'rgb(255 255 255 / 45%)';
  context.beginPath();
  context.ellipse(half * 0.05, -height * 0.42, half * 0.7, height * 0.32, 0, 0, Math.PI * 2);
  context.fill();
  context.fillStyle = '#ffffff';
  context.beginPath();
  context.arc(half * 0.62, -height * 0.18, Math.max(2.4, height * 0.26), 0, Math.PI * 2);
  context.fill();
  context.fillStyle = '#102a43';
  context.beginPath();
  context.arc(half * 0.67, -height * 0.18, Math.max(1.3, height * 0.14), 0, Math.PI * 2);
  context.fill();
  context.restore();
};

const drawBubbles = (context: CanvasRenderingContext2D, world: World): void => {
  for (const bubble of world.bubbles) {
    const x = bubble.x + Math.sin(bubble.sway) * 5;
    context.strokeStyle = 'rgb(255 255 255 / 70%)';
    context.fillStyle = 'rgb(255 255 255 / 16%)';
    context.beginPath();
    context.arc(x, bubble.y, bubble.radius, 0, Math.PI * 2);
    context.fill();
    context.stroke();
    context.fillStyle = 'rgb(255 255 255 / 85%)';
    context.beginPath();
    context.arc(x - bubble.radius * 0.35, bubble.y - bubble.radius * 0.35, bubble.radius * 0.22, 0, Math.PI * 2);
    context.fill();
  }

  for (const pop of world.pops) {
    const progress = pop.age / POP_SECONDS;
    context.strokeStyle = `rgb(255 255 255 / ${1 - progress})`;

    for (let spark = 0; spark < 6; spark += 1) {
      const angle = (spark / 6) * Math.PI * 2;
      const inner = pop.radius * (1 + progress);
      const outer = pop.radius * (1.4 + progress * 1.6);
      context.beginPath();
      context.moveTo(pop.x + Math.cos(angle) * inner, pop.y + Math.sin(angle) * inner);
      context.lineTo(pop.x + Math.cos(angle) * outer, pop.y + Math.sin(angle) * outer);
      context.stroke();
    }
  }
};

const drawFood = (context: CanvasRenderingContext2D, world: World): void => {
  context.fillStyle = '#e8a23c';

  for (const food of world.food) {
    context.beginPath();
    context.arc(food.x + Math.sin(world.time * 2 + food.sway) * 5, food.y, 3.4, 0, Math.PI * 2);
    context.fill();
  }
};

const drawRipples = (context: CanvasRenderingContext2D, world: World): void => {
  for (const ripple of world.ripples) {
    const progress = ripple.age / RIPPLE_SECONDS;
    context.strokeStyle = `rgb(255 255 255 / ${0.5 * (1 - progress)})`;
    context.lineWidth = 2;
    context.beginPath();
    context.ellipse(ripple.x, ripple.y, RIPPLE_SIZE * progress, RIPPLE_SIZE * 0.55 * progress, 0, 0, Math.PI * 2);
    context.stroke();
  }

  context.lineWidth = 1;
};

export const drawWorld = (context: CanvasRenderingContext2D, world: World, palette: LivePalette): void => {
  drawWater(context, world, palette);
  drawRipples(context, world);
  drawFood(context, world);
  [...world.fishes]
    .sort((first, second) => first.mass - second.mass)
    .forEach((fish) => {
      drawFish(context, fish);
    });
  drawPlants(context, world, palette);
  drawBubbles(context, world);
};
