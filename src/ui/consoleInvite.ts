export const REPOSITORY_URL = 'https://github.com/gabrielogregorio/safira';

const TITLE_STYLE = 'color: #0a5cab; font-size: 22px; font-weight: 700;';
const TEXT_STYLE = 'color: #1f8fe0; font-size: 14px;';

// Whoever opens the browser tools finds this in the console. Nothing about it shows on the page.
export const printConsoleInvite = (title: string, text: string): void => {
  console.log(`%c${title}\n%c${text}\n${REPOSITORY_URL}`, TITLE_STYLE, TEXT_STYLE);
};
