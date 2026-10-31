import { zipSync, strToU8 } from 'fflate';
import { downloadFile, downloadProject, readArchiveFile } from './archiveFiles';

describe('archive files', () => {
  let saved: Blob[];
  let clicked: string[];

  beforeEach(() => {
    saved = [];
    clicked = [];
    URL.createObjectURL = (blob) => {
      saved.push(blob as Blob);

      return 'blob:safira';
    };
    URL.revokeObjectURL = vi.fn();
    vi.spyOn(HTMLAnchorElement.prototype, 'click').mockImplementation(function click(this: HTMLAnchorElement) {
      clicked.push(this.download);
    });
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  it('downloads a file as it is', async () => {
    downloadFile('nota.txt', 'oi');

    expect(clicked).toEqual(['nota.txt']);
    await expect(saved[0].text()).resolves.toBe('oi');
  });

  it('downloads a project as a zip', () => {
    downloadProject({ name: 'Meu', files: { 'main.safira': 'mostre 1' } });

    expect(clicked[0]).toMatch(/\.zip$/);
    expect(saved).toHaveLength(1);
  });

  it('reads a zip back', async () => {
    const bytes = zipSync({ 'main.safira': strToU8('mostre 1') });
    const file = new File([new Uint8Array(bytes)], 'a.zip');

    await expect(readArchiveFile(file)).resolves.toMatchObject({ ok: true, files: { 'main.safira': 'mostre 1' } });
  });

  it('refuses what is not a zip', async () => {
    await expect(readArchiveFile(new File(['nada'], 'a.zip'))).resolves.toMatchObject({ ok: false });
  });
});
