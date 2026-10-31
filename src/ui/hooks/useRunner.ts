import { useCallback, useEffect, useRef, useState } from 'react';
import type { VariableSnapshot } from '@/language/interpreter';
import type { Breakpoints, RunMode, RunnerEvent, RunnerFailure, RunnerRequest, StartRequest } from '@/runtime/protocol';
import type { TerminalBuffer } from '@/ui/terminalBuffer';
import { appendOutput, EMPTY_TERMINAL } from '@/ui/terminalBuffer';
import { soundPlayer } from '@/ui/sound/sounds';

export type RunnerStatus = 'idle' | 'running' | 'paused' | 'waiting-input';

export interface RunnerWorker {
  postMessage: (request: RunnerRequest) => void;
  terminate: () => void;
  onmessage: ((message: MessageEvent<RunnerEvent>) => void) | null;
}

export type WorkerFactory = () => RunnerWorker;

export const createRunnerWorker: WorkerFactory = () =>
  new Worker(new URL('../../runtime/runner.worker.ts', import.meta.url), { type: 'module' });

export interface Runner {
  status: RunnerStatus;
  terminal: TerminalBuffer;
  variables: VariableSnapshot[];
  pausedAt: { file: string; line: number } | null;
  failure: RunnerFailure | null;
  duration: number | null;
  wasStopped: boolean;
  start: (request: Omit<StartRequest, 'type'>) => void;
  stop: () => void;
  resume: (mode: RunMode) => void;
  submitInput: (text: string) => void;
  updateBreakpoints: (breakpoints: Breakpoints) => void;
  dismissFailure: () => void;
}

const MILLISECONDS_PER_SECOND = 1000;

export const useRunner = (
  onFilesChanged: (files: Record<string, string>) => void,
  createWorker: WorkerFactory = createRunnerWorker,
  onFinished?: (failure: RunnerFailure | null) => void,
): Runner => {
  const workerRef = useRef<RunnerWorker | null>(null);
  const startedAt = useRef(0);
  const [status, setStatus] = useState<RunnerStatus>('idle');
  const [terminal, setTerminal] = useState<TerminalBuffer>(EMPTY_TERMINAL);
  const [variables, setVariables] = useState<VariableSnapshot[]>([]);
  const [pausedAt, setPausedAt] = useState<{ file: string; line: number } | null>(null);
  const [failure, setFailure] = useState<RunnerFailure | null>(null);
  const [duration, setDuration] = useState<number | null>(null);
  const [wasStopped, setWasStopped] = useState(false);

  const closeWorker = useCallback(() => {
    workerRef.current?.terminate();
    workerRef.current = null;
  }, []);

  useEffect(() => closeWorker, [closeWorker]);

  const handleEvent = useCallback(
    (event: RunnerEvent) => {
      switch (event.type) {
        case 'output':
          setTerminal((buffer) => appendOutput(buffer, event.items));
          break;
        case 'clear':
          setTerminal(EMPTY_TERMINAL);
          break;
        case 'tone':
          soundPlayer.tone(event.frequency, event.milliseconds);
          break;
        case 'input-request':
          setStatus('waiting-input');
          setVariables(event.variables);
          break;
        case 'paused':
          setStatus('paused');
          setPausedAt({ file: event.file, line: event.line });
          setVariables(event.variables);
          break;
        case 'files':
          onFilesChanged(event.files);
          break;
        case 'finished':
          closeWorker();
          onFilesChanged(event.files);
          setVariables(event.variables);
          setFailure(event.failure);
          setPausedAt(null);
          setDuration((performance.now() - startedAt.current) / MILLISECONDS_PER_SECOND);
          setStatus('idle');
          onFinished?.(event.failure);
          break;
      }
    },
    [closeWorker, onFilesChanged, onFinished],
  );

  const start = useCallback<Runner['start']>(
    (request) => {
      closeWorker();
      const worker = createWorker();
      worker.onmessage = (message) => {
        handleEvent(message.data);
      };
      workerRef.current = worker;
      startedAt.current = performance.now();
      setTerminal(EMPTY_TERMINAL);
      setVariables([]);
      setFailure(null);
      setDuration(null);
      setWasStopped(false);
      setPausedAt(null);
      setStatus('running');
      worker.postMessage({ type: 'start', ...request });
    },
    [closeWorker, createWorker, handleEvent],
  );

  const stop = useCallback(() => {
    closeWorker();
    setPausedAt(null);
    setWasStopped(true);
    setStatus('idle');
  }, [closeWorker]);

  const resume = useCallback((mode: RunMode) => {
    setPausedAt(null);
    setStatus('running');
    workerRef.current?.postMessage({ type: 'resume', mode });
  }, []);

  const submitInput = useCallback((text: string) => {
    setTerminal((buffer) => appendOutput(buffer, [{ inline: false, text, color: '' }]));
    setStatus('running');
    workerRef.current?.postMessage({ type: 'input', text });
  }, []);

  const updateBreakpoints = useCallback((breakpoints: Breakpoints) => {
    workerRef.current?.postMessage({ type: 'breakpoints', breakpoints });
  }, []);

  const dismissFailure = useCallback(() => {
    setFailure(null);
  }, []);

  return {
    status,
    terminal,
    variables,
    pausedAt,
    failure,
    duration,
    wasStopped,
    start,
    stop,
    resume,
    submitInput,
    updateBreakpoints,
    dismissFailure,
  };
};
