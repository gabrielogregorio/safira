export const prefersMotion = (): boolean =>
  document.documentElement.dataset['vision'] !== 'calm' &&
  typeof window.matchMedia === 'function' &&
  window.matchMedia('(prefers-reduced-motion: no-preference)').matches;
