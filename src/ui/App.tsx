import { useCallback, useEffect, useMemo, useState } from 'react';
import { createTranslator, detectLocale, TranslationContext } from '@/i18n/i18n';
import type { Project } from '@/projects/projectStore';
import { createProject, loadProjects, removeProject, saveProjects, upsertProject } from '@/projects/projectStore';
import type { Settings } from '@/settings/settings';
import { loadSettings, saveSettings, SYNTAX_PALETTES } from '@/settings/settings';
import type { WorkerFactory } from '@/ui/hooks/useRunner';
import { EditorScreen } from '@/ui/screens/EditorScreen';
import { HomeScreen } from '@/ui/screens/HomeScreen';
import { LessonsScreen } from '@/ui/screens/LessonsScreen';

type Screen = { name: 'home' } | { name: 'lessons' } | { name: 'editor'; projectId: string };

interface AppProps {
  createWorker?: WorkerFactory;
}

export const App = ({ createWorker }: AppProps) => {
  const [settings, setSettings] = useState<Settings>(loadSettings);
  const [projects, setProjects] = useState<Project[]>(loadProjects);
  const [screen, setScreen] = useState<Screen>({ name: 'home' });
  const [saveFailed, setSaveFailed] = useState(false);

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

  const changeSettings = useCallback((changes: Partial<Settings>) => {
    setSettings((current) => {
      const next = { ...current, ...changes };
      saveSettings(next);

      return next;
    });
  }, []);

  const persist = useCallback((next: Project[]) => {
    setSaveFailed(!saveProjects(next));
    setProjects(next);
  }, []);

  const handleCreate = useCallback(
    (name: string, source?: string) => {
      const project = createProject(name, source);
      persist(upsertProject(projects, project));
      setScreen({ name: 'editor', projectId: project.id });
    },
    [persist, projects],
  );

  const handleSave = useCallback((project: Project) => {
    setProjects((current) => {
      const next = upsertProject(current, project);
      setSaveFailed(!saveProjects(next));

      return next;
    });
  }, []);

  const activeProject =
    screen.name === 'editor' ? projects.find((project) => project.id === screen.projectId) : undefined;

  return (
    <TranslationContext.Provider value={translate}>
      <a className="skip-link" href="#content">
        {translate('Skip to content')}
      </a>
      {saveFailed ? (
        <div className="alert alert-error" role="alert">
          {translate('The browser refused to save your projects.')}
        </div>
      ) : null}
      {activeProject !== undefined ? (
        <EditorScreen
          key={activeProject.id}
          project={activeProject}
          settings={settings}
          locale={locale}
          createWorker={createWorker}
          onSaveProject={handleSave}
          onChangeSettings={changeSettings}
          onBack={() => {
            setScreen({ name: 'home' });
          }}
        />
      ) : null}
      {screen.name === 'lessons' ? (
        <LessonsScreen
          readLessons={settings.readLessons}
          onMarkRead={(id) => {
            if (!settings.readLessons.includes(id)) {
              changeSettings({ readLessons: [...settings.readLessons, id] });
            }
          }}
          onBack={() => {
            setScreen({ name: 'home' });
          }}
        />
      ) : null}
      {screen.name === 'home' ? (
        <HomeScreen
          projects={projects}
          settings={settings}
          locale={locale}
          onCreate={handleCreate}
          onOpen={(projectId) => {
            setScreen({ name: 'editor', projectId });
          }}
          onRename={(id, name) => {
            persist(projects.map((project) => (project.id === id ? { ...project, name } : project)));
          }}
          onDelete={(id) => {
            persist(removeProject(projects, id));
          }}
          onOpenLessons={() => {
            setScreen({ name: 'lessons' });
          }}
          onChangeSettings={changeSettings}
        />
      ) : null}
    </TranslationContext.Provider>
  );
};
