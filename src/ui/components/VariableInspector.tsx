import { useRef, useState } from 'react';
import { useTranslation } from '@/i18n/i18n';
import type { VariableSnapshot } from '@/language/interpreter';
import { soundPlayer } from '@/ui/sound/sounds';

interface VariableInspectorProps {
  variables: VariableSnapshot[];
}

const SEARCH_TYPING_RATES = [1, 1.12, 0.92, 1.2];

export const VariableInspector = ({ variables }: VariableInspectorProps) => {
  const t = useTranslation();
  const [search, setSearch] = useState('');
  const typingStep = useRef(0);
  const visible = variables.filter((variable) => variable.name.toLowerCase().includes(search.toLowerCase()));

  return (
    <section className="inspector" aria-label={t('Variables')}>
      <header className="inspector-header">
        <h2>{t('Variables')}</h2>
        <input
          type="search"
          data-sound="search"
          aria-label={t('Search variables')}
          placeholder={t('Search variables')}
          value={search}
          onChange={(event) => {
            typingStep.current = (typingStep.current + 1) % SEARCH_TYPING_RATES.length;
            void soundPlayer.play('searchTyping', SEARCH_TYPING_RATES[typingStep.current]);
            setSearch(event.target.value);
          }}
        />
      </header>
      {variables.length === 0 ? (
        <div className="inspector-empty">
          <p>{t('Run your program to see its variables here.')}</p>
          <p>{t('Click the dots beside the lines to pause there.')}</p>
        </div>
      ) : (
        <div className="inspector-table" role="region" aria-label={t('Variables')} tabIndex={0}>
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
                  <td className="inspector-value">{variable.value}</td>
                  <td>
                    <span className={`type-badge type-${variable.type}`}>{variable.type}</span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </section>
  );
};
