import type { ReactNode } from 'react';
import { useEffect, useRef } from 'react';
import { useTranslation } from '@/i18n/i18n';

interface ModalProps {
  title: string;
  children: ReactNode;
  onClose: () => void;
}

export const Modal = ({ title, children, onClose }: ModalProps) => {
  const t = useTranslation();
  const panelRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    panelRef.current?.focus();

    const closeOnEscape = (event: KeyboardEvent): void => {
      if (event.key === 'Escape') {
        onClose();
      }
    };

    document.addEventListener('keydown', closeOnEscape);

    return () => {
      document.removeEventListener('keydown', closeOnEscape);
    };
  }, [onClose]);

  return (
    <div className="modal-backdrop">
      <div ref={panelRef} className="modal" role="dialog" aria-modal="true" aria-label={title} tabIndex={-1}>
        <header className="modal-header">
          <h2>{title}</h2>
          <button type="button" className="button" onClick={onClose}>
            {t('Close')}
          </button>
        </header>
        <div className="modal-body">{children}</div>
      </div>
    </div>
  );
};
