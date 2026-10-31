import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { ThemeToggle } from './ThemeToggle';

const wheelTransform = () => document.querySelector<SVGGElement>('.orb-wheel')?.style.transform;

describe('ThemeToggle', () => {
  it('names the current theme', () => {
    render(<ThemeToggle theme="dark" onChange={vi.fn()} />);

    expect(screen.getByRole('button', { name: 'Theme: Dark' })).toBeInTheDocument();
  });

  it.each([
    ['light', 'dark'],
    ['dark', 'simple'],
    ['simple', 'light'],
  ] as const)('goes from %s to %s on click', async (current, next) => {
    const onChange = vi.fn();
    render(<ThemeToggle theme={current} onChange={onChange} />);
    await userEvent.click(screen.getByRole('button'));

    expect(onChange).toHaveBeenCalledWith(next);
  });

  it('keeps turning the wheel forward when the cycle restarts', () => {
    const { rerender } = render(<ThemeToggle theme="light" onChange={vi.fn()} />);

    expect(wheelTransform()).toBe('rotate(0deg)');

    rerender(<ThemeToggle theme="dark" onChange={vi.fn()} />);
    rerender(<ThemeToggle theme="simple" onChange={vi.fn()} />);
    rerender(<ThemeToggle theme="light" onChange={vi.fn()} />);

    expect(wheelTransform()).toBe('rotate(-360deg)');
  });

  it('follows a theme chosen elsewhere', () => {
    const { rerender } = render(<ThemeToggle theme="light" onChange={vi.fn()} />);
    rerender(<ThemeToggle theme="simple" onChange={vi.fn()} />);

    expect(wheelTransform()).toBe('rotate(-240deg)');
    expect(document.querySelector('.orb-slot[data-active="true"]')).toBe(document.querySelectorAll('.orb-slot')[2]);
  });
});
