import { useCallback, useEffect, useMemo, useState } from 'react';
import { examples, findExampleByPrefix } from '@/content/content';
import { useTranslation } from '@/i18n/i18n';
import { formatCode } from '@/language/formatter';
import type { Locale } from '@/language/messages';
import { getAllCommands } from '@/language/phrases';
import { isSupportedVersion, SUPPORTED_VERSIONS } from '@/language/version';
import { MAIN_FILE, type Project } from '@/projects/projectStore';
import type { RunMode } from '@/runtime/protocol';
import type { Settings, ThemeId } from '@/settings/settings';
import { clampFontSize } from '@/settings/settings';
import { CodeEditor } from '@/ui/components/CodeEditor';
import { DebugPanel } from '@/ui/components/DebugPanel';
import { Menu, MenuItem } from '@/ui/components/Menu';
import { Modal } from '@/ui/components/Modal';
import { Terminal } from '@/ui/components/Terminal';
import { TextPrompt } from '@/ui/components/TextPrompt';
import type { EditorTab } from '@/ui/editorTabs';
import {
  isDirty,
  isScript,
  mergeProgramFiles,
  nextUntitledName,
  openTab,
  toStoredText,
  withScriptExtension,
} from '@/ui/editorTabs';
import type { WorkerFactory } from '@/ui/hooks/useRunner';
import { createRunnerWorker, useRunner } from '@/ui/hooks/useRunner';

interface EditorScreenProps {
  project: Project;
  settings: Settings;
  locale: Locale;
  createWorker?: WorkerFactory;
  onSaveProject: (project: Project) => void;
  onChangeSettings: (changes: Partial<Settings>) => void;
  onBack: () => void;
}

type Dialog =
  | { kind: 'open' }
  | { kind: 'save-as' }
  | { kind: 'commands' }
  | { kind: 'confirm-close'; file: string }
  | { kind: 'confirm-leave' }
  | null;

const FONT_STEP = 1;
const FUNCTION_KEYS = ['F5', 'F6', 'F7', 'F10', 'F11'];
const BUG_REPORT_URL = 'https://github.com/safira-lang/safira-ide/issues';
const BLOG_URL = 'https://safiralang.blogspot.com/';
const THEME_IDS: ThemeId[] = ['simple', 'dark', 'light'];

const initialFile = (project: Project): string =>
  project.files[MAIN_FILE] === undefined ? (Object.keys(project.files)[0] ?? MAIN_FILE) : MAIN_FILE;

