import { EditorSelection, Facet, Prec, StateEffect, StateField } from '@codemirror/state';
import type { Extension, Transaction } from '@codemirror/state';
import type { DecorationSet } from '@codemirror/view';
import { Decoration, EditorView, keymap, WidgetType } from '@codemirror/view';
import { suggestCompletion } from '@/language/completion';
import type { Locale } from '@/language/messages';

interface Ghost {
  text: string;
  at: number;
}

const dismissGhost = StateEffect.define();
const ghostLocale = Facet.define<Locale, Locale>({ combine: (locales) => locales[0] ?? 'en-us' });
const ghostScripts = Facet.define<string[], string[]>({ combine: (lists) => lists[0] ?? [] });

const acceptGhost = (view: EditorView): boolean => {
  const ghost = view.state.field(ghostField);

  if (ghost === null) {
    return false;
  }

  view.dispatch({
    changes: { from: ghost.at, insert: ghost.text },
    selection: EditorSelection.cursor(ghost.at + ghost.text.length),
    userEvent: 'input.complete',
  });

  return true;
};

class GhostWidget extends WidgetType {
  constructor(private readonly text: string) {
    super();
  }

  override eq(other: GhostWidget): boolean {
    return other.text === this.text;
  }

  toDOM(view: EditorView): HTMLElement {
    const element = document.createElement('span');
    element.className = 'cm-ghost-text';
    element.textContent = this.text;
    element.setAttribute('aria-hidden', 'true');
    element.addEventListener('mousedown', (event) => {
      event.preventDefault();
      acceptGhost(view);
    });

    return element;
  }

  override ignoreEvent(): boolean {
    return false;
  }
}

const ghostAfterTyping = (transaction: Transaction): Ghost | null => {
  const { doc, selection } = transaction.state;
  const { main } = selection;

  if (!transaction.isUserEvent('input.type') || !main.empty) {
    return null;
  }

  const line = doc.lineAt(main.head);
  const before = line.text.slice(0, main.head - line.from);
  const after = line.text.slice(main.head - line.from);
  const text = suggestCompletion(
    before,
    after,
    doc.toString(),
    transaction.state.facet(ghostLocale),
    transaction.state.facet(ghostScripts),
  );

  return text === null ? null : { text, at: main.head };
};

const ghostField = StateField.define<Ghost | null>({
  create: () => null,
  update: (ghost, transaction) => {
    if (transaction.effects.some((effect) => effect.is(dismissGhost))) {
      return null;
    }

    return transaction.docChanged || transaction.selection !== undefined ? ghostAfterTyping(transaction) : ghost;
  },
  provide: (field) =>
    EditorView.decorations.from(field, (ghost): DecorationSet =>
      ghost === null
        ? Decoration.none
        : Decoration.set([Decoration.widget({ widget: new GhostWidget(ghost.text), side: 1 }).range(ghost.at)]),
    ),
});

const ghostKeys = Prec.highest(
  keymap.of([
    { key: 'Tab', run: acceptGhost },
    {
      key: 'Escape',
      run: (view) => {
        if (view.state.field(ghostField) === null) {
          return false;
        }

        view.dispatch({ effects: dismissGhost.of(null) });

        return true;
      },
    },
  ]),
);

// The suggestion is only painted over the text: it enters the document when it is accepted.
export const ghostText = (locale: Locale, scriptPaths: string[]): Extension => [
  ghostLocale.of(locale),
  ghostScripts.of(scriptPaths),
  ghostField,
  ghostKeys,
];
