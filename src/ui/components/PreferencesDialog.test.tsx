import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { DEFAULT_SETTINGS } from '@/settings/settings';
import { PreferencesDialog } from './PreferencesDialog';

const setup = () => {
  const onChange = vi.fn();
  render(<PreferencesDialog settings={DEFAULT_SETTINGS} locale="en-us" onChange={onChange} onClose={vi.fn()} />);

  return onChange;
};

describe('PreferencesDialog', () => {
  it('marks the current theme and language', () => {
    setup();

    expect(screen.getByRole('radio', { name: 'Light' })).toBeChecked();
    expect(screen.getByRole('radio', { name: 'English' })).toBeChecked();
  });

  it('changes the theme together with the syntax colors', async () => {
    const onChange = setup();
    await userEvent.click(screen.getByRole('radio', { name: 'Dark' }));

    expect(onChange).toHaveBeenCalledWith({ theme: 'dark', syntax: 'dark' });
  });

  it('changes the language', async () => {
    const onChange = setup();
    await userEvent.click(screen.getByRole('radio', { name: 'Español' }));

    expect(onChange).toHaveBeenCalledWith({ locale: 'es' });
  });

  it('shows one picture per choice, hidden from screen readers', () => {
    setup();

    expect(document.querySelectorAll('svg.choice-art[aria-hidden="true"]')).toHaveLength(6);
  });
});
