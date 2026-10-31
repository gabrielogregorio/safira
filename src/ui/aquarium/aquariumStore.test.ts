import { loadFishes, saveFishes } from './aquariumStore';
import { FISH_COUNT, MASS_LOST_PER_SECOND } from './aquariumWorld';

describe('aquariumStore', () => {
  beforeEach(() => {
    localStorage.clear();
  });

  it('starts with the whole population, also after the browser is cleared', () => {
    expect(loadFishes()).toHaveLength(FISH_COUNT);
  });

  it('keeps who is alive and how heavy, losing weight while away', () => {
    saveFishes([{ id: 3, species: 1, mass: 2 }], 0);

    const [fish] = loadFishes(1000);

    expect(loadFishes(1000)).toHaveLength(1);
    expect(fish.mass).toBeCloseTo(2 - MASS_LOST_PER_SECOND);
  });

  it('never loses the last fish on a reset by accident: an empty tank stays empty', () => {
    saveFishes([], 0);

    expect(loadFishes(1)).toEqual([]);
  });

  it('survives broken data', () => {
    localStorage.setItem('safira.aquarium.v1', '{');

    expect(loadFishes()).toHaveLength(FISH_COUNT);
  });
});
