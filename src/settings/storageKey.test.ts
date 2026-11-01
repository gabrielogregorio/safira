import { storageKey, storagePrefixFor } from './storageKey';

describe('storage keys', () => {
  it.each(['/', '/safira/', '/safira/index.html'])('uses the site prefix at %s', (pathname) => {
    expect(storagePrefixFor(pathname)).toBe('safira.');
  });

  it.each([
    ['/safira/preview/1.0.0/', 'safira-preview.1.0.0.'],
    ['/safira/preview/1.0.0/index.html', 'safira-preview.1.0.0.'],
    ['/safira/preview/fix-menu/', 'safira-preview.fix-menu.'],
  ])('gives %s its own prefix', (pathname, prefix) => {
    expect(storagePrefixFor(pathname)).toBe(prefix);
  });

  it('keeps the keys of the site that already hold data', () => {
    expect(storageKey('projects.v1')).toBe('safira.projects.v1');
  });
});
