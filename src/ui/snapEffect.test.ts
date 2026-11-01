import { planGrains } from './snapEffect';

const part = { left: 10, top: 20, width: 100, height: 50, color: '#123', delay: 300 };

describe('planGrains', () => {
  it('gives bigger parts more dust, inside their own area', () => {
    const grains = planGrains(part, 1000, () => 0.5);

    expect(grains).toHaveLength(60);
    expect(grains[0]).toMatchObject({ x: 60, y: 45, color: '#123' });
    expect(grains[0].startsAt).toBeGreaterThanOrEqual(300);
  });

  it('never goes over the room left', () => {
    expect(planGrains(part, 7)).toHaveLength(7);
  });

  it('gives a tiny part a few grains, and blows them up and to the right', () => {
    const grains = planGrains({ ...part, width: 2, height: 2 }, 1000);

    expect(grains).toHaveLength(6);
    expect(grains.every((grain) => grain.speedX > 0 && grain.speedY < 0)).toBe(true);
  });
});
