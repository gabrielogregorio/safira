import { defineCommandMatrix } from './commandMatrix';
import { SPANISH, PORTUGUESE } from './dialects';

it('has a word for every command', () => {
  expect(new Set(Object.keys(SPANISH))).toEqual(new Set(Object.keys(PORTUGUESE)));
});

defineCommandMatrix('Spanish', SPANISH);
