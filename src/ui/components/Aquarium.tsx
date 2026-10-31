import * as Dialog from '@radix-ui/react-dialog';
import type { CSSProperties } from 'react';
import { useEffect, useRef, useState } from 'react';
import { useTranslation } from '@/i18n/i18n';
import { prefersMotion } from '@/ui/motion';
import { soundPlayer } from '@/ui/sound/sounds';
import { CloseButton } from './CloseButton';

export interface ScreenPoint {
  x: number;
  y: number;
}

interface AquariumProps {
  origin: ScreenPoint;
  onClose: () => void;
}

const SHRINK_MILLISECONDS = 480;

const FISHES = [
  { body: '#ffb347', fin: '#ff8a2a', top: 16, size: 74, seconds: 19, start: 12, goesLeft: false },
  { body: '#ffe066', fin: '#f2b705', top: 30, size: 48, seconds: 13, start: 64, goesLeft: true },
  { body: '#ff8fb1', fin: '#f0507f', top: 44, size: 92, seconds: 24, start: 36, goesLeft: false },
  { body: '#7fe3ff', fin: '#1f9fe0', top: 56, size: 56, seconds: 16, start: 82, goesLeft: true },
  { body: '#b6f27a', fin: '#56b92e', top: 68, size: 64, seconds: 21, start: 22, goesLeft: false },
  { body: '#ffb347', fin: '#ff8a2a', top: 24, size: 38, seconds: 11, start: 48, goesLeft: false },
  { body: '#d3a6ff', fin: '#9a5ff0', top: 76, size: 44, seconds: 15, start: 70, goesLeft: true },
  { body: '#ffffff', fin: '#ff7a3c', top: 38, size: 60, seconds: 27, start: 90, goesLeft: true },
];

const BUBBLES = [8, 17, 26, 38, 47, 59, 68, 77, 86, 94];
const WEEDS = [6, 13, 30, 52, 71, 84, 93];

const FishArt = ({ body, fin }: { body: string; fin: string }) => (
  <svg viewBox="0 0 64 36" aria-hidden="true">
    <path className="aquarium-tail" d="M16 18 L1 6 L5 18 L1 30 Z" fill={fin} />
    <path d="M12 18 C22 3 46 3 60 18 C46 33 22 33 12 18 Z" fill={body} />
    <path d="M30 7 C34 1 42 1 46 8 Z" fill={fin} />
    <path d="M32 19 C36 26 42 26 44 21 Z" fill={fin} fillOpacity="0.8" />
    <path d="M14 15 C26 5 44 6 54 13 C42 10 26 11 14 15 Z" fill="#ffffff" fillOpacity="0.6" />
    <circle cx="50" cy="15" r="3.4" fill="#ffffff" />
    <circle cx="51" cy="15" r="1.8" fill="#102a43" />
  </svg>
);

export const Aquarium = ({ origin, onClose }: AquariumProps) => {
  const t = useTranslation();
  const [isClosing, setIsClosing] = useState(false);
  const closeTimer = useRef<ReturnType<typeof setTimeout> | null>(null);

  useEffect(
    () => () => {
      if (closeTimer.current !== null) {
        clearTimeout(closeTimer.current);
      }
    },
    [],
  );

  const close = (): void => {
    if (isClosing) {
      return;
    }

    void soundPlayer.play('modalClose');

    if (prefersMotion()) {
      setIsClosing(true);
      closeTimer.current = setTimeout(onClose, SHRINK_MILLISECONDS);
    } else {
      onClose();
    }
  };

  const originStyle = { '--origin-x': `${origin.x}px`, '--origin-y': `${origin.y}px` } as CSSProperties;

  return (
    <Dialog.Root
      open
      onOpenChange={(isOpen) => {
        if (!isOpen) {
          close();
        }
      }}>
      <Dialog.Portal>
        <Dialog.Content
          className={isClosing ? 'aquarium aquarium-closing' : 'aquarium'}
          style={originStyle}
          aria-describedby={undefined}>
          <Dialog.Title className="aquarium-title">{t('Aquarium')}</Dialog.Title>
          <div className="aquarium-light" aria-hidden="true" />
          {WEEDS.map((left, index) => (
            <span
              key={left}
              className="aquarium-weed"
              aria-hidden="true"
              style={{ left: `${left}%`, height: `${90 + (index % 3) * 50}px`, animationDelay: `-${index * 0.7}s` }}
            />
          ))}
          {FISHES.map((fish) => (
            <div
              key={`${fish.body}-${fish.top}`}
              className={fish.goesLeft ? 'aquarium-fish aquarium-fish-left' : 'aquarium-fish'}
              aria-hidden="true"
              style={
                {
                  '--start': `${fish.start}%`,
                  top: `${fish.top}%`,
                  width: `${fish.size}px`,
                  animationDuration: `${fish.seconds}s`,
                  animationDelay: `-${(fish.start / 100) * fish.seconds}s`,
                } as CSSProperties
              }>
              <FishArt body={fish.body} fin={fish.fin} />
            </div>
          ))}
          {BUBBLES.map((left, index) => (
            <span
              key={left}
              className="aquarium-bubble"
              aria-hidden="true"
              style={{
                left: `${left}%`,
                width: `${8 + (index % 4) * 6}px`,
                height: `${8 + (index % 4) * 6}px`,
                animationDuration: `${6 + (index % 5)}s`,
                animationDelay: `-${index * 1.1}s`,
              }}
            />
          ))}
          <Dialog.Close asChild>
            <CloseButton />
          </Dialog.Close>
        </Dialog.Content>
      </Dialog.Portal>
    </Dialog.Root>
  );
};
