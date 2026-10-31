import { useState } from 'react';
import { examples } from '@/content/content';
import { LOCALES, useTranslation } from '@/i18n/i18n';
import type { Locale } from '@/language/messages';
import type { Project } from '@/projects/projectStore';
import type { Settings, ThemeId } from '@/settings/settings';
import { TextPrompt } from '@/ui/components/TextPrompt';

interface HomeScreenProps {
  projects: Project[];
  settings: Settings;
  locale: Locale;
  onCreate: (name: string, source?: string) => void;
  onOpen: (id: string) => void;
  onRename: (id: string, name: string) => void;
  onDelete: (id: string) => void;
  onOpenLessons: () => void;
  onChangeSettings: (changes: Partial<Settings>) => void;
}

const THEME_IDS: ThemeId[] = ['simple', 'dark', 'light'];

export const HomeScreen = ({
  projects,
  settings,
  locale,
  onCreate,
  onOpen,
  onRename,
  onDelete,
  onOpenLessons,
  onChangeSettings,
}: HomeScreenProps) => {
  const t = useTranslation();
  const [name, setName] = useState('');
  const [renaming, setRenaming] = useState<Project | null>(null);
  const themeLabels: Record<ThemeId, string> = { simple: t('Simple'), dark: t('Dark'), light: t('Light') };

  return (
    <main id="content" className="home">
      <header className="home-hero">
        <h1>Safira</h1>
        <p>{t('Programming in natural language, right in the browser.')}</p>
        <div className="home-settings">
          <label className="field">
            {t('Language')}
            <select
              value={locale}
              onChange={(event) => {
                onChangeSettings({ locale: event.target.value as Locale });
              }}>
              {LOCALES.map((option) => (
                <option key={option.id} value={option.id}>
                  {option.label}
                </option>
              ))}
            </select>
          </label>
          <label className="field">
            {t('Theme')}
            <select
              value={settings.theme}
              onChange={(event) => {
                const theme = event.target.value as ThemeId;
                onChangeSettings({ theme, syntax: theme });
              }}>
              {THEME_IDS.map((theme) => (
                <option key={theme} value={theme}>
                  {themeLabels[theme]}
                </option>
              ))}
            </select>
          </label>
          <button type="button" className="button" onClick={onOpenLessons}>
            {t('Lessons')}
          </button>
        </div>
      </header>

      <section className="home-section" aria-labelledby="new-project-title">
        <h2 id="new-project-title">{t('New project')}</h2>
        <form
          className="form-row"
          onSubmit={(event) => {
            event.preventDefault();
            onCreate(name.trim() === '' ? t('New project') : name.trim());
          }}>
          <label className="field">
            {t('Project name')}
            <input
              value={name}
              onChange={(event) => {
                setName(event.target.value);
              }}
            />
          </label>
          <button type="submit" className="button button-primary">
            {t('Create project')}
          </button>
        </form>
        <h3>{t('Start from an example')}</h3>
        <ul className="example-grid">
          {examples.map((example) => (
            <li key={example.id}>
              <button
                type="button"
                className="example-card"
                onClick={() => {
                  onCreate(example.title, example.text);
                }}>
                {example.title}
              </button>
            </li>
          ))}
        </ul>
      </section>

      <section className="home-section" aria-labelledby="my-projects-title">
        <h2 id="my-projects-title">{t('My projects')}</h2>
        {projects.length === 0 ? <p>{t('You have no projects yet.')}</p> : null}
        <ul className="project-list">
          {projects.map((project) => (
            <li key={project.id} className="project-row">
              <span className="project-name">{project.name}</span>
              <button
                type="button"
                className="button button-primary"
                aria-label={`${t('Open')} ${project.name}`}
                onClick={() => {
                  onOpen(project.id);
                }}>
                {t('Open')}
              </button>
              <button
                type="button"
                className="button"
                aria-label={`${t('Rename')} ${project.name}`}
                onClick={() => {
                  setRenaming(project);
                }}>
                {t('Rename')}
              </button>
              <button
                type="button"
                className="button"
                aria-label={`${t('Delete')} ${project.name}`}
                onClick={() => {
                  onDelete(project.id);
                }}>
                {t('Delete')}
              </button>
            </li>
          ))}
        </ul>
      </section>

      {renaming === null ? null : (
        <TextPrompt
          title={t('Rename')}
          label={t('Project name')}
          initialValue={renaming.name}
          onClose={() => {
            setRenaming(null);
          }}
          onSubmit={(value) => {
            onRename(renaming.id, value);
            setRenaming(null);
          }}
        />
      )}
    </main>
  );
};
