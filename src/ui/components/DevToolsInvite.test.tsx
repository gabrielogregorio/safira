import { act, render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { DevToolsInvite, REPOSITORY_URL } from './DevToolsInvite';

const announce = (isOpen: boolean): void => {
  act(() => {
    window.dispatchEvent(new CustomEvent('devtoolschange', { detail: { isOpen, orientation: 'vertical' } }));
  });
};

describe('DevToolsInvite', () => {
  beforeEach(() => {
    vi.spyOn(console, 'log').mockImplementation(() => undefined);
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  it('prints the invite once in the console', () => {
    const { rerender } = render(<DevToolsInvite />);
    rerender(<DevToolsInvite />);

    expect(console.log).toHaveBeenCalledTimes(1);
  });

  it('stays hidden until the tools open', () => {
    render(<DevToolsInvite />);

    expect(screen.queryByRole('status')).not.toBeInTheDocument();

    announce(true);

    expect(screen.getByRole('link', { name: 'Open the repository' })).toHaveAttribute('href', REPOSITORY_URL);
  });

  it('does not come back after being closed', async () => {
    render(<DevToolsInvite />);
    announce(true);
    await userEvent.click(screen.getByRole('button'));
    announce(true);

    expect(screen.queryByRole('status')).not.toBeInTheDocument();
  });
});
