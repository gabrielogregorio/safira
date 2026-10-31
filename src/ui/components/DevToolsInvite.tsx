import devtools from 'devtools-detect';
import type { DevToolsEvent } from 'devtools-detect';
import { useEffect, useRef, useState } from 'react';
import { useTranslation } from '@/i18n/i18n';
import { CloseButton } from './CloseButton';

export const REPOSITORY_URL = 'https://github.com/gabrielogregorio/safira';

const CONSOLE_TITLE_STYLE = 'color: #0a5cab; font-size: 22px; font-weight: 700;';
const CONSOLE_TEXT_STYLE = 'color: #1f8fe0; font-size: 14px;';

// The detector only sees docked tools, by the size of the window. Who undocks them still finds this in the console.
const printInvite = (title: string, text: string): void => {
  console.log(`%c${title}\n%c${text}\n${REPOSITORY_URL}`, CONSOLE_TITLE_STYLE, CONSOLE_TEXT_STYLE);
};

export const DevToolsInvite = () => {
  const t = useTranslation();
  const [isVisible, setIsVisible] = useState(devtools.isOpen);
  const wasDismissed = useRef(false);
  const title = t('Curious about what is inside?');
  const text = t('Safira is open source. Get the repository, run it on your computer and change whatever you want.');

  useEffect(() => {
    printInvite(title, text);
    // Once per visit: changing the language must not print it again.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  useEffect(() => {
    const showInvite = (event: DevToolsEvent): void => {
      if (event.detail.isOpen && !wasDismissed.current) {
        setIsVisible(true);
      }
    };

    window.addEventListener('devtoolschange', showInvite);

    return () => {
      window.removeEventListener('devtoolschange', showInvite);
    };
  }, []);

  if (!isVisible) {
    return null;
  }

  return (
    <aside className="devtools-invite" role="status">
      <div>
        <h2>{title}</h2>
        <p>{text}</p>
        <a className="button button-primary" href={REPOSITORY_URL} target="_blank" rel="noreferrer">
          {t('Open the repository')}
        </a>
      </div>
      <CloseButton
        onClick={() => {
          wasDismissed.current = true;
          setIsVisible(false);
        }}
      />
    </aside>
  );
};
