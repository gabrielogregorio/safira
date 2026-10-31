import { strToU8, zipSync } from 'fflate';
import {
  exportArchive,
  importArchive,
  MAXIMUM_ARCHIVE_BYTES,
  MAXIMUM_ARCHIVE_FILES,
  toArchiveFileName,
  toProjectName,
} from './projectArchive';

const zipOf = (files: Record<string, string>): Uint8Array =>
  zipSync(Object.fromEntries(Object.entries(files).map(([name, text]) => [name, strToU8(text)])));

describe('project archives', () => {
  it('restores what was exported, with accents and folders', () => {
    const files = { 'main.safira': '#safira 1.0\nmostre "olá"', 'dados/notas.txt': 'açaí' };

    expect(importArchive(exportArchive(files))).toEqual({ ok: true, files, skipped: [] });
  });

  it('keeps empty folders', () => {
    const files = { 'main.safira': 'x', 'vazia/.keep': '' };

    expect(importArchive(exportArchive(files))).toMatchObject({ files });
  });

  it('removes the single folder that wraps a zipped project', () => {
    expect(importArchive(zipOf({ 'jogo/main.safira': 'a', 'jogo/lib/x.safira': 'b' }))).toMatchObject({
      files: { 'main.safira': 'a', 'lib/x.safira': 'b' },
    });
  });

  it('keeps folders when there are several at the root', () => {
    expect(importArchive(zipOf({ 'a/x': '1', 'b/y': '2' }))).toMatchObject({ files: { 'a/x': '1', 'b/y': '2' } });
  });

  it('refuses paths that try to leave the project', () => {
    const result = importArchive(zipOf({ '../fora.txt': 'mal', 'bom.txt': 'ok' }));

    expect(result).toEqual({ ok: true, files: { 'bom.txt': 'ok' }, skipped: ['../fora.txt'] });
  });

  it('skips binary files and reports them', () => {
    const archive = zipSync({ 'foto.png': new Uint8Array([0xff, 0xd8, 0xff, 0x00]), 'a.txt': strToU8('ok') });

    expect(importArchive(archive)).toEqual({ ok: true, files: { 'a.txt': 'ok' }, skipped: ['foto.png'] });
  });

  it('ignores the metadata of macOS archives', () => {
    expect(importArchive(zipOf({ '__MACOSX/a': 'x', 'b.txt': 'ok' }))).toMatchObject({ files: { 'b.txt': 'ok' } });
  });

  it('rejects what is not a zip file', () => {
    expect(importArchive(strToU8('isso nao e zip'))).toEqual({ ok: false, failure: 'invalid' });
  });

  it('rejects an archive without files', () => {
    expect(importArchive(zipSync({}))).toEqual({ ok: false, failure: 'empty' });
  });

  it('rejects an archive that expands beyond the limit', () => {
    const bomb = zipSync({ 'a.txt': new Uint8Array(MAXIMUM_ARCHIVE_BYTES + 1) });

    expect(importArchive(bomb)).toEqual({ ok: false, failure: 'too-large' });
  });

  it('accepts an archive exactly at the size limit', () => {
    const archive = zipSync({ 'a.txt': new Uint8Array(MAXIMUM_ARCHIVE_BYTES).fill(97) });

    expect(importArchive(archive).ok).toBe(true);
  });

  it('rejects an archive with too many files', () => {
    const files = Object.fromEntries(
      Array.from({ length: MAXIMUM_ARCHIVE_FILES + 1 }, (_value, index) => [`${index}.txt`, 'x']),
    );

    expect(importArchive(zipOf(files))).toEqual({ ok: false, failure: 'too-large' });
  });

  it('builds a safe file name for the download', () => {
    expect(toArchiveFileName('Meu jogo: fase 1')).toBe('Meu-jogo-fase-1.zip');
    expect(toArchiveFileName('   ')).toBe('safira.zip');
  });

  it('uses the file name as the project name', () => {
    expect(toProjectName('jogo.ZIP')).toBe('jogo');
  });
});
