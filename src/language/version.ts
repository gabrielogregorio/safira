export const LANGUAGE_VERSION = '1.0';

export const LEGACY_VERSION = '0.38';

// The scripts of the 0.9 series, which the bundled examples and lessons still declare.
const PREVIOUS_VERSION = '0.9';

export const SUPPORTED_VERSIONS = [LEGACY_VERSION, PREVIOUS_VERSION, LANGUAGE_VERSION];

const HEADER_PATTERN = /^#safira (\S+)[ \t]*(?:\n|$)/;

const buildHeader = (version: string): string => `#safira ${version}\n`;

export interface VersionedSource {
  version: string;
  isDeclared: boolean;
  body: string;
}

export const readScriptVersion = (source: string): VersionedSource => {
  const match = HEADER_PATTERN.exec(source);

  if (match === null) {
    return { version: LEGACY_VERSION, isDeclared: false, body: source };
  }

  return { version: match[1], isDeclared: true, body: source.slice(match[0].length) };
};

export const isSupportedVersion = (version: string): boolean => SUPPORTED_VERSIONS.includes(version);

export const addScriptVersion = (body: string, version: string = LANGUAGE_VERSION): string =>
  buildHeader(version) + body;
