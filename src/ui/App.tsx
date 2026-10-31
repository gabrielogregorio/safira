import { useCallback, useEffect, useLayoutEffect, useMemo, useRef, useState } from 'react';
import { createTranslator, detectLocale, TranslationContext } from '@/i18n/i18n';
import { clearDrafts } from '@/projects/draftStore';
import { toProjectName } from '@/projects/projectArchive';
import type { Project } from '@/projects/projectStore';
import {
  createProject,
  loadProjects,
  removeProject,
  saveProjects,
  upsertProject,
} from '@/projects/projectStore';
import { useRoute } from '@/routing/useRoute';
import type { Settings } from '@/settings/settings';
import { loadSettings, saveSettings, SYNTAX_PALETTES } from '@/settings/settings';
import { downloadProject, readArchiveFile } from '@/ui/archiveFiles';
import { describeArchiveResult } from '@/ui/archiveMessages';
import { CloseButton } from '@/ui/components/CloseButton';
import { LanguageToggle } from '@/ui/components/LanguageToggle';
import { SceneBackdrop } from '@/ui/components/SceneBackdrop';
import { SoundToggle } from '@/ui/components/SoundToggle';
import { themeAtPhase } from '@/ui/sky/skyClock';
import { useSkyClock } from '@/ui/sky/useSkyClock';
import { ThemeToggle } from '@/ui/components/ThemeToggle';
import type { WorkerFactory } from '@/ui/hooks/useRunner';
import { prefersMotion } from '@/ui/motion';
import { menuItemAt, soundForClick, soundPlayer } from '@/ui/sound/sounds';
import { scrambleDocument } from '@/ui/textScramble';
import { EditorScreen } from '@/ui/screens/EditorScreen';
import { HomeScreen } from '@/ui/screens/HomeScreen';

interface AppProps {
  createWorker?: WorkerFactory;
}

const THEME_CHANGE_MILLISECONDS = 1700;

