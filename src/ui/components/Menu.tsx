import type { ReactNode } from 'react';

interface MenuProps {
  label: string;
  children: ReactNode;
}

interface MenuItemProps {
  label: string;
  disabled?: boolean;
  onSelect: () => void;
}

export const Menu = ({ label, children }: MenuProps) => (
  <details className="menu">
    <summary>{label}</summary>
    <div className="menu-items">{children}</div>
  </details>
);

export const MenuItem = ({ label, disabled = false, onSelect }: MenuItemProps) => (
  <button
    type="button"
    className="menu-item"
    disabled={disabled}
    onClick={(event) => {
      event.currentTarget.closest('details')?.removeAttribute('open');
      onSelect();
    }}>
    {label}
  </button>
);
