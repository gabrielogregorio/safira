const SITE_PREFIX = 'safira.';
const PREVIEW_PATH = /\/preview\/([^/]+)\//;

export const storagePrefixFor = (pathname: string): string => {
  const branch = PREVIEW_PATH.exec(pathname)?.[1];

  return branch === undefined ? SITE_PREFIX : `safira-preview.${branch}.`;
};

/** Previews live on the origin of the site, so each one keeps its data under its own prefix. */
export const storagePrefix = (): string => storagePrefixFor(location.pathname);

export const storageKey = (name: string): string => storagePrefix() + name;
