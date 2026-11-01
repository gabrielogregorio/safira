import { KeyTracker, normalizeKey, parseKeyCombo } from './keys';

describe('normalizeKey', () => {
  it.each([
    ['ArrowUp', 'arrowup'],
    ['ARROWUP', 'arrowup'],
    ['cima', 'arrowup'],
    ['Pra Cima', 'arrowup'],
    ['up', 'arrowup'],
    ['arriba', 'arrowup'],
    ['上', 'arrowup'],
    ['Enter', 'enter'],
    ['enter', 'enter'],
    ['ENTER', 'enter'],
    ['エンター', 'enter'],
    [' ', 'space'],
    ['espaço', 'space'],
    ['A', 'a'],
    ['a', 'a'],
    ['7', '7'],
    ['Esc', 'escape'],
  ])('reads %s', (name, key) => {
    expect(normalizeKey(name)).toBe(key);
  });

  it('knows nothing about other names', () => {
    expect(normalizeKey('banana')).toBeNull();
  });
});

describe('parseKeyCombo', () => {
  it('splits a combination', () => {
    expect(parseKeyCombo('Shift+Enter')).toEqual(['shift', 'enter']);
  });

  it('refuses a combination with an unknown key', () => {
    expect(parseKeyCombo('Shift+banana')).toBeNull();
  });
});

describe('KeyTracker', () => {
  it('answers a press once', () => {
    const keys = new KeyTracker();
    keys.press('enter');

    expect(keys.check('press', ['enter'])).toBe(true);
    expect(keys.check('press', ['enter'])).toBe(false);
  });

  it('ignores the repeat of a key that is still down', () => {
    const keys = new KeyTracker();
    keys.press('enter');
    keys.check('press', ['enter']);
    keys.press('enter');

    expect(keys.check('press', ['enter'])).toBe(false);
  });

  it('answers a hold for as long as the key is down', () => {
    const keys = new KeyTracker();
    keys.press('a');

    expect(keys.check('hold', ['a'])).toBe(true);
    expect(keys.check('hold', ['a'])).toBe(true);

    keys.release('a');

    expect(keys.check('hold', ['a'])).toBe(false);
  });

  it('answers a release once', () => {
    const keys = new KeyTracker();
    keys.press('a');

    expect(keys.check('release', ['a'])).toBe(false);

    keys.release('a');

    expect(keys.check('release', ['a'])).toBe(true);
    expect(keys.check('release', ['a'])).toBe(false);
  });

  it('ignores the release of a key that went down before the program started', () => {
    const keys = new KeyTracker();
    keys.release('enter');

    expect(keys.check('release', ['enter'])).toBe(false);
  });

  it('lets two conditions see the same press', () => {
    const keys = new KeyTracker();
    keys.press('enter');

    expect(keys.check('press', ['enter'])).toBe(true);
    expect(keys.check('press', ['shift', 'enter'])).toBe(false);
  });

  it('needs the other keys of a combination', () => {
    const keys = new KeyTracker();
    keys.press('shift');
    keys.press('enter');

    expect(keys.check('press', ['shift', 'enter'])).toBe(true);
    expect(keys.check('hold', ['shift', 'enter'])).toBe(true);
  });

  it('forgets what was held when the window loses the focus', () => {
    const keys = new KeyTracker();
    keys.press('a');
    keys.clear();

    expect(keys.check('hold', ['a'])).toBe(false);
  });
});
