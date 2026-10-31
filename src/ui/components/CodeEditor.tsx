import { defaultKeymap, history, historyKeymap, indentWithTab } from '@codemirror/commands';
import type { Range } from '@codemirror/state';
import { Compartment, EditorState, RangeSet, StateEffect, StateField } from '@codemirror/state';
import type { DecorationSet, ViewUpdate } from '@codemirror/view';
import { Decoration, EditorView, gutter, GutterMarker, keymap, lineNumbers, ViewPlugin } from '@codemirror/view';
import { useEffect, useRef } from 'react';
import { highlightCode } from '@/language/highlight';
import type { Locale } from '@/language/messages';
import type { CodeFont } from '@/settings/settings';
import { editorSounds } from './editorSounds';
import { ghostText } from './ghostText';

interface CodeEditorProps {
  value: string;
  label: string;
  fontSize: number;
  codeFont: CodeFont;
  suggestions: boolean;
  locale: Locale;
  scriptPaths: string[];
  breakpoints: number[];
  debugLine: number | null;
  errorLine: number | null;
  onChange: (value: string) => void;
  onToggleBreakpoint: (line: number) => void;
  onCursorChange: (line: number, column: number) => void;
}

interface LineMarks {
  debugLine: number | null;
  errorLine: number | null;
}

const setBreakpoints = StateEffect.define<number[]>();
const setLineMarks = StateEffect.define<LineMarks>();

class BreakpointDot extends GutterMarker {
  public constructor(private readonly isActive: boolean) {
    super();
  }

  public override toDOM(): HTMLElement {
    const dot = document.createElement('span');
    dot.className = this.isActive ? 'breakpoint-dot breakpoint-dot-active' : 'breakpoint-dot';

    return dot;
  }
}

const breakpointMarker = new BreakpointDot(true);
const emptyBreakpointMarker = new BreakpointDot(false);

const hasBreakpointAt = (state: EditorState, position: number): boolean => {
  let isFound = false;
  state.field(breakpointField).between(position, position, () => {
    isFound = true;

    return false;
  });

  return isFound;
};

const lineFromDocument = (state: EditorState, line: number): number | null =>
  line >= 1 && line <= state.doc.lines ? state.doc.line(line).from : null;

const breakpointField = StateField.define<RangeSet<GutterMarker>>({
  create: () => RangeSet.empty,
  update(markers, transaction) {
    let result = markers.map(transaction.changes);

    for (const effect of transaction.effects) {
      if (effect.is(setBreakpoints)) {
        const positions = effect.value
          .map((line) => lineFromDocument(transaction.state, line))
          .filter((position) => position !== null);
        result = RangeSet.of(
          positions.map((position) => breakpointMarker.range(position)),
          true,
        );
      }
    }

    return result;
  },
});

const debugDecoration = Decoration.line({ class: 'editor-line-debug' });
const errorDecoration = Decoration.line({ class: 'editor-line-error' });

const lineMarkField = StateField.define<DecorationSet>({
  create: () => Decoration.none,
  update(decorations, transaction) {
    let result = decorations.map(transaction.changes);

    for (const effect of transaction.effects) {
      if (effect.is(setLineMarks)) {
        const ranges: Range<Decoration>[] = [];
        const debugPosition = lineFromDocument(transaction.state, effect.value.debugLine ?? 0);
        const errorPosition = lineFromDocument(transaction.state, effect.value.errorLine ?? 0);

        if (debugPosition !== null) {
          ranges.push(debugDecoration.range(debugPosition));
        }

        if (errorPosition !== null) {
          ranges.push(errorDecoration.range(errorPosition));
        }

        result = Decoration.set(ranges, true);
      }
    }

    return result;
  },
  provide: (field) => EditorView.decorations.from(field),
});

const buildHighlight = (view: EditorView): DecorationSet =>
  Decoration.set(
    highlightCode(view.state.doc.toString()).map(({ start, end, category }) =>
      Decoration.mark({ class: `syntax-${category}` }).range(start, end),
    ),
    true,
  );

const syntaxHighlight = ViewPlugin.fromClass(
  class {
    public decorations: DecorationSet;

    public constructor(view: EditorView) {
      this.decorations = buildHighlight(view);
    }

    public update(update: ViewUpdate): void {
      if (update.docChanged) {
        this.decorations = buildHighlight(update.view);
      }
    }
  },
  { decorations: (plugin) => plugin.decorations },
);

