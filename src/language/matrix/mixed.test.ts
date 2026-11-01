import { defineLanguageMixture, LANGUAGES } from './commandMatrix';

it('mixes the five languages', () => {
  expect(LANGUAGES).toHaveLength(5);
});

defineLanguageMixture();
