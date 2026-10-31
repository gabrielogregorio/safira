import { defineCommandMatrix } from './commandMatrix';
import { ENGLISH, PORTUGUESE } from './dialects';

it('has a word for every command', () => {
  expect(new Set(Object.keys(ENGLISH))).toEqual(new Set(Object.keys(PORTUGUESE)));
});

defineCommandMatrix('English', ENGLISH);
