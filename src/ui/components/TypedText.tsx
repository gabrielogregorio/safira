import { useEffect, useState } from 'react';
import { prefersMotion } from '@/ui/motion';

const LETTER_MILLISECONDS = 24;

export interface TypedText {
  shown: string;
  isDone: boolean;
  finish: () => void;
}

const letterCount = (text: string): number => Array.from(text).length;

/** Reveals a text letter by letter. Without motion it arrives whole. */
export const useTypedText = (text: string): TypedText => {
  const [progress, setProgress] = useState({ text, letters: 0 });
  const isCurrent = progress.text === text;
  const letters = isCurrent ? progress.letters : 0;
  const total = letterCount(text);

  if (!isCurrent) {
    setProgress({ text, letters: 0 });
  }

  const isDone = letters >= total || !prefersMotion();

  useEffect(() => {
    if (isDone) {
      return undefined;
    }

    const timer = setInterval(() => {
      setProgress((current) => ({ ...current, letters: current.letters + 1 }));
    }, LETTER_MILLISECONDS);

    return () => {
      clearInterval(timer);
    };
  }, [isDone, text]);

  return {
    shown: isDone ? text : Array.from(text).slice(0, letters).join(''),
    isDone,
    finish: () => {
      setProgress({ text, letters: total });
    },
  };
};

interface TypedLineProps {
  text: string;
}

/** Screen readers get the whole sentence once, not one letter at a time. */
export const TypedLine = ({ text }: TypedLineProps) => {
  const { shown, isDone } = useTypedText(text);

  if (isDone) {
    return text;
  }

  return (
    <>
      <span aria-hidden="true">{shown}</span>
      <span className="visually-hidden">{text}</span>
    </>
  );
};
