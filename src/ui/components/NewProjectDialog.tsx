import { useState } from 'react';
import { examples } from '@/content/content';
import { useTranslation } from '@/i18n/i18n';
import { Modal } from './Modal';

interface NewProjectDialogProps {
  initialExampleId: string | null;
  onCreate: (name: string, source?: string) => void;
  onClose: () => void;
}

export const NewProjectDialog = ({ initialExampleId, onCreate, onClose }: NewProjectDialogProps) => {
  const t = useTranslation();
  const [name, setName] = useState('');
  const [exampleId, setExampleId] = useState<string | null>(initialExampleId);
  const selected = examples.find((example) => example.id === exampleId);

  return (
    <Modal title={t('New project')} onClose={onClose}>
      <form
        className="new-project"
        onSubmit={(event) => {
          event.preventDefault();
          const fallbackName = selected?.title ?? t('New project');
          onCreate(name.trim() === '' ? fallbackName : name.trim(), selected?.text);
        }}>
        <label className="field">
          {t('Project name (optional)')}
          <input
            data-autofocus
            value={name}
            onChange={(event) => {
              setName(event.target.value);
            }}
          />
        </label>
        <h3>{t('Example (optional)')}</h3>
        <ul className="example-grid">
          {examples.map((example) => (
            <li key={example.id}>
              <button
                type="button"
                className="example-card"
                data-fixed-text
                aria-pressed={exampleId === example.id}
                onClick={() => {
                  setExampleId(exampleId === example.id ? null : example.id);
                }}>
                {example.title}
              </button>
            </li>
          ))}
        </ul>
        <div className="new-project-footer">
          <button type="submit" className="button button-primary">
            {t('Go ahead')}
          </button>
        </div>
      </form>
    </Modal>
  );
};
