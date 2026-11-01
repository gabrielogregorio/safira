import type { JSX } from 'react';
import { useCallback, useEffect, useLayoutEffect, useRef, useState } from 'react';
import Markdown from 'react-markdown';
import { useTranslation } from '@/i18n/i18n';
import { stepKey } from '@/lessons/lessonPlace';
import type { LessonMode } from '@/ui/hooks/useLessonMode';
import { storageKey } from '@/settings/storageKey';
import { prefersMotion } from '@/ui/motion';
import { soundPlayer } from '@/ui/sound/sounds';
import { LessonBrief } from './LessonBrief';
import { useTypedText } from './TypedText';

const MET_KEY = storageKey('cat.met');
const CAT_SIZE = 96;
const EDGE_MARGIN = 12;
const PANIC_RATE = 1.6;
const DRAG_START_PIXELS = 4;
const PHONE_WIDTH = 768;
const PHONE_BOTTOM_ROOM = 64;
const HAND_HEIGHT = 0.66;
const POINT_REACH = 140;
const HALF_TURN = 180;
const LIGHT_DELAY_MILLISECONDS = 180;
const HALF = 0.5;
const READ_INDENT = 24;
const READ_GAP = 38;
const ANGRY_RATE = 0.7;
const GOODBYE_MILLISECONDS = 2500;
const LEAVING_MILLISECONDS = 900;
const MOST_DRIFT_X = 46;
const MOST_DRIFT_Y = 36;
const SHORTEST_TRIP_MILLISECONDS = 1500;
const TRIP_VARIATION_MILLISECONDS = 750;

/** 0 is the top of the code field and 1 the bottom. */
// He stays in the upper part, with the balloon growing down, so the first lines of code stay in sight.
const HEIGHT_IN_FIELD: Record<Scene, number> = {
  intro: 0.2,
  read: 0.2,
  write: 0.2,

  play: 0.08,
  input: 0.08,
  result: 0.3,
  farewell: 0.08,
};

export interface Trip {
  driftX: number;
  driftY: number;
  milliseconds: number;
}

type Scene = 'intro' | 'read' | 'play' | 'write' | 'input' | 'result' | 'farewell';

const HOME_FIELD = '.code-editor';

const TARGETS: Record<Scene, string> = {
  intro: '.cm-content',
  read: '.cm-line',
  write: '.cm-line',
  play: '.aero-button-run',
  input: '.terminal-input',
  farewell: '.menubar-trigger:nth-child(3)',
  result: '[role="log"]',
};

// While typing, a lone backtick would show up as a stray mark until its pair arrives.
const hideOpenCode = (text: string): string => {
  const marks = text.split('`').length - 1;

  return marks % 2 === 0 ? text : text.slice(0, text.lastIndexOf('`')) + text.slice(text.lastIndexOf('`') + 1);
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
      <rect x="116" y="65" width="32" height="10" rx="5" />
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
    <g className="cat-ears" stroke="#24527e" strokeWidth="1.2">
      <ellipse cx="45" cy="0" rx="9" ry="27" fill="url(#cat-fur)" transform="rotate(-9 45 22)" />
      <ellipse cx="45" cy="1" rx="4.4" ry="19" fill="#2f7fc4" stroke="none" transform="rotate(-9 45 22)" />
      <path d="M71 18 C70 -4 74 -20 84 -24 C92 -22 92 -6 83 4 C86 8 84 14 83 20 Z" fill="url(#cat-fur)" />
      <path d="M76 12 C76 -4 78 -14 83 -18 C87 -14 86 -6 80 2 Z" fill="#2f7fc4" stroke="none" />
    </g>
    <ellipse cx="60" cy="38" rx="27" ry="23" fill="url(#cat-fur)" stroke="#24527e" strokeWidth="1.2" />
    {isUpset ? (
      <g fill="none" stroke="#0e2a46" strokeWidth="2.4" strokeLinecap="round">
        <path d="M42 40 q6 5 12 0" />
        <path d="M66 40 q6 5 12 0" />
        <path d="M50 54 q10 -7 20 0" />
      </g>
    ) : (
      <g>
        <ellipse cx="48" cy="38" rx="6" ry="4.6" fill="#f2ffd9" />
        <ellipse cx="72" cy="38" rx="6" ry="4.6" fill="#f2ffd9" />
        <ellipse cx="50" cy="38" rx="1.5" ry="4.2" fill="#10202e" />
        <ellipse cx="74" cy="38" rx="1.5" ry="4.2" fill="#10202e" />
        <path d="M41 36 L55 34 L55 32 L41 31 Z" fill="#3f93d8" />
        <path d="M65 34 L79 36 L79 31 L65 32 Z" fill="#3f93d8" />
        <path d="M41 33 L55 37M79 33 L65 37" stroke="#0e2a46" strokeWidth="2.2" strokeLinecap="round" />
        <path d="M55 54 h10" fill="none" stroke="#0e2a46" strokeWidth="1.8" strokeLinecap="round" />
      </g>
    )}
    <path d="M57.5 47 h5 l-2.5 2.6 Z" fill="#20384f" />
    <g stroke="#0e2a46" strokeWidth="1" strokeLinecap="round" opacity="0.65">
      <path d="M36 46 L22 42M36 50 L22 52M84 46 L98 42M84 50 L98 52" />
    </g>
    <ellipse cx="60" cy="24" rx="17" ry="6" fill="#ffffff" fillOpacity="0.5" />
  </g>
);

