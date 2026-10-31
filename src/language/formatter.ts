const INDENT = '    ';

export const formatCode = (code: string): string => {
  let depth = 0;
  const lines: string[] = [];

  for (const rawLine of code.split('\n')) {
    const line = rawLine.trim();

    if (line.includes('{')) {
      lines.push(INDENT.repeat(depth) + line);
      depth += line.includes('}') ? 0 : 1;
    } else {
      if (line.includes('}')) {
        depth = Math.max(depth - 1, 0);
      }

      lines.push(INDENT.repeat(depth) + line);
    }
  }

  return lines.join('\n');
};
