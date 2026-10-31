import type { CheckResult } from '@/lessons/lessonCheck';
import { checkProgram } from '@/lessons/lessonCheck';
import type { CheckWorker } from '@/ui/hooks/useLessonMode';
import type { RunnerEvent, RunnerRequest } from '@/runtime/protocol';
import { RunnerSession } from '@/runtime/runnerSession';
import type { RunnerWorker } from '@/ui/hooks/useRunner';

export class FakeWorker implements RunnerWorker {
  public onmessage: ((message: MessageEvent<RunnerEvent>) => void) | null = null;
  public terminated = false;
  public requests: RunnerRequest[] = [];
  private readonly session = new RunnerSession(
    (event) => {
      if (!this.terminated) {
        this.onmessage?.({ data: event } as MessageEvent<RunnerEvent>);
      }
    },
    { now: () => 0, sleep: () => Promise.resolve() },
  );

  public postMessage(request: RunnerRequest): void {
    this.requests.push(request);
    void this.session.handle(request);
  }

  public terminate(): void {
    this.terminated = true;
  }
}

export const createFakeCheckWorker = (): CheckWorker => {
  const worker: CheckWorker = {
    onmessage: null,
    terminate: () => undefined,
    postMessage: (request) => {
      void checkProgram(request).then((result) => {
        worker.onmessage?.({ data: result } as MessageEvent<CheckResult>);
      });
    },
  };

  return worker;
};
