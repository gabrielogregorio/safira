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
    <path d="M2 5.5a1.5 1.5 0 0 1 1.5-1.5h5.6l2.2 2.5h9.2A1.5 1.5 0 0 1 22 8v11H2Z" fill="#e0a324" stroke="#a8730f" strokeWidth="1" />
    {isOpen ? (
      <path d="M5.5 10H23l-3 9.5H2Z" fill="#ffe08a" stroke="#a8730f" strokeWidth="1" strokeLinejoin="round" />
    ) : (
      <path d="M2 9h20v10.5H2Z" fill="#ffd465" stroke="#a8730f" strokeWidth="1" />
    )}
    <path d={isOpen ? 'M6.5 11h15l-.6 2H5.6Z' : 'M3 10h18v3H3Z'} fill="#ffffff" fillOpacity="0.55" />
  </svg>
);

export const CameraIcon = () => (
  <svg className="aero-icon" viewBox="0 0 24 24" aria-hidden="true">
    <path d="M8.5 5 10 3h4l1.5 2H20a2 2 0 0 1 2 2v11a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V7a2 2 0 0 1 2-2Z" fill="currentColor" />
    <circle cx="12" cy="12.5" r="4.6" fill="#9fd0ff" stroke="#ffffff" strokeWidth="1.6" />
  </svg>
);

export const OlderIcon = () => (
  <svg className="aero-icon" viewBox="0 0 24 24" aria-hidden="true">
    <path d="M15 4.5 7 12l8 7.5" fill="none" stroke="currentColor" strokeWidth="3.4" strokeLinecap="round" strokeLinejoin="round" />
  </svg>
);

export const NewerIcon = () => (
  <svg className="aero-icon" viewBox="0 0 24 24" aria-hidden="true">
    <path d="M9 4.5 17 12l-8 7.5" fill="none" stroke="currentColor" strokeWidth="3.4" strokeLinecap="round" strokeLinejoin="round" />
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
