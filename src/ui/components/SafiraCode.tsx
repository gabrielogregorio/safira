import { useMemo } from 'react';
import { highlightCode } from '@/language/highlight';

interface SafiraCodeProps {
  code: string;
}

interface CodePiece {
  text: string;
  className: string | undefined;
}

export const splitHighlightedCode = (code: string): CodePiece[] => {
  const pieces: CodePiece[] = [];
  let position = 0;

  for (const { start, end, category } of highlightCode(code)) {
    if (start > position) {
      pieces.push({ text: code.slice(position, start), className: undefined });
    }

    pieces.push({ text: code.slice(start, end), className: `syntax-${category}` });
    position = end;
  }

  if (position < code.length) {
    pieces.push({ text: code.slice(position), className: undefined });
  }

  return pieces;
};

export const SafiraCode = ({ code }: SafiraCodeProps) => {
  const pieces = useMemo(() => splitHighlightedCode(code), [code]);

  return (
    <code>
      {pieces.map((piece, index) => (
        <span key={index} className={piece.className}>
          {piece.text}
        </span>
      ))}
    </code>
  );
};
