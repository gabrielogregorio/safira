const PlusMark = ({ x, y }: { x: number; y: number }) => (
  <path
    d={`M${x} ${y - 3.5}v7M${x - 3.5} ${y}h7`}
    className="aero-plus"
    strokeWidth="2.2"
    strokeLinecap="round"
    fill="none"
  />
);

export const NewFileIcon = () => (
  <svg className="aero-icon" viewBox="0 0 24 24" aria-hidden="true">
    <path d="M6 2h8.5L20 7.5V20a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2Z" fill="currentColor" />
    <path d="M14.5 2v5.5H20Z" fill="#9fd0ff" />
    <PlusMark x={12} y={15} />
  </svg>
);

export const NewFolderIcon = () => (
  <svg className="aero-icon" viewBox="0 0 24 24" aria-hidden="true">
    <path
      d="M2.5 6.5a2 2 0 0 1 2-2h4.8l2.2 2.6h8a2 2 0 0 1 2 2V18a2 2 0 0 1-2 2h-15a2 2 0 0 1-2-2Z"
      fill="currentColor"
    />
    <PlusMark x={12} y={13.5} />
  </svg>
);

export const PlayIcon = () => (
  <svg className="aero-icon" viewBox="0 0 24 24" aria-hidden="true">
    <path
      d="M7 4.6v14.8a1.2 1.2 0 0 0 1.85 1l11.2-7.4a1.2 1.2 0 0 0 0-2L8.85 3.6A1.2 1.2 0 0 0 7 4.6Z"
      fill="currentColor"
    />
  </svg>
);

export const StopIcon = () => (
  <svg className="aero-icon" viewBox="0 0 24 24" aria-hidden="true">
    <rect x="5" y="5" width="14" height="14" rx="2.6" fill="currentColor" />
  </svg>
);

export const CloseIcon = () => (
  <svg className="aero-icon" viewBox="0 0 24 24" aria-hidden="true">
    <path
      d="M6.5 6.5l11 11M17.5 6.5l-11 11"
      stroke="currentColor"
      strokeWidth="3.4"
      strokeLinecap="round"
      fill="none"
    />
  </svg>
);

export const BackIcon = () => (
  <svg className="aero-icon" viewBox="0 0 24 24" aria-hidden="true">
    <rect x="4.5" y="5" width="3" height="14" rx="1.2" fill="currentColor" />
    <path
      d="M19.5 6.4v11.2a1 1 0 0 1-1.55.84L9.6 12.84a1 1 0 0 1 0-1.68l8.35-5.6a1 1 0 0 1 1.55.84Z"
      fill="currentColor"
    />
  </svg>
);