const SAUCER_LIGHTS = [22, 40, 58, 76, 94];

// He has no feet: the body sits in an alien saucer that keeps him floating.
const Saucer = () => (
  <g>
    <path className="cat-beam" d="M38 112 L22 134 H94 L78 112 Z" fill="url(#cat-beam)" />
    <ellipse cx="58" cy="107" rx="46" ry="12" fill="url(#cat-saucer)" stroke="#24527e" strokeWidth="1.2" />
    <ellipse cx="58" cy="102" rx="34" ry="6" fill="#ffffff" fillOpacity="0.55" />
    {SAUCER_LIGHTS.map((x, index) => (
      <circle
        key={x}
        className="cat-saucer-light"
        cx={x}
        cy={index === 0 || index === SAUCER_LIGHTS.length - 1 ? 108 : 112}
        r="3"
        fill="#7dff9b"
        stroke="#1d8f55"
        strokeWidth="0.8"
        style={{ animationDelay: `${String(index * LIGHT_DELAY_MILLISECONDS)}ms` }}
      />
    ))}
  </g>
);

const CatArt = ({ pose }: { pose: Pose }) => {
  const Hand = HANDS[pose];

  return (
    <svg viewBox="0 0 120 120" aria-hidden="true">
      <defs>
        <linearGradient id="cat-saucer" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stopColor="#f4fbff" />
          <stop offset="50%" stopColor="#a9c6dc" />
          <stop offset="100%" stopColor="#4f7696" />
        </linearGradient>
        <linearGradient id="cat-beam" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stopColor="#7dff9b" stopOpacity="0.6" />
          <stop offset="100%" stopColor="#7dff9b" stopOpacity="0" />
        </linearGradient>
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
      <ellipse cx="58" cy="94" rx="13" ry="13" fill="#cfeaf9" fillOpacity="0.55" />
      <Saucer />
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
  isWaitingInput: boolean;
  onAbandon: () => void;
}

interface Spot {
  x: number;
  y: number;
}

/** A trip never repeats exactly: the arrival and the speed change a little each time. */
export const planTrip = (random: () => number = Math.random): Trip => ({
  driftX: -random() * MOST_DRIFT_X,
  driftY: (random() - HALF) * MOST_DRIFT_Y,
  milliseconds: SHORTEST_TRIP_MILLISECONDS + random() * TRIP_VARIATION_MILLISECONDS,
});

// He lives inside the code field, so he never covers the output or an error, and only points at them.
const whereToStand = (element: HTMLElement, scene: Scene, trip: Trip): Spot | null => {
  if (window.innerWidth <= PHONE_WIDTH) {
    return { x: window.innerWidth - CAT_SIZE - EDGE_MARGIN, y: window.innerHeight - CAT_SIZE - PHONE_BOTTOM_ROOM };
  }

  const box = document.querySelector(HOME_FIELD)?.getBoundingClientRect();

  if (box === undefined) {
    return null;
  }

  element.style.setProperty('--cat-room-width', `${String(box.width - CAT_SIZE - EDGE_MARGIN * 2 - MOST_DRIFT_X)}px`);
  const lowest = box.bottom - CAT_SIZE - EDGE_MARGIN;
  const highest = box.top + EDGE_MARGIN;
  const y = Math.min(lowest, Math.max(highest, highest + (lowest - highest) * HEIGHT_IN_FIELD[scene] + trip.driftY));
  element.style.setProperty('--cat-room-height', `${String(box.bottom - y - EDGE_MARGIN)}px`);

  // Showing the code, he flies right under its last line, however short the code is.
  const lastLine = [...document.querySelectorAll('.cm-line')].at(-1)?.getBoundingClientRect();

  if (scene === 'read' && lastLine !== undefined) {
    return { x: lastLine.left + READ_INDENT, y: Math.min(lowest, lastLine.bottom + READ_GAP) };
  }

  return { x: box.right - CAT_SIZE - EDGE_MARGIN + trip.driftX, y };
};

// He turns to the target, and the arm goes to the angle that leaves the finger on it.
const lookAtTarget = (element: HTMLElement, scene: Scene, spot: Spot): void => {
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

const placeOnScreen = (element: HTMLElement, scene: Scene, trip: Trip): void => {
  const spot = whereToStand(element, scene, trip);

  if (spot !== null) {
    element.style.setProperty('--cat-trip', `${String(Math.round(trip.milliseconds))}ms`);
    element.style.transform = `translate(${String(spot.x)}px, ${String(spot.y)}px)`;
    lookAtTarget(element, scene, spot);
  }
};

// He runs along the line from the stone to him, far enough to leave the screen.
// Called on every move of the stone, so the transition turns him around in the middle of the run.
const fleeFrom = (element: HTMLElement, stone: DOMRect): void => {
  const cat = element.getBoundingClientRect();
  const distanceX = cat.left + CAT_SIZE / 2 - (stone.left + stone.width / 2) || 1;
  const distanceY = cat.top + CAT_SIZE / 2 - (stone.top + stone.height / 2);
  const length = Math.hypot(distanceX, distanceY);
  const reach = Math.hypot(window.innerWidth, window.innerHeight);
  const x = cat.left + (distanceX / length) * reach;
  const y = cat.top + (distanceY / length) * reach;

  element.dataset['facing'] = distanceX < 0 ? 'left' : 'right';
  element.style.transform = `translate(${String(x)}px, ${String(y)}px)`;
};

export const ProfessorCat = ({ lesson, hasError, isWaitingInput, onAbandon }: ProfessorCatProps) => {
  const t = useTranslation();
  const root = useRef<HTMLDivElement>(null);
  const stone = useRef<HTMLButtonElement>(null);
  const pressedAt = useRef<{ x: number; y: number } | null>(null);
  const [isHoldingStone, setIsHoldingStone] = useState(false);
  const [hasMet, setHasMet] = useState(() => readFlag(MET_KEY));
  const key = stepKey(lesson.place);
  const [codeReadAt, setCodeReadAt] = useState<string | null>(null);

  const scene = ((): Scene => {
    if (isWaitingInput) {
      return 'input';
    }

    if (lesson.isLastStep && lesson.isDone && lesson.hasRun) {
      return 'farewell';
    }

    if (!hasMet && !lesson.hasRun) {
      return 'intro';
    }

    if (lesson.hasRun || !lesson.isOnStepFile) {
      return 'result';
    }

    if (lesson.step?.check !== null) {
      return 'write';
    }

    // The code comes first: the play only comes up after he points at what will run.
    return codeReadAt === key ? 'play' : 'read';
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

  const trip = useRef<Trip>(planTrip());
  const tripScene = useRef(scene);

  const reposition = useCallback(() => {
    if (root.current !== null && !root.current.classList.contains('cat-fleeing')) {
      if (tripScene.current !== scene) {
        tripScene.current = scene;
        trip.current = planTrip();
      }

      placeOnScreen(root.current, scene, trip.current);
    }
  }, [scene]);

  // The first placement is not a trip: he appears there instead of flying in from the corner of the page.
  const hasArrived = useRef(false);

  useLayoutEffect(() => {
    if (root.current === null) {
      return;
    }

    root.current.classList.toggle('cat-just-arrived', !hasArrived.current);
    reposition();

    if (!hasArrived.current) {
      hasArrived.current = true;
      root.current.getBoundingClientRect();
      root.current.classList.remove('cat-just-arrived');
    }
  });

  useEffect(() => {
    window.addEventListener('resize', reposition);

    return () => {
      window.removeEventListener('resize', reposition);
    };
  }, [reposition]);

  const isHere = !isHoldingStone;

  // The button lives in the toolbar, so the page carries the signal that lights it up.
  const isAskingForRun = isHere && scene === 'play';

  useEffect(() => {
    if (!isAskingForRun) {
      return undefined;
    }

    document.documentElement.dataset['spotlight'] = 'run';

    return () => {
      delete document.documentElement.dataset['spotlight'];
    };
  }, [isAskingForRun]);

  // He talks only after the saucer stops. Before that the balloon does not exist.
  const stage = `${key}:${scene}`;
  const [settledStage, setSettledStage] = useState(stage);
  const isSettled = settledStage === stage || !prefersMotion();

  useEffect(() => {
    if (isSettled) {
      return undefined;
    }

    const timer = setTimeout(() => {
      setSettledStage(stage);
    }, trip.current.milliseconds);

    return () => {
      clearTimeout(timer);
    };
  }, [isSettled, stage]);

  useEffect(() => {
    if (isHere && isSettled) {
      void soundPlayer.play('catMeow', scene === 'farewell' ? ANGRY_RATE : 1);
    }
  }, [isHere, isSettled, scene, stage]);

  const speech = ((): string => {
    if (!isSettled || lesson.step === undefined) {
      return '';
    }

    switch (scene) {
      case 'intro':
        return t('Meow! I am a therian, and I will teach you to program.');
      case 'read':
        return t('Read this code.');
      case 'play':
        return t('Press ▶');
      case 'write':
        return t('Write your answer and press ▶ Run.');
      case 'input':
        return t('Type your answer here and press Enter.');
      case 'farewell':
        return t('Enough! I taught you too much already. Figure it out with the Examples menu. Goodbye, forever.');
      case 'result':
        return lesson.isOnStepFile ? t('Look at the result over there.') : '';
    }
  })();
  const typed = useTypedText(speech);
  const [isLeaving, setIsLeaving] = useState(false);
  const hasSaidGoodbye = scene === 'farewell' && isSettled && typed.isDone;

  useEffect(() => {
    if (!hasSaidGoodbye) {
      return undefined;
    }

    const timer = setTimeout(
      () => {
        setIsLeaving(true);
      },
      prefersMotion() ? GOODBYE_MILLISECONDS : 0,
    );

    return () => {
      clearTimeout(timer);
    };
  }, [hasSaidGoodbye]);

  useEffect(() => {
    if (!isLeaving) {
      return undefined;
    }

    if (root.current !== null) {
      root.current.style.transform = `translate(${String(window.innerWidth + CAT_SIZE)}px, ${String(-CAT_SIZE)}px)`;
    }

    const timer = setTimeout(onAbandon, prefersMotion() ? LEAVING_MILLISECONDS : 0);

    return () => {
      clearTimeout(timer);
    };
  }, [isLeaving, onAbandon]);

  if (lesson.step === undefined) {
    return null;
  }

  const runFromStone = (): void => {
    fleeFrom(root.current as HTMLDivElement, (stone.current as HTMLButtonElement).getBoundingClientRect());
  };

  const pickUpStone = (): void => {
    runFromStone();
    void soundPlayer.play('catMeow', PANIC_RATE);
    setIsHoldingStone(true);
  };

  const dropStone = (): void => {
    pressedAt.current = null;
    setIsHoldingStone(false);

    (stone.current as HTMLButtonElement).style.transform = '';
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

          if (isHoldingStone) {
            runFromStone();
          } else {
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

  if (isHoldingStone || isLeaving) {
    return (
      <>
        <div ref={root} className="cat cat-fleeing" data-pose="wave">
          <div className="cat-bird">
            <CatArt pose="wave" />
          </div>
        </div>
        {isLeaving ? null : stoneButton}
      </>
    );
  }

  const { step } = lesson;

  return (
    <>
      <div ref={root} className={`cat cat-at-${scene}`} data-pose={pose}>
        {isSettled ? (
          <section className="cat-bubble" aria-label={t('The cat')} aria-live="polite">
            <div className="lesson-brief-text" data-fixed-text aria-hidden={typed.isDone ? undefined : true}>
              <Markdown>{hideOpenCode(typed.shown)}</Markdown>
            </div>
            {typed.isDone ? null : (
              <>
                <div className="visually-hidden" data-fixed-text>
                  <Markdown>{speech}</Markdown>
                </div>
                <div className="lesson-actions">
                  <button type="button" className="button" onClick={typed.finish}>
                    {t('Show it all')}
                  </button>
                </div>
              </>
            )}
            {scene === 'intro' && typed.isDone ? (
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
            ) : null}
            {scene === 'read' && typed.isDone ? (
              <div className="lesson-actions">
                <button
                  type="button"
                  className="button button-primary"
                  onClick={() => {
                    setCodeReadAt(key);
                  }}>
                  {t('Continue')}
                </button>
              </div>
            ) : null}
            {scene === 'result' && typed.isDone ? (
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
            ) : null}
          </section>
        ) : null}
        <div className="cat-bird">
          <CatArt pose={pose} />
        </div>
      </div>
      {stoneButton}
    </>
  );
};
