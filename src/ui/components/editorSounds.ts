import type { Transaction } from '@codemirror/state';
import { EditorView } from '@codemirror/view';
import { soundPlayer } from '@/ui/sound/sounds';

const TYPING_RATES = [1, 0.94, 1.06, 0.97, 1.03];
const HOLD_MILLISECONDS = 180;
const HOLD_PER_LINE_MILLISECONDS = 70;
const LONGEST_HOLD_MILLISECONDS = 2500;
const RISE_PER_LINE = 0.012;
const LINES_THAT_RISE = 30;

let typingStep = 0;

const isTyping = (transaction: Transaction): boolean =>
  (transaction.isUserEvent('input') && !transaction.isUserEvent('input.paste')) ||
  transaction.isUserEvent('delete.backward') ||
  transaction.isUserEvent('delete.forward');

const selectedLines = (transaction: Transaction): number => {
  const { doc, selection } = transaction.state;
  const { anchor, head } = selection.main;

  return Math.abs(doc.lineAt(head).number - doc.lineAt(anchor).number) + 1;
};

// The longer the selection, the longer the sound lasts after the mouse stops, and it rises a little too.
export const holdForLines = (lines: number): { milliseconds: number; rate: number } => ({
  milliseconds: Math.min(HOLD_MILLISECONDS + lines * HOLD_PER_LINE_MILLISECONDS, LONGEST_HOLD_MILLISECONDS),
  rate: 1 + Math.min(lines, LINES_THAT_RISE) * RISE_PER_LINE,
});

const soundOf = (transaction: Transaction): void => {
  if (transaction.isUserEvent('input.complete')) {
    void soundPlayer.play('accept');
  } else if (isTyping(transaction)) {
    typingStep = (typingStep + 1) % TYPING_RATES.length;
    void soundPlayer.play('typing', TYPING_RATES[typingStep]);
  } else if (transaction.isUserEvent('select.pointer') && !transaction.state.selection.main.empty) {
    const { milliseconds, rate } = holdForLines(selectedLines(transaction));
    void soundPlayer.sustain('selection', milliseconds, rate);
  }
};

export const editorSounds = EditorView.updateListener.of((update) => {
  update.transactions.forEach(soundOf);
});
