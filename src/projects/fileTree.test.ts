import type { TreeNode } from './fileTree';
import {
  buildFileTree,
  folderMarkerPath,
  isFolderMarker,
  isInsideFolder,
  joinPath,
  sanitizePath,
  visibleFiles,
  extensionStart,
  filesOfFolder,
  isPathTaken,
  movePath,
  parentFolder,
  planMove,
  provisionalName,
  renameTarget,
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

describe('movePath', () => {
  it('moves the item and what is inside it, and nothing else', () => {
    expect(movePath('a.txt', 'a.txt', 'b.txt')).toBe('b.txt');
    expect(movePath('dados/x/a.txt', 'dados', 'info')).toBe('info/x/a.txt');
    expect(movePath('dados2/a.txt', 'dados', 'info')).toBe('dados2/a.txt');
  });
});

describe('isPathTaken', () => {
  it('sees files and folders', () => {
    expect(isPathTaken(['a.txt', 'dados/.keep'], 'a.txt')).toBe(true);
    expect(isPathTaken(['a.txt', 'dados/.keep'], 'dados')).toBe(true);
    expect(isPathTaken(['a.txt', 'dados/.keep'], 'dad')).toBe(false);
  });
});

describe('extensionStart', () => {
  it.each([
    ['main.safira', 4],
    ['a.b.txt', 3],
    ['leia', 4],
    ['.env', 4],
  ])('finds it in %s', (name, position) => {
    expect(extensionStart(name)).toBe(position);
  });
});

describe('renameTarget', () => {
  const file = { kind: 'file', name: 'a.txt', path: 'dados/a.txt' } as const;
  const folder: TreeNode = { kind: 'folder', name: 'dados', path: 'x/dados', children: [] };

  it('stays in the same folder', () => {
    expect(renameTarget(file, 'b.safira')).toBe('dados/b.safira');
    expect(renameTarget(folder, 'info')).toBe('x/info');
  });

  it('keeps the extension when none is typed', () => {
    expect(renameTarget(file, ' b ')).toBe('dados/b.txt');
  });

  it('does not give an extension to a folder', () => {
    expect(renameTarget(folder, 'a.b')).toBe('x/a.b');
  });

  it.each(['', '  ', '.', '..', 'a/b', 'a\\b'])('refuses "%s"', (typed) => {
    expect(renameTarget(file, typed)).toBeNull();
  });
});

describe('planMove', () => {
  const paths = ['a.txt', 'b.txt', 'dados/c.txt', 'vazia/.keep'];
  const file = (path: string): TreeNode => ({ kind: 'file', name: path.split('/').at(-1) as string, path });
  const folder = (path: string): TreeNode => ({ kind: 'folder', name: path, path, children: [] });
  const namesAfter = (order: string[], moved: string[]): string[] =>
    buildFileTree(moved, order).map((node) => node.path);

  it('changes the order among siblings', () => {
    const plan = planMove(paths, [], file('b.txt'), file('a.txt'), 'before');

    expect(plan?.target).toBe('b.txt');
    expect(namesAfter(plan?.order ?? [], paths)).toEqual(['dados', 'vazia', 'b.txt', 'a.txt']);
  });

  it('puts an item after another', () => {
    const plan = planMove(paths, [], file('a.txt'), file('b.txt'), 'after');

    expect(namesAfter(plan?.order ?? [], paths)).toEqual(['dados', 'vazia', 'b.txt', 'a.txt']);
  });

  it('moves into a folder and back to the root', () => {
    expect(planMove(paths, [], file('a.txt'), folder('vazia'), 'inside')?.target).toBe('vazia/a.txt');
    expect(planMove(paths, [], file('dados/c.txt'), null, 'inside')?.target).toBe('c.txt');
  });

  it('refuses moves that cannot happen', () => {
    expect(planMove(paths, [], folder('dados'), folder('dados'), 'inside')).toBeNull();
    expect(planMove(['a/b/c.txt'], [], folder('a'), folder('a/b'), 'inside')).toBeNull();
    expect(planMove(['a.txt', 'x/a.txt'], [], file('a.txt'), folder('x'), 'inside')).toBeNull();
    expect(planMove(paths, [], file('a.txt'), file('a.txt'), 'before')).toBeNull();
  });

  it('finds the parent of a path', () => {
    expect(parentFolder('a/b/c.txt')).toBe('a/b');
    expect(parentFolder('c.txt')).toBeNull();
  });
});

describe('filesOfFolder', () => {
  it('keeps only what is inside, relative to the folder', () => {
    const files = { 'a/b/c.txt': '1', 'a/d.txt': '2', 'ab/e.txt': '3', 'f.txt': '4' };

    expect(filesOfFolder(files, 'a')).toEqual({ 'b/c.txt': '1', 'd.txt': '2' });
  });
});
