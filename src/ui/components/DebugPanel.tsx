import { useState } from 'react';
import { useTranslation } from '@/i18n/i18n';
import type { VariableSnapshot } from '@/language/interpreter';

interface DebugPanelProps {
  variables: VariableSnapshot[];
  onNextLine: () => void;
  onContinue: () => void;
}

export const DebugPanel = ({ variables, onNextLine, onContinue }: DebugPanelProps) => {
  const t = useTranslation();
  const [search, setSearch] = useState('');
  const visible = variables.filter((variable) => variable.name.toLowerCase().includes(search.toLowerCase()));

  return (
    <section className="debug-panel" aria-label={t('Variables')}>
      <div className="debug-actions">
        <button type="button" className="button button-primary" onClick={onNextLine}>
          {t('Next line')}
        </button>
        <button type="button" className="button" onClick={onContinue}>
          {t('Continue')}
        </button>
        <input
          aria-label={t('Search variables')}
          placeholder={t('Search variables')}
          value={search}
          onChange={(event) => {
            setSearch(event.target.value);
          }}
        />
      </div>
      <table>
        <thead>
          <tr>
            <th scope="col">{t('Variable')}</th>
            <th scope="col">{t('Value')}</th>
            <th scope="col">{t('Type')}</th>
          </tr>
        </thead>
        <tbody>
          {visible.map((variable) => (
            <tr key={variable.name}>
              <td>{variable.name}</td>
              <td>{variable.value}</td>
              <td>{variable.type}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </section>
  );
};
