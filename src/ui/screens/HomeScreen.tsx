import type { ReactNode } from 'react';
import { useRef, useState } from 'react';
import { useTranslation } from '@/i18n/i18n';
import type { Project } from '@/projects/projectStore';
import { routeToHash } from '@/routing/routes';
import { ArchiveInput } from '@/ui/components/ArchiveInput';
import { Modal } from '@/ui/components/Modal';
import { NewProjectDialog } from '@/ui/components/NewProjectDialog';
import { SafiraLogo } from '@/ui/components/SafiraLogo';
import { TextPrompt } from '@/ui/components/TextPrompt';

interface HomeScreenProps {
  projects: Project[];
  isCreating: boolean;
  initialExampleId: string | null;
  onStartCreating: () => void;
  onCancelCreating: () => void;
  onCreate: (name: string, source?: string) => void;
  onImportProject: (file: File) => void;
  onExportProject: (project: Project) => void;
  onRename: (id: string, name: string) => void;
  onDelete: (id: string) => void;
  onOpenLessons: () => void;
  preferenceToggles: ReactNode;
}

const HERO_LOGO_SIZE = 84;

export const HomeScreen = ({
  projects,
  isCreating,
  initialExampleId,
  onStartCreating,
  onCancelCreating,
  onCreate,
  onImportProject,
  onExportProject,
  onRename,
  onDelete,
  onOpenLessons,
  preferenceToggles,
}: HomeScreenProps) => {
  const t = useTranslation();
  const [renaming, setRenaming] = useState<Project | null>(null);
  const [deleting, setDeleting] = useState<Project | null>(null);
  const archiveInput = useRef<HTMLInputElement>(null);

  return (
    <main id="content" tabIndex={-1} className="home">
      <header className="home-hero">
        <div className="home-brand">
          <SafiraLogo size={HERO_LOGO_SIZE} />
          <h1 data-fixed-text>Safira</h1>
          <div className="home-corner">{preferenceToggles}</div>
        </div>
        <p>{t('Programming in natural language, right in the browser.')}</p>
        <div className="home-settings">
          <button type="button" className="button button-primary" onClick={onStartCreating}>
            {t('Create project')}
          </button>
          <button
            type="button"
            className="button"
            onClick={() => {
              archiveInput.current?.click();
            }}>
            {t('Import project (.zip)')}
          </button>
          <ArchiveInput ref={archiveInput} label={t('Import project (.zip)')} onSelect={onImportProject} />
          <button type="button" className="button" onClick={onOpenLessons}>
            {t('Lessons')}
          </button>
        </div>
      </header>

      <section className="home-section" aria-labelledby="my-projects-title">
        <h2 id="my-projects-title">{t('My projects')}</h2>
        {projects.length === 0 ? <p>{t('You have no projects yet.')}</p> : null}
        <ul className="project-list">
          {projects.map((project) => (
            <li key={project.id} className="project-row">
              <span className="project-name" data-fixed-text>
                {project.name}
              </span>
              <a
                className="button button-primary"
                href={routeToHash({ name: 'project', projectId: project.id, file: null })}
                aria-label={`${t('Open')} ${project.name}`}>
                {t('Open')}
              </a>
              <button
                type="button"
                className="button"
                aria-label={`${t('Export')} ${project.name}`}
                onClick={() => {
                  onExportProject(project);
                }}>
                {t('Export')}
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
                  setDeleting(project);
                }}>
                {t('Delete')}
              </button>
            </li>
          ))}
        </ul>
      </section>

      {isCreating ? (
        <NewProjectDialog initialExampleId={initialExampleId} onCreate={onCreate} onClose={onCancelCreating} />
      ) : null}

      {deleting === null ? null : (
        <Modal
          title={t('Delete project?')}
          onClose={() => {
            setDeleting(null);
          }}>
          <p>{t('"{name}" and all its files will be deleted. This cannot be undone.', { name: deleting.name })}</p>
          <div className="form-row">
            <button
              type="button"
              className="button"
              data-autofocus
              onClick={() => {
                setDeleting(null);
              }}>
              {t('Cancel')}
            </button>
            <button
              type="button"
              className="button button-stop"
              onClick={() => {
                onDelete(deleting.id);
                setDeleting(null);
              }}>
              {t('Delete')}
            </button>
          </div>
        </Modal>
      )}

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
