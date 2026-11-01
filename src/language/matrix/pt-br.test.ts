import { defineCommandMatrix } from './commandMatrix';
import { PORTUGUESE } from './dialects';

it('has a word for every command', () => {
  expect(new Set(Object.keys(PORTUGUESE))).toEqual(new Set(Object.keys(PORTUGUESE)));
});

defineCommandMatrix('Portuguese', PORTUGUESE);
