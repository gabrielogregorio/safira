export type Vector3 = [number, number, number];

export interface GemMesh {
  positions: Float32Array;
  normals: Float32Array;
}

const SIDES = 16;
const TABLE_RADIUS = 0.56;
const TABLE_HEIGHT = -0.46;
const GIRDLE_RADIUS = 1;
const GIRDLE_HEIGHT = -0.02;
const PAVILION_RADIUS = 0.56;
const PAVILION_HEIGHT = 0.5;
const CULET_HEIGHT = 1.05;
const AIM_DEPTH_PIXELS = 160;
const FOLLOW_RATE = 6;

const subtract = (tip: Vector3, base: Vector3): Vector3 => [tip[0] - base[0], tip[1] - base[1], tip[2] - base[2]];

const dot = (first: Vector3, second: Vector3): number =>
  first[0] * second[0] + first[1] * second[1] + first[2] * second[2];

export const cross = (first: Vector3, second: Vector3): Vector3 => [
  first[1] * second[2] - first[2] * second[1],
  first[2] * second[0] - first[0] * second[2],
  first[0] * second[1] - first[1] * second[0],
];

export const normalize = (vector: Vector3): Vector3 => {
  const length = Math.hypot(...vector);

  return [vector[0] / length, vector[1] / length, vector[2] / length];
};

const ring = (radius: number, height: number, turnOffset: number): Vector3[] =>
  Array.from({ length: SIDES }, (_, index) => {
    const angle = ((index + turnOffset) / SIDES) * Math.PI * 2;

    return [Math.cos(angle) * radius, Math.sin(angle) * radius, height];
  });

// The gem is convex around the origin, so facing away from the origin means facing outwards.
const outwardFacet = (first: Vector3, second: Vector3, third: Vector3): { corners: Vector3[]; normal: Vector3 } => {
  const normal = normalize(cross(subtract(second, first), subtract(third, first)));
  const center: Vector3 = [
    (first[0] + second[0] + third[0]) / 3,
    (first[1] + second[1] + third[1]) / 3,
    (first[2] + second[2] + third[2]) / 3,
  ];

  if (dot(normal, center) < 0) {
    return { corners: [first, third, second], normal: [-normal[0], -normal[1], -normal[2]] };
  }

  return { corners: [first, second, third], normal };
};

export const buildGemMesh = (): GemMesh => {
  const table = ring(TABLE_RADIUS, TABLE_HEIGHT, 0);
  const girdle = ring(GIRDLE_RADIUS, GIRDLE_HEIGHT, 0.5);
  const pavilion = ring(PAVILION_RADIUS, PAVILION_HEIGHT, 1);
  const tableCenter: Vector3 = [0, 0, TABLE_HEIGHT];
  const culet: Vector3 = [0, 0, CULET_HEIGHT];
  const triangles: [Vector3, Vector3, Vector3][] = [];
  const at = (points: Vector3[], index: number): Vector3 => points[index % SIDES];

  for (let index = 0; index < SIDES; index += 1) {
    triangles.push(
      [tableCenter, at(table, index), at(table, index + 1)],
      [at(table, index), at(table, index + 1), at(girdle, index)],
      [at(table, index + 1), at(girdle, index), at(girdle, index + 1)],
      [at(girdle, index), at(girdle, index + 1), at(pavilion, index)],
      [at(girdle, index + 1), at(pavilion, index), at(pavilion, index + 1)],
      [at(pavilion, index), at(pavilion, index + 1), culet],
    );
  }

  const facets = triangles.map(([first, second, third]) => outwardFacet(first, second, third));

  return {
    positions: new Float32Array(facets.flatMap(({ corners }) => corners.flat())),
    normals: new Float32Array(facets.flatMap(({ normal }) => [...normal, ...normal, ...normal])),
  };
};

export const RESTING_AXIS: Vector3 = normalize([0.42, 0.34, 0.84]);

// Screen coordinates grow downwards, and the gem looks out of the screen towards the person.
export const aimAxis = (horizontalPixels: number, verticalPixels: number): Vector3 =>
  normalize([horizontalPixels, -verticalPixels, AIM_DEPTH_PIXELS]);

export const easeAxis = (current: Vector3, target: Vector3, seconds: number): Vector3 => {
  const amount = 1 - Math.exp(-seconds * FOLLOW_RATE);

  return normalize([
    current[0] + (target[0] - current[0]) * amount,
    current[1] + (target[1] - current[1]) * amount,
    current[2] + (target[2] - current[2]) * amount,
  ]);
};

// Column by column, the model's +Z (the tip of the gem) becomes the axis, with the spin around it.
export const rotationMatrix = (axis: Vector3, spin: number): Float32Array => {
  const side = normalize(cross([0, 1, 0], axis));
  const up = cross(axis, side);
  const cosine = Math.cos(spin);
  const sine = Math.sin(spin);

  return new Float32Array([
    side[0] * cosine + up[0] * sine,
    side[1] * cosine + up[1] * sine,
    side[2] * cosine + up[2] * sine,
    up[0] * cosine - side[0] * sine,
    up[1] * cosine - side[1] * sine,
    up[2] * cosine - side[2] * sine,
    ...axis,
  ]);
};
