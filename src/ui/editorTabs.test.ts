import {
  isDirty,
  isScript,
  mergeProgramFiles,
  moveTab,
  nextUntitledName,
  openTab,
  toStoredText,
  withScriptExtension,
} from './editorTabs';

describe('editor tabs', () => {
  it('hides the version line of a script from the editor', () => {
    expect(openTab('a.safira', '#safira 0.9\nmostre 1')).toMatchObject({ text: 'mostre 1', version: '0.9' });
  });

  it('writes the version line back when saving a script', () => {
    expect(toStoredText({ file: 'a.safira', text: 'mostre 1' })).toBe('#safira 1.0\nmostre 1');
  });

  it('keeps a text file exactly as it is', () => {
    expect(openTab('a.txt', '#safira 0.9').text).toBe('#safira 0.9');
    expect(toStoredText({ file: 'a.txt', text: 'oi' })).toBe('oi');
    expect(isScript('a.txt')).toBe(false);
  });

  it('marks a tab as changed only when the text differs from the saved one', () => {
    const tab = openTab('a.safira', 'mostre 1');

    expect(isDirty(tab)).toBe(false);
    expect(isDirty({ ...tab, text: 'mostre 2' })).toBe(true);
  });

  it('finds the first free name', () => {
    expect(nextUntitledName(['script-1.safira'])).toBe('script-2.safira');
  });

  it('adds the extension only when the name has none', () => {
    expect(withScriptExtension('novo')).toBe('novo.safira');
    expect(withScriptExtension('dados.txt')).toBe('dados.txt');
  });

  it('updates clean tabs with what the program wrote and preserves unsaved work', () => {
    const clean = openTab('a.txt', 'velho');
    const dirty = { ...openTab('b.txt', 'velho'), text: 'editado' };
    const result = mergeProgramFiles([clean, dirty], { 'a.txt': 'novo', 'b.txt': 'novo' });

    expect(result.map((tab) => tab.text)).toEqual(['novo', 'editado']);
  });

  it('reads the version of a text file that becomes a script', () => {
    const moved = moveTab(openTab('a.txt', '#safira 0.9\nmostre 1'), 'a.safira');

    expect(moved).toMatchObject({ file: 'a.safira', version: '0.9' });
  });

  it('keeps the version a script already had when it moves', () => {
    const moved = moveTab(openTab('a.safira', '#safira 0.9\nmostre 1'), 'pasta/a.safira');

    expect(moved).toMatchObject({ file: 'pasta/a.safira', text: 'mostre 1', version: '0.9' });
  });

  it('keeps a tab whose file the program did not send', () => {
    const tab = openTab('a.txt', 'x');

    expect(mergeProgramFiles([tab], {})).toEqual([tab]);
  });
});
