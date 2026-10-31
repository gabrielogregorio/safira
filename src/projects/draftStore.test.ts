import { clearDrafts, loadDrafts, saveDrafts } from './draftStore';

describe('draftStore', () => {
  beforeEach(() => {
    localStorage.clear();
  });

  it('starts without drafts', () => {
    expect(loadDrafts('a')).toEqual({});
  });

  it('keeps the drafts of each project apart', () => {
    saveDrafts('a', { 'main.safira': 'um' });
    saveDrafts('b', { 'main.safira': 'dois' });

    expect(loadDrafts('a')).toEqual({ 'main.safira': 'um' });
    expect(loadDrafts('b')).toEqual({ 'main.safira': 'dois' });
  });

  it('replaces the previous drafts of a project', () => {
    saveDrafts('a', { x: '1' });
    saveDrafts('a', { y: '2' });

    expect(loadDrafts('a')).toEqual({ y: '2' });
  });

  it('removes the project when it has nothing left and keeps the others', () => {
    saveDrafts('a', { x: '1' });
    saveDrafts('b', { x: '2' });
    clearDrafts('a');

    expect(loadDrafts('a')).toEqual({});
    expect(loadDrafts('b')).toEqual({ x: '2' });
  });

  it('survives corrupted storage', () => {
    localStorage.setItem('safira.drafts.v1', '{quebrado');

    expect(loadDrafts('a')).toEqual({});
  });

  it('does not throw when the browser blocks storage', () => {
    vi.spyOn(Storage.prototype, 'setItem').mockImplementationOnce(() => {
      throw new Error('full');
    });

    expect(() => {
      saveDrafts('a', { x: '1' });
    }).not.toThrow();
  });
});
