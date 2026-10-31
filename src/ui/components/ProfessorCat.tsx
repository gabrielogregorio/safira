import type { JSX } from 'react';
import { useCallback, useEffect, useLayoutEffect, useRef, useState } from 'react';
import Markdown from 'react-markdown';
import { useTranslation } from '@/i18n/i18n';
import { stepKey } from '@/lessons/lessonPlace';
import type { LessonMode } from '@/ui/hooks/useLessonMode';
import { prefersMotion } from '@/ui/motion';
import { soundPlayer } from '@/ui/sound/sounds';
import { LessonBrief } from './LessonBrief';

const MET_KEY = 'safira.cat.met';
const CAT_SIZE = 96;
const EDGE_MARGIN = 12;
const FLEE_MILLISECONDS = 800;
const PANIC_RATE = 1.6;
const DRAG_START_PIXELS = 4;
const PHONE_WIDTH = 768;
const PHONE_BOTTOM_ROOM = 64;
const HAND_HEIGHT = 0.66;
const POINT_REACH = 140;
const HALF_TURN = 180;

type Scene = 'intro' | 'explain' | 'play' | 'result';

const TARGETS: Record<Scene, string> = {
  intro: '.cm-content',
  explain: '.cm-content',
  play: '.aero-button-run',
  result: '[role="log"]',
};

const readFlag = (key: string): boolean => {
  try {
    return sessionStorage.getItem(key) === 'true';
  } catch {
    return false;
  }
};

const writeFlag = (key: string): void => {
  try {
    sessionStorage.setItem(key, 'true');
  } catch {
    // Without storage he only comes back sooner, which hurts nobody.
  }
};

interface PlaceRule {
  anchor: string;
  x: (box: DOMRect) => number;
  y: (box: DOMRect) => number;
}

const rightInside = (box: DOMRect): number => box.right - CAT_SIZE - EDGE_MARGIN;
const bottomInside = (box: DOMRect): number => box.bottom - CAT_SIZE - EDGE_MARGIN;

const PLACES: Record<Scene, PlaceRule> = {
  intro: { anchor: '.code-editor', x: rightInside, y: bottomInside },
  explain: { anchor: '.code-editor', x: rightInside, y: bottomInside },
  // Below the bars, so he never covers the lesson switch, and the arm reaches up to the button.
  play: { anchor: '.output-column', x: rightInside, y: (box) => box.top + EDGE_MARGIN },
  result: { anchor: '.inspector', x: rightInside, y: bottomInside },
};

type Pose = 'wave' | 'point' | 'thumbs' | 'facepalm';

const Arm = ({ toX, toY }: { toX: number; toY: number }) => (
  <path
    d={`M72 80 Q${String((72 + toX) / 2)} ${String(toY + 12)} ${String(toX)} ${String(toY)}`}
    className="cat-sleeve"
  />
);

const HAND_LINE = { stroke: '#b9764e', strokeWidth: 1.4 };

const PointingHand = () => (
  <g className="cat-pointing-arm">
    <Arm toX={100} toY={80} />
    <g fill="#f5cda9" {...HAND_LINE}>
      <rect x="100" y="66" width="24" height="28" rx="10" />
      <rect x="116" y="70" width="32" height="10" rx="5" />
      <path d="M102 68 q2 -11 11 -8 q4 3 -1 10 Z" />
    </g>
  </g>
);

const ThumbsUpHand = () => (
  <g className="cat-thumbs-arm">
    <Arm toX={100} toY={76} />
    <g fill="#f5cda9" {...HAND_LINE}>
      <rect x="96" y="62" width="30" height="28" rx="11" />
      <rect x="104" y="34" width="12" height="34" rx="6" />
      <path d="M100 68h22M100 75h24M100 82h22" fill="none" />
    </g>
  </g>
);

const WavingHand = () => (
  <g className="cat-waving-arm">
    <Arm toX={102} toY={62} />
    <g fill="#f5cda9" {...HAND_LINE}>
      <rect x="94" y="44" width="26" height="24" rx="10" />
      <rect x="94" y="22" width="7" height="26" rx="3.5" />
      <rect x="103" y="18" width="7" height="30" rx="3.5" />
      <rect x="112" y="22" width="7" height="26" rx="3.5" />
      <rect x="118" y="46" width="14" height="7" rx="3.5" />
    </g>
  </g>
);

