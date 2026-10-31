import { defineCommandMatrix } from './commandMatrix';
import { PORTUGUESE } from './dialects';

it('has a word for every command', () => {
  expect(Object.keys(PORTUGUESE).sort()).toEqual(Object.keys(PORTUGUESE).sort());
});

defineCommandMatrix('Portuguese', PORTUGUESE);
