import * as Dialog from '@radix-ui/react-dialog';
import type { ReactNode } from 'react';
import { useCallback, useLayoutEffect, useRef } from 'react';
import { prefersMotion } from '@/ui/motion';
import { soundPlayer } from '@/ui/sound/sounds';
import { CloseButton } from './CloseButton';

interface ModalProps {
  title: string;
  children: ReactNode;
  onClose: () => void;
  isWide?: boolean;
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

const CLOSING_MILLISECONDS = 420;

const playClosingAnimation = (overlay: HTMLElement): void => {
  const ghost = overlay.cloneNode(true) as HTMLElement;
  ghost.classList.add('modal-closing');
  ghost.setAttribute('aria-hidden', 'true');
  ghost.removeAttribute('data-state');
  ghost.querySelector('[role="dialog"]')?.removeAttribute('role');
  document.body.append(ghost);
  setTimeout(() => {
    ghost.remove();
  }, CLOSING_MILLISECONDS);
};

export const Modal = ({ title, children, onClose, isWide = false }: ModalProps) => {
  const overlay = useRef<HTMLDivElement | null>(null);
  const keepOverlay = useCallback((node: HTMLDivElement | null) => {
    overlay.current = node ?? overlay.current;
  }, []);

  useLayoutEffect(() => {
    void soundPlayer.play('modalOpen');

    return () => {
      void soundPlayer.play('modalClose');

      if (overlay.current !== null && prefersMotion()) {
        playClosingAnimation(overlay.current);
      }
    };
  }, []);

  return (
    <Dialog.Root
      open
      onOpenChange={(isOpen) => {
        if (!isOpen) {
          onClose();
        }
      }}>
      <Dialog.Portal>
        <Dialog.Overlay ref={keepOverlay} className="modal-backdrop">
          <div className="modal-zoom" aria-hidden="true">
            {ZOOM_RECTANGLES.map((rectangle) => (
              <span key={rectangle} />
            ))}
          </div>
          <Dialog.Content
            className={isWide ? 'modal modal-wide' : 'modal'}
            aria-describedby={undefined}
            onOpenAutoFocus={focusMarkedElement}>
            <header className="modal-header">
              <Dialog.Title asChild>
                <h2>{title}</h2>
              </Dialog.Title>
              <Dialog.Close asChild>
                <CloseButton />
              </Dialog.Close>
            </header>
            <div className="modal-body">{children}</div>
          </Dialog.Content>
        </Dialog.Overlay>
      </Dialog.Portal>
    </Dialog.Root>
  );
};
