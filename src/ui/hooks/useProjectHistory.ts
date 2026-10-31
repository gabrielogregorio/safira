import { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import type { Project } from '@/projects/projectStore';
import type { Snapshot } from '@/projects/snapshotStore';
import { createSnapshot, loadSnapshots, MAXIMUM_SNAPSHOTS, saveSnapshots } from '@/projects/snapshotStore';

export interface ProjectHistory {
  snapshots: Snapshot[];
  viewed: Snapshot | null;
  // Grows on every jump in time, so that the editor starts again from what is shown.
  generation: number;
  shownProject: Project;
  saveProject: (project: Project) => void;
  addSnapshot: () => boolean;
  show: (snapshotId: string | null) => void;
}

const hasSameContent = (first: Pick<Snapshot, 'files'>, second: Pick<Snapshot, 'files'>): boolean =>
  JSON.stringify(first.files) === JSON.stringify(second.files);

export const useProjectHistory = (project: Project, onSaveProject: (project: Project) => void): ProjectHistory => {
  const [snapshots, setSnapshots] = useState<Snapshot[]>([]);
  const [viewed, setViewed] = useState<Snapshot | null>(null);
  const [generation, setGeneration] = useState(0);
  const latestProject = useRef(project);
  const latestSnapshots = useRef(snapshots);
  const latestViewed = useRef(viewed);

  useEffect(() => {
    latestProject.current = project;
  }, [project]);

  useEffect(() => {
    let isCurrent = true;

    void loadSnapshots(project.id).then((loaded) => {
      if (isCurrent) {
        latestSnapshots.current = loaded;
        setSnapshots(loaded);
      }
    });

    return () => {
      isCurrent = false;
    };
  }, [project.id]);

  const store = useCallback((source: Project): boolean => {
    const last = latestSnapshots.current.at(-1);

    if (last !== undefined && hasSameContent(last, source)) {
      return false;
    }

    const next = [...latestSnapshots.current, createSnapshot(source)].slice(-MAXIMUM_SNAPSHOTS);
    latestSnapshots.current = next;
    setSnapshots(next);
    void saveSnapshots(source.id, next);

    return true;
  }, []);

  const addSnapshot = useCallback((): boolean => store(latestProject.current), [store]);

  // Looking at the past changes nothing. The first edit makes that past the present, and the old present a snapshot.
  const saveProject = useCallback(
    (next: Project) => {
      const shown = latestViewed.current;

      if (shown === null) {
        onSaveProject(next);
      } else if (next.files === shown.files && next.breakpoints === shown.breakpoints) {
        onSaveProject({ ...latestProject.current, name: next.name });
      } else {
        store(latestProject.current);
        latestViewed.current = null;
        setViewed(null);
        onSaveProject(next);
      }
    },
    [onSaveProject, store],
  );

  const show = useCallback((snapshotId: string | null) => {
    const target = latestSnapshots.current.find((snapshot) => snapshot.id === snapshotId) ?? null;
    latestViewed.current = target;
    setViewed(target);
    setGeneration((current) => current + 1);
  }, []);

  const shownProject = useMemo(
    () =>
      viewed === null
        ? project
        : { ...project, files: viewed.files, breakpoints: viewed.breakpoints, order: viewed.order },
    [project, viewed],
  );

  return { snapshots, viewed, generation, shownProject, saveProject, addSnapshot, show };
};
