import type { ArchiveResult } from '@/projects/projectArchive';
import { exportArchive, importArchive, toArchiveFileName } from '@/projects/projectArchive';
import type { Project } from '@/projects/projectStore';

export const downloadProject = (project: Pick<Project, 'name' | 'files'>): void => {
  const bytes = exportArchive(project.files);
  const url = URL.createObjectURL(new Blob([bytes.slice()], { type: 'application/zip' }));
  const link = document.createElement('a');
  link.href = url;
  link.download = toArchiveFileName(project.name);
  link.click();
  URL.revokeObjectURL(url);
};

export const readArchiveFile = async (file: File): Promise<ArchiveResult> =>
  importArchive(new Uint8Array(await file.arrayBuffer()));
