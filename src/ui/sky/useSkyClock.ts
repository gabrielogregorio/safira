import { useCallback, useEffect, useRef, useState } from 'react';
import type { ThemeId } from '@/settings/settings';
import { phaseAt, phaseOfTheme, SKY_TICK_MILLISECONDS } from './skyClock';

// Time passes while the page is open and is never saved: a reload starts again from the chosen theme.
export const useSkyClock = (chosenTheme: ThemeId) => {
  const [phase, setPhase] = useState(() => phaseOfTheme(chosenTheme));
  const start = useRef({ theme: chosenTheme, time: 0 });

  useEffect(() => {
    start.current.time = Date.now();

    const timer = setInterval(() => {
      setPhase(phaseAt(start.current.theme, Date.now() - start.current.time));
    }, SKY_TICK_MILLISECONDS);

    return () => {
      clearInterval(timer);
    };
  }, []);

  const travelTo = useCallback((theme: ThemeId) => {
    start.current = { theme, time: Date.now() };
    setPhase(phaseOfTheme(theme));
  }, []);

  return { phase, travelTo };
};
