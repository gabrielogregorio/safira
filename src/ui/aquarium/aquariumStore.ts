import type { StoredFish } from './aquariumWorld';
import { createPopulation, MASS_LOST_PER_SECOND, MINIMUM_MASS, SPECIES } from './aquariumWorld';

const STORAGE_KEY = 'safira.aquarium.v1';
const MILLISECONDS_PER_SECOND = 1000;

interface StoredAquarium {
  savedAt: number;
  fishes: StoredFish[];
}

const isFish = (value: unknown): value is StoredFish => {
  const fish = value as Partial<StoredFish> | null;

  return (
    typeof fish?.id === 'number' &&
    typeof fish.mass === 'number' &&
    typeof fish.species === 'number' &&
    SPECIES[fish.species] !== undefined
  );
};

// The aquarium belongs to this computer. Fish that were eaten stay eaten, and the only reset is clearing the browser.
export const loadFishes = (now: number = Date.now()): StoredFish[] => {
  try {
    const stored = JSON.parse(localStorage.getItem(STORAGE_KEY) ?? 'null') as StoredAquarium | null;

    if (stored === null || !Array.isArray(stored.fishes)) {
      return createPopulation();
    }

    const elapsed = Math.max(0, now - stored.savedAt) / MILLISECONDS_PER_SECOND;

    return stored.fishes
      .filter(isFish)
      .map((fish) => ({ ...fish, mass: Math.max(MINIMUM_MASS, fish.mass - MASS_LOST_PER_SECOND * elapsed) }));
  } catch {
    return createPopulation();
  }
};

export const saveFishes = (fishes: StoredFish[], now: number = Date.now()): void => {
  try {
    const stored: StoredAquarium = {
      savedAt: now,
      fishes: fishes.map(({ id, species, mass }) => ({ id, species, mass })),
    };
    localStorage.setItem(STORAGE_KEY, JSON.stringify(stored));
  } catch {
    // Losing the fish weight of one visit is better than getting in the way of the aquarium.
  }
};
