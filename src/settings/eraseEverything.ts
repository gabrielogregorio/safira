import { storagePrefix } from './storageKey';

const removeFrom = (storage: Storage, prefix: string): void => {
  for (const key of Object.keys(storage).filter((name) => name.startsWith(prefix))) {
    storage.removeItem(key);
  }
};

/** Everything this copy of Safira keeps in this browser: projects, settings, fish and the fate of Professor Cat. */
export const eraseEverything = (prefix: string = storagePrefix()): void => {
  removeFrom(localStorage, prefix);
  removeFrom(sessionStorage, prefix);
};
