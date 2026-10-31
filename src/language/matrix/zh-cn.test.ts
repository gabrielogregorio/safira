import { defineCommandMatrix } from './commandMatrix';
import { CHINESE, PORTUGUESE } from './dialects';

it('has a word for every command', () => {
  expect(Object.keys(CHINESE).sort()).toEqual(Object.keys(PORTUGUESE).sort());
});

defineCommandMatrix('Chinese', CHINESE);
