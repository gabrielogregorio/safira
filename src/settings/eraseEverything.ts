const PREFIX = 'safira.';

const removeFrom = (storage: Storage): void => {
  for (const key of Object.keys(storage).filter((name) => name.startsWith(PREFIX))) {
    storage.removeItem(key);
  }
};

/** Everything Safira keeps in this browser: projects, settings, fish and the fate of Professor Cat. */
export const eraseEverything = (): void => {
  removeFrom(localStorage);
  removeFrom(sessionStorage);
};
