import { defineCommandMatrix } from './commandMatrix';
import { JAPANESE, PORTUGUESE } from './dialects';

it('has a word for every command', () => {
  expect(Object.keys(JAPANESE).sort()).toEqual(Object.keys(PORTUGUESE).sort());
});

defineCommandMatrix('Japanese', JAPANESE);
