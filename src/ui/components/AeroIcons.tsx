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

export const ProjectBadge = () => (
  <svg className="project-badge" viewBox="0 0 24 24" aria-hidden="true">
    <path d="M7 3h10l5 6.5L12 21 2 9.5Z" fill="#bfe9ff" />
    <path d="M7 3 12 9.5 17 3ZM2 9.5h20L12 21Z" fill="#ffffff" fillOpacity="0.55" />
  </svg>
);

export const TreeFileIcon = ({ isScript }: { isScript: boolean }) => (
  <svg className="tree-icon" viewBox="0 0 24 24" aria-hidden="true">
    <path d="M5 1.5h9.5L20 7v15.5H5Z" fill={isScript ? '#bfe6ff' : '#f7fbff'} stroke="#3f7fb8" strokeWidth="1" />
    <path d="M14.5 1.5V7H20Z" fill="#7cc4f5" stroke="#3f7fb8" strokeWidth="1" strokeLinejoin="round" />
    {isScript ? (
      <path d="M9 11h7l2.5 3-6 6-6-6Z" fill="#1f7fe0" stroke="#0a5cab" strokeWidth="0.8" />
    ) : (
      <path d="M8 11.5h9M8 14.5h9M8 17.5h6" stroke="#7fa6c8" strokeWidth="1.4" strokeLinecap="round" />
    )}
  </svg>
);

export const TreeFolderIcon = ({ isOpen }: { isOpen: boolean }) => (
  <svg className="tree-icon" viewBox="0 0 24 24" aria-hidden="true">
    <path
      d="M2 5.5a1.5 1.5 0 0 1 1.5-1.5h5.6l2.2 2.5h9.2A1.5 1.5 0 0 1 22 8v11H2Z"
      fill="#e0a324"
      stroke="#a8730f"
      strokeWidth="1"
    />
    {isOpen ? (
      <path d="M5.5 10H23l-3 9.5H2Z" fill="#ffe08a" stroke="#a8730f" strokeWidth="1" strokeLinejoin="round" />
    ) : (
      <path d="M2 9h20v10.5H2Z" fill="#ffd465" stroke="#a8730f" strokeWidth="1" />
    )}
    <path d={isOpen ? 'M6.5 11h15l-.6 2H5.6Z' : 'M3 10h18v3H3Z'} fill="#ffffff" fillOpacity="0.55" />
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

export const GitHubIcon = () => (
  <svg viewBox="0 0 16 16" aria-hidden="true">
    <path
      fill="currentColor"
      d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27s1.36.09 2 .27c1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.01 8.01 0 0 0 16 8c0-4.42-3.58-8-8-8z"
    />
  </svg>
);

export const WikiIcon = () => (
  <svg viewBox="0 0 24 24" aria-hidden="true">
    <path
      d="M12 6.5C10 5 7 4.5 3.5 5v13.5c3.5-.5 6.500 0 8.500 1.500 2-1.500 5-2 8.500-1.500V5C17 4.500 14 5 12 6.500zM12 6.500V20"
      fill="none"
      stroke="currentColor"
      strokeWidth="2.200"
      strokeLinecap="round"
      strokeLinejoin="round"
    />
  </svg>
);

export const MaximizeIcon = () => (
  <svg viewBox="0 0 24 24" aria-hidden="true">
    <path
      d="M4 9V4h5M15 4h5v5M20 15v5h-5M9 20H4v-5"
      fill="none"
      stroke="currentColor"
      strokeWidth="2.6"
      strokeLinecap="round"
      strokeLinejoin="round"
    />
  </svg>
);

export const MinimizeIcon = () => (
  <svg viewBox="0 0 24 24" aria-hidden="true">
    <path
      d="M9 4v5H4M20 9h-5V4M15 20v-5h5M4 15h5v5"
      fill="none"
      stroke="currentColor"
      strokeWidth="2.6"
      strokeLinecap="round"
      strokeLinejoin="round"
    />
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
