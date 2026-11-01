import { storageKey } from '@/settings/storageKey';

const STORAGE_KEY = storageKey('drafts.v1');

export type ProjectDrafts = Record<string, string>;

type AllDrafts = Record<string, ProjectDrafts>;

const readAll = (): AllDrafts => {
  try {
    const parsed: unknown = JSON.parse(localStorage.getItem(STORAGE_KEY) ?? '{}');

    return typeof parsed === 'object' && parsed !== null ? (parsed as AllDrafts) : {};
  } catch {
    return {};
  }
};

const writeAll = (drafts: AllDrafts): void => {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(drafts));
  } catch {
    // Drafts are a safety net: the open tabs keep working when the browser refuses to store them.
  }
};

export const loadDrafts = (projectId: string): ProjectDrafts => readAll()[projectId] ?? {};

export const saveDrafts = (projectId: string, drafts: ProjectDrafts): void => {
  const others = Object.entries(readAll()).filter(([id]) => id !== projectId);
  const entries = Object.keys(drafts).length === 0 ? others : [...others, [projectId, drafts] as const];

  writeAll(Object.fromEntries(entries));
};

export const clearDrafts = (projectId: string): void => {
  saveDrafts(projectId, {});
};
