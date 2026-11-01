import { defineCommandMatrix } from './commandMatrix';
import { CHINESE, PORTUGUESE } from './dialects';

it('has a word for every command', () => {
  expect(new Set(Object.keys(CHINESE))).toEqual(new Set(Object.keys(PORTUGUESE)));
});

defineCommandMatrix('Chinese', CHINESE);
