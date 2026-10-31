import type { ComponentProps } from 'react';
import { useTranslation } from '@/i18n/i18n';
import { CloseIcon } from './AeroIcons';

export const CloseButton = (props: ComponentProps<'button'>) => {
  const t = useTranslation();

  return (
    <button
      type="button"
      className="aero-button aero-button-close"
      aria-label={t('Close')}
      title={t('Close')}
      {...props}>
      <CloseIcon />
    </button>
  );
};
