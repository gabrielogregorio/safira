import type { RunnerEvent, RunnerRequest } from './protocol';
import { RunnerSession } from './runnerSession';

const session = new RunnerSession(
  (event: RunnerEvent) => {
    self.postMessage(event);
  },
  {
    now: () => performance.now(),
    sleep: (milliseconds) =>
      new Promise((resolve) => {
        setTimeout(resolve, milliseconds);
      }),
  },
);

self.onmessage = (message: MessageEvent<RunnerRequest>): void => {
  void session.handle(message.data);
};
