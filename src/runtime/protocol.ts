import type { VariableSnapshot } from '@/language/interpreter';
import type { Locale } from '@/language/messages';

export type RunMode = 'run' | 'debug' | 'step';

export type Breakpoints = Record<string, number[]>;

export interface StartRequest {
  type: 'start';
  file: string;
  files: Record<string, string>;
  locale: Locale;
  mode: RunMode;
  breakpoints: Breakpoints;
}

export type RunnerRequest =
  | StartRequest
  | { type: 'input'; text: string }
  | { type: 'resume'; mode: RunMode }
  | { type: 'breakpoints'; breakpoints: Breakpoints };

export interface OutputItem {
  inline: boolean;
  text: string;
  color: string;
}

export interface RunnerFailure {
  message: string;
  file: string;
  line: number;
  example: string | null;
}

export type RunnerEvent =
  | { type: 'output'; items: OutputItem[] }
  | { type: 'clear' }
  | { type: 'input-request' }
  | { type: 'paused'; file: string; line: number; variables: VariableSnapshot[] }
  | { type: 'files'; files: Record<string, string> }
  | { type: 'finished'; failure: RunnerFailure | null; files: Record<string, string>; variables: VariableSnapshot[] };
