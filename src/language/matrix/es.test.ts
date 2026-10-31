import { defineCommandMatrix } from './commandMatrix';
import { SPANISH, PORTUGUESE } from './dialects';

it('has a word for every command', () => {
  expect(Object.keys(SPANISH).sort()).toEqual(Object.keys(PORTUGUESE).sort());
});

defineCommandMatrix('Spanish', SPANISH);
