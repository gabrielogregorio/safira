import { prefersMotion } from './motion';

describe('prefersMotion', () => {
  beforeEach(() => {
    vi.stubGlobal('matchMedia', () => ({ matches: true }));
  });

  afterEach(() => {
    vi.unstubAllGlobals();
    delete document.documentElement.dataset['vision'];
  });

  it('follows the system preference', () => {
    expect(prefersMotion()).toBe(true);
  });

  it('turns motion off in the calm mode, even when the system allows it', () => {
    document.documentElement.dataset['vision'] = 'calm';

    expect(prefersMotion()).toBe(false);
  });
});
