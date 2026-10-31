import { useCallback, useSyncExternalStore } from 'react';
import type { Route } from './routes';
import { parseRoute, routeToHash } from './routes';

const HASH_EVENT = 'hashchange';

const subscribe = (listener: () => void): (() => void) => {
  window.addEventListener(HASH_EVENT, listener);

  return () => {
    window.removeEventListener(HASH_EVENT, listener);
  };
};

const readHash = (): string => window.location.hash;

export const navigateTo = (route: Route): void => {
  const hash = routeToHash(route);

  if (hash !== window.location.hash) {
    window.history.pushState(null, '', hash);
    window.dispatchEvent(new HashChangeEvent(HASH_EVENT));
  }
};

export const useRoute = (): { route: Route; navigate: (route: Route) => void } => {
  const hash = useSyncExternalStore(subscribe, readHash);
  const navigate = useCallback((route: Route) => {
    navigateTo(route);
  }, []);

  return { route: parseRoute(hash), navigate };
};
