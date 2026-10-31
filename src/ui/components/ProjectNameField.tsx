import { useEffect, useRef, useState } from 'react';
import { useTranslation } from '@/i18n/i18n';

interface ProjectNameFieldProps {
  name: string;
  onRename: (name: string) => void;
}

export const ProjectNameField = ({ name, onRename }: ProjectNameFieldProps) => {
  const t = useTranslation();
  const [isEditing, setIsEditing] = useState(false);
  const input = useRef<HTMLInputElement>(null);
  const opener = useRef<HTMLButtonElement>(null);
  const isFinished = useRef(false);
  const shouldRestoreFocus = useRef(false);

  useEffect(() => {
    if (isEditing) {
      input.current?.focus();
      input.current?.select();
    } else if (shouldRestoreFocus.current) {
      shouldRestoreFocus.current = false;
      opener.current?.focus();
    }
  }, [isEditing]);

  const finish = (typedName: string | null): void => {
    if (isFinished.current) {
      return;
    }

    isFinished.current = true;
    const trimmedName = typedName?.trim() ?? '';

    if (trimmedName !== '' && trimmedName !== name) {
      onRename(trimmedName);
    }

    setIsEditing(false);
  };

  if (isEditing) {
    return (
      <input
        ref={input}
        className="project-name-input"
        aria-label={t('Project name')}
        defaultValue={name}
        onBlur={(event) => {
          finish(event.target.value);
        }}
        onKeyDown={(event) => {
          if (event.key === 'Enter') {
            // Without this, the key press lands on the restored button and opens the field again.
            event.preventDefault();
            shouldRestoreFocus.current = true;
            finish(event.currentTarget.value);
          } else if (event.key === 'Escape') {
            shouldRestoreFocus.current = true;
            finish(null);
          }
        }}
      />
    );
  }

  return (
    <button
      ref={opener}
      type="button"
      className="project-name-button"
      title={`${name} - ${t('Rename')}`}
      onClick={() => {
        isFinished.current = false;
        setIsEditing(true);
      }}>
      {name}
    </button>
  );
};
