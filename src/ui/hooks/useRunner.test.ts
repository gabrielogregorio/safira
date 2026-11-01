import { act, renderHook, waitFor } from '@testing-library/react';
import { FakeWorker } from '@/ui/fakeWorker';
import { soundPlayer } from '@/ui/sound/sounds';
import { createRunnerWorker, useRunner } from './useRunner';

const MAIN = 'main.safira';

const setup = () => {
  const workers: FakeWorker[] = [];
  const onFiles = vi.fn();
  const hook = renderHook(() =>
    useRunner(onFiles, () => {
      const worker = new FakeWorker();
      workers.push(worker);

      return worker;
    }),
  );

  const start = (source: string, mode: 'run' | 'step' = 'run'): void => {
    act(() => {
      hook.result.current.start({ file: MAIN, files: { [MAIN]: source }, locale: 'pt-br', mode, breakpoints: {} });
    });
  };

  return { ...hook, workers, onFiles, start };
};

describe('useRunner', () => {
  afterEach(() => {
    vi.restoreAllMocks();
    vi.unstubAllGlobals();
  });

  it('creates the real worker as a module', () => {
    const Worker = vi.fn(function WorkerStub(this: object) {
      return this;
    });
    vi.stubGlobal('Worker', Worker);
    const worker = createRunnerWorker();

    expect(worker).toBeInstanceOf(Worker);
    expect(Worker).toHaveBeenCalledExactlyOnceWith(expect.any(URL), { type: 'module' });
    expect(String(Worker.mock.calls[0]?.at(0))).toContain('runner.worker');
  });

  it('empties the terminal when the program asks for it', async () => {
    const { result, start } = setup();
    start('mostre 1\nlimpe a tela\nmostre 2');

    await waitFor(() => {
      expect(result.current.status).toBe('idle');
    });
    expect(result.current.terminal.lines.flat().map((item) => item.text)).toEqual(['2']);
  });

  it('plays the note of the program', async () => {
    const tone = vi.spyOn(soundPlayer, 'tone').mockReturnValue(undefined);
    const { result, start } = setup();
    start('toque C por 1s');

    await waitFor(() => {
      expect(tone).toHaveBeenCalledOnce();
    });
    await waitFor(() => {
      expect(result.current.status).toBe('idle');
    });
    expect(tone.mock.calls[0]?.[0]).toBeGreaterThan(0);
  });

  it('sends new breakpoints to the program that is running', async () => {
    const { result, workers, start } = setup();
    start('mostre 1\nmostre 2', 'step');
    await waitFor(() => {
      expect(result.current.status).toBe('paused');
    });

    act(() => {
      result.current.updateBreakpoints({ [MAIN]: [2] });
    });

    expect(workers[0]?.requests.at(-1)).toEqual({ type: 'breakpoints', breakpoints: { [MAIN]: [2] } });
  });

  it('goes back to idle and closes the worker at the end', async () => {
    const { result, workers, start } = setup();
    start('mostre 1');

    await waitFor(() => {
      expect(result.current.status).toBe('idle');
    });
    expect(workers[0]?.terminated).toBe(true);
    expect(result.current.terminal.lines).toHaveLength(1);
    expect(result.current.duration).not.toBeNull();
  });

  it('keeps the failure until it is dismissed', async () => {
    const { result, start } = setup();
    start('mostre nada');

    await waitFor(() => {
      expect(result.current.failure?.line).toBe(1);
    });

    act(() => {
      result.current.dismissFailure();
    });

    expect(result.current.failure).toBeNull();
  });

  it('shows the variables known when waiting for input', async () => {
    const { result, start } = setup();
    start('x = 1\nn = digitado');

    await waitFor(() => {
      expect(result.current.status).toBe('waiting-input');
    });
    expect(result.current.variables.map((variable) => variable.name)).toEqual(['x']);
  });

  it('echoes the typed text in the terminal', async () => {
    const { result, start } = setup();
    start('n = digitado');
    await waitFor(() => {
      expect(result.current.status).toBe('waiting-input');
    });

    act(() => {
      result.current.submitInput('Ana');
    });

    await waitFor(() => {
      expect(result.current.status).toBe('idle');
    });
    expect(result.current.terminal.lines[0]?.[0]?.text).toBe('Ana');
  });

  it('marks the run as stopped and closes the worker', async () => {
    const { result, workers, start } = setup();
    start('n = digitado');
    await waitFor(() => {
      expect(result.current.status).toBe('waiting-input');
    });

    act(() => {
      result.current.stop();
    });

    expect(result.current.wasStopped).toBe(true);
    expect(result.current.status).toBe('idle');
    expect(workers[0]?.terminated).toBe(true);
  });

  it('reports the pause position and clears it when resuming', async () => {
    const { result, start } = setup();
    start('mostre 1', 'step');
    await waitFor(() => {
      expect(result.current.pausedAt).toEqual({ file: MAIN, line: 1 });
    });

    act(() => {
      result.current.resume('run');
    });

    await waitFor(() => {
      expect(result.current.status).toBe('idle');
    });
    expect(result.current.pausedAt).toBeNull();
  });

  it('forwards the files changed by the program', async () => {
    const { onFiles, start } = setup();
    start('crie o arquivo "a.txt"');

    await waitFor(() => {
      expect(onFiles).toHaveBeenCalledWith(expect.objectContaining({ 'a.txt': '' }));
    });
  });

  it('closes the worker when the screen goes away', () => {
    const { workers, start, unmount } = setup();
    start('n = digitado');
    unmount();

    expect(workers[0]?.terminated).toBe(true);
  });
});
