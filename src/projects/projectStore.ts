import { addScriptVersion } from '@/language/version';

export const MAIN_FILE = 'main.safira';

const STORAGE_KEY = 'safira.projects.v1';

export interface Project {
  id: string;
  name: string;
  files: Record<string, string>;
  breakpoints: Record<string, number[]>;
  order?: string[];
  updatedAt: number;
}

const isProject = (value: unknown): value is Project => {
  const candidate = value as Partial<Project> | null;

  return typeof candidate?.id === 'string' && typeof candidate.name === 'string' && typeof candidate.files === 'object';
};

export const loadProjects = (): Project[] => {
  try {
    const parsed: unknown = JSON.parse(localStorage.getItem(STORAGE_KEY) ?? '[]');

    return Array.isArray(parsed) ? parsed.filter(isProject) : [];
  } catch {
    return [];
  }
};

export const saveProjects = (projects: Project[]): boolean => {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(projects));

    return true;
  } catch {
    return false;
  }
};

export const createProject = (name: string, source: string = addScriptVersion('')): Project => ({
  id: crypto.randomUUID(),
  name,
  files: { [MAIN_FILE]: source },
  breakpoints: {},
  updatedAt: Date.now(),
});

export const upsertProject = (projects: Project[], project: Project): Project[] => {
  const others = projects.filter((candidate) => candidate.id !== project.id);

  return [{ ...project, updatedAt: Date.now() }, ...others];
};

export const removeProject = (projects: Project[], id: string): Project[] =>
  projects.filter((project) => project.id !== id);
