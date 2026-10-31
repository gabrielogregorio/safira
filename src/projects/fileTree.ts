export const FOLDER_MARKER = '.keep';

export interface FileNode {
  kind: 'file';
  name: string;
  path: string;
}

export interface FolderNode {
  kind: 'folder';
  name: string;
  path: string;
  children: TreeNode[];
}

export type TreeNode = FileNode | FolderNode;

export const folderMarkerPath = (folder: string): string => `${folder}/${FOLDER_MARKER}`;

export const isFolderMarker = (path: string): boolean => path.split('/').at(-1) === FOLDER_MARKER;

export const visibleFiles = (paths: string[]): string[] => paths.filter((path) => !isFolderMarker(path));

export const sanitizePath = (path: string): string | null => {
  const segments = path.trim().replace(/\\/g, '/').split('/').filter(Boolean);
  const isValid = segments.length > 0 && segments.every((segment) => segment !== '.' && segment !== '..');

  return isValid ? segments.join('/') : null;
};

export const joinPath = (folder: string | null, name: string): string => (folder === null ? name : `${folder}/${name}`);

export const isInsideFolder = (path: string, folder: string): boolean => path.startsWith(`${folder}/`);

export const isPathTaken = (paths: string[], path: string): boolean =>
  paths.some((existing) => existing === path || isInsideFolder(existing, path));

export const provisionalName = (base: string, extension: string, paths: string[], folder: string | null): string => {
  let candidate = `${base}${extension}`;
  let copy = 2;

  while (isPathTaken(paths, joinPath(folder, candidate))) {
    candidate = `${base}-${copy}${extension}`;
    copy += 1;
  }

  return candidate;
};

export const movePath = (path: string, from: string, to: string): string =>
  path === from || isInsideFolder(path, from) ? `${to}${path.slice(from.length)}` : path;

// The dot that starts the extension. A name like `.env` has none, so all of it is the stem.
export const extensionStart = (name: string): number => {
  const dot = name.lastIndexOf('.');

  return dot > 0 ? dot : name.length;
};

const isSafeSegment = (name: string): boolean => name !== '.' && name !== '..' && !/[/\\]/.test(name);

// A typed name without an extension keeps the one the file had, as a file manager does.
export const renameTarget = (node: TreeNode, typedName: string): string | null => {
  const typed = typedName.trim();

  if (typed === '' || !isSafeSegment(typed)) {
    return null;
  }

  const name =
    node.kind === 'file' && extensionStart(typed) === typed.length
      ? `${typed}${node.name.slice(extensionStart(node.name))}`
      : typed;

  return `${node.path.slice(0, node.path.length - node.name.length)}${name}`;
};

const byFoldersThenName = (first: TreeNode, second: TreeNode): number => {
  if (first.kind !== second.kind) {
    return first.kind === 'folder' ? -1 : 1;
  }

  return first.name.localeCompare(second.name);
};

const sortTree = (nodes: TreeNode[]): TreeNode[] =>
  nodes
    .map((node) => (node.kind === 'folder' ? { ...node, children: sortTree(node.children) } : node))
    .sort(byFoldersThenName);

const findOrCreateFolder = (siblings: TreeNode[], name: string, path: string): FolderNode => {
  const existing = siblings.find((node): node is FolderNode => node.kind === 'folder' && node.name === name);

  if (existing !== undefined) {
    return existing;
  }

  const folder: FolderNode = { kind: 'folder', name, path, children: [] };
  siblings.push(folder);

  return folder;
};

export const buildFileTree = (paths: string[]): TreeNode[] => {
  const root: TreeNode[] = [];

  for (const path of paths) {
    const segments = path.split('/');
    const fileName = segments.pop() as string;
    let siblings = root;
    let currentPath = '';

    for (const segment of segments) {
      currentPath = currentPath === '' ? segment : `${currentPath}/${segment}`;
      siblings = findOrCreateFolder(siblings, segment, currentPath).children;
    }

    if (fileName !== FOLDER_MARKER) {
      siblings.push({ kind: 'file', name: fileName, path });
    }
  }

  return sortTree(root);
};
