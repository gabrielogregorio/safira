import { createTranslator } from '@/i18n/i18n';
import { describeArchiveResult } from './archiveMessages';

const t = createTranslator('en-us');

describe('describeArchiveResult', () => {
  it('counts the files without folder markers', () => {
    expect(describeArchiveResult(t, { ok: true, files: { a: '', 'b/.keep': '' }, skipped: [] })).toBe(
      'Imported 1 files.',
    );
  });

  it('lists what was skipped', () => {
    expect(describeArchiveResult(t, { ok: true, files: { a: '' }, skipped: ['x.png'] })).toBe(
      'Imported 1 files. Skipped: x.png.',
    );
  });

  it.each([
    ['invalid', 'This file is not a valid .zip.'],
    ['empty', 'This .zip has no text files.'],
    ['too-large', 'This .zip is too large: the limit is 500 files and 4 MB.'],
  ] as const)('explains the failure %s', (failure, message) => {
    expect(describeArchiveResult(t, { ok: false, failure })).toBe(message);
  });
});
