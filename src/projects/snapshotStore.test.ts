import { createSnapshot, loadSnapshots, removeSnapshots, saveSnapshots } from './snapshotStore';

describe('snapshotStore', () => {
  it('keeps the content of a project', () => {
    const snapshot = createSnapshot({ files: { 'a.txt': '1' }, breakpoints: { 'a.txt': [1] }, order: ['a.txt'] });

    expect(snapshot).toMatchObject({ files: { 'a.txt': '1' }, breakpoints: { 'a.txt': [1] }, order: ['a.txt'] });
  });

  it('stores snapshots per project and forgets them', async () => {
    const snapshot = createSnapshot({ files: {}, breakpoints: {} });
    await saveSnapshots('um', [snapshot]);

    expect(await loadSnapshots('um')).toEqual([snapshot]);
    expect(await loadSnapshots('dois')).toEqual([]);

    await removeSnapshots('um');

    expect(await loadSnapshots('um')).toEqual([]);
  });
});
