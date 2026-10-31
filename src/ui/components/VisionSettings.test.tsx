import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { useState } from 'react';
import { VISION_MODES } from '@/settings/vision';
import type { VisionMode } from '@/settings/vision';
import { VisionSettings } from './VisionSettings';

const Harness = ({ onChange }: { onChange: (vision: VisionMode) => void }) => {
  const [vision, setVision] = useState<VisionMode>('tritanopia');

  return (
    <VisionSettings
      vision={vision}
      onChange={(next) => {
        setVision(next);
        onChange(next);
      }}
    />
  );
};

const open = async (onChange = vi.fn()) => {
  render(<Harness onChange={onChange} />);
  await userEvent.click(screen.getByRole('button', { name: 'Accessibility' }));

  return onChange;
};

describe('VisionSettings', () => {
  it('stays closed until the gear is pressed', () => {
    render(<Harness onChange={vi.fn()} />);

    expect(screen.queryByRole('dialog')).not.toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Accessibility' })).toHaveAttribute(
      'title',
      'Accessibility: Tritanopia (weak blue)',
    );
  });

  it('lists every mode with the current one chosen and focused', async () => {
    await open();

    expect(screen.getByRole('dialog', { name: 'Accessibility' })).toBeInTheDocument();
    expect(screen.getAllByRole('radio')).toHaveLength(VISION_MODES.length);
    expect(screen.getByRole('radio', { name: 'Tritanopia (weak blue)' })).toBeChecked();
    expect(screen.getByRole('radio', { name: 'Tritanopia (weak blue)' })).toHaveFocus();
  });

  it('applies a choice at once and stays open to compare', async () => {
    const onChange = await open();
    await userEvent.click(screen.getByRole('radio', { name: 'Low vision (cataract, glaucoma)' }));

    expect(onChange).toHaveBeenCalledExactlyOnceWith('lowVision');
    expect(screen.getByRole('radio', { name: 'Low vision (cataract, glaucoma)' })).toBeChecked();
    expect(screen.getByRole('dialog')).toBeInTheDocument();
  });

  it('explains what each mode does', async () => {
    await open();

    expect(screen.getByRole('radio', { name: 'Achromatopsia (no colors)' })).toHaveAccessibleDescription(
      'For those who do not see colors. Uses grays, with bold, italics and underlines to tell things apart.',
    );
  });

  it('closes like any modal', async () => {
    await open();
    await userEvent.keyboard('{Escape}');

    expect(screen.queryByRole('dialog')).not.toBeInTheDocument();
  });
});
