import { useEffect, useRef, useState } from 'react';
import { useTranslation } from '@/i18n/i18n';
import { soundPlayer } from '@/ui/sound/sounds';
import type { TerminalBuffer } from '@/ui/terminalBuffer';

interface TerminalProps {
  buffer: TerminalBuffer;
  footer: string | null;
  isWaitingInput: boolean;
  onSubmitInput: (text: string) => void;
}

const TERMINAL_TYPING_RATES = [1, 0.9, 1.08, 0.95];

export const Terminal = ({ buffer, footer, isWaitingInput, onSubmitInput }: TerminalProps) => {
  const t = useTranslation();
  const typingStep = useRef(0);
  const [text, setText] = useState('');
  const logRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    logRef.current?.scrollTo({ top: logRef.current.scrollHeight });
  }, [buffer, footer]);

  useEffect(() => {
    if (isWaitingInput) {
      inputRef.current?.focus();
    }
  }, [isWaitingInput]);

  return (
    <section className="terminal" aria-label={t('Terminal')}>
      <div ref={logRef} className="terminal-log" role="log" aria-live="polite" tabIndex={0}>
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
