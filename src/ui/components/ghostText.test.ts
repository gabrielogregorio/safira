import { EditorState } from '@codemirror/state';
import { EditorView } from '@codemirror/view';
import { fireEvent } from '@testing-library/react';
import { suggestCompletion } from '@/language/completion';
import { ghostText } from './ghostText';

vi.mock('@/language/completion', () => ({ suggestCompletion: vi.fn() }));

const openEditor = (doc = ''): EditorView => {
  const view = new EditorView({
    parent: document.body,
    state: EditorState.create({ doc, extensions: ghostText('pt-br', { 'a.safira': 'x' }) }),
  });
  views.push(view);

  return view;
};

const views: EditorView[] = [];

const type = (view: EditorView, text: string): void => {
  const at = view.state.selection.main.head;
  view.dispatch({
    changes: { from: at, insert: text },
    selection: { anchor: at + text.length },
    userEvent: 'input.type',
  });
};

const ghost = (): HTMLElement | null => document.querySelector<HTMLElement>('.cm-ghost-text');

const press = (view: EditorView, key: string): boolean =>
  !view.contentDOM.dispatchEvent(new KeyboardEvent('keydown', { key, bubbles: true, cancelable: true }));

describe('ghostText', () => {
  beforeEach(() => {
    vi.mocked(suggestCompletion).mockReturnValue('stre');
  });

  afterEach(() => {
    views.splice(0).forEach((view) => {
      view.destroy();
    });
    vi.clearAllMocks();
  });

  it('paints the suggestion after the text, hidden from screen readers and out of the document', () => {
    const view = openEditor();
    type(view, 'mo');

    expect(ghost()).toHaveTextContent('stre');
    expect(ghost()).toHaveAttribute('aria-hidden', 'true');
    expect(view.state.doc.toString()).toBe('mo');
  });

  it('asks for a suggestion with the text around the cursor, the language and the scripts', () => {
    const view = openEditor('fim');
    view.dispatch({ selection: { anchor: 0 } });
    type(view, 'mo');

    expect(suggestCompletion).toHaveBeenCalledExactlyOnceWith('mo', 'fim', 'mofim', 'pt-br', { 'a.safira': 'x' });
  });

  it('shows nothing when there is no suggestion', () => {
    vi.mocked(suggestCompletion).mockReturnValue(null);
    type(openEditor(), 'mo');

    expect(ghost()).toBeNull();
  });

  it('only suggests while typing, not when the text arrives from elsewhere', () => {
    const view = openEditor();
    view.dispatch({ changes: { from: 0, insert: 'mo' }, selection: { anchor: 2 }, userEvent: 'input.paste' });

    expect(suggestCompletion).not.toHaveBeenCalled();
    expect(ghost()).toBeNull();
  });

  it('does not suggest over a selection', () => {
    const view = openEditor();
    view.dispatch({ changes: { from: 0, insert: 'mo' }, selection: { anchor: 0, head: 2 }, userEvent: 'input.type' });

    expect(suggestCompletion).not.toHaveBeenCalled();
  });

  it('drops the suggestion when the cursor moves away', () => {
    const view = openEditor();
    type(view, 'mo');
    view.dispatch({ selection: { anchor: 0 } });

    expect(ghost()).toBeNull();
  });

  it('keeps it through a change that touches neither the text nor the cursor', () => {
    const view = openEditor();
    type(view, 'mo');
    view.dispatch({ scrollIntoView: true });

    expect(ghost()).toHaveTextContent('stre');
  });

  it('reuses the element when the same suggestion comes back at the same place', () => {
    const view = openEditor();
    type(view, 'mo');
    const element = ghost();
    view.dispatch({ selection: { anchor: 2 }, userEvent: 'input.type' });

    expect(ghost()).toBe(element);
  });

  it('draws a new element when the suggestion changes', () => {
    const view = openEditor();
    type(view, 'mo');
    const element = ghost();
    vi.mocked(suggestCompletion).mockReturnValue('ldura');
    view.dispatch({ selection: { anchor: 2 }, userEvent: 'input.type' });

    expect(ghost()).not.toBe(element);
    expect(ghost()).toHaveTextContent('ldura');
  });

  it('accepts with Tab, as if it had been typed', () => {
    const view = openEditor();
    type(view, 'mo');

    expect(press(view, 'Tab')).toBe(true);
    expect(view.state.doc.toString()).toBe('mostre');
    expect(view.state.selection.main.head).toBe(6);
    expect(ghost()).toBeNull();
  });

  it('leaves Tab alone when there is nothing to accept', () => {
    const view = openEditor();

    expect(press(view, 'Tab')).toBe(false);
    expect(view.state.doc.toString()).toBe('');
  });

  it('dismisses with Escape and keeps the text', () => {
    const view = openEditor();
    type(view, 'mo');

    expect(press(view, 'Escape')).toBe(true);
    expect(ghost()).toBeNull();
    expect(view.state.doc.toString()).toBe('mo');
  });

  it('leaves Escape alone when there is nothing to dismiss', () => {
    expect(press(openEditor(), 'Escape')).toBe(false);
  });

  it('lets the editor handle a key that lands on the suggestion', () => {
    const view = openEditor();
    type(view, 'mo');
    fireEvent.keyDown(ghost() as HTMLElement, { key: 'Tab' });

    expect(view.state.doc.toString()).toBe('mostre');
  });

  it('accepts when clicked', () => {
    const view = openEditor();
    type(view, 'mo');
    const notPrevented = fireEvent.mouseDown(ghost() as HTMLElement);

    expect(notPrevented).toBe(false);
    expect(view.state.doc.toString()).toBe('mostre');
  });
});
