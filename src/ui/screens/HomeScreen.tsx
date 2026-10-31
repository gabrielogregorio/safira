import { useState } from 'react';
import { useTranslation } from '@/i18n/i18n';
import type { Project } from '@/projects/projectStore';
import { NewProjectDialog } from '@/ui/components/NewProjectDialog';
import { SafiraLogo } from '@/ui/components/SafiraLogo';
import { TextPrompt } from '@/ui/components/TextPrompt';

interface HomeScreenProps {
  projects: Project[];
  onCreate: (name: string, source?: string) => void;
  onOpen: (id: string) => void;
  onRename: (id: string, name: string) => void;
  onDelete: (id: string) => void;
  onOpenLessons: () => void;
  onOpenPreferences: () => void;
}

const HERO_LOGO_SIZE = 64;

export const HomeScreen = ({
  projects,
  onCreate,
  onOpen,
  onRename,
  onDelete,
  onOpenLessons,
  onOpenPreferences,
}: HomeScreenProps) => {
  const t = useTranslation();
  const [isCreating, setIsCreating] = useState(false);
  const [renaming, setRenaming] = useState<Project | null>(null);

  return (
    <main id="content" className="home">
      <header className="home-hero">
        <div className="home-brand">
          <SafiraLogo size={HERO_LOGO_SIZE} />
          <h1>Safira</h1>
        </div>
        <p>{t('Programming in natural language, right in the browser.')}</p>
        <div className="home-settings">
          <button
            type="button"
            className="button button-primary"
            onClick={() => {
              setIsCreating(true);
            }}>
            {t('Create project')}
          </button>
          <button type="button" className="button" onClick={onOpenLessons}>
            {t('Lessons')}
          </button>
          <button type="button" className="button" onClick={onOpenPreferences}>
            {t('Theme and language')}
          </button>
        </div>
      </header>

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

      {isCreating ? (
        <NewProjectDialog
          onCreate={onCreate}
          onClose={() => {
            setIsCreating(false);
          }}
        />
      ) : null}

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
