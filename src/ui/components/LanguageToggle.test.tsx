import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import type { Locale } from '@/language/messages';
import { LanguageToggle } from './LanguageToggle';

describe('LanguageToggle', () => {
  it('names the current language', () => {
    render(<LanguageToggle locale="pt-br" onChange={vi.fn()} />);

    expect(screen.getByRole('button', { name: 'Language: Português (Brasil)' })).toBeInTheDocument();
  });

  it('falls back to the code of a language it does not know', () => {
    render(<LanguageToggle locale={'fr' as string as Locale} onChange={vi.fn()} />);

    expect(screen.getByRole('button', { name: 'Language: fr' })).toBeInTheDocument();
  });

  it.each([
    ['en-us', 'pt-br'],
    ['pt-br', 'es'],
    ['es', 'zh-cn'],
    ['zh-cn', 'ja'],
    ['ja', 'en-us'],
  ] as const)('goes from %s to %s on click', async (current, next) => {
    const onChange = vi.fn();
    render(<LanguageToggle locale={current} onChange={onChange} />);
    await userEvent.click(screen.getByRole('button'));

    expect(onChange).toHaveBeenCalledWith(next);
  });

  it('hides the flags from screen readers', () => {
    render(<LanguageToggle locale="es" onChange={vi.fn()} />);

    expect(document.querySelector('svg')).toHaveAttribute('aria-hidden', 'true');
  });
});
