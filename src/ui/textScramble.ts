const SCRAMBLE_CHARACTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789#%&@$*+=<>/?';
const SCRAMBLE_IDEOGRAPHS = 'アカサタナハマヤラワンあいうえお光水空語字文安明星海風雲月火木金土';
const IDEOGRAPH = /[\u3040-\u30ff\u3400-\u9fff]/;
const SCRAMBLE_MILLISECONDS = 700;
const MAXIMUM_TEXT_NODES = 500;
const IGNORED_ELEMENTS = '.cm-editor, .terminal-log, .inspector-table, pre, script, style, svg';
const FIXED_OR_TRANSLATED = '[data-fixed-text], [data-translated]';

export const randomCharacter = (): string =>
  SCRAMBLE_CHARACTERS.charAt(Math.floor(Math.random() * SCRAMBLE_CHARACTERS.length));

// Ideographs are twice as wide as Latin letters, so they scramble among themselves to keep the layout still.
export const randomCharacterLike = (character: string): string =>
  IDEOGRAPH.test(character)
    ? SCRAMBLE_IDEOGRAPHS.charAt(Math.floor(Math.random() * SCRAMBLE_IDEOGRAPHS.length))
    : randomCharacter();

export const scrambleFrame = (
  text: string,
  progress: number,
  pick: (character: string) => string = randomCharacterLike,
): string =>
  [...text]
    .map((character, index) => {
      const isRevealed = index / text.length < progress;

      return isRevealed || character.trim() === '' ? character : pick(character);
    })
    .join('');

// Names people chose and pt-BR content never change with the language, so their letters stay still.
const isFixedText = (element: Element): boolean =>
  element.closest(FIXED_OR_TRANSLATED)?.hasAttribute('data-fixed-text') === true;

export const collectTextNodes = (root: Node): Text[] => {
  const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, {
    acceptNode: (node) => {
      const isBlank = (node.nodeValue ?? '').trim() === '';
      const parent = node.parentElement;
      const isIgnored = parent === null || parent.closest(IGNORED_ELEMENTS) !== null || isFixedText(parent);

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
  const targets = collectTextNodes(root).map((node) => {
    const finalText = node.nodeValue ?? '';

    return { node, finalText, drawnText: finalText };
  });
  let startedAt: number | null = null;
  let frame = 0;

  // React may rewrite a node during the animation; that text is newer, so it is never overwritten.
  const drawEach = (textOf: (finalText: string) => string): void => {
    for (const target of targets) {
      if (target.node.nodeValue === target.drawnText) {
        target.drawnText = textOf(target.finalText);
        target.node.nodeValue = target.drawnText;
      }
    }
  };

  const restore = (): void => {
    drawEach((finalText) => finalText);
  };

  const draw = (now: number): void => {
    // Counted from the first frame: a slow page may take longer than the animation to paint it.
    startedAt ??= now;

    const progress = (now - startedAt) / SCRAMBLE_MILLISECONDS;

    if (progress >= 1) {
      restore();

      return;
    }

    drawEach((finalText) => scrambleFrame(finalText, progress));
    frame = requestAnimationFrame(draw);
  };

  // Scrambled right away, so that the new text never flashes before the animation.
  drawEach((finalText) => scrambleFrame(finalText, 0));
  frame = requestAnimationFrame(draw);

  return () => {
    cancelAnimationFrame(frame);
    restore();
  };
};
