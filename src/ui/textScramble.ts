const SCRAMBLE_CHARACTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789#%&@$*+=<>/?';
const SCRAMBLE_MILLISECONDS = 700;
const MAXIMUM_TEXT_NODES = 500;
const IGNORED_ELEMENTS = '.cm-editor, .terminal-log, .inspector-table, pre, script, style, svg';

export const randomCharacter = (): string =>
  SCRAMBLE_CHARACTERS.charAt(Math.floor(Math.random() * SCRAMBLE_CHARACTERS.length));

export const scrambleFrame = (text: string, progress: number, pick: () => string = randomCharacter): string =>
  [...text]
    .map((character, index) => {
      const isRevealed = index / text.length < progress;

      return isRevealed || character.trim() === '' ? character : pick();
    })
    .join('');

export const collectTextNodes = (root: Node): Text[] => {
  const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, {
    acceptNode: (node) => {
      const isBlank = (node.nodeValue ?? '').trim() === '';
      const isIgnored = node.parentElement?.closest(IGNORED_ELEMENTS) !== null;

      return isBlank || isIgnored ? NodeFilter.FILTER_REJECT : NodeFilter.FILTER_ACCEPT;
    },
  });
  const nodes: Text[] = [];

  while (walker.nextNode() !== null && nodes.length < MAXIMUM_TEXT_NODES) {
    nodes.push(walker.currentNode as Text);
  }

  return nodes;
};

export const scrambleDocument = (root: Node): (() => void) => {
  const targets = collectTextNodes(root).map((node) => ({ node, finalText: node.nodeValue ?? '' }));
  const startedAt = performance.now();
  let frame = 0;

  const restore = (): void => {
    for (const { node, finalText } of targets) {
      node.nodeValue = finalText;
    }
  };

  const draw = (now: number): void => {
    const progress = (now - startedAt) / SCRAMBLE_MILLISECONDS;

    if (progress >= 1) {
      restore();

      return;
    }

    for (const { node, finalText } of targets) {
      node.nodeValue = scrambleFrame(finalText, progress);
    }

    frame = requestAnimationFrame(draw);
  };

  frame = requestAnimationFrame(draw);

  return () => {
    cancelAnimationFrame(frame);
    restore();
  };
};
