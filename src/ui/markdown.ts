export type MarkdownBlock =
  | { kind: 'heading'; level: 1 | 2 | 3; text: string }
  | { kind: 'paragraph'; text: string }
  | { kind: 'code'; text: string };

const FENCE = '```';
const HEADING_PATTERN = /^(#{1,3}) (\S.*)$/;

export const parseMarkdown = (text: string): MarkdownBlock[] => {
  const blocks: MarkdownBlock[] = [];
  let code: string[] | null = null;

  for (const line of text.split('\n')) {
    const heading = HEADING_PATTERN.exec(line);

    if (line.trim().startsWith(FENCE)) {
      if (code !== null) {
        blocks.push({ kind: 'code', text: code.join('\n') });
      }

      code = code === null ? [] : null;
    } else if (code !== null) {
      code.push(line);
    } else if (heading !== null) {
      const level = heading[1].length as 1 | 2 | 3;
      blocks.push({ kind: 'heading', level, text: heading[2] });
    } else if (line.trim() !== '') {
      blocks.push({ kind: 'paragraph', text: line.replace(/\*\*/g, '').trim() });
    }
  }

  return blocks;
};
