import {
  clampFontSize,
  clampPanelSize,
  PANEL_LIMITS,
  DEFAULT_SETTINGS,
  loadSettings,
  MAXIMUM_FONT_SIZE,
  MINIMUM_FONT_SIZE,
  saveSettings,
} from './settings';

describe('settings', () => {
  beforeEach(() => {
    localStorage.clear();
  });

  it.each([
    [PANEL_LIMITS.sidebar.minimum - 1, PANEL_LIMITS.sidebar.minimum],
    [PANEL_LIMITS.sidebar.minimum, PANEL_LIMITS.sidebar.minimum],
    [PANEL_LIMITS.sidebar.maximum, PANEL_LIMITS.sidebar.maximum],
    [PANEL_LIMITS.sidebar.maximum + 1, PANEL_LIMITS.sidebar.maximum],
  ])('limits the sidebar %i to %i', (size, expected) => {
    expect(clampPanelSize('sidebar', size)).toBe(expected);
  });

  it('keeps panel sizes in whole pixels', () => {
    expect(clampPanelSize('output', 300.6)).toBe(301);
  });

  it('starts with the defaults', () => {
    expect(loadSettings()).toEqual(DEFAULT_SETTINGS);
  });

  it('keeps what was saved and fills new fields', () => {
    saveSettings({ ...DEFAULT_SETTINGS, theme: 'light' });

    expect(loadSettings().theme).toBe('light');
  });

  it('survives corrupted storage', () => {
    localStorage.setItem('safira.settings.v1', '{quebrado');

    expect(loadSettings()).toEqual(DEFAULT_SETTINGS);
  });

  it('does not throw when the browser blocks storage', () => {
    vi.spyOn(Storage.prototype, 'setItem').mockImplementationOnce(() => {
      throw new Error('blocked');
    });

    expect(() => {
      saveSettings(DEFAULT_SETTINGS);
    }).not.toThrow();
  });

  it.each([
    [MINIMUM_FONT_SIZE - 1, MINIMUM_FONT_SIZE],
    [MINIMUM_FONT_SIZE, MINIMUM_FONT_SIZE],
    [MAXIMUM_FONT_SIZE, MAXIMUM_FONT_SIZE],
    [MAXIMUM_FONT_SIZE + 1, MAXIMUM_FONT_SIZE],
  ])('limits the font size %i to %i', (size, expected) => {
    expect(clampFontSize(size)).toBe(expected);
  });
});
