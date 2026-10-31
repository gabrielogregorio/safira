import { driveExecution } from './driver';
import type { Effect, Execution } from './interpreter';

function* script(effects: Effect[], replies: (string | undefined)[]): Execution<void> {
  for (const effect of effects) {
    replies.push(yield effect);
  }
}

const createHost = () => ({
  onStep: vi.fn(),
  onOutput: vi.fn(),
  onClear: vi.fn(),
  onInput: vi.fn(() => Promise.resolve('digitado')),
  onSleep: vi.fn(() => Promise.resolve()),
  onTone: vi.fn(),
  onFilesChanged: vi.fn(),
});

describe('driveExecution', () => {
  it('sends each effect to the host', async () => {
    const host = createHost();
    await driveExecution(
      script(
        [
          { type: 'step', file: 'a', line: 1 },
          { type: 'output', inline: true, text: 'oi', color: '#fff' },
          { type: 'clear' },
          { type: 'sleep', milliseconds: 5 },
          { type: 'files' },
        ],
        [],
      ),
      host,
    );

    expect(host.onStep).toHaveBeenCalledWith('a', 1);
    expect(host.onOutput).toHaveBeenCalledWith(true, 'oi', '#fff');
    expect(host.onClear).toHaveBeenCalledTimes(1);
    expect(host.onSleep).toHaveBeenCalledWith(5);
    expect(host.onFilesChanged).toHaveBeenCalledTimes(1);
  });

  it('gives the typed text back to the program', async () => {
    const replies: (string | undefined)[] = [];
    await driveExecution(script([{ type: 'input' }, { type: 'clear' }], replies), createHost());

    expect(replies).toEqual(['digitado', undefined]);
  });

  it('waits for a pause on a step', async () => {
    let release = (): void => undefined;
    const host = {
      ...createHost(),
      onStep: () =>
        new Promise<void>((resolve) => {
          release = resolve;
        }),
    };
    const finished = driveExecution(script([{ type: 'step', file: 'a', line: 1 }, { type: 'clear' }], []), host);
    await Promise.resolve();

    expect(host.onClear).not.toHaveBeenCalled();

    release();
    await finished;

    expect(host.onClear).toHaveBeenCalledTimes(1);
  });
});
