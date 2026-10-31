import { CYCLE_MILLISECONDS, phaseAt, sceneOffset, sceneOpacity, themeAtPhase } from './skyClock';

const FOUR_HOURS = CYCLE_MILLISECONDS / 3;

describe('phaseAt', () => {
  it('starts at the chosen theme', () => {
    expect(phaseAt('dark', 0)).toBe(1);
  });

  it('reaches the next climate after four hours', () => {
    expect(phaseAt('light', FOUR_HOURS)).toBeCloseTo(1);
  });

  it('comes back to the chosen theme after twelve hours', () => {
    expect(themeAtPhase(phaseAt('simple', CYCLE_MILLISECONDS))).toBe('simple');
  });
});

describe('themeAtPhase', () => {
  it('keeps the theme until halfway to the next one', () => {
    expect(themeAtPhase(0.4)).toBe('light');
    expect(themeAtPhase(0.6)).toBe('dark');
  });

  it('wraps from the last theme to the first', () => {
    expect(themeAtPhase(2.9)).toBe('light');
  });
});

describe('sceneOpacity', () => {
  it('shows only one scene at its peak', () => {
    expect([0, 1, 2].map((scene) => sceneOpacity(scene, 1))).toEqual([0, 1, 0]);
  });

  it('crosses two scenes that always add up to one', () => {
    expect(sceneOpacity(0, 0.5) + sceneOpacity(1, 0.5)).toBeCloseTo(1);
    expect(sceneOpacity(2, 0.5)).toBe(0);
  });

  it('crosses the last scene into the first', () => {
    expect(sceneOpacity(2, 2.9)).toBeCloseTo(0);
    expect(sceneOpacity(0, 2.9)).toBeCloseTo(1);
  });
});

describe('sceneOffset', () => {
  it('is zero at the peak of the scene', () => {
    expect(sceneOffset(1, 1)).toBe(0);
  });

  it('is negative before the peak and positive after it', () => {
    expect(sceneOffset(1, 0.5)).toBeCloseTo(-0.5);
    expect(sceneOffset(1, 1.5)).toBeCloseTo(0.5);
  });

  it('takes the short way around the cycle', () => {
    expect(sceneOffset(0, 2.5)).toBeCloseTo(-0.5);
  });
});
