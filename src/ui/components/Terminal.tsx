import type { KeyboardEvent as ReactKeyboardEvent } from 'react';
import { useEffect, useRef, useState } from 'react';
import { useTranslation } from '@/i18n/i18n';
import { normalizeKey } from '@/language/keys';
import { soundPlayer } from '@/ui/sound/sounds';
import type { TerminalBuffer } from '@/ui/terminalBuffer';
import { MaximizeIcon, MinimizeIcon } from './AeroIcons';

interface TerminalProps {
  buffer: TerminalBuffer;
  footer: string | null;
  isWaitingInput: boolean;
  onSubmitInput: (text: string) => void;
  isListeningKeys?: boolean;
  onKey?: (key: string, isDown: boolean) => void;
  onKeysLost?: () => void;
}

interface PadKey {
  key: string;
  mark: string;
  label: string;
}

const TERMINAL_TYPING_RATES = [1, 0.9, 1.08, 0.95];

const doNothing = (): void => undefined;

export const Terminal = ({
  buffer,
  footer,
  isWaitingInput,
  onSubmitInput,
  isListeningKeys = false,
  onKey = doNothing,
  onKeysLost = doNothing,
}: TerminalProps) => {
  const t = useTranslation();
  const typingStep = useRef(0);
  const [text, setText] = useState('');
  const logRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);
  const [hasFocus, setHasFocus] = useState(false);
  const [isMaximized, setIsMaximized] = useState(false);
  const padKeys: PadKey[] = [
    { key: 'arrowup', mark: '↑', label: t('Up') },
    { key: 'arrowleft', mark: '←', label: t('Left') },
    { key: 'arrowdown', mark: '↓', label: t('Down') },
    { key: 'arrowright', mark: '→', label: t('Right') },
    { key: 'enter', mark: '⏎', label: 'Enter' },
  ];

  useEffect(() => {
    logRef.current?.scrollTo({ top: logRef.current.scrollHeight });
  }, [buffer, footer]);

  useEffect(() => {
    if (isWaitingInput) {
      inputRef.current?.focus();
    }
  }, [isWaitingInput]);

  // Only the program area hears the keys, so typing anywhere else stays with the page.
  const forwardKey = (event: ReactKeyboardEvent, isDown: boolean): void => {
    const key = normalizeKey(event.key);

    if (isListeningKeys && key !== null && !event.ctrlKey && !event.metaKey) {
      event.preventDefault();
      onKey(key, isDown);
    }
  };

  return (
    <section className={isMaximized ? 'terminal terminal-maximized' : 'terminal'} aria-label={t('Terminal')}>
      <button
        type="button"
        className="aero-button terminal-size"
        aria-label={isMaximized ? t('Minimize the program') : t('Maximize the program')}
        title={isMaximized ? t('Minimize the program') : t('Maximize the program')}
        onClick={() => {
          setIsMaximized(!isMaximized);
          logRef.current?.focus();
        }}>
        {isMaximized ? <MinimizeIcon /> : <MaximizeIcon />}
      </button>
      {/* The log takes the focus by design: it is where a running program hears the keys. */}
      {/* eslint-disable-next-line jsx-a11y/no-noninteractive-element-interactions */}
      <div
        ref={logRef}
        className="terminal-log"
        role="log"
        aria-live="polite"
        tabIndex={0}
        onFocus={() => {
          setHasFocus(true);
        }}
        onBlur={() => {
          setHasFocus(false);
          onKeysLost();
        }}
        onKeyDown={(event) => {
          forwardKey(event, true);
        }}
        onKeyUp={(event) => {
          forwardKey(event, false);
        }}>
        {buffer.lines.map((segments, lineIndex) => (
          <div key={lineIndex} className="terminal-line">
            {segments.map((segment, segmentIndex) => (
              <span key={segmentIndex} style={segment.color === '' ? undefined : { color: segment.color }}>
                {segment.text}
              </span>
            ))}
          </div>
        ))}
        {footer === null ? null : <div className="terminal-footer">{footer}</div>}
      </div>
      {isListeningKeys && !hasFocus ? (
        <button
          type="button"
          className="terminal-keys-hint"
          onClick={() => {
            logRef.current?.focus();
          }}>
          {t('Click here to use the keyboard')}
        </button>
      ) : null}
      {isListeningKeys ? (
        <div className="key-pad">
          {padKeys.map(({ key, mark, label }) => (
            <button
              key={key}
              type="button"
              className={`key-pad-button key-pad-${key}`}
              aria-label={label}
              onPointerDown={() => {
                onKey(key, true);
              }}
              onPointerUp={() => {
                onKey(key, false);
              }}
              onPointerCancel={() => {
                onKey(key, false);
              }}>
              {mark}
            </button>
          ))}
        </div>
      ) : null}
      {isWaitingInput ? (
        <form
          className="terminal-input"
          onSubmit={(event) => {
            event.preventDefault();
            void soundPlayer.play('terminalSend');
            onSubmitInput(text);
            setText('');
          }}>
          <input
            ref={inputRef}
            data-sound="terminalFocus"
            aria-label={t('Type here and press Enter')}
            placeholder={t('Type here and press Enter')}
            value={text}
            onChange={(event) => {
              typingStep.current = (typingStep.current + 1) % TERMINAL_TYPING_RATES.length;
              void soundPlayer.play('terminalTyping', TERMINAL_TYPING_RATES[typingStep.current]);
              setText(event.target.value);
            }}
          />
          <button type="submit" className="button button-primary">
            {t('Send')}
          </button>
        </form>
      ) : null}
    </section>
  );
};
