const CURRENT_DIRECTORY_PREFIX = /^(\.\/)+/;

export const normalizePath = (path: string): string => path.trim().replace(CURRENT_DIRECTORY_PREFIX, '');

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
