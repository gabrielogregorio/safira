import {
  buildFileTree,
  folderMarkerPath,
  isFolderMarker,
  isInsideFolder,
  joinPath,
  sanitizePath,
  visibleFiles,
  provisionalName,
} from './fileTree';

describe('buildFileTree', () => {
  it('lists folders first and sorts by name', () => {
    expect(buildFileTree(['b.txt', 'pasta/x.txt', 'a.txt']).map((node) => node.name)).toEqual([
      'pasta',
      'a.txt',
      'b.txt',
    ]);
  });

  it('nests folders and keeps the full path', () => {
    expect(buildFileTree(['a/b/c.txt'])).toEqual([
      {
        kind: 'folder',
        name: 'a',
        path: 'a',
        children: [
          {
            kind: 'folder',
            name: 'b',
            path: 'a/b',
            children: [{ kind: 'file', name: 'c.txt', path: 'a/b/c.txt' }],
          },
        ],
      },
    ]);
  });

  it('shows an empty folder and hides its marker', () => {
    expect(buildFileTree([folderMarkerPath('vazia')])).toEqual([
      { kind: 'folder', name: 'vazia', path: 'vazia', children: [] },
    ]);
  });

  it('merges files of the same folder', () => {
    const [folder] = buildFileTree(['p/a', 'p/b']);

    expect(folder).toMatchObject({ children: [{ name: 'a' }, { name: 'b' }] });
  });
});

describe('paths', () => {
  it.each([
    ['nome.safira', 'nome.safira'],
    ['  a/b  ', 'a/b'],
    ['/a//b/', 'a/b'],
    ['a\\b', 'a/b'],
  ])('cleans %s', (path, expected) => {
    expect(sanitizePath(path)).toBe(expected);
  });

  it.each(['', '   ', '/', '../a', 'a/../b', './a'])('refuses %s', (path) => {
    expect(sanitizePath(path)).toBeNull();
  });

  it('joins a name to a folder', () => {
    expect(joinPath('a', 'b')).toBe('a/b');
    expect(joinPath(null, 'b')).toBe('b');
  });

  it('knows what is inside a folder without matching similar names', () => {
    expect(isInsideFolder('a/b', 'a')).toBe(true);
    expect(isInsideFolder('ab/c', 'a')).toBe(false);
  });

  it('hides folder markers from file lists', () => {
    expect(isFolderMarker('a/.keep')).toBe(true);
    expect(visibleFiles(['a/.keep', 'b.txt'])).toEqual(['b.txt']);
  });
});

describe('provisionalName', () => {
  it('uses the base when it is free', () => {
    expect(provisionalName('novo', '.safira', ['main.safira'], null)).toBe('novo.safira');
  });

  it('numbers the name past the ones in use', () => {
    expect(provisionalName('novo', '.safira', ['novo.safira', 'novo-2.safira'], null)).toBe('novo-3.safira');
  });

  it('only looks inside the target folder', () => {
    expect(provisionalName('novo', '.safira', ['novo.safira'], 'dados')).toBe('novo.safira');
    expect(provisionalName('novo', '.safira', ['dados/novo.safira'], 'dados')).toBe('novo-2.safira');
  });

  it('sees folders as taken names', () => {
    expect(provisionalName('pasta', '', ['pasta/.keep'], null)).toBe('pasta-2');
  });
});
