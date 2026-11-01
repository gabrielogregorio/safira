import { addScriptVersion, readScriptVersion } from '@/language/version';

export interface EditorTab {
  file: string;
  text: string;
  savedText: string;
  version: string;
}

const SCRIPT_EXTENSION = '.safira';

export const isScript = (file: string): boolean => file.endsWith(SCRIPT_EXTENSION);

export const openTab = (file: string, stored: string): EditorTab => {
  const { body, version } = isScript(file) ? readScriptVersion(stored) : { body: stored, version: '' };

  return { file, text: body, savedText: body, version };
};

export const toStoredText = (tab: Pick<EditorTab, 'file' | 'text'>): string =>
  isScript(tab.file) ? addScriptVersion(tab.text) : tab.text;

export const moveTab = (tab: EditorTab, file: string): EditorTab => ({
  ...tab,
  file,
  version: tab.version === '' ? readScriptVersion(tab.text).version : tab.version,
});

export const isDirty = (tab: EditorTab): boolean => tab.text !== tab.savedText;

export const nextUntitledName = (existing: string[]): string => {
  let number = 1;

  while (existing.includes(`script-${number}${SCRIPT_EXTENSION}`)) {
    number += 1;
  }

  return `script-${number}${SCRIPT_EXTENSION}`;
};

export const withScriptExtension = (name: string): string => (name.includes('.') ? name : name + SCRIPT_EXTENSION);

export const mergeProgramFiles = (tabs: EditorTab[], files: Record<string, string>): EditorTab[] =>
  tabs.map((tab) => {
    const stored = files[tab.file];

    return stored === undefined || isDirty(tab) ? tab : openTab(tab.file, stored);
  });