const FacepalmHand = () => (
  <g>
    <Arm toX={78} toY={46} />
    <g fill="#f5cda9" {...HAND_LINE}>
      <rect x="62" y="26" width="30" height="24" rx="10" />
      <rect x="40" y="26" width="26" height="7" rx="3.5" />
      <rect x="38" y="35" width="28" height="7" rx="3.5" />
      <rect x="40" y="44" width="26" height="7" rx="3.5" />
    </g>
  </g>
);

const HANDS: Record<Pose, () => JSX.Element> = {
  wave: WavingHand,
  point: PointingHand,
  thumbs: ThumbsUpHand,
  facepalm: FacepalmHand,
};

const CatFace = ({ isUpset }: { isUpset: boolean }) => (
  <g className="cat-head">
    <path d="M36 28 L38 4 L54 18 Z" fill="url(#cat-fur)" stroke="#24527e" strokeWidth="1.2" />
    <path d="M84 28 L82 4 L66 18 Z" fill="url(#cat-fur)" stroke="#24527e" strokeWidth="1.2" />
    <path d="M41 22 L41 11 L49 18 Z" fill="#ffb3c7" />
    <path d="M79 22 L79 11 L71 18 Z" fill="#ffb3c7" />
    <ellipse cx="60" cy="38" rx="27" ry="23" fill="url(#cat-fur)" stroke="#24527e" strokeWidth="1.2" />
    {isUpset ? (
      <g fill="none" stroke="#0e2a46" strokeWidth="2.4" strokeLinecap="round">
        <path d="M42 40 q6 5 12 0" />
        <path d="M66 40 q6 5 12 0" />
        <path d="M50 54 q10 -7 20 0" />
      </g>
    ) : (
      <g>
        <ellipse cx="49" cy="38" rx="6.4" ry="7.6" fill="#ffffff" />
        <ellipse cx="73" cy="38" rx="6.4" ry="7.6" fill="#ffffff" />
        <ellipse cx="51.5" cy="38" rx="3.4" ry="5.4" fill="#123b2c" />
        <ellipse cx="75.5" cy="38" rx="3.4" ry="5.4" fill="#123b2c" />
        <circle cx="53" cy="35" r="1.4" fill="#ffffff" />
        <circle cx="77" cy="35" r="1.4" fill="#ffffff" />
        <path d="M54 52 q6 5 12 0" fill="none" stroke="#0e2a46" strokeWidth="1.8" strokeLinecap="round" />
      </g>
    )}
    <path d="M57 46 h6 l-3 3 Z" fill="#ff8fab" />
    <g stroke="#0e2a46" strokeWidth="1" strokeLinecap="round" opacity="0.65">
      <path d="M36 46 L22 42M36 50 L22 52M84 46 L98 42M84 50 L98 52" />
    </g>
    <ellipse cx="60" cy="24" rx="17" ry="6" fill="#ffffff" fillOpacity="0.5" />
  </g>
);

const CatArt = ({ pose }: { pose: Pose }) => {
  const Hand = HANDS[pose];

  return (
    <svg viewBox="0 0 120 120" aria-hidden="true">
      <defs>
        <linearGradient id="cat-fur" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stopColor="#bfe9ff" />
          <stop offset="55%" stopColor="#5db7ee" />
          <stop offset="100%" stopColor="#1f7fd0" />
        </linearGradient>
      </defs>
      <path
        className="cat-tail"
        d="M34 98 C10 100 8 74 22 66"
        fill="none"
        stroke="#2f8fdc"
        strokeWidth="9"
        strokeLinecap="round"
      />
      <ellipse cx="58" cy="88" rx="28" ry="26" fill="url(#cat-fur)" stroke="#24527e" strokeWidth="1.2" />
      <ellipse cx="58" cy="94" rx="15" ry="15" fill="#e6f7ff" fillOpacity="0.8" />
      <ellipse cx="44" cy="112" rx="10" ry="5.5" fill="#e6f7ff" stroke="#24527e" strokeWidth="1" />
      <ellipse cx="72" cy="112" rx="10" ry="5.5" fill="#e6f7ff" stroke="#24527e" strokeWidth="1" />
      <CatFace isUpset={pose === 'facepalm'} />
      <Hand />
    </svg>
  );
};

