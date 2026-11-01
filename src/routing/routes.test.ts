import type { Route } from './routes';
import { parseRoute, routeToHash } from './routes';

describe('routes', () => {
  it.each<[string, Route]>([
    ['#/', { name: 'home' }],
    ['#/new', { name: 'new', exampleId: null }],
    ['#/aquarium', { name: 'aquarium' }],
    ['#/globe', { name: 'globe' }],
    ['#/new/16-listas', { name: 'new', exampleId: '16-listas' }],
    ['#/projects/abc', { name: 'project', projectId: 'abc', file: null }],
    ['#/projects/abc/main.safira', { name: 'project', projectId: 'abc', file: 'main.safira' }],
  ])('reads and writes %s', (hash, route) => {
    expect(parseRoute(hash)).toEqual(route);
    expect(routeToHash(route)).toBe(hash);
  });

  it('keeps a file inside a folder in a single segment', () => {
    const route: Route = { name: 'project', projectId: 'abc', file: 'dados/notas.txt' };

    expect(routeToHash(route)).toBe('#/projects/abc/dados%2Fnotas.txt');
    expect(parseRoute(routeToHash(route))).toEqual(route);
  });

  it.each(['', '#', '#/nada', '#/projects', '#/%E0%A4%A', '#/lessons/aula-02'])(
    'sends %s to the home screen',
    (hash) => {
      expect(parseRoute(hash)).toEqual({ name: 'home' });
    },
  );
});
