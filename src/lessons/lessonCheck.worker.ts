import type { CheckRequest } from './lessonCheck';
import { checkProgram } from './lessonCheck';

self.onmessage = (message: MessageEvent<CheckRequest>): void => {
  void checkProgram(message.data).then((result) => {
    self.postMessage(result);
  });
};