export const App = ({ createWorker }: AppProps) => {
  const { route, navigate } = useRoute();
  const [settings, setSettings] = useState<Settings>(loadSettings);
  const [projects, setProjects] = useState<Project[]>(loadProjects);
  const [saveFailed, setSaveFailed] = useState(false);
  const [archiveNotice, setArchiveNotice] = useState<string | null>(null);
  const themeTimer = useRef<ReturnType<typeof setTimeout> | null>(null);
  const { phase, travelTo } = useSkyClock(settings.theme);
  const skyTheme = themeAtPhase(phase);
  const shownTheme = useRef(skyTheme);
  const syntaxTheme = settings.syntax === settings.theme ? skyTheme : settings.syntax;

  const locale = useMemo(
    () => detectLocale(window.location.search, settings.locale, navigator.language),
    [settings.locale],
  );
  const translate = useMemo(() => createTranslator(locale), [locale]);
  const shownLocale = useRef(locale);

  useEffect(() => {
    const root = document.documentElement;
    root.lang = locale === 'en-us' ? 'en' : locale;

    if (shownTheme.current !== skyTheme && prefersMotion()) {
      root.dataset['themeChanging'] = 'true';

      if (themeTimer.current !== null) {
        clearTimeout(themeTimer.current);
      }

      themeTimer.current = setTimeout(() => {
        delete root.dataset['themeChanging'];
      }, THEME_CHANGE_MILLISECONDS);
    }

    shownTheme.current = skyTheme;
    root.dataset['theme'] = skyTheme;
    root.dataset['codeFont'] = settings.codeFont;

    for (const [category, color] of Object.entries(SYNTAX_PALETTES[syntaxTheme])) {
      root.style.setProperty(`--syntax-${category}`, color);
    }
  }, [locale, settings.codeFont, skyTheme, syntaxTheme]);

  useLayoutEffect(() => {
    if (shownLocale.current === locale) {
      return undefined;
    }

    shownLocale.current = locale;

    return prefersMotion() ? scrambleDocument(document.body) : undefined;
  }, [locale]);

  useEffect(
    () => () => {
      if (themeTimer.current !== null) {
        clearTimeout(themeTimer.current);
      }
    },
    [],
  );

  useEffect(() => {
    soundPlayer.setEnabled(settings.sound);
  }, [settings.sound]);

  useEffect(() => {
    const playClick = (event: MouseEvent): void => {
      const sound = soundForClick(event.target);

      if (sound !== null) {
        void soundPlayer.play(sound);
      }
    };

    let hoveredItem: Element | null = null;

    const playHover = (event: PointerEvent): void => {
      const item = menuItemAt(event.target);

      if (event.pointerType === 'mouse' && item !== hoveredItem) {
        hoveredItem = item;

        if (item !== null && item.getAttribute('aria-disabled') !== 'true') {
          void soundPlayer.play('hover');
        }
      }
    };

    document.addEventListener('pointerdown', soundPlayer.prepare, { once: true });
    document.addEventListener('click', playClick);
    document.addEventListener('pointerover', playHover);

    return () => {
      document.removeEventListener('pointerdown', soundPlayer.prepare);
      document.removeEventListener('click', playClick);
      document.removeEventListener('pointerover', playHover);
    };
  }, []);

  const changeSettings = useCallback(
    (changes: Partial<Settings>) => {
      // Applied now, so that the click that turns the sound on is already heard and the one that turns it off is not.
      if (changes.sound !== undefined) {
        soundPlayer.setEnabled(changes.sound);
      }

      if (changes.locale !== undefined) {
        void soundPlayer.play('language');
      }

      if (changes.theme !== undefined) {
        void soundPlayer.play('weather');
        travelTo(changes.theme);
      }

      setSettings((current) => {
        const next = { ...current, ...changes };
        saveSettings(next);

        return next;
      });
    },
    [travelTo],
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

  const importProject = useCallback(
    (file: File) => {
      void handleImportProject(file);
    },
    [handleImportProject],
  );

  const handleSave = useCallback((project: Project) => {
    setProjects((current) => {
      const next = upsertProject(current, project);
      setSaveFailed(!saveProjects(next));

      return next;
    });
  }, []);

  const goHome = useCallback(() => {
    navigate({ name: 'home' });
  }, [navigate]);

  const activeProject =
    route.name === 'project' ? projects.find((project) => project.id === route.projectId) : undefined;
  const isHome = activeProject === undefined;
  const preferenceToggles = (
    <div className="orb-toggles">
      <ThemeToggle
        theme={skyTheme}
        onChange={(theme) => {
          changeSettings({ theme, syntax: theme });
        }}
      />
      <LanguageToggle
        locale={locale}
        onChange={(nextLocale) => {
          changeSettings({ locale: nextLocale });
        }}
      />
      <SoundToggle
        isOn={settings.sound}
        onChange={(sound) => {
          changeSettings({ sound });
        }}
      />
    </div>
  );

  return (
    <TranslationContext.Provider value={translate}>
      <SceneBackdrop phase={phase} />
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
          <CloseButton
            onClick={() => {
              setArchiveNotice(null);
            }}
          />
        </div>
      )}
      {activeProject !== undefined ? (
        <EditorScreen
          key={activeProject.id}
          project={activeProject}
          routeFile={route.name === 'project' ? route.file : null}
          settings={{ ...settings, theme: skyTheme }}
          locale={locale}
          createWorker={createWorker}
          onSaveProject={handleSave}
          routeLesson={route.name === 'project' ? route.lesson : undefined}
          onSelectFile={(file) => {
            navigate({ name: 'project', projectId: activeProject.id, file });
          }}
          onChangeLesson={(file, lesson) => {
            navigate({ name: 'project', projectId: activeProject.id, file, lesson });
          }}
          onChangeSettings={changeSettings}
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
          onImportProject={importProject}
          onExportProject={downloadProject}
          onRename={(id, name) => {
            persist(projects.map((project) => (project.id === id ? { ...project, name } : project)));
          }}
          onDelete={(id) => {
            persist(removeProject(projects, id));
            clearDrafts(id);
          }}
          preferenceToggles={preferenceToggles}
        />
      ) : null}
    </TranslationContext.Provider>
  );
};
