import { normalizePath, VirtualFileSystem } from './virtualFileSystem';

describe('VirtualFileSystem', () => {
  it('treats ./a and a as the same file', () => {
    const files = new VirtualFileSystem({ './a': 'x' });

    expect(files.read('a')).toBe('x');
    expect(normalizePath('././a')).toBe('a');
  });

  it('returns null for a file that does not exist', () => {
    expect(new VirtualFileSystem().read('a')).toBeNull();
  });

  it('appends to the end of a file', () => {
    const files = new VirtualFileSystem({ a: 'x' });
    files.append('a', 'y');

    expect(files.read('a')).toBe('xy');
  });

  it('tells if a delete removed something', () => {
    const files = new VirtualFileSystem({ a: 'x' });

    expect(files.delete('a')).toBe(true);
    expect(files.delete('a')).toBe(false);
    expect(files.exists('a')).toBe(false);
  });

  it('lists files in order and exports a snapshot', () => {
    const files = new VirtualFileSystem({ b: '2', a: '1' });

    expect(files.list()).toEqual(['a', 'b']);
    expect(files.snapshot()).toEqual({ a: '1', b: '2' });
  });
});
