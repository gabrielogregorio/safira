import { defineCommandMatrix } from './commandMatrix';
import { ENGLISH, PORTUGUESE } from './dialects';

it('has a word for every command', () => {
  expect(Object.keys(ENGLISH).sort()).toEqual(Object.keys(PORTUGUESE).sort());
});

defineCommandMatrix('English', ENGLISH);
