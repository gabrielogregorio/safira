import { fireEvent, render, screen } from '@testing-library/react';
import { createRef } from 'react';
import { ArchiveInput } from './ArchiveInput';

const setup = () => {
  const onSelect = vi.fn();
  render(<ArchiveInput ref={createRef()} label="Import" onSelect={onSelect} />);

  return { onSelect, input: screen.getByLabelText('Import') };
};

describe('ArchiveInput', () => {
  it('hands over the chosen file', () => {
    const { onSelect, input } = setup();
    const file = new File(['x'], 'a.zip');
    fireEvent.change(input, { target: { files: [file] } });

    expect(onSelect).toHaveBeenCalledExactlyOnceWith(file);
  });

  it('does nothing when the choice is cancelled', () => {
    const { onSelect, input } = setup();
    fireEvent.change(input, { target: { files: [] } });

    expect(onSelect).not.toHaveBeenCalled();
  });
});
