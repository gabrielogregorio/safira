import { useCallback, useEffect, useLayoutEffect, useMemo, useRef, useState } from 'react';
import { createTranslator, detectLocale, LocaleContext, TranslationContext } from '@/i18n/i18n';
import { clearDrafts } from '@/projects/draftStore';
import { toProjectName } from '@/projects/projectArchive';
import type { Project } from '@/projects/projectStore';
import { createProject, loadProjects, removeProject, saveProjects, upsertProject } from '@/projects/projectStore';
import { useRoute } from '@/routing/useRoute';
import type { Settings } from '@/settings/settings';
import { loadSettings, saveSettings } from '@/settings/settings';
import { applyVision } from '@/settings/vision';
import { downloadProject, readArchiveFile } from '@/ui/archiveFiles';
import { describeArchiveResult } from '@/ui/archiveMessages';
import type { ScreenPoint } from '@/ui/components/Aquarium';
import { Aquarium } from '@/ui/components/Aquarium';
import { CloseButton } from '@/ui/components/CloseButton';
import { GlobeWallpaper } from '@/ui/components/GlobeWallpaper';
import { LanguageToggle } from '@/ui/components/LanguageToggle';
import { SceneBackdrop } from '@/ui/components/SceneBackdrop';
import { SettingsDialog } from '@/ui/components/SettingsDialog';
import { eraseEverything } from '@/settings/eraseEverything';
import { markReturnFromSnap, snapAway } from '@/ui/snapEffect';
import { SoundToggle } from '@/ui/components/SoundToggle';
import { themeAtPhase } from '@/ui/sky/skyClock';
import { useSkyClock } from '@/ui/sky/useSkyClock';
import { ThemeToggle } from '@/ui/components/ThemeToggle';
import type { CheckWorkerFactory } from '@/ui/hooks/useLessonMode';
import type { WorkerFactory } from '@/ui/hooks/useRunner';
import { prefersMotion } from '@/ui/motion';
import {
  clickableAt,
  isPlainTextField,
  LANGUAGE_SOUNDS,
  soundForClick,
  soundPlayer,
  WEATHER_SOUNDS,
} from '@/ui/sound/sounds';
import { scrambleDocument } from '@/ui/textScramble';
import { EditorScreen } from '@/ui/screens/EditorScreen';
import { HomeScreen } from '@/ui/screens/HomeScreen';
import { printConsoleInvite } from '@/ui/consoleInvite';

// With the dust before it and the fade in after it, the site comes back in about 5 seconds.
const DARK_PAUSE_MILLISECONDS = 1200;

interface AppProps {
  createWorker?: WorkerFactory;
  createLessonCheckWorker?: CheckWorkerFactory;
}

const THEME_CHANGE_MILLISECONDS = 1700;

export const App = ({ createWorker, createLessonCheckWorker }: AppProps) => {
  const { route, navigate } = useRoute();
  const [settings, setSettings] = useState<Settings>(loadSettings);
  const [projects, setProjects] = useState<Project[]>(loadProjects);
  const [saveFailed, setSaveFailed] = useState(false);
  const [archiveNotice, setArchiveNotice] = useState<string | null>(null);
  const themeTimer = useRef<ReturnType<typeof setTimeout> | null>(null);
  const [aquariumOrigin, setAquariumOrigin] = useState<ScreenPoint>(() => ({
    x: window.innerWidth / 2,
    y: window.innerHeight / 2,
  }));
  const { phase, travelTo } = useSkyClock(settings.theme);
  const skyTheme = themeAtPhase(phase);
  const shownTheme = useRef(skyTheme);

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

    applyVision(root, settings.vision, skyTheme);
  }, [locale, settings.codeFont, settings.vision, skyTheme]);

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
    printConsoleInvite(
      translate('Curious about what is inside?'),
      translate('Safira is open source. Get the repository, run it on your computer and change whatever you want.'),
    );
    // Once per visit: changing the language must not print it again.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  useEffect(() => {
    const playClick = (event: MouseEvent): void => {
      const sound = soundForClick(event.target);

      if (sound !== null) {
        void soundPlayer.play(sound);
      }
    };

    let hoveredItem: Element | null = null;

    const playTyping = (event: Event): void => {
      if (isPlainTextField(event.target)) {
        void soundPlayer.play('terminalTyping');
      }
    };

    const playHover = (event: PointerEvent): void => {
      const item = clickableAt(event.target);

      if (event.pointerType === 'mouse' && item !== hoveredItem) {
        hoveredItem = item;

        const note = item?.getAttribute('data-hover-rate');

        if (note !== undefined && note !== null) {
          void soundPlayer.play('hoverSpecial', Number(note));
        } else if (item !== null) {
          void soundPlayer.play('hover');
        }
      }
    };

    document.addEventListener('pointerdown', soundPlayer.prepare, { once: true });
    document.addEventListener('click', playClick);
    document.addEventListener('pointerover', playHover);
    document.addEventListener('input', playTyping);

    return () => {
      document.removeEventListener('pointerdown', soundPlayer.prepare);
      document.removeEventListener('click', playClick);
      document.removeEventListener('pointerover', playHover);
      document.removeEventListener('input', playTyping);
    };
  }, []);

  const changeSettings = useCallback(
    (changes: Partial<Settings>) => {
      // Applied now, so that the click that turns the sound on is already heard and the one that turns it off is not.
      if (changes.sound !== undefined) {
        soundPlayer.setEnabled(changes.sound);
      }

      if (changes.locale !== undefined && changes.locale !== null) {
        void soundPlayer.play(LANGUAGE_SOUNDS[changes.locale]);
      }

      if (changes.theme !== undefined) {
        void soundPlayer.play(WEATHER_SOUNDS[changes.theme]);
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
  const isHome = activeProject === undefined && route.name !== 'globe';
  const preferenceToggles = (
    <div className="orb-toggles">
      <ThemeToggle
        theme={skyTheme}
        onChange={(theme) => {
          changeSettings({ theme });
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
    <LocaleContext.Provider value={locale}>
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
            createLessonCheckWorker={createLessonCheckWorker}
            onSaveProject={handleSave}
            onSelectFile={(file) => {
              navigate({ name: 'project', projectId: activeProject.id, file });
            }}
            onChangeSettings={changeSettings}
            onBack={goHome}
          />
        ) : null}
        {route.name === 'aquarium' ? (
          <Aquarium origin={aquariumOrigin} theme={skyTheme} isSoundOn={settings.sound} onClose={goHome} />
        ) : null}
        {route.name === 'globe' ? <GlobeWallpaper onClose={goHome} /> : null}
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
            onOpenAquarium={(origin) => {
              setAquariumOrigin(origin);
              navigate({ name: 'aquarium' });
            }}
            onExportProject={downloadProject}
            onRename={(id, name) => {
              persist(projects.map((project) => (project.id === id ? { ...project, name } : project)));
            }}
            onDelete={(id) => {
              persist(removeProject(projects, id));
              clearDrafts(id);
            }}
            preferenceToggles={preferenceToggles}
            settingsButton={
              <SettingsDialog
                vision={settings.vision}
                onEraseEverything={() => {
                  eraseEverything();
                  markReturnFromSnap();
                  void soundPlayer.play('snapDust');
                  void snapAway().then(() => {
                    setTimeout(() => {
                      window.location.hash = '#/';
                      window.location.reload();
                    }, DARK_PAUSE_MILLISECONDS);
                  });
                }}
                onChange={(vision) => {
                  changeSettings({ vision });
                }}
              />
            }
          />
        ) : null}
      </TranslationContext.Provider>
    </LocaleContext.Provider>
  );
};
