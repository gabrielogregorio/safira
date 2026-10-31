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

// What is inside a folder, with paths that start at that folder.
export const filesOfFolder = (files: Record<string, string>, folder: string): Record<string, string> =>
  Object.fromEntries(
    Object.entries(files)
      .filter(([path]) => isInsideFolder(path, folder))
      .map(([path, text]) => [path.slice(folder.length + 1), text]),
  );

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

export const parentFolder = (path: string): string | null => {
  const slash = path.lastIndexOf('/');

  return slash === -1 ? null : path.slice(0, slash);
};

const byFoldersThenName = (first: TreeNode, second: TreeNode): number => {
  if (first.kind !== second.kind) {
    return first.kind === 'folder' ? -1 : 1;
  }

  return first.name.localeCompare(second.name);
};

// A place the person chose wins. What has no place yet goes after it, in the usual order.
const byChosenOrder =
  (ranks: Map<string, number>) =>
  (first: TreeNode, second: TreeNode): number => {
    const firstRank = ranks.get(first.path);
    const secondRank = ranks.get(second.path);

    if (firstRank !== undefined && secondRank !== undefined) {
      return firstRank - secondRank;
    }

    if (firstRank === undefined && secondRank === undefined) {
      return byFoldersThenName(first, second);
    }

    return firstRank === undefined ? 1 : -1;
  };

const sortTree = (nodes: TreeNode[], ranks: Map<string, number>): TreeNode[] =>
  nodes
    .map((node) => (node.kind === 'folder' ? { ...node, children: sortTree(node.children, ranks) } : node))
    .sort(byChosenOrder(ranks));

const findOrCreateFolder = (siblings: TreeNode[], name: string, path: string): FolderNode => {
  const existing = siblings.find((node): node is FolderNode => node.kind === 'folder' && node.name === name);

  if (existing !== undefined) {
    return existing;
  }

  const folder: FolderNode = { kind: 'folder', name, path, children: [] };
  siblings.push(folder);

  return folder;
};

export const buildFileTree = (paths: string[], order: string[] = []): TreeNode[] => {
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

  return sortTree(root, new Map(order.map((path, index) => [path, index])));
};

const flattenTree = (nodes: TreeNode[]): string[] =>
  nodes.flatMap((node) => (node.kind === 'folder' ? [node.path, ...flattenTree(node.children)] : [node.path]));

export type DropPlace = 'before' | 'after' | 'inside';

export interface PlannedMove {
  target: string;
  order: string[];
}

// Without an anchor the item goes to the end of the root. Returns null for a move that cannot happen.
export const planMove = (
  paths: string[],
  order: string[],
  node: TreeNode,
  anchor: TreeNode | null,
  place: DropPlace,
): PlannedMove | null => {
  const anchorPath = anchor?.path ?? '';
  const destination = place === 'inside' ? (anchor?.path ?? null) : parentFolder(anchorPath);
  const target = joinPath(destination, node.name);
  const isIntoItself = destination !== null && (destination === node.path || isInsideFolder(destination, node.path));

  if (anchor?.path === node.path || isIntoItself || (target !== node.path && isPathTaken(paths, target))) {
    return null;
  }

  const others = flattenTree(buildFileTree(paths, order))
    .filter((path) => path !== node.path)
    .map((path) => movePath(path, node.path, target));
  const index = others.indexOf(anchorPath) + Number(place === 'after');

  if (place === 'inside') {
    return { target, order: [...others, target] };
  }

  return { target, order: [...others.slice(0, index), target, ...others.slice(index)] };
};
