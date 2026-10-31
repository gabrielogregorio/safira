import { defineCommandMatrix } from './commandMatrix';
import { JAPANESE, PORTUGUESE } from './dialects';

it('has a word for every command', () => {
  expect(new Set(Object.keys(JAPANESE))).toEqual(new Set(Object.keys(PORTUGUESE)));
});

defineCommandMatrix('Japanese', JAPANESE);
