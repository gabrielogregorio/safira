import type { Transaction } from '@codemirror/state';
import { EditorView } from '@codemirror/view';
import { soundPlayer } from '@/ui/sound/sounds';

const TYPING_RATES = [1, 0.94, 1.06, 0.97, 1.03];
const RISE_PER_LINE = 0.012;
const LINES_THAT_RISE = 30;

let typingStep = 0;

const isTyping = (transaction: Transaction): boolean =>
  (transaction.isUserEvent('input') && !transaction.isUserEvent('input.paste')) ||
  transaction.isUserEvent('delete.backward') ||
  transaction.isUserEvent('delete.forward');

// A whole line at once, by shortcut, by cutting or with a selection. One character at a time is just typing.
export const removesWholeLine = (transaction: Transaction): boolean => {
  let removesLine = false;

  transaction.changes.iterChanges((fromA, toA) => {
    const removed = transaction.startState.sliceDoc(fromA, toA);
    const line = transaction.startState.doc.lineAt(fromA);
    const isWholeLine = fromA === line.from && toA === line.to;

    removesLine ||= removed.trim() !== '' && (removed.includes('\n') || isWholeLine);
  });

  return transaction.isUserEvent('delete') && removesLine;
};

const selectedLines = (transaction: Transaction): number => {
  const { doc, selection } = transaction.state;
  const { anchor, head } = selection.main;

  return Math.abs(doc.lineAt(head).number - doc.lineAt(anchor).number) + 1;
};

// The sound goes on while the mouse is pressed, and rises a little as the selection grows.
export const rateForLines = (lines: number): number => 1 + Math.min(lines, LINES_THAT_RISE) * RISE_PER_LINE;

const soundOf = (transaction: Transaction): void => {
  if (transaction.isUserEvent('input.complete')) {
    void soundPlayer.play('accept');
  } else if (removesWholeLine(transaction)) {
    void soundPlayer.play('lineDelete');
  } else if (isTyping(transaction)) {
    typingStep = (typingStep + 1) % TYPING_RATES.length;
    void soundPlayer.play('typing', TYPING_RATES[typingStep]);
  } else if (transaction.isUserEvent('select.pointer') && !transaction.state.selection.main.empty) {
    document.addEventListener('pointerup', soundPlayer.release, { once: true });
    window.addEventListener('blur', soundPlayer.release, { once: true });
    void soundPlayer.hold('selection', rateForLines(selectedLines(transaction)));
  }
};

export const editorSounds = EditorView.updateListener.of((update) => {
  update.transactions.forEach(soundOf);
});
