import localforage from 'localforage';
import type { Project } from './projectStore';

export const MAXIMUM_SNAPSHOTS = 200;

export interface Snapshot {
  id: string;
  createdAt: number;
  files: Record<string, string>;
  breakpoints: Record<string, number[]>;
  order?: string[];
}

// Snapshots can be many and large, so they stay out of localStorage. The project itself still lives there, because
// the app needs it synchronously and it is written on every pause in typing.
const store = localforage.createInstance({ name: 'safira', storeName: 'snapshots' });

export const createSnapshot = (project: Pick<Project, 'files' | 'breakpoints' | 'order'>): Snapshot => ({
  id: crypto.randomUUID(),
  createdAt: Date.now(),
  files: project.files,
  breakpoints: project.breakpoints,
  ...(project.order === undefined ? {} : { order: project.order }),
});

export const loadSnapshots = async (projectId: string): Promise<Snapshot[]> => {
  try {
    return (await store.getItem<Snapshot[]>(projectId)) ?? [];
  } catch {
    return [];
  }
};

export const saveSnapshots = async (projectId: string, snapshots: Snapshot[]): Promise<boolean> => {
  try {
    await store.setItem(projectId, snapshots);

    return true;
  } catch {
    return false;
  }
};

export const removeSnapshots = async (projectId: string): Promise<void> => {
  try {
    await store.removeItem(projectId);
  } catch {
    // Orphan snapshots take space and nothing else.
  }
};
