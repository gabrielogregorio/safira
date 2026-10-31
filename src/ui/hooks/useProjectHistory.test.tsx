import { act, renderHook, waitFor } from '@testing-library/react';
import type { Project } from '@/projects/projectStore';
import { removeSnapshots } from '@/projects/snapshotStore';
import { useProjectHistory } from './useProjectHistory';

const project: Project = { id: 'p', name: 'P', files: { 'a.txt': 'hoje' }, breakpoints: {}, updatedAt: 0 };

const setup = () => {
  const onSave = vi.fn();
  const { result, rerender } = renderHook(({ current }) => useProjectHistory(current, onSave), {
    initialProps: { current: project },
  });

  return { result, rerender, onSave };
};

describe('useProjectHistory', () => {
  beforeEach(async () => {
    await removeSnapshots('p');
  });

  it('does not repeat a snapshot of the same content', () => {
    const { result } = setup();
    act(() => {
      expect(result.current.addSnapshot()).toBe(true);
    });
    act(() => {
      expect(result.current.addSnapshot()).toBe(false);
    });

    expect(result.current.snapshots).toHaveLength(1);
  });

  it('shows the past without changing the project', () => {
    const { result, rerender, onSave } = setup();
    act(() => {
      result.current.addSnapshot();
    });
    const edited = { ...project, files: { 'a.txt': 'amanha' } };
    rerender({ current: edited });
    act(() => {
      result.current.show(result.current.snapshots[0].id);
    });

    expect(result.current.shownProject.files).toEqual({ 'a.txt': 'hoje' });
    expect(onSave).not.toHaveBeenCalled();
  });

  it('keeps the present as a snapshot when the past is edited', () => {
    const { result, rerender, onSave } = setup();
    act(() => {
      result.current.addSnapshot();
    });
    const edited = { ...project, files: { 'a.txt': 'amanha' } };
    rerender({ current: edited });
    act(() => {
      result.current.show(result.current.snapshots[0].id);
    });
    const change = { ...result.current.shownProject, files: { 'a.txt': 'outro' } };
    act(() => {
      result.current.saveProject(change);
    });

    expect(onSave).toHaveBeenCalledWith(change);
    expect(result.current.viewed).toBeNull();
    expect(result.current.snapshots.at(-1)?.files).toEqual({ 'a.txt': 'amanha' });
  });

  it('renames while looking at the past without leaving it', () => {
    const { result, onSave } = setup();
    act(() => {
      result.current.addSnapshot();
    });
    act(() => {
      result.current.show(result.current.snapshots[0].id);
    });
    act(() => {
      result.current.saveProject({ ...result.current.shownProject, name: 'Novo' });
    });

    expect(onSave).toHaveBeenCalledWith(expect.objectContaining({ name: 'Novo', files: project.files }));
    expect(result.current.viewed).not.toBeNull();
  });

  it('loads what was stored', async () => {
    const first = setup();
    act(() => {
      first.result.current.addSnapshot();
    });
    await waitFor(async () => {
      const second = renderHook(() => useProjectHistory(project, vi.fn()));
      await waitFor(() => {
        expect(second.result.current.snapshots).toHaveLength(1);
      });
    });
  });
});
