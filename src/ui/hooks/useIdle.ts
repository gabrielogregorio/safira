import { useEffect, useState } from 'react';

const IDLE_MILLISECONDS = 3000;

// For screens that can be a wallpaper: the close button leaves when nobody is moving the mouse.
export const useIdle = (): boolean => {
  const [isIdle, setIsIdle] = useState(false);

  useEffect(() => {
    let timer = setTimeout(setIsIdle, IDLE_MILLISECONDS, true);

    const wake = (): void => {
      setIsIdle(false);
      clearTimeout(timer);
      timer = setTimeout(setIsIdle, IDLE_MILLISECONDS, true);
    };

    window.addEventListener('pointermove', wake);
    window.addEventListener('keydown', wake);

    return () => {
      clearTimeout(timer);
      window.removeEventListener('pointermove', wake);
      window.removeEventListener('keydown', wake);
    };
  }, []);

  return isIdle;
};
