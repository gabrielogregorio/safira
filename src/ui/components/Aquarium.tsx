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
  feedFish,
  movePointer,
  pressPointer,
  releasePointer,
  resizeWorld,
  scrollPointer,
  stepWorld,
  warmUpWorld,
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

const SAVE_MILLISECONDS = 10000;
const FRAME_MILLISECONDS = 1000 / 30;
const LONGEST_STEP_SECONDS = 0.1;
const LARGEST_PIXEL_RATIO = 2;
const MILLISECONDS_PER_SECOND = 1000;
const SEA_GAIN = 0.48;

const EVENT_SOUNDS: Record<WorldEvent['kind'], SoundName> = {
  eat: 'fishEat',
  chomp: 'fishChomp',
  burst: 'fishBurst',
  flee: 'fishFlee',
  pop: 'pop',
  plant: 'plant',
  food: 'foodDrop',
  hold: 'waterHold',
};

const playEvents = (events: WorldEvent[]): void => {
  for (const event of events) {
    void soundPlayer.play(EVENT_SOUNDS[event.kind], 'voice' in event ? event.voice : 1);
  }
};

export const Aquarium = ({ origin, theme, isSoundOn, onClose }: AquariumProps) => {
  const t = useTranslation();
  const isIdle = useIdle();
  // Decided once: a still picture must not start moving in the middle of a visit.
  const [isMoving] = useState(prefersMotion);
  // A state and not a ref: the dialog mounts its content after this effect would run.
  const [canvas, setCanvas] = useState<HTMLCanvasElement | null>(null);
  const worldRef = useRef<World | null>(null);
  const latestTheme = useRef(theme);

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

      if (!isMoving) {
        drawWorld(context, world, palette);
      }
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

    warmUpWorld(world);
    fit();

    if (isMoving) {
      frame = requestAnimationFrame(draw);
    }

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
  }, [canvas, isMoving]);

  useEffect(() => {
    if (isSoundOn) {
      void soundPlayer.hold(SEA_SOUNDS[theme], 1, SEA_GAIN);
    }

    return soundPlayer.release;
  }, [isSoundOn, theme]);

  const close = (): void => {
    void soundPlayer.play('aquariumClose');
    onClose();
  };

  const handlePointer = (event: PointerEvent, act: (world: World, x: number, y: number) => void): void => {
    if (isMoving && worldRef.current !== null) {
      act(worldRef.current, event.clientX, event.clientY);
    }
  };

  const originStyle = { '--origin-x': `${origin.x}px`, '--origin-y': `${origin.y}px` } as CSSProperties;
  const classes = isIdle ? 'aquarium is-idle' : 'aquarium';

  return (
    <Dialog.Root open onOpenChange={close}>
      <Dialog.Portal>
        <Dialog.Content className={classes} style={originStyle} aria-describedby={undefined}>
          <Dialog.Title className="aquarium-title">{t('Aquarium')}</Dialog.Title>
          <canvas
            ref={setCanvas}
            className="aquarium-water"
            role="img"
            aria-label={t('Aquarium')}
            onWheel={() => {
              if (isMoving && worldRef.current !== null) {
                playEvents(scrollPointer(worldRef.current));
              }
            }}
            onContextMenu={(event) => {
              event.preventDefault();
            }}
            onPointerDown={(event) => {
              event.currentTarget.setPointerCapture(event.pointerId);
              handlePointer(event, (world, x, y) => {
                pressPointer(world, x, y, event.buttons);
              });
            }}
            onPointerMove={(event) => {
              handlePointer(event, (world, x, y) => {
                movePointer(world, x, y, event.buttons);
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
          {isMoving ? (
            <button
              type="button"
              className="button aquarium-feed"
              onClick={() => {
                if (worldRef.current !== null) {
                  playEvents(feedFish(worldRef.current));
                }
              }}>
              {t('Feed the fish')}
            </button>
          ) : (
            <p className="aquarium-feed aquarium-note">
              {t('The animation is off because of your motion preference.')}
            </p>
          )}
          <Dialog.Close asChild>
            <CloseButton />
          </Dialog.Close>
        </Dialog.Content>
      </Dialog.Portal>
    </Dialog.Root>
  );
};
