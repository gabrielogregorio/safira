import type { Execution } from './interpreter';

export interface ExecutionHost {
  onStep?: (file: string, line: number) => void | Promise<void>;
  onOutput: (inline: boolean, text: string, color: string) => void;
  onClear: () => void;
  onInput: () => Promise<string>;
  onSleep: (milliseconds: number) => Promise<void>;
  onTone: (frequency: number, milliseconds: number) => Promise<void>;
  onFilesChanged: () => void;
}

export const driveExecution = async (execution: Execution<void>, host: ExecutionHost): Promise<void> => {
  let reply: string | undefined;

  for (;;) {
    const next = execution.next(reply);
    reply = undefined;

    if (next.done === true) {
      return;
    }

    const effect = next.value;

    switch (effect.type) {
      case 'step': {
        const pause = host.onStep?.(effect.file, effect.line);

        if (pause !== undefined) {
          await pause;
        }

        break;
      }
      case 'output':
        host.onOutput(effect.inline, effect.text, effect.color);
        break;
      case 'clear':
        host.onClear();
        break;
      case 'input':
        reply = await host.onInput();
        break;
      case 'sleep':
        await host.onSleep(effect.milliseconds);
        break;
      case 'tone':
        await host.onTone(effect.frequency, effect.milliseconds);
        break;
      case 'files':
        host.onFilesChanged();
        break;
    }
  }
};
