import { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { createTranslator, detectLocale, TranslationContext } from '@/i18n/i18n';
import { addScriptVersion } from '@/language/version';
import { clearDrafts } from '@/projects/draftStore';
import { toProjectName } from '@/projects/projectArchive';
import type { Project } from '@/projects/projectStore';
import {
  createProject,
  loadProjects,
  MAIN_FILE,
  removeProject,
  saveProjects,
  upsertProject,
} from '@/projects/projectStore';
import { useRoute } from '@/routing/useRoute';
import type { Settings } from '@/settings/settings';
import { loadSettings, saveSettings, SYNTAX_PALETTES } from '@/settings/settings';
import { downloadProject, readArchiveFile } from '@/ui/archiveFiles';
import { describeArchiveResult } from '@/ui/archiveMessages';
import { PreferencesDialog } from '@/ui/components/PreferencesDialog';
import type { SweepKind } from '@/ui/components/SceneSweep';
import { canAnimateScenes, SCENE_SWEEP_MIDPOINT_MILLISECONDS, SceneSweep } from '@/ui/components/SceneSweep';
import type { WorkerFactory } from '@/ui/hooks/useRunner';
import { EditorScreen } from '@/ui/screens/EditorScreen';
import { HomeScreen } from '@/ui/screens/HomeScreen';
import { LessonsScreen } from '@/ui/screens/LessonsScreen';

interface AppProps {
  createWorker?: WorkerFactory;
}

const sweepKindOf = (changes: Partial<Settings>): SweepKind | null => {
  if (changes.locale !== undefined) {
    return 'language';
  }

  return changes.theme === undefined ? null : 'theme';
};

export const App = ({ createWorker }: AppProps) => {
  const { route, navigate } = useRoute();
  const [settings, setSettings] = useState<Settings>(loadSettings);
  const [projects, setProjects] = useState<Project[]>(loadProjects);
  const [saveFailed, setSaveFailed] = useState(false);
  const [isChoosingPreferences, setIsChoosingPreferences] = useState(false);
  const [sweep, setSweep] = useState<SweepKind | null>(null);
  const [archiveNotice, setArchiveNotice] = useState<string | null>(null);
  const sweepTimer = useRef<ReturnType<typeof setTimeout> | null>(null);

  const locale = useMemo(
    () => detectLocale(window.location.search, settings.locale, navigator.language),
    [settings.locale],
  );
  const translate = useMemo(() => createTranslator(locale), [locale]);

  useEffect(() => {
    const root = document.documentElement;
    root.lang = locale === 'en-us' ? 'en' : locale;
    root.dataset['theme'] = settings.theme;

    for (const [category, color] of Object.entries(SYNTAX_PALETTES[settings.syntax])) {
      root.style.setProperty(`--syntax-${category}`, color);
    }
  }, [locale, settings.syntax, settings.theme]);

  useEffect(
    () => () => {
      if (sweepTimer.current !== null) {
        clearTimeout(sweepTimer.current);
      }
    },
    [],
  );

  const applySettings = useCallback((changes: Partial<Settings>) => {
    setSettings((current) => {
      const next = { ...current, ...changes };
      saveSettings(next);

      return next;
    });
  }, []);

  const changeSettings = useCallback(
    (changes: Partial<Settings>) => {
      const kind = sweepKindOf(changes);

      if (kind === null || !canAnimateScenes()) {
        applySettings(changes);

        return;
      }

      setSweep(kind);
      sweepTimer.current = setTimeout(() => {
        applySettings(changes);
      }, SCENE_SWEEP_MIDPOINT_MILLISECONDS);
    },
    [applySettings],
  );

  const persist = useCallback((next: Project[]) => {
    setSaveFailed(!saveProjects(next));
    setProjects(next);
  }, []);

  const handleCreate = useCallback(
    (name: string, source?: string) => {
      const project = createProject(name, source);
      persist(upsertProject(projects, project));
      navigate({ name: 'project', projectId: project.id, file: null });
    },
    [navigate, persist, projects],
  );

  const handleImportProject = useCallback(
    async (file: File) => {
      const result = await readArchiveFile(file);

      if (result.ok) {
        const project = { ...createProject(toProjectName(file.name)), files: result.files };
        persist(upsertProject(projects, project));
      }

      setArchiveNotice(describeArchiveResult(translate, result));
    },
    [persist, projects, translate],
  );

  const handleOpenLessonCode = useCallback(
    (lessonTitle: string, code: string) => {
      const source = addScriptVersion(code);
      const existing = projects.find((project) => project.files[MAIN_FILE] === source);

      if (existing === undefined) {
        handleCreate(lessonTitle, source);
      } else {
        navigate({ name: 'project', projectId: existing.id, file: null });
      }
    },
    [handleCreate, navigate, projects],
  );

  const handleSave = useCallback((project: Project) => {
    setProjects((current) => {
      const next = upsertProject(current, project);
      setSaveFailed(!saveProjects(next));

      return next;
    });
  }, []);

  const openPreferences = useCallback(() => {
    setIsChoosingPreferences(true);
  }, []);

  const goHome = useCallback(() => {
    navigate({ name: 'home' });
  }, [navigate]);

  const activeProject =
    route.name === 'project' ? projects.find((project) => project.id === route.projectId) : undefined;
  const isHome = activeProject === undefined && route.name !== 'lessons';

  return (
    <TranslationContext.Provider value={translate}>
      <a
        className="skip-link"
        href="#content"
        onClick={(event) => {
          event.preventDefault();
          document.getElementById('content')?.focus();
        }}>
        {translate('Skip to content')}
      </a>
      {saveFailed ? (
        <div className="alert alert-error" role="alert">
          {translate('The browser refused to save your projects.')}
        </div>
      ) : null}
      {archiveNotice === null || !isHome ? null : (
        <div className="alert" role="status">
          <p>{archiveNotice}</p>
          <button
            type="button"
            className="button"
            onClick={() => {
              setArchiveNotice(null);
            }}>
            {translate('Close')}
          </button>
        </div>
      )}
      {activeProject !== undefined ? (
        <EditorScreen
          key={activeProject.id}
          project={activeProject}
          routeFile={route.name === 'project' ? route.file : null}
          settings={settings}
          locale={locale}
          createWorker={createWorker}
          onSaveProject={handleSave}
          onSelectFile={(file) => {
            navigate({ name: 'project', projectId: activeProject.id, file });
          }}
          onChangeSettings={changeSettings}
          onOpenPreferences={openPreferences}
          onBack={goHome}
        />
      ) : null}
      {route.name === 'lessons' ? (
        <LessonsScreen
          lessonId={route.lessonId}
          section={route.section}
          readLessons={settings.readLessons}
          onOpenPreferences={openPreferences}
          onOpenCode={handleOpenLessonCode}
          onMarkRead={(id) => {
            if (!settings.readLessons.includes(id)) {
              changeSettings({ readLessons: [...settings.readLessons, id] });
            }
          }}
          onBack={goHome}
        />
      ) : null}
      {isHome ? (
        <HomeScreen
          projects={projects}
          isCreating={route.name === 'new'}
          initialExampleId={route.name === 'new' ? route.exampleId : null}
          onStartCreating={() => {
            navigate({ name: 'new', exampleId: null });
          }}
          onCancelCreating={goHome}
          onCreate={handleCreate}
          onImportProject={(file) => {
            void handleImportProject(file);
          }}
          onExportProject={downloadProject}
          onRename={(id, name) => {
            persist(projects.map((project) => (project.id === id ? { ...project, name } : project)));
          }}
          onDelete={(id) => {
            persist(removeProject(projects, id));
            clearDrafts(id);
          }}
          onOpenLessons={() => {
            navigate({ name: 'lessons', lessonId: null, section: null });
          }}
          onOpenPreferences={openPreferences}
        />
      ) : null}
      {isChoosingPreferences ? (
        <PreferencesDialog
          settings={settings}
          locale={locale}
          onChange={changeSettings}
          onClose={() => {
            setIsChoosingPreferences(false);
          }}
        />
      ) : null}
      {sweep === null ? null : (
        <SceneSweep
          kind={sweep}
          onFinished={() => {
            setSweep(null);
          }}
        />
      )}
    </TranslationContext.Provider>
  );
};
