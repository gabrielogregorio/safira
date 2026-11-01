import { render, screen, within } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { useState } from 'react';
import { VISION_MODES } from '@/settings/vision';
import type { VisionMode } from '@/settings/vision';
import { SettingsDialog } from './SettingsDialog';

const Harness = ({ onChange, onErase = vi.fn() }: { onChange: (vision: VisionMode) => void; onErase?: () => void }) => {
  const [vision, setVision] = useState<VisionMode>('tritanopia');

  return (
    <SettingsDialog
      vision={vision}
      onChange={(next) => {
        setVision(next);
        onChange(next);
      }}
      onEraseEverything={onErase}
    />
  );
};

const open = async (onChange = vi.fn()) => {
  render(<Harness onChange={onChange} />);
  await userEvent.click(screen.getByRole('button', { name: 'Settings' }));

  return onChange;
};

describe('SettingsDialog', () => {
  it('stays closed until the gear is pressed', () => {
    render(<Harness onChange={vi.fn()} />);

    expect(screen.queryByRole('dialog')).not.toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Settings' })).toHaveAttribute(
      'title',
      'Accessibility: Tritanopia (weak blue)',
    );
  });

  it('lists every mode with the current one chosen and focused', async () => {
    await open();

    expect(screen.getByRole('dialog', { name: 'Settings' })).toBeInTheDocument();
    expect(screen.getByRole('radiogroup', { name: 'Accessibility' })).toBeInTheDocument();
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

  it('only erases after the confirmation', async () => {
    const onErase = vi.fn();
    render(<Harness onChange={vi.fn()} onErase={onErase} />);
    await userEvent.click(screen.getByRole('button', { name: 'Settings' }));
    await userEvent.click(screen.getByRole('button', { name: 'Delete everything' }));

    expect(onErase).not.toHaveBeenCalled();
    expect(screen.getByRole('button', { name: 'Cancel' })).toHaveFocus();

    await userEvent.click(screen.getByRole('button', { name: 'Cancel' }));

    expect(onErase).not.toHaveBeenCalled();

    await userEvent.click(screen.getByRole('button', { name: 'Delete everything' }));
    const dialog = screen.getByRole('dialog', { name: 'Delete everything?' });
    await userEvent.click(within(dialog).getByRole('button', { name: 'Delete everything' }));

    expect(onErase).toHaveBeenCalledTimes(1);
  });
});
