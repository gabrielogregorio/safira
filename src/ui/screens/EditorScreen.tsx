import type { CSSProperties, ReactNode } from 'react';
import { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { findExampleByPrefix } from '@/content/content';
import { useTranslation } from '@/i18n/i18n';
import { formatCode } from '@/language/formatter';
import type { Locale } from '@/language/messages';
import { getAllCommands } from '@/language/phrases';
import { isSupportedVersion, SUPPORTED_VERSIONS } from '@/language/version';
import { clearDrafts, loadDrafts, saveDrafts } from '@/projects/draftStore';
import type { TreeNode } from '@/projects/fileTree';
import { folderMarkerPath, isInsideFolder, joinPath, sanitizePath, visibleFiles } from '@/projects/fileTree';
import { MAIN_FILE, type Project } from '@/projects/projectStore';
import type { RunMode } from '@/runtime/protocol';
import type { PanelName, Settings } from '@/settings/settings';
import { clampPanelSize, PANEL_LIMITS } from '@/settings/settings';
import { CodeEditor } from '@/ui/components/CodeEditor';
import { SafiraLogo } from '@/ui/components/SafiraLogo';
import { VariableInspector } from '@/ui/components/VariableInspector';
import { describeArchiveResult } from '@/ui/archiveMessages';
import { downloadProject, readArchiveFile } from '@/ui/archiveFiles';
import { ArchiveInput } from '@/ui/components/ArchiveInput';
import { FileSidebar } from '@/ui/components/FileSidebar';
import { IdeMenuBar } from '@/ui/components/IdeMenuBar';
import { Modal } from '@/ui/components/Modal';
import { Terminal } from '@/ui/components/Terminal';
import { Splitter } from '@/ui/components/Splitter';
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
  routeFile: string | null;
  settings: Settings;
  locale: Locale;
  createWorker?: WorkerFactory;
  onSaveProject: (project: Project) => void;
  onSelectFile: (file: string) => void;
  onChangeSettings: (changes: Partial<Settings>) => void;
  languageToggle: ReactNode;
  onBack: () => void;
}

type Dialog =
  | { kind: 'open' }
  | { kind: 'save-as' }
  | { kind: 'commands' }
  | { kind: 'confirm-close'; file: string }
  | { kind: 'confirm-leave' }
  | { kind: 'new-file'; folder: string | null }
  | { kind: 'new-folder'; folder: string | null }
  | { kind: 'delete-node'; node: TreeNode }
  | null;

const TOOLBAR_LOGO_SIZE = 30;
const MOBILE_PANELS: MobilePanel[] = ['files', 'code', 'output', 'variables'];
const DRAFT_DELAY_MILLISECONDS = 300;
const FUNCTION_KEYS = ['F5', 'F6', 'F7', 'F10', 'F11'];
type MobilePanel = 'files' | 'code' | 'output' | 'variables';

const restoreTabs = (project: Project, routeFile: string | null): EditorTab[] => {
  const drafts = loadDrafts(project.id);
  const routed = routeFile !== null && project.files[routeFile] !== undefined ? routeFile : null;
  const firstFile = routed ?? initialFile(project);
  const files = [...new Set([firstFile, ...Object.keys(drafts)])];

  return files.map((file) => {
    const tab = openTab(file, project.files[file] ?? '');
    const draft = drafts[file];

    return draft === undefined ? tab : { ...tab, text: draft };
  });
};

const initialFile = (project: Project): string =>
  project.files[MAIN_FILE] === undefined ? (Object.keys(project.files)[0] ?? MAIN_FILE) : MAIN_FILE;

