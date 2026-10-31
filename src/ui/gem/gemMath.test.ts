import type { Vector3 } from './gemMath';
import { aimAxis, buildGemMesh, cross, easeAxis, normalize, RESTING_AXIS, rotationMatrix } from './gemMath';

const FLOAT_DIGITS = 5;

const rotate = (matrix: Float32Array, [x, y, z]: Vector3): Vector3 => [
  matrix[0] * x + matrix[3] * y + matrix[6] * z,
  matrix[1] * x + matrix[4] * y + matrix[7] * z,
  matrix[2] * x + matrix[5] * y + matrix[8] * z,
];

describe('buildGemMesh', () => {
  const { positions, normals } = buildGemMesh();

  it('has three corners and one normal per corner', () => {
    expect(positions.length % 9).toBe(0);
    expect(normals).toHaveLength(positions.length);
  });

  it('turns every facet outwards, in counter clockwise order', () => {
    for (let index = 0; index < positions.length; index += 9) {
      const [ax, ay, az, bx, by, bz, cx, cy, cz] = positions.slice(index, index + 9) as unknown as number[] as [
        number,
        number,
        number,
        number,
        number,
        number,
        number,
        number,
        number,
      ];
      const normal = cross([bx - ax, by - ay, bz - az], [cx - ax, cy - ay, cz - az]);
      const center = [ax + bx + cx, ay + by + cy, az + bz + cz] as Vector3;

      expect(normal[0] * center[0] + normal[1] * center[1] + normal[2] * center[2]).toBeGreaterThan(0);
    }
  });

  it('ends in a point on +Z', () => {
    expect(Math.max(...positions.filter((_, index) => index % 3 === 2))).toBeCloseTo(1.05);
  });
});

describe('aimAxis', () => {
  it('leans right, left, up and down with the mouse', () => {
    expect(aimAxis(300, 0)[0]).toBeGreaterThan(0.8);
    expect(aimAxis(-300, 0)[0]).toBeLessThan(-0.8);
    expect(aimAxis(0, -300)[1]).toBeGreaterThan(0.8);
    expect(aimAxis(0, 300)[1]).toBeLessThan(-0.8);
  });

  it('looks at the person when the mouse is over the gem', () => {
    expect(aimAxis(0, 0)).toEqual([0, -0, 1]);
  });
});

describe('easeAxis', () => {
  it('moves towards the target without passing it', () => {
    const next = easeAxis([0, 0, 1], [1, 0, 0], 0.016);

    expect(next[0]).toBeGreaterThan(0);
    expect(next[0]).toBeLessThan(0.2);
  });

  it('reaches the target after a long time', () => {
    expect(easeAxis([0, 0, 1], [1, 0, 0], 60)[0]).toBeCloseTo(1, FLOAT_DIGITS);
  });
});

describe('rotationMatrix', () => {
  it('sends the tip of the gem along the axis, whatever the spin', () => {
    const axis = normalize([0.3, -0.5, 0.7]);

    for (const spin of [0, 1, 4]) {
      const tip = rotate(rotationMatrix(axis, spin), [0, 0, 1]);

      expect(tip[0]).toBeCloseTo(axis[0], FLOAT_DIGITS);
      expect(tip[1]).toBeCloseTo(axis[1], FLOAT_DIGITS);
      expect(tip[2]).toBeCloseTo(axis[2], FLOAT_DIGITS);
    }
  });

  it('spins the sides around the axis', () => {
    const first = rotate(rotationMatrix(RESTING_AXIS, 0), [1, 0, 0]);
    const second = rotate(rotationMatrix(RESTING_AXIS, 1), [1, 0, 0]);

    expect(first).not.toEqual(second);
    expect(Math.hypot(...second)).toBeCloseTo(1, FLOAT_DIGITS);
  });

  it('keeps working with the mouse straight above the gem', () => {
    expect(Math.hypot(...rotationMatrix(aimAxis(0, -5000), 2))).toBeGreaterThan(0);
    expect([...rotationMatrix(aimAxis(0, -5000), 2)].every(Number.isFinite)).toBe(true);
  });
});
