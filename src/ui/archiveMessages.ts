import type { Translate } from '@/i18n/i18n';
import type { ArchiveResult } from '@/projects/projectArchive';
import { visibleFiles } from '@/projects/fileTree';

export const describeArchiveResult = (t: Translate, result: ArchiveResult): string => {
  if (!result.ok) {
    if (result.failure === 'too-large') {
      return t('This .zip is too large: the limit is 500 files and 4 MB.');
    }

    return result.failure === 'empty' ? t('This .zip has no text files.') : t('This file is not a valid .zip.');
  }

  const count = visibleFiles(Object.keys(result.files)).length;

  return result.skipped.length === 0
    ? t('Imported {count} files.', { count })
    : t('Imported {count} files. Skipped: {skipped}.', { count, skipped: result.skipped.join(', ') });
};