const Stone = () => (
  <svg viewBox="0 0 48 34" aria-hidden="true">
    <defs>
      <radialGradient id="cat-stone" cx="38%" cy="28%" r="80%">
        <stop offset="0%" stopColor="#eef3f7" />
        <stop offset="50%" stopColor="#9aa8b5" />
        <stop offset="100%" stopColor="#566676" />
      </radialGradient>
    </defs>
    <path
      d="M4 26 C2 14 12 5 25 4 C38 3 46 13 44 24 C43 31 34 32 24 32 C14 32 5 32 4 26 Z"
      fill="url(#cat-stone)"
      stroke="#44525f"
      strokeWidth="1.2"
    />
    <ellipse cx="18" cy="12" rx="9" ry="4" fill="#ffffff" fillOpacity="0.65" />
  </svg>
);

interface ProfessorCatProps {
  lesson: LessonMode;
  hasError: boolean;
}

const whereToStand = (scene: Scene): { x: number; y: number } | null => {
  if (window.innerWidth <= PHONE_WIDTH) {
    return { x: window.innerWidth - CAT_SIZE - EDGE_MARGIN, y: window.innerHeight - CAT_SIZE - PHONE_BOTTOM_ROOM };
  }

  const rule = PLACES[scene];
  const box = document.querySelector(rule.anchor)?.getBoundingClientRect();

  return box === undefined ? null : { x: rule.x(box), y: rule.y(box) };
};

// He turns to the target, and the arm goes to the angle that leaves the finger on it.
const lookAtTarget = (element: HTMLElement, scene: Scene, spot: { x: number; y: number }): void => {
  const target = document.querySelector(TARGETS[scene])?.getBoundingClientRect();

  if (target === undefined || target.width === 0) {
    return;
  }

  const handX = spot.x + CAT_SIZE / 2;
  const handY = spot.y + CAT_SIZE * HAND_HEIGHT;
  const distanceX = target.left + Math.min(target.width / 2, POINT_REACH) - handX;
  const distanceY = target.top + Math.min(target.height / 2, POINT_REACH) - handY;
  const angle = (Math.atan2(distanceY, Math.abs(distanceX)) * HALF_TURN) / Math.PI;

  element.dataset['facing'] = distanceX < 0 ? 'left' : 'right';
  element.style.setProperty('--point-angle', `${String(Math.round(angle))}deg`);
};

const placeOnScreen = (element: HTMLElement, scene: Scene): void => {
  const spot = whereToStand(scene);

  if (spot !== null) {
    element.style.transform = `translate(${String(spot.x)}px, ${String(spot.y)}px)`;
    lookAtTarget(element, scene, spot);
  }
};

