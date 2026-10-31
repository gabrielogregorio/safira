import * as Dialog from '@radix-ui/react-dialog';
import type { CSSProperties, PointerEvent } from 'react';
import { useEffect, useRef, useState } from 'react';
import { useTranslation } from '@/i18n/i18n';
import type { ThemeId } from '@/settings/settings';
import { loadFishes, saveFishes } from '@/ui/aquarium/aquariumStore';
import { drawWorld, easePalette, startingPalette } from '@/ui/aquarium/aquariumRenderer';
import type { World, WorldEvent } from '@/ui/aquarium/aquariumWorld';
import {
  createWorld,
  movePointer,
  pressPointer,
  releasePointer,
  resizeWorld,
  stepWorld,
} from '@/ui/aquarium/aquariumWorld';
import { useIdle } from '@/ui/hooks/useIdle';
import { prefersMotion } from '@/ui/motion';
import type { SoundName } from '@/ui/sound/sounds';
import { SEA_SOUNDS, soundPlayer } from '@/ui/sound/sounds';
import { CloseButton } from './CloseButton';

export interface ScreenPoint {
  x: number;
  y: number;
}

interface AquariumProps {
  origin: ScreenPoint;
  theme: ThemeId;
  isSoundOn: boolean;
  onClose: () => void;
}

const SHRINK_MILLISECONDS = 480;
const SAVE_MILLISECONDS = 10000;
const FRAME_MILLISECONDS = 1000 / 30;
const LONGEST_STEP_SECONDS = 0.1;
const LARGEST_PIXEL_RATIO = 2;
const MILLISECONDS_PER_SECOND = 1000;
const SEA_GAIN = 0.8;

const EVENT_SOUNDS: Record<WorldEvent['kind'], SoundName> = {
  eat: 'fishEat',
  chomp: 'fishChomp',
  flee: 'fishFlee',
  pop: 'pop',
  plant: 'plant',
  food: 'foodDrop',
  hold: 'waterHold',
  swish: 'waterSwish',
};

const playEvents = (events: WorldEvent[]): void => {
  for (const event of events) {
    void soundPlayer.play(EVENT_SOUNDS[event.kind], 'voice' in event ? event.voice : 1);
  }
};

export const Aquarium = ({ origin, theme, isSoundOn, onClose }: AquariumProps) => {
  const t = useTranslation();
  const [isClosing, setIsClosing] = useState(false);
  const isIdle = useIdle();
  // A state and not a ref: the dialog mounts its content after this effect would run.
  const [canvas, setCanvas] = useState<HTMLCanvasElement | null>(null);
  const worldRef = useRef<World | null>(null);
  const latestTheme = useRef(theme);
  const closeTimer = useRef<ReturnType<typeof setTimeout> | null>(null);

  useEffect(() => {
    latestTheme.current = theme;
  }, [theme]);

  useEffect(() => {
    const context = canvas?.getContext('2d') ?? null;

    if (canvas === null || context === null) {
      return undefined;
    }

    const world = createWorld(loadFishes(), window.innerWidth, window.innerHeight);
    const palette = startingPalette(latestTheme.current);
    worldRef.current = world;
    let frame = 0;
    let lastTime = performance.now();

    const fit = (): void => {
      const ratio = Math.min(window.devicePixelRatio, LARGEST_PIXEL_RATIO);
      canvas.setAttribute('width', String(window.innerWidth * ratio));
      canvas.setAttribute('height', String(window.innerHeight * ratio));
      context.setTransform(ratio, 0, 0, ratio, 0, 0);
      resizeWorld(world, window.innerWidth, window.innerHeight);
    };

    const save = (): void => {
      saveFishes(world.fishes);
    };

    const draw = (time: number): void => {
      frame = requestAnimationFrame(draw);

      if (time - lastTime >= FRAME_MILLISECONDS) {
        const seconds = Math.min(LONGEST_STEP_SECONDS, (time - lastTime) / MILLISECONDS_PER_SECOND);
        lastTime = time;
        playEvents(stepWorld(world, seconds));
        easePalette(palette, latestTheme.current, seconds);
        drawWorld(context, world, palette);
      }
    };

    fit();
    frame = requestAnimationFrame(draw);
    const saveTimer = setInterval(save, SAVE_MILLISECONDS);
    window.addEventListener('resize', fit);
    window.addEventListener('pagehide', save);

    return () => {
      cancelAnimationFrame(frame);
      clearInterval(saveTimer);
      window.removeEventListener('resize', fit);
      window.removeEventListener('pagehide', save);
      save();
    };
  }, [canvas]);

  useEffect(() => {
    if (isSoundOn) {
      void soundPlayer.hold(SEA_SOUNDS[theme], 1, SEA_GAIN);
    }

    return soundPlayer.release;
  }, [isSoundOn, theme]);

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

  const handlePointer = (event: PointerEvent, act: (world: World, x: number, y: number) => void): void => {
    if (worldRef.current !== null) {
      act(worldRef.current, event.clientX, event.clientY);
    }
  };

  const originStyle = { '--origin-x': `${origin.x}px`, '--origin-y': `${origin.y}px` } as CSSProperties;
  const classes = ['aquarium', isClosing ? 'aquarium-closing' : '', isIdle ? 'is-idle' : ''].filter(Boolean).join(' ');

  return (
    <Dialog.Root
      open
      onOpenChange={(isOpen) => {
        if (!isOpen) {
          close();
        }
      }}>
      <Dialog.Portal>
        <Dialog.Content className={classes} style={originStyle} aria-describedby={undefined}>
          <Dialog.Title className="aquarium-title">{t('Aquarium')}</Dialog.Title>
          <canvas
            ref={setCanvas}
            className="aquarium-water"
            role="img"
            aria-label={t('Aquarium')}
            onPointerDown={(event) => {
              event.currentTarget.setPointerCapture(event.pointerId);
              handlePointer(event, pressPointer);
            }}
            onPointerMove={(event) => {
              handlePointer(event, (world, x, y) => {
                playEvents(movePointer(world, x, y));
              });
            }}
            onPointerUp={(event) => {
              handlePointer(event, (world) => {
                playEvents(releasePointer(world));
              });
            }}
            onPointerCancel={(event) => {
              handlePointer(event, (world) => {
                world.pointer = null;
              });
            }}
          />
          <Dialog.Close asChild>
            <CloseButton />
          </Dialog.Close>
        </Dialog.Content>
      </Dialog.Portal>
    </Dialog.Root>
  );
};
