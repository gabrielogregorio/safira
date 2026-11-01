import { eraseEverything } from './eraseEverything';

describe('eraseEverything', () => {
  it('removes what is from Safira and nothing else', () => {
    localStorage.setItem('safira.projects.v1', '[]');
    localStorage.setItem('safira.aquarium.v1', '{}');
    sessionStorage.setItem('safira.cat.met', 'true');
    localStorage.setItem('other-site', 'keep');

    eraseEverything();

    expect(localStorage.getItem('safira.projects.v1')).toBeNull();
    expect(localStorage.getItem('safira.aquarium.v1')).toBeNull();
    expect(sessionStorage.getItem('safira.cat.met')).toBeNull();
    expect(localStorage.getItem('other-site')).toBe('keep');
  });
});
