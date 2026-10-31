import { strFromU8, strToU8, unzipSync, zipSync } from 'fflate';
import { FOLDER_MARKER, folderMarkerPath, isFolderMarker, sanitizePath } from './fileTree';

export const MAXIMUM_ARCHIVE_FILES = 500;
export const MAXIMUM_ARCHIVE_BYTES = 4 * 1024 * 1024;

export type ArchiveFailure = 'invalid' | 'too-large' | 'empty';

export type ArchiveResult =
  { ok: true; files: Record<string, string>; skipped: string[] } | { ok: false; failure: ArchiveFailure };

const DIRECTORY_SUFFIX = '/';
const REPLACEMENT_CHARACTER = '�';
const IGNORED_ENTRY = /(^|\/)(__MACOSX|\.DS_Store)(\/|$)/;

export const exportArchive = (files: Record<string, string>): Uint8Array => {
  const entries: Record<string, Uint8Array> = {};

  for (const [path, text] of Object.entries(files)) {
    if (isFolderMarker(path)) {
      entries[path.slice(0, -FOLDER_MARKER.length)] = new Uint8Array();
    } else {
      entries[path] = strToU8(text);
    }
  }

  return zipSync(entries);
};

const decodeText = (bytes: Uint8Array): string | null => {
  const text = strFromU8(bytes);

  return text.includes(REPLACEMENT_CHARACTER) || text.includes('\0') ? null : text;
};

const stripCommonRoot = (files: Record<string, string>): Record<string, string> => {
  const paths = Object.keys(files);
  const root = paths[0]?.split('/')[0];
  const hasCommonRoot = root !== undefined && paths.length > 0 && paths.every((path) => path.startsWith(`${root}/`));

  if (!hasCommonRoot) {
    return files;
  }

  return Object.fromEntries(Object.entries(files).map(([path, text]) => [path.slice(root.length + 1), text]));
};

const readEntries = (bytes: Uint8Array): Record<string, Uint8Array> | null => {
  let totalBytes = 0;
  let fileCount = 0;
  let isTooLarge = false;

  const entries = unzipSync(bytes, {
    filter: (entry) => {
      totalBytes += entry.originalSize;
      fileCount += 1;
      isTooLarge ||= totalBytes > MAXIMUM_ARCHIVE_BYTES || fileCount > MAXIMUM_ARCHIVE_FILES;

      return !isTooLarge;
    },
  });

  return isTooLarge ? null : entries;
};

export const importArchive = (bytes: Uint8Array): ArchiveResult => {
  let entries: Record<string, Uint8Array> | null;

  try {
    entries = readEntries(bytes);
  } catch {
    return { ok: false, failure: 'invalid' };
  }

  if (entries === null) {
    return { ok: false, failure: 'too-large' };
  }

  const files: Record<string, string> = {};
  const skipped: string[] = [];

  for (const [name, content] of Object.entries(entries)) {
    const path = sanitizePath(name);
    const text = decodeText(content);

    if (path === null || text === null) {
      skipped.push(name);
    } else if (!IGNORED_ENTRY.test(name)) {
      files[name.endsWith(DIRECTORY_SUFFIX) ? folderMarkerPath(path) : path] = text;
    }
  }

  if (Object.keys(files).length === 0) {
    return { ok: false, failure: 'empty' };
  }

  return { ok: true, files: stripCommonRoot(files), skipped };
};

export const toArchiveFileName = (projectName: string): string => {
  const slug = projectName.trim().replace(/[^\p{L}\p{N}_-]+/gu, '-');

  return `${slug === '' ? 'safira' : slug}.zip`;
};

export const toProjectName = (fileName: string): string => fileName.replace(/\.zip$/i, '');