const isTouchScreen = (): boolean =>
  typeof window.matchMedia === 'function' && window.matchMedia('(pointer: coarse)').matches;

export const CodeEditor = ({
  value,
  label,
  fontSize,
  codeFont,
  suggestions,
  locale,
  scriptPaths,
  breakpoints,
  debugLine,
  errorLine,
  onChange,
  onToggleBreakpoint,
  onCursorChange,
}: CodeEditorProps) => {
  const hostRef = useRef<HTMLDivElement>(null);
  const viewRef = useRef<EditorView | null>(null);
  const callbacks = useRef({ onChange, onToggleBreakpoint, onCursorChange });
  const fontCompartment = useRef(new Compartment());
  const ghostCompartment = useRef(new Compartment());

  useEffect(() => {
    callbacks.current = { onChange, onToggleBreakpoint, onCursorChange };
  }, [onChange, onToggleBreakpoint, onCursorChange]);

  useEffect(() => {
    const host = hostRef.current;

    if (host === null) {
      return undefined;
    }

    const view = new EditorView({
      parent: host,
      state: EditorState.create({
        doc: value,
        extensions: [
          ghostCompartment.current.of(suggestions ? ghostText(locale, scriptPaths) : []),
          history(),
          keymap.of([indentWithTab, ...defaultKeymap, ...historyKeymap]),
          breakpointField,
          lineMarkField,
          gutter({
            class: 'editor-breakpoints',
            lineMarker: (editorView, line) =>
              hasBreakpointAt(editorView.state, line.from) ? breakpointMarker : emptyBreakpointMarker,
            lineMarkerChange: (update) =>
              update.transactions.some((transaction) =>
                transaction.effects.some((effect) => effect.is(setBreakpoints)),
              ),
            initialSpacer: () => emptyBreakpointMarker,
            domEventHandlers: {
              mousedown: (editorView, block) => {
                callbacks.current.onToggleBreakpoint(editorView.state.doc.lineAt(block.from).number);

                return true;
              },
            },
          }),
          lineNumbers(),
          syntaxHighlight,
          EditorView.lineWrapping,
          editorSounds,
          EditorView.contentAttributes.of({ 'aria-label': label }),
          fontCompartment.current.of(EditorView.theme({ '&': { fontSize: `${fontSize}px` } })),
          EditorView.updateListener.of((update) => {
            if (update.docChanged) {
              callbacks.current.onChange(update.state.doc.toString());
            }

            if (update.selectionSet || update.docChanged) {
              const head = update.state.selection.main.head;
              const line = update.state.doc.lineAt(head);
              callbacks.current.onCursorChange(line.number, head - line.from + 1);
            }
          }),
        ],
      }),
    });
    viewRef.current = view;

    if (!isTouchScreen()) {
      view.focus();
    }

    return () => {
      view.destroy();
      viewRef.current = null;
    };
    // The view is created once; the effects below keep it in sync with the props.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  useEffect(() => {
    const view = viewRef.current;

    if (view !== null && view.state.doc.toString() !== value) {
      view.dispatch({ changes: { from: 0, to: view.state.doc.length, insert: value } });
    }
  }, [value]);

  useEffect(() => {
    viewRef.current?.dispatch({ effects: setBreakpoints.of(breakpoints) });
  }, [breakpoints, value]);

  useEffect(() => {
    viewRef.current?.dispatch({ effects: setLineMarks.of({ debugLine, errorLine }) });
  }, [debugLine, errorLine]);

  useEffect(() => {
    viewRef.current?.dispatch({
      effects: fontCompartment.current.reconfigure(EditorView.theme({ '&': { fontSize: `${fontSize}px` } })),
    });
  }, [fontSize]);

  useEffect(() => {
    viewRef.current?.requestMeasure();
  }, [codeFont]);

  useEffect(() => {
    viewRef.current?.dispatch({
      effects: ghostCompartment.current.reconfigure(suggestions ? ghostText(locale, scriptPaths) : []),
    });
  }, [suggestions, locale, scriptPaths]);

  return <div ref={hostRef} className="code-editor" />;
};
