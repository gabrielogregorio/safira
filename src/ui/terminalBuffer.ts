import type { OutputItem } from '@/runtime/protocol';

export interface TerminalSegment {
  text: string;
  color: string;
}

export interface TerminalBuffer {
  lines: TerminalSegment[][];
  isLastLineOpen: boolean;
}

export const MAXIMUM_TERMINAL_LINES = 5000;

export const EMPTY_TERMINAL: TerminalBuffer = { lines: [], isLastLineOpen: false };

export const appendOutput = (buffer: TerminalBuffer, items: OutputItem[]): TerminalBuffer => {
  const lines = [...buffer.lines];
  let isLastLineOpen = buffer.isLastLineOpen;

  for (const { inline, text, color } of items) {
    const segment = { text, color };

    if (isLastLineOpen) {
      lines[lines.length - 1] = [...lines[lines.length - 1], segment];
    } else {
      lines.push([segment]);
    }

    isLastLineOpen = inline;
  }

  return { lines: lines.slice(-MAXIMUM_TERMINAL_LINES), isLastLineOpen };
};
