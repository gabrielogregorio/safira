import type { ReactNode } from 'react';
import { useEffect, useRef, useState } from 'react';
import { useTranslation } from '@/i18n/i18n';
import type { Project } from '@/projects/projectStore';
import { routeToHash } from '@/routing/routes';
import { ArchiveInput } from '@/ui/components/ArchiveInput';
import { Modal } from '@/ui/components/Modal';
import { NewProjectDialog } from '@/ui/components/NewProjectDialog';
import { AeroOrb } from '@/ui/components/AeroOrb';
import type { ScreenPoint } from '@/ui/components/Aquarium';
import { ProjectNameField } from '@/ui/components/ProjectNameField';
import { soundPlayer } from '@/ui/sound/sounds';
import { TextPrompt } from '@/ui/components/TextPrompt';

interface HomeScreenProps {
  projects: Project[];
  isCreating: boolean;
  initialExampleId: string | null;
  onStartCreating: () => void;
  onCancelCreating: () => void;
  onCreate: (name: string, source?: string) => void;
  onImportProject: (file: File) => void;
  onOpenAquarium: (origin: ScreenPoint) => void;
  onExportProject: (project: Project) => void;
  onRename: (id: string, name: string) => void;
  onDelete: (id: string) => void;
  preferenceToggles: ReactNode;
}

const HERO_ORB_SIZE = 96;

export const HomeScreen = ({
  projects,
  isCreating,
  initialExampleId,
  onStartCreating,
  onCancelCreating,
  onCreate,
  onImportProject,
  onOpenAquarium,
  onExportProject,
  onRename,
  onDelete,
  preferenceToggles,
}: HomeScreenProps) => {
  const t = useTranslation();
  const [renaming, setRenaming] = useState<Project | null>(null);
  const [deleting, setDeleting] = useState<Project | null>(null);
  const archiveInput = useRef<HTMLInputElement>(null);
  const [isDropping, setIsDropping] = useState(false);

  useEffect(() => {
    const carriesFiles = (event: DragEvent): boolean => event.dataTransfer?.types.includes('Files') === true;

    const showDropTarget = (event: DragEvent): void => {
      if (carriesFiles(event)) {
        event.preventDefault();
        setIsDropping(true);
      }
    };

    const hideDropTarget = (event: DragEvent): void => {
      if (event.relatedTarget === null) {
        setIsDropping(false);
      }
    };

    const importDroppedFile = (event: DragEvent): void => {
      event.preventDefault();
      setIsDropping(false);

      const file = event.dataTransfer?.files[0];

      if (file !== undefined) {
        void soundPlayer.play('import');
        onImportProject(file);
      }
    };

    document.addEventListener('dragenter', showDropTarget);
    document.addEventListener('dragover', showDropTarget);
    document.addEventListener('dragleave', hideDropTarget);
    document.addEventListener('drop', importDroppedFile);

    return () => {
      document.removeEventListener('dragenter', showDropTarget);
      document.removeEventListener('dragover', showDropTarget);
      document.removeEventListener('dragleave', hideDropTarget);
      document.removeEventListener('drop', importDroppedFile);
    };
  }, [onImportProject]);

  return (
    <main id="content" tabIndex={-1} className="home">
      {isDropping ? (
        <div className="drop-target" data-testid="drop-target">
          <p>{t('Drop the .zip to create a project')}</p>
        </div>
      ) : null}
      <header className="home-hero">
        <div className="home-brand">
          <button
            type="button"
            className="aero-orb-button"
            data-sound="aquarium"
            aria-label={t('Open the aquarium')}
            title={t('Open the aquarium')}
            onClick={(event) => {
              const { left, top, width, height } = event.currentTarget.getBoundingClientRect();
              onOpenAquarium({ x: left + width / 2, y: top + height / 2 });
            }}>
            <AeroOrb size={HERO_ORB_SIZE} />
          </button>
          <h1 data-fixed-text>Safira</h1>
        </div>
        <p>{t('Programming in natural language, right in the browser.')}</p>
        <div className="home-settings">
          <button type="button" className="button button-primary" onClick={onStartCreating}>
            {t('Create project')}
          </button>
          <button
            type="button"
            className="button"
            data-sound="import"
            onClick={() => {
              archiveInput.current?.click();
            }}>
            {t('Import project (.zip)')}
          </button>
          <ArchiveInput ref={archiveInput} label={t('Import project (.zip)')} onSelect={onImportProject} />
          <div className="home-corner">{preferenceToggles}</div>
        </div>
      </header>

      <section className="home-section" aria-labelledby="my-projects-title">
        <h2 id="my-projects-title">{t('My projects')}</h2>
        {projects.length === 0 ? <p>{t('You have no projects yet.')}</p> : null}
        <ul className="project-list">
          {projects.map((project) => (
            <li key={project.id} className="project-row">
              <span className="project-name" data-fixed-text>
                <ProjectNameField
                  name={project.name}
                  onRename={(name) => {
                    onRename(project.id, name);
                  }}
                />
              </span>
              <a
                className="button button-primary"
                data-sound="homeOpen"
                href={routeToHash({ name: 'project', projectId: project.id, file: null })}
                aria-label={`${t('Open')} ${project.name}`}>
                {t('Open')}
              </a>
              <button
                type="button"
                className="button"
                data-sound="export"
                aria-label={`${t('Export')} ${project.name}`}
                onClick={() => {
                  onExportProject(project);
                }}>
                {t('Export')}
              </button>
              <button
                type="button"
                className="button"
                data-sound="renameStart"
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
          openSound="alert"
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
              data-sound="delete"
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
            void soundPlayer.play('rename');
            onRename(renaming.id, value);
            setRenaming(null);
          }}
        />
      )}
    </main>
  );
};