export const EditorScreen = ({
  project,
  settings,
  locale,
  createWorker = createRunnerWorker,
  onSaveProject,
  onChangeSettings,
  onBack,
}: EditorScreenProps) => {
  const t = useTranslation();
  const [tabs, setTabs] = useState<EditorTab[]>(() => {
    const file = initialFile(project);

    return [openTab(file, project.files[file] ?? '')];
  });
  const [activeFile, setActiveFile] = useState(tabs[0]?.file ?? MAIN_FILE);
  const [dialog, setDialog] = useState<Dialog>(null);
  const [cursor, setCursor] = useState({ line: 1, column: 1 });

  const activeTab = tabs.find((tab) => tab.file === activeFile) ?? tabs[0];
  const breakpoints = useMemo(() => project.breakpoints[activeFile] ?? [], [project.breakpoints, activeFile]);

  const handleProgramFiles = useCallback(
    (files: Record<string, string>) => {
      onSaveProject({ ...project, files: { ...project.files, ...files } });
      setTabs((current) => mergeProgramFiles(current, files));
    },
    [onSaveProject, project],
  );

  const runner = useRunner(handleProgramFiles, createWorker);
  const isRunning = runner.status !== 'idle';

  const currentFiles = useCallback(() => {
    const files = { ...project.files };

    for (const tab of tabs) {
      files[tab.file] = toStoredText(tab);
    }

    return files;
  }, [project.files, tabs]);

  const startRun = useCallback(
    (mode: RunMode) => {
      runner.start({ file: activeFile, files: currentFiles(), locale, mode, breakpoints: project.breakpoints });
    },
    [activeFile, currentFiles, locale, project.breakpoints, runner],
  );

  const runOrResume = useCallback(
    (mode: RunMode) => {
      if (runner.status === 'paused') {
        runner.resume(mode);
      } else if (!isRunning) {
        startRun(mode);
      }
    },
    [isRunning, runner, startRun],
  );

  const saveFile = useCallback(
    (file: string, tab: EditorTab) => {
      onSaveProject({ ...project, files: { ...project.files, [file]: toStoredText({ file, text: tab.text }) } });
      setTabs((current) =>
        current.map((candidate) =>
          candidate.file === tab.file ? { ...candidate, file, savedText: candidate.text } : candidate,
        ),
      );
      setActiveFile(file);
    },
    [onSaveProject, project],
  );

  const openFile = useCallback((file: string, stored: string) => {
    setTabs((current) => (current.some((tab) => tab.file === file) ? current : [...current, openTab(file, stored)]));
    setActiveFile(file);
    setDialog(null);
  }, []);

  const newTab = useCallback(() => {
    const file = nextUntitledName([...Object.keys(project.files), ...tabs.map((tab) => tab.file)]);
    openFile(file, toStoredText({ file, text: '' }));
  }, [openFile, project.files, tabs]);

  const closeTab = useCallback(
    (file: string) => {
      const remaining = tabs.filter((tab) => tab.file !== file);

      if (remaining.length === 0) {
        const replacement = nextUntitledName([]);
        setTabs([openTab(replacement, '')]);
        setActiveFile(replacement);
      } else {
        setTabs(remaining);

        if (activeFile === file) {
          setActiveFile(remaining[0].file);
        }
      }

      setDialog(null);
    },
    [activeFile, tabs],
  );

  const toggleBreakpoint = useCallback(
    (line: number) => {
      const lines = breakpoints.includes(line)
        ? breakpoints.filter((candidate) => candidate !== line)
        : [...breakpoints, line];
      const next = { ...project.breakpoints, [activeFile]: lines };
      onSaveProject({ ...project, breakpoints: next });
      runner.updateBreakpoints(next);
    },
    [activeFile, breakpoints, onSaveProject, project, runner],
  );

  const clearBreakpoints = useCallback(() => {
    onSaveProject({ ...project, breakpoints: {} });
    runner.updateBreakpoints({});
  }, [onSaveProject, project, runner]);

  const updateActiveText = useCallback(
    (text: string) => {
      setTabs((current) => current.map((tab) => (tab.file === activeFile ? { ...tab, text } : tab)));
    },
    [activeFile],
  );

  const toggleFullScreen = useCallback(() => {
    if (document.fullscreenElement === null) {
      void document.documentElement.requestFullscreen();
    } else {
      void document.exitFullscreen();
    }
  }, []);

  useEffect(() => {
    const handleKey = (event: KeyboardEvent): void => {
      const key = event.key.toLowerCase();
      const isControl = event.ctrlKey || event.metaKey;

      if (FUNCTION_KEYS.includes(event.key) || (isControl && ['s', 'o', 'n'].includes(key))) {
        event.preventDefault();
      }

      if (event.key === 'F5') {
        runOrResume('run');
      } else if (event.key === 'F6') {
        runOrResume('step');
      } else if (event.key === 'F7') {
        runOrResume('debug');
      } else if (event.key === 'F10') {
        toggleBreakpoint(cursor.line);
      } else if (event.key === 'F11') {
        toggleFullScreen();
      } else if (isControl && key === 's' && event.shiftKey) {
        setDialog({ kind: 'save-as' });
      } else if (isControl && key === 's' && activeTab !== undefined) {
        saveFile(activeTab.file, activeTab);
      } else if (isControl && key === 'o') {
        setDialog({ kind: 'open' });
      } else if (isControl && key === 'n') {
        newTab();
      }
    };

    window.addEventListener('keydown', handleKey);

    return () => {
      window.removeEventListener('keydown', handleKey);
    };
  }, [activeTab, cursor.line, newTab, runOrResume, saveFile, toggleBreakpoint, toggleFullScreen]);

  useEffect(() => {
    const warnBeforeLeaving = (event: BeforeUnloadEvent): void => {
      if (tabs.some(isDirty)) {
        event.preventDefault();
      }
    };

    window.addEventListener('beforeunload', warnBeforeLeaving);

    return () => {
      window.removeEventListener('beforeunload', warnBeforeLeaving);
    };
  }, [tabs]);

  if (activeTab === undefined) {
    return null;
  }

  const failure = runner.failure;
  const failureExample =
    failure?.example === null || failure === null ? undefined : findExampleByPrefix(failure.example);
  const isVersionSupported = !isScript(activeTab.file) || isSupportedVersion(activeTab.version);
  const themeLabels: Record<ThemeId, string> = { simple: t('Simple'), dark: t('Dark'), light: t('Light') };

  const terminalFooter = (): string | null => {
    if (runner.wasStopped) {
      return t('Execution stopped');
    }

    return runner.duration === null || failure !== null
      ? null
      : t('Script finished in {seconds} seconds', { seconds: runner.duration.toFixed(3) });
  };

  return (
    <div className="editor-screen">
      <header className="toolbar">
        <button
          type="button"
          className="button"
          onClick={() => {
            if (tabs.some(isDirty)) {
              setDialog({ kind: 'confirm-leave' });
            } else {
              onBack();
            }
          }}>
          {t('Back to projects')}
        </button>
        <h1 className="toolbar-title">{project.name}</h1>
        <nav className="menu-bar" aria-label={t('Safira IDE')}>
          <Menu label={t('File')}>
            <MenuItem
              label={t('Open file (Ctrl+O)')}
              onSelect={() => {
                setDialog({ kind: 'open' });
              }}
            />
            <MenuItem label={t('New tab (Ctrl+N)')} onSelect={newTab} />
            <MenuItem
              label={t('Save (Ctrl+S)')}
              onSelect={() => {
                saveFile(activeTab.file, activeTab);
              }}
            />
            <MenuItem
              label={t('Save as (Ctrl+Shift+S)')}
              onSelect={() => {
                setDialog({ kind: 'save-as' });
              }}
            />
          </Menu>
          <Menu label={t('Run')}>
            <MenuItem
              label={t('Run all (F5)')}
              onSelect={() => {
                runOrResume('run');
              }}
            />
            <MenuItem
              label={t('Run line by line (F6)')}
              onSelect={() => {
                runOrResume('step');
              }}
            />
            <MenuItem
              label={t('Run to breakpoint (F7)')}
              onSelect={() => {
                runOrResume('debug');
              }}
            />
            <MenuItem label={t('Stop execution')} disabled={!isRunning} onSelect={runner.stop} />
            <MenuItem
              label={t('Toggle breakpoint (F10)')}
              onSelect={() => {
                toggleBreakpoint(cursor.line);
              }}
            />
            <MenuItem label={t('Clear breakpoints')} onSelect={clearBreakpoints} />
          </Menu>
          <Menu label={t('Examples')}>
            {examples.map((example) => (
              <MenuItem
                key={example.id}
                label={example.title}
                onSelect={() => {
                  openFile(`${example.id}.safira`, example.text);
                }}
              />
            ))}
          </Menu>
          <Menu label={t('Interface')}>
            {THEME_IDS.map((theme) => (
              <MenuItem
                key={theme}
                label={`${t('Theme')}: ${themeLabels[theme]}`}
                onSelect={() => {
                  onChangeSettings({ theme });
                }}
              />
            ))}
            {THEME_IDS.map((theme) => (
              <MenuItem
                key={theme}
                label={`${t('Syntax colors')}: ${themeLabels[theme]}`}
                onSelect={() => {
                  onChangeSettings({ syntax: theme });
                }}
              />
            ))}
            <MenuItem
              label={t('Increase font')}
              onSelect={() => {
                onChangeSettings({ fontSize: clampFontSize(settings.fontSize + FONT_STEP) });
              }}
            />
            <MenuItem
              label={t('Decrease font')}
              onSelect={() => {
                onChangeSettings({ fontSize: clampFontSize(settings.fontSize - FONT_STEP) });
              }}
            />
            <MenuItem label={t('Full screen (F11)')} onSelect={toggleFullScreen} />
          </Menu>
          <Menu label={t('Help')}>
            <MenuItem
              label={t('Available commands')}
              onSelect={() => {
                setDialog({ kind: 'commands' });
              }}
            />
            <MenuItem
              label={t('Report a bug')}
              onSelect={() => {
                window.open(BUG_REPORT_URL, '_blank', 'noopener');
              }}
            />
            <MenuItem
              label={t('Community blog')}
              onSelect={() => {
                window.open(BLOG_URL, '_blank', 'noopener');
              }}
            />
          </Menu>
        </nav>
        <div className="toolbar-actions">
          <button
            type="button"
            className="button button-primary"
            disabled={isRunning}
            onClick={() => {
              startRun('run');
            }}>
            {t('Run')}
          </button>
          <button type="button" className="button" disabled={!isRunning} onClick={runner.stop}>
            {t('Stop execution')}
          </button>
          <button
            type="button"
            className="button"
            onClick={() => {
              updateActiveText(formatCode(activeTab.text));
            }}>
            {t('Format code')}
          </button>
        </div>
      </header>

      <nav className="tab-bar" aria-label={t('Virtual files of this project')}>
        {tabs.map((tab) => (
          <div key={tab.file} className={tab.file === activeFile ? 'tab tab-active' : 'tab'}>
            <button
              type="button"
              aria-current={tab.file === activeFile ? 'page' : undefined}
              onClick={() => {
                setActiveFile(tab.file);
              }}>
              {tab.file}
              {isDirty(tab) ? <span title={t('Not saved')}> ●</span> : null}
            </button>
            <button
              type="button"
              className="tab-close"
              aria-label={t('Close tab {name}', { name: tab.file })}
              onClick={() => {
                if (isDirty(tab)) {
                  setDialog({ kind: 'confirm-close', file: tab.file });
                } else {
                  closeTab(tab.file);
                }
              }}>
              ×
            </button>
          </div>
        ))}
      </nav>

      {isVersionSupported ? null : (
        <div className="alert" role="alert">
          {t('This script declares Safira {version}, but this IDE supports: {supported}.', {
            version: activeTab.version,
            supported: SUPPORTED_VERSIONS.join(', '),
          })}
        </div>
      )}

      <main id="content" className="workspace">
        <CodeEditor
          key={activeTab.file}
          value={activeTab.text}
          label={t('Code editor')}
          fontSize={settings.fontSize}
          breakpoints={breakpoints}
          debugLine={runner.pausedAt?.file === activeFile ? runner.pausedAt.line : null}
          errorLine={failure?.file === activeFile ? failure.line : null}
          onChange={updateActiveText}
          onToggleBreakpoint={toggleBreakpoint}
          onCursorChange={(line, column) => {
            setCursor({ line, column });
          }}
        />
        <div className="output-column">
          {failure === null ? null : (
            <div className="alert alert-error" role="alert">
              <p>
                {t('Line {line}', { line: failure.line })}: {failure.message}
              </p>
              <div className="form-row">
                {failureExample === undefined ? null : (
                  <button
                    type="button"
                    className="button"
                    onClick={() => {
                      openFile(`${failureExample.id}.safira`, failureExample.text);
                    }}>
                    {t('See an example')}
                  </button>
                )}
                <button type="button" className="button" onClick={runner.dismissFailure}>
                  {t('Close')}
                </button>
              </div>
            </div>
          )}
          {runner.status === 'paused' ? (
            <DebugPanel
              variables={runner.variables}
              onNextLine={() => {
                runner.resume('step');
              }}
              onContinue={() => {
                runner.resume('debug');
              }}
            />
          ) : null}
          <Terminal
            buffer={runner.terminal}
            footer={terminalFooter()}
            isWaitingInput={runner.status === 'waiting-input'}
            onSubmitInput={runner.submitInput}
          />
        </div>
      </main>

      <footer className="status-bar">{t('Line {line}, column {column}', cursor)}</footer>

      {dialog?.kind === 'open' ? (
        <Modal
          title={t('Virtual files of this project')}
          onClose={() => {
            setDialog(null);
          }}>
          <ul className="file-list">
            {Object.keys(currentFiles())
              .sort((first, second) => first.localeCompare(second))
              .map((file) => (
                <li key={file}>
                  <button
                    type="button"
                    className="menu-item"
                    onClick={() => {
                      openFile(file, currentFiles()[file] ?? '');
                    }}>
                    {file}
                  </button>
                </li>
              ))}
          </ul>
        </Modal>
      ) : null}

      {dialog?.kind === 'save-as' ? (
        <TextPrompt
          title={t('Save as (Ctrl+Shift+S)')}
          label={t('File name')}
          initialValue={activeTab.file}
          onClose={() => {
            setDialog(null);
          }}
          onSubmit={(name) => {
            saveFile(withScriptExtension(name), activeTab);
            setDialog(null);
          }}
        />
      ) : null}

      {dialog?.kind === 'commands' ? (
        <Modal
          title={t('Available commands')}
          onClose={() => {
            setDialog(null);
          }}>
          <ul className="command-list">
            {getAllCommands()
              .filter(([, definition]) => definition.phrases.length > 0)
              .map(([key, definition]) => (
                <li key={key}>{definition.phrases.join(', ')}</li>
              ))}
          </ul>
        </Modal>
      ) : null}

      {dialog?.kind === 'confirm-close' || dialog?.kind === 'confirm-leave' ? (
        <Modal
          title={t('Do you want to save your program?')}
          onClose={() => {
            setDialog(null);
          }}>
          <div className="form-row">
            <button
              type="button"
              className="button button-primary"
              onClick={() => {
                if (dialog.kind === 'confirm-close') {
                  const tab = tabs.find((candidate) => candidate.file === dialog.file);

                  if (tab !== undefined) {
                    saveFile(tab.file, tab);
                  }

                  closeTab(dialog.file);
                } else {
                  const files = currentFiles();
                  onSaveProject({ ...project, files });
                  onBack();
                }
              }}>
              {t('Save')}
            </button>
            <button
              type="button"
              className="button"
              onClick={() => {
                if (dialog.kind === 'confirm-close') {
                  closeTab(dialog.file);
                } else {
                  onBack();
                }
              }}>
              {t("Don't save")}
            </button>
            <button
              type="button"
              className="button"
              onClick={() => {
                setDialog(null);
              }}>
              {t('Cancel')}
            </button>
          </div>
        </Modal>
      ) : null}
    </div>
  );
};
