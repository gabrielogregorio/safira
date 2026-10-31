import * as Dialog from '@radix-ui/react-dialog';
import type { ReactNode } from 'react';
import { useTranslation } from '@/i18n/i18n';

interface ModalProps {
  title: string;
  children: ReactNode;
  onClose: () => void;
}

const ZOOM_RECTANGLES = [0, 1, 2, 3];

const focusMarkedElement = (event: Event): void => {
  const content = event.currentTarget as HTMLElement;
  const target = content.querySelector<HTMLElement>('[data-autofocus]');

  if (target !== null) {
    event.preventDefault();
    target.focus();
  }
};

export const Modal = ({ title, children, onClose }: ModalProps) => {
  const t = useTranslation();

  return (
    <Dialog.Root
      open
      onOpenChange={(isOpen) => {
        if (!isOpen) {
          onClose();
        }
      }}>
      <Dialog.Portal>
        <Dialog.Overlay className="modal-backdrop">
          <div className="modal-zoom" aria-hidden="true">
            {ZOOM_RECTANGLES.map((rectangle) => (
              <span key={rectangle} />
            ))}
          </div>
          <Dialog.Content className="modal" aria-describedby={undefined} onOpenAutoFocus={focusMarkedElement}>
            <header className="modal-header">
              <Dialog.Title asChild>
                <h2>{title}</h2>
              </Dialog.Title>
              <Dialog.Close className="button">{t('Close')}</Dialog.Close>
            </header>
            <div className="modal-body">{children}</div>
          </Dialog.Content>
        </Dialog.Overlay>
      </Dialog.Portal>
    </Dialog.Root>
  );
};
