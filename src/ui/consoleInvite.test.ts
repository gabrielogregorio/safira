import { printConsoleInvite, REPOSITORY_URL } from './consoleInvite';

describe('printConsoleInvite', () => {
  it('invites to the repository in the console', () => {
    const log = vi.spyOn(console, 'log').mockImplementation(() => undefined);
    printConsoleInvite('Oi', 'Venha');

    expect(log.mock.calls[0][0]).toContain(REPOSITORY_URL);
    expect(log.mock.calls[0][0]).toContain('Oi');
    vi.restoreAllMocks();
  });
});
