import {
  addScriptVersion,
  isSupportedVersion,
  LANGUAGE_VERSION,
  LEGACY_VERSION,
  readScriptVersion,
  SUPPORTED_VERSIONS,
} from './version';

describe('script version', () => {
  it('reads the hidden first line and separates it from the code', () => {
    expect(readScriptVersion('#safira 0.9\nmostre 1')).toEqual({ version: '0.9', isDeclared: true, body: 'mostre 1' });
  });

  it('treats a script without the line as a legacy script', () => {
    expect(readScriptVersion('mostre 1')).toEqual({ version: LEGACY_VERSION, isDeclared: false, body: 'mostre 1' });
  });

  it('does not read a normal comment as a version', () => {
    expect(readScriptVersion('# safira 0.9\nmostre 1').isDeclared).toBe(false);
  });

  it('writes the current version by default and reads it back', () => {
    expect(readScriptVersion(addScriptVersion('mostre 1'))).toMatchObject({
      version: LANGUAGE_VERSION,
      body: 'mostre 1',
    });
  });

  it('declares every supported version', () => {
    expect(SUPPORTED_VERSIONS).toEqual(['0.38', '0.9', '1.0', '1.1']);
  });

  it('accepts a declared version and refuses an unknown one', () => {
    expect(isSupportedVersion(LEGACY_VERSION)).toBe(true);
    expect(isSupportedVersion('9.0')).toBe(false);
  });
});
