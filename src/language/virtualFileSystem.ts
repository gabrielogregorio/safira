const CURRENT_DIRECTORY_PREFIX = /^(\.\/)+/;

export const normalizePath = (path: string): string => path.trim().replace(CURRENT_DIRECTORY_PREFIX, '');

const SAFIRA_EXTENSION = '.safira';

export const withSafiraExtension = (name: string): string =>
  name.endsWith(SAFIRA_EXTENSION) ? name : `${name}${SAFIRA_EXTENSION}`;

const walkPath = (folder: string[], path: string): string => {
  const walked = [...folder];

  for (const segment of path.split('/')) {
    if (segment === '..') {
      walked.pop();
    } else if (segment !== '.' && segment !== '') {
      walked.push(segment);
    }
  }

  return walked.join('/');
};

// Beside the file that imports first, as `./` promises. Then from the root, which is how old scripts name files.
export const importCandidates = (importer: string, name: string): string[] => {
  const file = withSafiraExtension(name);

  return [...new Set([walkPath(importer.split('/').slice(0, -1), file), walkPath([], file)])];
};

export class VirtualFileSystem {
  private readonly files: Map<string, string>;

  public constructor(initialFiles: Record<string, string> = {}) {
    this.files = new Map(Object.entries(initialFiles).map(([path, text]) => [normalizePath(path), text]));
  }

  public exists(path: string): boolean {
    return this.files.has(normalizePath(path));
  }

  public read(path: string): string | null {
    return this.files.get(normalizePath(path)) ?? null;
  }

  public write(path: string, text: string): void {
    this.files.set(normalizePath(path), text);
  }

  public append(path: string, text: string): void {
    const normalized = normalizePath(path);
    this.files.set(normalized, (this.files.get(normalized) ?? '') + text);
  }

  public delete(path: string): boolean {
    return this.files.delete(normalizePath(path));
  }

  public list(): string[] {
    return [...this.files.keys()].sort((first, second) => first.localeCompare(second));
  }

  public snapshot(): Record<string, string> {
    return Object.fromEntries(this.files);
  }
}
