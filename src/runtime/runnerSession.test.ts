import { Interpreter } from '@/language/interpreter';
import { noteFrequency } from '@/language/notes';
import type { RunnerEvent, RunnerRequest } from './protocol';
import { RunnerSession } from './runnerSession';

const MAIN = 'main.safira';

const createSession = (): { session: RunnerSession; events: RunnerEvent[]; sleeps: number[] } => {
  const events: RunnerEvent[] = [];
  const sleeps: number[] = [];
  const session = new RunnerSession((event) => events.push(event), {
    now: () => 0,
    sleep: (milliseconds) => {
      sleeps.push(milliseconds);

      return Promise.resolve();
    },
  });

  return { session, events, sleeps };
};

const startRequest = (source: string, overrides: Partial<RunnerRequest & { type: 'start' }> = {}): RunnerRequest => ({
  type: 'start',
  file: MAIN,
  files: { [MAIN]: source },
  locale: 'pt-br',
  mode: 'run',
  breakpoints: {},
  ...overrides,
});

const outputTexts = (events: RunnerEvent[]): string[] =>
  events.flatMap((event) => (event.type === 'output' ? event.items.map((item) => item.text) : []));

const flushMicrotasks = (): Promise<void> =>
  new Promise((resolve) => {
    setTimeout(resolve, 0);
  });

