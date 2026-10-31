import type { ArchiveResult } from '@/projects/projectArchive';
import { exportArchive, importArchive, toArchiveFileName } from '@/projects/projectArchive';
import type { Project } from '@/projects/projectStore';

const saveBlob = (blob: Blob, fileName: string): void => {
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = fileName;
  link.click();
  URL.revokeObjectURL(url);
};

export const downloadProject = (project: Pick<Project, 'name' | 'files'>): void => {
  const bytes = exportArchive(project.files);
  saveBlob(new Blob([bytes.slice()], { type: 'application/zip' }), toArchiveFileName(project.name));
};

export const downloadFile = (name: string, text: string): void => {
  saveBlob(new Blob([text], { type: 'text/plain;charset=utf-8' }), name);
};

export const readArchiveFile = async (file: File): Promise<ArchiveResult> =>
  importArchive(new Uint8Array(await file.arrayBuffer()));