export const EditorScreen = ({
  project,
  routeFile,
  settings,
  locale,
  createWorker = createRunnerWorker,
  onSaveProject,
  onSelectFile,
  onChangeSettings,
  languageToggle,
  onBack,
}: EditorScreenProps) => {
  const t = useTranslation();
  const [tabs, setTabs] = useState<EditorTab[]>(() => restoreTabs(project, routeFile));
  const [wasRecovered, setWasRecovered] = useState(() => Object.keys(loadDrafts(project.id)).length > 0);
  const [dialog, setDialog] = useState<Dialog>(null);
  const [cursor, setCursor] = useState({ line: 1, column: 1 });
  const [mobilePanel, setMobilePanel] = useState<MobilePanel>('code');
  const [archiveNotice, setArchiveNotice] = useState<string | null>(null);
  const archiveInput = useRef<HTMLInputElement>(null);

  const latestProject = useRef(project);
  const latestTabs = useRef(tabs);
  const activeFile = tabs.some((tab) => tab.file === routeFile) ? (routeFile as string) : (tabs[0]?.file ?? MAIN_FILE);
  const activeTab = tabs.find((tab) => tab.file === activeFile) ?? tabs[0];

  if (routeFile !== null && project.files[routeFile] !== undefined && !tabs.some((tab) => tab.file === routeFile)) {
    setTabs([...tabs, openTab(routeFile, project.files[routeFile])]);
  }

  useEffect(() => {
    latestProject.current = project;
    latestTabs.current = tabs;
  }, [project, tabs]);

  useEffect(() => {
    const timer = setTimeout(() => {
      saveDrafts(project.id, Object.fromEntries(tabs.filter(isDirty).map((tab) => [tab.file, tab.text])));
    }, DRAFT_DELAY_MILLISECONDS);

    return () => {
      clearTimeout(timer);
    };
  }, [project.id, tabs]);
  const breakpoints = useMemo(() => project.breakpoints[activeFile] ?? [], [project.breakpoints, activeFile]);

  const handleProgramFiles = useCallback(
    (files: Record<string, string>) => {
      const current = latestProject.current;
      const next = { ...files };

      for (const tab of latestTabs.current.filter(isDirty)) {
        const stored = current.files[tab.file];

        if (stored === undefined) {
          Reflect.deleteProperty(next, tab.file);
        } else {
          next[tab.file] = stored;
        }
      }

      onSaveProject({ ...current, files: next });
      setTabs((openTabs) => mergeProgramFiles(openTabs, files));
    },
    [onSaveProject],
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

  const hasBreakpoints = Object.values(project.breakpoints).some((lines) => lines.length > 0);

  const runOrResume = useCallback(
    (requested: RunMode) => {
      const mode = requested === 'run' && hasBreakpoints ? 'debug' : requested;

      if (runner.status === 'paused') {
        runner.resume(mode);
      } else if (!isRunning) {
        setMobilePanel('output');
        runner.start({ file: activeFile, files: currentFiles(), locale, mode, breakpoints: project.breakpoints });
      }
    },
    [activeFile, currentFiles, hasBreakpoints, isRunning, locale, project.breakpoints, runner],
  );

  const saveFile = useCallback(
    (file: string, tab: EditorTab) => {
      onSaveProject({ ...project, files: { ...project.files, [file]: toStoredText({ file, text: tab.text }) } });
      setTabs((current) =>
        current.map((candidate) =>
          candidate.file === tab.file ? { ...candidate, file, savedText: candidate.text } : candidate,
        ),
      );
      onSelectFile(file);
    },
    [onSaveProject, onSelectFile, project],
  );

  const openFile = useCallback(
    (file: string, stored: string) => {
      setTabs((current) => (current.some((tab) => tab.file === file) ? current : [...current, openTab(file, stored)]));
      onSelectFile(file);
      setDialog(null);
    },
    [onSelectFile],
  );

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
        onSelectFile(replacement);
      } else {
        setTabs(remaining);

        if (activeFile === file) {
          onSelectFile(remaining[0].file);
        }
      }

      setDialog(null);
    },
    [activeFile, onSelectFile, tabs],
  );

  const createFile = useCallback(
    (folder: string | null, name: string) => {
      const path = sanitizePath(joinPath(folder, withScriptExtension(name)));

      if (path === null) {
        return;
      }

      const stored = project.files[path] ?? toStoredText({ file: path, text: '' });
      onSaveProject({ ...project, files: { ...project.files, [path]: stored } });
      openFile(path, stored);
    },
    [onSaveProject, openFile, project],
  );

  const createFolder = useCallback(
    (folder: string | null, name: string) => {
      const path = sanitizePath(joinPath(folder, name));

      if (path !== null) {
        onSaveProject({ ...project, files: { ...project.files, [folderMarkerPath(path)]: '' } });
      }

      setDialog(null);
    },
    [onSaveProject, project],
  );

  const deleteNode = useCallback(
    (node: TreeNode) => {
      const isDeleted = (path: string): boolean => path === node.path || isInsideFolder(path, node.path);
      const files = Object.fromEntries(Object.entries(project.files).filter(([path]) => !isDeleted(path)));
      const remaining = tabs.filter((tab) => !isDeleted(tab.file));
      onSaveProject({ ...project, files });
      setDialog(null);

      if (remaining.length === 0) {
        const replacement = nextUntitledName(Object.keys(files));
        setTabs([openTab(replacement, '')]);
        onSelectFile(replacement);
      } else {
        setTabs(remaining);

        if (isDeleted(activeFile)) {
          onSelectFile(remaining[0].file);
        }
      }
    },
    [activeFile, onSaveProject, onSelectFile, project, tabs],
  );

  const importIntoProject = useCallback(
    async (file: File) => {
      const result = await readArchiveFile(file);

      if (result.ok) {
        onSaveProject({ ...latestProject.current, files: { ...latestProject.current.files, ...result.files } });
        setTabs((current) => mergeProgramFiles(current, result.files));
      }

      setArchiveNotice(describeArchiveResult(t, result));
    },
    [onSaveProject, t],
  );

  const resizePanel = useCallback(
    (panel: PanelName, size: number) => {
      onChangeSettings({ panels: { ...settings.panels, [panel]: clampPanelSize(panel, size) } });
    },
    [onChangeSettings, settings.panels],
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

      if (isControl && event.key === 'Enter') {
        event.preventDefault();
        event.stopPropagation();
        runOrResume('run');

        return;
      }

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

    window.addEventListener('keydown', handleKey, true);

    return () => {
      window.removeEventListener('keydown', handleKey, true);
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

  const panelLabels: Record<MobilePanel, string> = {
    files: t('Files'),
    code: t('Code'),
    output: t('Output'),
    variables: t('Variables'),
  };

  const panelStyle = {
    '--sidebar-width': `${settings.panels.sidebar}px`,
    '--output-width': `${settings.panels.output}px`,
    '--inspector-height': `${settings.panels.inspector}px`,
  } as CSSProperties;

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
        {languageToggle}
        <button
          type="button"
          className="button button-back"
          aria-label={t('Back to projects')}
          onClick={() => {
            if (tabs.some(isDirty)) {
              setDialog({ kind: 'confirm-leave' });
            } else {
              onBack();
            }
          }}>
          <span aria-hidden="true">‹</span>
          <span className="label-wide">{t('Back to projects')}</span>
        </button>
        <SafiraLogo size={TOOLBAR_LOGO_SIZE} />
        <h1 className="toolbar-title" data-fixed-text>
          {project.name}
        </h1>
        <div className="toolbar-actions">
          <button
            type="button"
            className="button button-primary"
            title="Ctrl+Enter"
            disabled={isRunning && runner.status !== 'paused'}
            onClick={() => {
              runOrResume('run');
            }}>
            {runner.status === 'paused' ? t('Continue') : t('Run')}
          </button>
          <button type="button" className="button button-stop" disabled={!isRunning} onClick={runner.stop}>
            {t('Stop')}
          </button>
        </div>
        <IdeMenuBar
          settings={settings}
          isRunning={isRunning}
          onOpenFile={() => {
            setDialog({ kind: 'open' });
          }}
          onNewTab={newTab}
          onSave={() => {
            saveFile(activeTab.file, activeTab);
          }}
          onSaveAs={() => {
            setDialog({ kind: 'save-as' });
          }}
          onFormat={() => {
            updateActiveText(formatCode(activeTab.text));
          }}
          onRun={runOrResume}
          onStop={runner.stop}
          onToggleBreakpoint={() => {
            toggleBreakpoint(cursor.line);
          }}
          onClearBreakpoints={clearBreakpoints}
          onOpenExample={(id, text) => {
            openFile(`${id}.safira`, text);
          }}
          onExportProject={() => {
            downloadProject({ name: project.name, files: currentFiles() });
          }}
          onImportArchive={() => {
            archiveInput.current?.click();
          }}
          onChangeSettings={onChangeSettings}
          onToggleFullScreen={toggleFullScreen}
          onShowCommands={() => {
            setDialog({ kind: 'commands' });
          }}
        />
      </header>

      <nav className="tab-bar" aria-label={t('Virtual files of this project')}>
        {tabs.map((tab) => (
          <div key={tab.file} className={tab.file === activeFile ? 'tab tab-active' : 'tab'}>
            <button
              type="button"
              aria-current={tab.file === activeFile ? 'page' : undefined}
              onClick={() => {
                onSelectFile(tab.file);
              }}>
              <span data-fixed-text>{tab.file}</span>
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

      <ArchiveInput
        ref={archiveInput}
        label={t('Import .zip into this project')}
        onSelect={(file) => {
          void importIntoProject(file);
        }}
      />

      {archiveNotice === null ? null : (
        <div className="alert" role="status">
          <p>{archiveNotice}</p>
          <button
            type="button"
            className="button"
            onClick={() => {
              setArchiveNotice(null);
            }}>
            {t('Close')}
          </button>
        </div>
      )}

      {wasRecovered ? (
        <div className="alert" role="status">
          <p>{t('Your unsaved work was recovered.')}</p>
          <div className="form-row">
            <button
              type="button"
              className="button"
              onClick={() => {
                setWasRecovered(false);
              }}>
              {t('Keep')}
            </button>
            <button
              type="button"
              className="button"
              onClick={() => {
                clearDrafts(project.id);
                setTabs((current) => current.map((tab) => ({ ...tab, text: tab.savedText })));
                setWasRecovered(false);
              }}>
              {t('Discard')}
            </button>
          </div>
        </div>
      ) : null}

      {isVersionSupported ? null : (
        <div className="alert" role="alert">
          {t('This script declares Safira {version}, but this IDE supports: {supported}.', {
            version: activeTab.version,
            supported: SUPPORTED_VERSIONS.join(', '),
          })}
        </div>
      )}

      <main id="content" tabIndex={-1} className={`workspace workspace-${mobilePanel}`} style={panelStyle}>
        <FileSidebar
          paths={Object.keys(project.files)}
          activeFile={activeFile}
          onOpen={(path) => {
            openFile(path, project.files[path] ?? '');
            setMobilePanel('code');
          }}
          onNewFile={(folder) => {
            setDialog({ kind: 'new-file', folder });
          }}
          onNewFolder={(folder) => {
            setDialog({ kind: 'new-folder', folder });
          }}
          onDelete={(node) => {
            setDialog({ kind: 'delete-node', node });
          }}
        />
        <Splitter
          label={t('Resize the files panel')}
          orientation="vertical"
          value={settings.panels.sidebar}
          minimum={PANEL_LIMITS.sidebar.minimum}
          maximum={PANEL_LIMITS.sidebar.maximum}
          onChange={(size) => {
            resizePanel('sidebar', size);
          }}
        />
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
        <Splitter
          label={t('Resize the output panel')}
          orientation="vertical"
          value={settings.panels.output}
          minimum={PANEL_LIMITS.output.minimum}
          maximum={PANEL_LIMITS.output.maximum}
          growsTowardStart
          onChange={(size) => {
            resizePanel('output', size);
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
            <div className="debug-bar" role="status">
              <span>{t('Paused on line {line}', { line: runner.pausedAt?.line ?? 0 })}</span>
              <button
                type="button"
                className="button"
                onClick={() => {
                  runner.resume('step');
                }}>
                {t('Next line')}
              </button>
              <button
                type="button"
                className="button"
                onClick={() => {
                  runOrResume('run');
                }}>
                {t('Continue')}
              </button>
            </div>
          ) : null}
          <Terminal
            buffer={runner.terminal}
            footer={terminalFooter()}
            isWaitingInput={runner.status === 'waiting-input'}
            onSubmitInput={runner.submitInput}
          />
          <Splitter
            label={t('Resize the variables panel')}
            orientation="horizontal"
            value={settings.panels.inspector}
            minimum={PANEL_LIMITS.inspector.minimum}
            maximum={PANEL_LIMITS.inspector.maximum}
            growsTowardStart
            onChange={(size) => {
              resizePanel('inspector', size);
            }}
          />
          <VariableInspector variables={runner.variables} />
        </div>
      </main>

      <nav className="mobile-panels" aria-label={t('Safira IDE')}>
        {MOBILE_PANELS.map((panel) => (
          <button
            key={panel}
            type="button"
            className="mobile-panel-button"
            aria-pressed={mobilePanel === panel}
            onClick={() => {
              setMobilePanel(panel);
            }}>
            {panelLabels[panel]}
          </button>
        ))}
      </nav>

      <footer className="status-bar">{t('Line {line}, column {column}', cursor)}</footer>

      {dialog?.kind === 'open' ? (
        <Modal
          title={t('Virtual files of this project')}
          onClose={() => {
            setDialog(null);
          }}>
          <ul className="file-list">
            {visibleFiles(Object.keys(currentFiles()))
              .sort((first, second) => first.localeCompare(second))
              .map((file) => (
                <li key={file}>
                  <button
                    type="button"
                    className="menu-item"
                    data-fixed-text
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
          title={t('Save as')}
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

      {dialog?.kind === 'new-file' ? (
        <TextPrompt
          title={t('New file')}
          label={t('File name')}
          initialValue=""
          onClose={() => {
            setDialog(null);
          }}
          onSubmit={(name) => {
            createFile(dialog.folder, name);
          }}
        />
      ) : null}

      {dialog?.kind === 'new-folder' ? (
        <TextPrompt
          title={t('New folder')}
          label={t('Folder name')}
          initialValue=""
          onClose={() => {
            setDialog(null);
          }}
          onSubmit={(name) => {
            createFolder(dialog.folder, name);
          }}
        />
      ) : null}

      {dialog?.kind === 'delete-node' ? (
        <Modal
          title={t('Delete this item?')}
          onClose={() => {
            setDialog(null);
          }}>
          <p>{t('"{name}" will be deleted. This cannot be undone.', { name: dialog.node.path })}</p>
          <div className="form-row">
            <button
              type="button"
              className="button"
              data-autofocus
              onClick={() => {
                setDialog(null);
              }}>
              {t('Cancel')}
            </button>
            <button
              type="button"
              className="button button-stop"
              onClick={() => {
                deleteNode(dialog.node);
              }}>
              {t('Delete')}
            </button>
          </div>
        </Modal>
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
                  clearDrafts(project.id);
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
