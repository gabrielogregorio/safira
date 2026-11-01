import { EditorState } from '@codemirror/state';
import type { TransactionSpec } from '@codemirror/state';
import { EditorView } from '@codemirror/view';
import type { MockInstance } from 'vitest';
import { soundPlayer } from '@/ui/sound/sounds';
import { editorSounds, rateForLines, removesWholeLine } from './editorSounds';

const views: EditorView[] = [];

const openEditor = (doc: string): EditorView => {
  const view = new EditorView({
    parent: document.body,
    state: EditorState.create({ doc, extensions: editorSounds }),
  });
  views.push(view);

  return view;
};

describe('editorSounds', () => {
  let play: MockInstance<typeof soundPlayer.play>;
  let hold: MockInstance<typeof soundPlayer.hold>;

  beforeEach(() => {
    play = vi.spyOn(soundPlayer, 'play').mockResolvedValue(undefined);
    hold = vi.spyOn(soundPlayer, 'hold').mockResolvedValue(undefined);
  });

  afterEach(() => {
    views.splice(0).forEach((view) => {
      view.destroy();
    });
    vi.restoreAllMocks();
  });

  const dispatch = (doc: string, spec: TransactionSpec): void => {
    openEditor(doc).dispatch(spec);
  };

  it('plays the acceptance of a suggestion', () => {
    dispatch('mo', { changes: { from: 2, insert: 'stre' }, userEvent: 'input.complete' });

    expect(play).toHaveBeenCalledExactlyOnceWith('accept');
  });

  it('plays the deletion of a whole line', () => {
    dispatch('um\ndois', { changes: { from: 0, to: 3 }, userEvent: 'delete.line' });

    expect(play).toHaveBeenCalledExactlyOnceWith('lineDelete');
  });

  it('counts a line emptied by a selection as a whole line', () => {
    dispatch('um', { changes: { from: 0, to: 2 }, userEvent: 'delete.selection' });

    expect(play).toHaveBeenCalledExactlyOnceWith('lineDelete');
  });

  it('types with a rate that changes from one key to the next', () => {
    const view = openEditor('');
    view.dispatch({ changes: { from: 0, insert: 'a' }, userEvent: 'input.type' });
    view.dispatch({ changes: { from: 1, insert: 'b' }, userEvent: 'input.type' });

    const [first, second] = play.mock.calls;

    expect(first?.[0]).toBe('typing');
    expect(second?.[0]).toBe('typing');
    expect(first?.[1]).not.toBe(second?.[1]);
  });

  it.each(['delete.backward', 'delete.forward'])('treats %s of one character as typing', (userEvent) => {
    dispatch('abc', { changes: { from: 1, to: 2 }, userEvent });

    expect(play).toHaveBeenCalledExactlyOnceWith('typing', expect.any(Number));
  });

  it('stays silent when pasting', () => {
    dispatch('', { changes: { from: 0, insert: 'colado' }, userEvent: 'input.paste' });

    expect(play).not.toHaveBeenCalled();
  });

  it('holds a sound while selecting with the mouse, higher as the selection grows, until the button is released', () => {
    const release = vi.spyOn(soundPlayer, 'release').mockReturnValue(undefined);
    dispatch('a\nb\nc', { selection: { anchor: 5, head: 0 }, userEvent: 'select.pointer' });

    expect(hold).toHaveBeenCalledExactlyOnceWith('selection', rateForLines(3));
    expect(release).not.toHaveBeenCalled();

    document.dispatchEvent(new Event('pointerup'));
    window.dispatchEvent(new Event('blur'));

    expect(release).toHaveBeenCalledTimes(2);
  });

  it('holds nothing when the mouse only places the cursor', () => {
    dispatch('abc', { selection: { anchor: 1 }, userEvent: 'select.pointer' });

    expect(hold).not.toHaveBeenCalled();
  });

  it('stops rising after thirty lines', () => {
    expect(rateForLines(30)).toBeGreaterThan(rateForLines(1));
    expect(rateForLines(500)).toBe(rateForLines(30));
  });

  it('does not take a change that only adds text for a removed line', () => {
    const state = EditorState.create({ doc: 'a' });

    expect(removesWholeLine(state.update({ changes: { from: 0, to: 1, insert: 'b' }, userEvent: 'input.type' }))).toBe(
      false,
    );
  });
});
