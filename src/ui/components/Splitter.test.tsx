import { fireEvent, render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { Splitter } from './Splitter';

const setup = (growsTowardStart = false, orientation: 'vertical' | 'horizontal' = 'vertical') => {
  const onChange = vi.fn();
  render(
    <Splitter
      label="Dividir"
      orientation={orientation}
      value={200}
      minimum={100}
      maximum={400}
      growsTowardStart={growsTowardStart}
      onChange={onChange}
    />,
  );
  const separator = screen.getByRole('separator', { name: 'Dividir' });
  separator.setPointerCapture = vi.fn();

  return { onChange, separator };
};

describe('Splitter', () => {
  it('tells its value to screen readers', () => {
    const { separator } = setup();

    expect(separator).toHaveAttribute('aria-valuenow', '200');
    expect(separator).toHaveAttribute('aria-valuemin', '100');
    expect(separator).toHaveAttribute('aria-valuemax', '400');
  });

  it('grows while dragging', () => {
    const { onChange, separator } = setup();
    fireEvent.pointerDown(separator, { clientX: 50 });
    fireEvent.pointerMove(separator, { clientX: 80 });

    expect(onChange).toHaveBeenCalledWith(230);
  });

  it('inverts the drag for a panel at the end', () => {
    const { onChange, separator } = setup(true);
    fireEvent.pointerDown(separator, { clientX: 50 });
    fireEvent.pointerMove(separator, { clientX: 80 });

    expect(onChange).toHaveBeenCalledWith(170);
  });

  it('uses the vertical position in a horizontal divider', () => {
    const { onChange, separator } = setup(false, 'horizontal');
    fireEvent.pointerDown(separator, { clientY: 10 });
    fireEvent.pointerMove(separator, { clientY: 30 });

    expect(onChange).toHaveBeenCalledWith(220);
  });

  it('stops when the pointer is released', () => {
    const { onChange, separator } = setup();
    fireEvent.pointerDown(separator, { clientX: 50 });
    fireEvent.pointerUp(separator);
    fireEvent.pointerMove(separator, { clientX: 80 });

    expect(onChange).not.toHaveBeenCalled();
  });

  it('ignores a move without a drag', () => {
    const { onChange, separator } = setup();
    fireEvent.pointerMove(separator, { clientX: 80 });

    expect(onChange).not.toHaveBeenCalled();
  });

  it('works with the arrows of the keyboard', async () => {
    const { onChange, separator } = setup();
    separator.focus();
    await userEvent.keyboard('{ArrowRight}');
    await userEvent.keyboard('{ArrowLeft}');

    expect(onChange).toHaveBeenNthCalledWith(1, 216);
    expect(onChange).toHaveBeenNthCalledWith(2, 184);
  });

  it('ignores the arrows of the other axis', async () => {
    const { onChange, separator } = setup();
    separator.focus();
    await userEvent.keyboard('{ArrowUp}');

    expect(onChange).not.toHaveBeenCalled();
  });
});
