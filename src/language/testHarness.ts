import { driveExecution } from './driver';
import { Interpreter, SafiraError } from './interpreter';
import { VirtualFileSystem } from './virtualFileSystem';

export interface RecordedEvent {
  type: 'line' | 'inline' | 'clear';
  text?: string;
  color?: string;
}

export interface RunResult {
  events: RecordedEvent[];
  texts: string[];
  error: SafiraError | null;
  files: VirtualFileSystem;
  sleeps: number[];
  tones: { frequency: number; milliseconds: number }[];
}

const MAIN_FILE = 'main.safira';

export const runScript = async (source: string, inputs: string[] = [], extraFiles = {}): Promise<RunResult> => {
  const files = new VirtualFileSystem({ ...extraFiles, [MAIN_FILE]: source });
  const interpreter = new Interpreter({ files, locale: 'pt-br', random: (minimum) => minimum });
  const events: RecordedEvent[] = [];
  const sleeps: number[] = [];
  const tones: RunResult['tones'] = [];
  const queue = [...inputs];
  let error: SafiraError | null = null;

  try {
    await driveExecution(interpreter.run(MAIN_FILE), {
      onOutput: (inline, text, color) => events.push({ type: inline ? 'inline' : 'line', text, color }),
      onClear: () => events.push({ type: 'clear' }),
      onInput: () => Promise.resolve(queue.shift() ?? ''),
      onSleep: (milliseconds) => {
        sleeps.push(milliseconds);

        return Promise.resolve();
      },
      onTone: (frequency, milliseconds) => {
        tones.push({ frequency, milliseconds });

        return Promise.resolve();
      },
      onFilesChanged: () => undefined,
    });
  } catch (caught) {
    if (!(caught instanceof SafiraError)) {
      throw caught;
    }

    error = caught;
  }

  return { events, texts: events.map((event) => event.text ?? '<clear>'), error, files, sleeps, tones };
};