describe('RunnerSession', () => {
  describe('keys', () => {
    // A real turn of the event loop, or a program that waits for a key would never let the test send one.
    const createLiveSession = (): { session: RunnerSession; events: RunnerEvent[] } => {
      const events: RunnerEvent[] = [];
      const session = new RunnerSession((event) => events.push(event), {
        now: () => 0,
        sleep: () => flushMicrotasks(),
      });

      return { session, events };
    };

    const LOOP = 'enquanto verdadeiro {\n  se apertar Enter entao interrompa\n}\nmostre "nunca"';

    it('announces that the program listens once, and hears a key sent while it runs', async () => {
      const { events, session } = createLiveSession();
      const running = session.handle(startRequest(LOOP));
      await flushMicrotasks();
      await session.handle({ type: 'key', key: 'enter', isDown: true });
      await running;

      expect(events.filter((event) => event.type === 'keys-listening')).toHaveLength(1);
      expect(events.at(-1)).toMatchObject({ type: 'finished', failure: null });
      expect(outputTexts(events)).toEqual([]);
    });

    it('gives the messages a turn on each check', async () => {
      const { sleeps, session } = createSession();
      await session.handle(startRequest('se apertar Enter entao mostre "x"'));

      expect(sleeps).toEqual([0]);
    });

    it('hears a key going up and forgets the keys on request', async () => {
      const { events, session } = createLiveSession();
      const running = session.handle(
        startRequest('enquanto verdadeiro {\n  se soltar A entao interrompa\n  se segurar B entao mostre "b"\n}'),
      );
      await flushMicrotasks();
      await session.handle({ type: 'key', key: 'b', isDown: true });
      await session.handle({ type: 'keys-clear' });
      await session.handle({ type: 'key', key: 'a', isDown: true });
      await session.handle({ type: 'key', key: 'a', isDown: false });
      await running;

      expect(events.at(-1)).toMatchObject({ type: 'finished', failure: null });
    });
  });

  it('sends the output and finishes without failure', async () => {
    const { session, events } = createSession();
    await session.handle(startRequest('mostre "a"\nmostre "b"'));

    expect(outputTexts(events)).toEqual(['a', 'b']);
    expect(events.at(-1)).toMatchObject({ type: 'finished', failure: null });
  });

  it('reports a failure with its line and example', async () => {
    const { session, events } = createSession();
    await session.handle(startRequest('\nmostre nada'));

    expect(events.at(-1)).toMatchObject({
      type: 'finished',
      failure: { line: 2, file: MAIN, example: '02' },
    });
  });

  it('asks for input and continues with what was typed', async () => {
    const { session, events } = createSession();
    const finished = session.handle(startRequest('x = 1\nn = o que o usuario digitar\nmostre n'));
    await flushMicrotasks();

    expect(events.at(-1)).toEqual({
      type: 'input-request',
      variables: [{ name: 'x', value: '1', type: 'float' }],
    });

    await session.handle({ type: 'input', text: 'Ana' });
    await finished;

    expect(outputTexts(events)).toEqual(['Ana']);
  });

  it('pauses on a breakpoint with the variables and resumes', async () => {
    const { session, events } = createSession();
    const finished = session.handle(
      startRequest('x = 1\nmostre x\nmostre 2', { mode: 'debug', breakpoints: { [MAIN]: [2] } }),
    );
    await flushMicrotasks();

    expect(events.at(-1)).toEqual({
      type: 'paused',
      file: MAIN,
      line: 2,
      variables: [{ name: 'x', value: '1', type: 'float' }],
    });

    await session.handle({ type: 'resume', mode: 'debug' });
    await finished;

    expect(outputTexts(events)).toEqual(['1', '2']);
  });

  it('pauses on the next command when the breakpoint is on a comment', async () => {
    const { session, events } = createSession();
    const finished = session.handle(startRequest('# nota\nmostre 1', { mode: 'debug', breakpoints: { [MAIN]: [1] } }));
    await flushMicrotasks();

    expect(events.at(-1)).toMatchObject({ type: 'paused', line: 2 });

    await session.handle({ type: 'resume', mode: 'run' });
    await finished;
  });

  it('pauses on every line in step mode', async () => {
    const { session, events } = createSession();
    const finished = session.handle(startRequest('mostre 1\nmostre 2', { mode: 'step' }));
    await flushMicrotasks();
    await session.handle({ type: 'resume', mode: 'step' });
    await flushMicrotasks();
    await session.handle({ type: 'resume', mode: 'run' });
    await finished;

    expect(events.filter((event) => event.type === 'paused')).toHaveLength(2);
  });

  it('ignores breakpoints in a normal run', async () => {
    const { session, events } = createSession();
    await session.handle(startRequest('mostre 1', { breakpoints: { [MAIN]: [1] } }));

    expect(events.some((event) => event.type === 'paused')).toBe(false);
  });

  it('uses breakpoints changed during the run', async () => {
    const { session, events } = createSession();
    const finished = session.handle(startRequest('mostre 1\nmostre 2', { mode: 'step' }));
    await flushMicrotasks();
    await session.handle({ type: 'breakpoints', breakpoints: { [MAIN]: [2] } });
    await session.handle({ type: 'resume', mode: 'debug' });
    await flushMicrotasks();

    expect(events.at(-1)).toMatchObject({ type: 'paused', line: 2 });

    await session.handle({ type: 'resume', mode: 'run' });
    await finished;
  });

  it('sends the virtual files changed by the program', async () => {
    const { session, events } = createSession();
    await session.handle(startRequest('crie o arquivo "a.txt"'));

    expect(events).toContainEqual({ type: 'files', files: { [MAIN]: 'crie o arquivo "a.txt"', 'a.txt': '' } });
    expect(events.at(-1)).toMatchObject({ files: { 'a.txt': '' } });
  });

  it('forwards a clear and flushes the text before it', async () => {
    const { session, events } = createSession();
    await session.handle(startRequest('mostre 1\nlimpatela'));

    expect(events.map((event) => event.type)).toEqual(['output', 'clear', 'finished']);
  });

  it('waits the requested time', async () => {
    const { session, sleeps } = createSession();
    await session.handle(startRequest('espere 2 segundos'));

    expect(sleeps).toEqual([2000]);
  });

  it('plays a note and waits for it', async () => {
    const { session, events, sleeps } = createSession();
    await session.handle(startRequest('toque C por 2 segundos'));

    expect(events).toContainEqual({ type: 'tone', frequency: noteFrequency('C'), milliseconds: 2000 });
    expect(sleeps).toEqual([2000]);
  });

  it('does not pause in debug on a file without breakpoints', async () => {
    const { session, events } = createSession();
    await session.handle(startRequest('mostre 1', { mode: 'debug', breakpoints: { 'outro.safira': [1] } }));

    expect(events.some((event) => event.type === 'paused')).toBe(false);
    expect(events.at(-1)).toMatchObject({ type: 'finished', failure: null });
  });

  it('finishes with a message when the blocks are too deep to read', async () => {
    const { session, events } = createSession();
    vi.spyOn(Interpreter.prototype, 'run').mockImplementationOnce(() => {
      throw new RangeError('Maximum call stack size exceeded');
    });
    await session.handle(startRequest('mostre 1'));

    expect(events.at(-1)).toMatchObject({
      type: 'finished',
      failure: { message: 'Este programa tem blocos demais, um dentro do outro', file: MAIN, line: 1 },
    });
  });

  it('does not hide an error that is not from the script', async () => {
    const { session, events } = createSession();
    vi.spyOn(Interpreter.prototype, 'run').mockImplementationOnce(() => {
      throw new TypeError('quebrou');
    });

    await expect(session.handle(startRequest('mostre 1'))).rejects.toThrow(TypeError);
    expect(events.some((event) => event.type === 'finished')).toBe(false);
  });

  it('splits a long output in batches', async () => {
    const { session, events } = createSession();
    await session.handle(startRequest('repita 450 vezes { mostre 1 }'));

    expect(events.filter((event) => event.type === 'output').length).toBeGreaterThanOrEqual(3);
    expect(outputTexts(events)).toHaveLength(450);
  });
});
