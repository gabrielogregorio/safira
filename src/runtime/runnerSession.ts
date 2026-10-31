import { driveExecution } from '@/language/driver';
import { Interpreter, SafiraError } from '@/language/interpreter';
import { snapBreakpoints } from '@/language/statementLines';
import { VirtualFileSystem } from '@/language/virtualFileSystem';
import type { Breakpoints, OutputItem, RunMode, RunnerEvent, RunnerRequest, StartRequest } from './protocol';

const OUTPUT_BATCH_SIZE = 200;
const OUTPUT_BATCH_MILLISECONDS = 16;

export interface SessionClock {
  now: () => number;
  sleep: (milliseconds: number) => Promise<void>;
}

export class RunnerSession {
  private output: OutputItem[] = [];
  private lastFlush = 0;
  private mode: RunMode = 'run';
  private breakpoints: Breakpoints = {};
  private interpreter: Interpreter | null = null;
  private files = new VirtualFileSystem();
  private resolveInput: ((text: string) => void) | null = null;
  private resolvePause: (() => void) | null = null;

  public constructor(
    private readonly post: (event: RunnerEvent) => void,
    private readonly clock: SessionClock,
  ) {}

  public handle(request: RunnerRequest): Promise<void> {
    switch (request.type) {
      case 'start':
        return this.start(request);
      case 'input':
        this.resolveInput?.(request.text);
        this.resolveInput = null;
        break;
      case 'resume':
        this.mode = request.mode;
        this.resolvePause?.();
        this.resolvePause = null;
        break;
      case 'breakpoints':
        this.setBreakpoints(request.breakpoints);
        break;
    }

    return Promise.resolve();
  }

  private setBreakpoints(breakpoints: Breakpoints): void {
    this.breakpoints = Object.fromEntries(
      Object.entries(breakpoints).map(([file, lines]) => [file, snapBreakpoints(this.files.read(file) ?? '', lines)]),
    );
  }

  private flush(): void {
    if (this.output.length > 0) {
      this.post({ type: 'output', items: this.output });
      this.output = [];
    }

    this.lastFlush = this.clock.now();
  }

  private enqueue(item: OutputItem): void {
    this.output.push(item);
    const isBatchOld = this.clock.now() - this.lastFlush >= OUTPUT_BATCH_MILLISECONDS;

    if (this.output.length >= OUTPUT_BATCH_SIZE || isBatchOld) {
      this.flush();
    }
  }

  private shouldPause(file: string, line: number): boolean {
    if (this.mode === 'step') {
      return true;
    }

    return this.mode === 'debug' && (this.breakpoints[file] ?? []).includes(line);
  }

  private pause(file: string, line: number): Promise<void> | undefined {
    if (!this.shouldPause(file, line)) {
      return undefined;
    }

    this.flush();
    this.post({ type: 'paused', file, line, variables: this.interpreter?.getVariables() ?? [] });

    return new Promise((resolve) => {
      this.resolvePause = resolve;
    });
  }

  private async start(request: StartRequest): Promise<void> {
    this.mode = request.mode;
    this.files = new VirtualFileSystem(request.files);
    this.setBreakpoints(request.breakpoints);
    this.interpreter = new Interpreter({ files: this.files, locale: request.locale });
    const interpreter = this.interpreter;
    let failure = null;

    try {
      await driveExecution(interpreter.run(request.file), {
        onStep: (file, line) => this.pause(file, line),
        onOutput: (inline, text, color) => {
          this.enqueue({ inline, text, color });
        },
        onClear: () => {
          this.flush();
          this.post({ type: 'clear' });
        },
        onInput: () => {
          this.flush();
          this.post({ type: 'input-request', variables: interpreter.getVariables() });

          return new Promise((resolve) => {
            this.resolveInput = resolve;
          });
        },
        onSleep: (milliseconds) => {
          this.flush();

          return this.clock.sleep(milliseconds);
        },
        onTone: (frequency, milliseconds) => {
          this.flush();
          this.post({ type: 'tone', frequency, milliseconds });

          return this.clock.sleep(milliseconds);
        },
        onFilesChanged: () => {
          this.post({ type: 'files', files: this.files.snapshot() });
        },
      });
    } catch (error) {
      if (!(error instanceof SafiraError)) {
        throw error;
      }

      failure = {
        message: error.message,
        file: error.file,
        line: error.line,
        example: error.example,
        missingName: error.missingName,
      };
    }

    this.flush();
    this.post({
      type: 'finished',
      failure,
      files: this.files.snapshot(),
      variables: interpreter.getVariables(),
    });
  }
}
