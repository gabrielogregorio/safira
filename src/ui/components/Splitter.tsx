import type { KeyboardEvent, PointerEvent } from 'react';
import { useRef } from 'react';

interface SplitterProps {
  label: string;
  orientation: 'vertical' | 'horizontal';
  value: number;
  minimum: number;
  maximum: number;
  growsTowardStart?: boolean;
  onChange: (value: number) => void;
}

const KEYBOARD_STEP = 16;

export const Splitter = ({
  label,
  orientation,
  value,
  minimum,
  maximum,
  growsTowardStart = false,
  onChange,
}: SplitterProps) => {
  const dragStart = useRef<{ position: number; value: number } | null>(null);
  const isVertical = orientation === 'vertical';
  const direction = growsTowardStart ? -1 : 1;
  const readPosition = (event: PointerEvent): number => (isVertical ? event.clientX : event.clientY);

  const handleKeyDown = (event: KeyboardEvent): void => {
    const decreaseKey = isVertical ? 'ArrowLeft' : 'ArrowUp';
    const increaseKey = isVertical ? 'ArrowRight' : 'ArrowDown';

    if (event.key === decreaseKey || event.key === increaseKey) {
      event.preventDefault();
      onChange(value + (event.key === increaseKey ? 1 : -1) * direction * KEYBOARD_STEP);
    }
  };

  return (
    // A focusable separator is an interactive widget, which the rule does not recognize.
    // eslint-disable-next-line jsx-a11y/no-noninteractive-element-interactions
    <div
      className={`splitter splitter-${orientation}`}
      role="separator"
      tabIndex={0}
      aria-label={label}
      aria-orientation={orientation}
      aria-valuenow={value}
      aria-valuemin={minimum}
      aria-valuemax={maximum}
      onKeyDown={handleKeyDown}
      onPointerDown={(event) => {
        event.currentTarget.setPointerCapture(event.pointerId);
        dragStart.current = { position: readPosition(event), value };
      }}
      onPointerMove={(event) => {
        if (dragStart.current !== null) {
          onChange(dragStart.current.value + (readPosition(event) - dragStart.current.position) * direction);
        }
      }}
      onPointerUp={() => {
        dragStart.current = null;
      }}
    />
  );
};