export const ProfessorCat = ({ lesson, hasError }: ProfessorCatProps) => {
  const t = useTranslation();
  const root = useRef<HTMLDivElement>(null);
  const stone = useRef<HTMLButtonElement>(null);
  const pressedAt = useRef<{ x: number; y: number } | null>(null);
  const [isHoldingStone, setIsHoldingStone] = useState(false);
  const [hasLeft, setHasLeft] = useState(false);
  const [hasMet, setHasMet] = useState(() => readFlag(MET_KEY));
  const key = stepKey(lesson.place);
  const [playAt, setPlayAt] = useState<string | null>(null);

  const scene = ((): Scene => {
    if (!hasMet && !lesson.hasRun) {
      return 'intro';
    }

    if (lesson.hasRun || !lesson.isOnStepFile) {
      return 'result';
    }

    return playAt === key ? 'play' : 'explain';
  })();

  const pose = ((): Pose => {
    if (hasError || lesson.verdict.status === 'failed') {
      return 'facepalm';
    }

    if (scene === 'intro') {
      return 'wave';
    }

    return scene === 'result' && lesson.isDone ? 'thumbs' : 'point';
  })();

  const reposition = useCallback(() => {
    if (root.current !== null) {
      placeOnScreen(root.current, scene);
    }
  }, [scene]);

  useLayoutEffect(reposition);

  useEffect(() => {
    window.addEventListener('resize', reposition);

    return () => {
      window.removeEventListener('resize', reposition);
    };
  }, [reposition]);

  const isHere = !isHoldingStone;

  useEffect(() => {
    if (isHere) {
      void soundPlayer.play('catMeow');
    }
  }, [isHere, key, scene]);

  useEffect(() => {
    if (!isHoldingStone) {
      return undefined;
    }

    const timer = setTimeout(
      () => {
        setHasLeft(true);
      },
      prefersMotion() ? FLEE_MILLISECONDS : 0,
    );

    return () => {
      clearTimeout(timer);
      setHasLeft(false);
    };
  }, [isHoldingStone]);

  if (lesson.step === undefined) {
    return null;
  }

  const pickUpStone = (): void => {
    void soundPlayer.play('catMeow', PANIC_RATE);
    setIsHoldingStone(true);
  };

  const dropStone = (): void => {
    pressedAt.current = null;
    setIsHoldingStone(false);

    if (stone.current !== null) {
      stone.current.style.transform = '';
    }
  };

  const stoneButton = (
    <button
      ref={stone}
      type="button"
      className={isHoldingStone ? 'cat-stone cat-stone-held' : 'cat-stone'}
      aria-label={t('Drag the stone')}
      aria-pressed={isHoldingStone}
      title={t('Drag the stone')}
      onPointerDown={(event) => {
        event.currentTarget.setPointerCapture(event.pointerId);
        pressedAt.current = { x: event.clientX, y: event.clientY };
      }}
      onPointerMove={(event) => {
        const start = pressedAt.current;

        if (start === null) {
          return;
        }

        const x = event.clientX - start.x;
        const y = event.clientY - start.y;

        if (Math.hypot(x, y) >= DRAG_START_PIXELS) {
          event.currentTarget.style.transform = `translate(${String(x)}px, ${String(y)}px)`;

          if (!isHoldingStone) {
            pickUpStone();
          }
        }
      }}
      onPointerUp={dropStone}
      onPointerCancel={dropStone}
      onClick={(event) => {
        // A click with no pointer comes from the keyboard, which has no way to drag.
        if (event.detail === 0) {
          if (isHoldingStone) {
            dropStone();
          } else {
            pickUpStone();
          }
        }
      }}>
      <Stone />
    </button>
  );

  if (isHoldingStone) {
    return (
      <>
        {hasLeft ? null : (
          <div ref={root} className="cat cat-fleeing" data-pose="wave">
            <div className="cat-bird">
              <CatArt pose="wave" />
            </div>
          </div>
        )}
        {stoneButton}
      </>
    );
  }

  const { step } = lesson;

  return (
    <>
      <div ref={root} className={`cat cat-at-${scene}`} data-pose={pose}>
        <section className="cat-bubble" aria-label={t('Professor Cat')} aria-live="polite">
          {scene === 'intro' ? (
            <>
              <p>
                {t(
                  'Meow! I am Professor Cat, and I will teach you to program, one step at a time. If you want me gone for a moment, drag the stone on the floor. When you let go, I come back.',
                )}
              </p>
              <div className="lesson-actions">
                <button
                  type="button"
                  className="button button-primary"
                  data-autofocus
                  onClick={() => {
                    writeFlag(MET_KEY);
                    setHasMet(true);
                  }}>
                  {t('Continue')}
                </button>
              </div>
            </>
          ) : null}
          {scene === 'explain' ? (
            <>
              <div className="lesson-brief-text" data-fixed-text>
                <h2>{step.title}</h2>
                <Markdown>{step.text}</Markdown>
              </div>
              <div className="lesson-actions">
                <button
                  type="button"
                  className="button button-primary"
                  onClick={() => {
                    setPlayAt(key);
                  }}>
                  {t('Continue')}
                </button>
              </div>
            </>
          ) : null}
          {scene === 'play' ? (
            <p>{step.check === null ? t('Press ▶ Run to see it work.') : t('Write your answer and press ▶ Run.')}</p>
          ) : null}
          {scene === 'result' ? (
            <>
              {lesson.isOnStepFile ? <p>{t('Look at the result up there.')}</p> : null}
              <LessonBrief
                step={step}
                verdict={lesson.verdict}
                isDone={lesson.isDone}
                isLastStep={lesson.isLastStep}
                isOnStepFile={lesson.isOnStepFile}
                onNext={lesson.goToNext}
                onBack={lesson.backToStep}
                onStartOver={lesson.startOver}
                onShowSolution={lesson.showSolution}
              />
            </>
          ) : null}
        </section>
        <div className="cat-bird">
          <CatArt pose={pose} />
        </div>
      </div>
      {stoneButton}
    </>
  );
};
