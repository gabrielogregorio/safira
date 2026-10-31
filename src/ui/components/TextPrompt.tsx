import { useState } from 'react';
import { useTranslation } from '@/i18n/i18n';
import { Modal } from './Modal';

interface TextPromptProps {
  title: string;
  label: string;
  initialValue: string;
  onSubmit: (value: string) => void;
  onClose: () => void;
}

export const TextPrompt = ({ title, label, initialValue, onSubmit, onClose }: TextPromptProps) => {
  const t = useTranslation();
  const [value, setValue] = useState(initialValue);

  return (
    <Modal title={title} onClose={onClose}>
      <form
        className="form-row"
        onSubmit={(event) => {
          event.preventDefault();

          if (value.trim() !== '') {
            onSubmit(value.trim());
          }
        }}>
        <label className="field">
          {label}
          <input
            data-autofocus
            value={value}
            onChange={(event) => {
              setValue(event.target.value);
            }}
          />
        </label>
        <button type="submit" className="button button-primary">
          {t('Save')}
        </button>
      </form>
    </Modal>
  );
};
