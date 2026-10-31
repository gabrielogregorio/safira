import type { CSSProperties } from 'react';
import { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { findExampleByPrefix } from '@/content/content';
import { useTranslation } from '@/i18n/i18n';
import { formatCode } from '@/language/formatter';
import type { Locale } from '@/language/messages';
import { getAllCommands } from '@/language/phrases';
import { addScriptVersion, isSupportedVersion, SUPPORTED_VERSIONS } from '@/language/version';
import { clearDrafts, loadDrafts } from '@/projects/draftStore';
import type { PlannedMove, TreeNode } from '@/projects/fileTree';
import {
  filesOfFolder,
  folderMarkerPath,
  isInsideFolder,
  joinPath,
  movePath,
  parentFolder,
  provisionalName,
  sanitizePath,
} from '@/projects/fileTree';
import { MAIN_FILE, type Project } from '@/projects/projectStore';
import type { LessonPlace } from '@/routing/routes';
import { routeToHash } from '@/routing/routes';
import type { RunMode } from '@/runtime/protocol';
import type { PanelName, Settings } from '@/settings/settings';
import { clampPanelSize, PANEL_LIMITS } from '@/settings/settings';
import { BackIcon, PlayIcon, StopIcon } from '@/ui/components/AeroIcons';
import { CloseButton } from '@/ui/components/CloseButton';
import { CodeEditor } from '@/ui/components/CodeEditor';
import { VariableInspector } from '@/ui/components/VariableInspector';
import { describeArchiveResult } from '@/ui/archiveMessages';
import { downloadFile, downloadProject, readArchiveFile } from '@/ui/archiveFiles';
import { ArchiveInput } from '@/ui/components/ArchiveInput';
import { FileSidebar } from '@/ui/components/FileSidebar';
import { LessonsDialog } from '@/ui/components/LessonsDialog';
import { IdeMenuBar } from '@/ui/components/IdeMenuBar';
import { Modal } from '@/ui/components/Modal';
import { Terminal } from '@/ui/components/Terminal';
import { Splitter } from '@/ui/components/Splitter';
import type { EditorTab } from '@/ui/editorTabs';
import {
  isDirty,
  isScript,
  mergeProgramFiles,
  moveTab,
  nextUntitledName,
  openTab,
  toStoredText,
  withScriptExtension,
} from '@/ui/editorTabs';
import type { WorkerFactory } from '@/ui/hooks/useRunner';
import { createRunnerWorker, useRunner } from '@/ui/hooks/useRunner';
import { soundPlayer } from '@/ui/sound/sounds';

interface EditorScreenProps {
  project: Project;
  routeFile: string | null;
  routeLesson?: LessonPlace;
  settings: Settings;
  locale: Locale;
  createWorker?: WorkerFactory;
  onSaveProject: (project: Project) => void;
  onSelectFile: (file: string) => void;
  onChangeLesson: (file: string, lesson: LessonPlace) => void;
  onChangeSettings: (changes: Partial<Settings>) => void;
  onBack: () => void;
}

type Dialog = { kind: 'commands' } | { kind: 'delete-node'; node: TreeNode } | null;

const MOBILE_PANELS: MobilePanel[] = ['files', 'code', 'output', 'variables'];
const AUTOSAVE_MILLISECONDS = 300;
const SCRIPT_EXTENSION = '.safira';
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
  routeLesson,
  settings,
  locale,
  createWorker = createRunnerWorker,
  onSaveProject,
  onSelectFile,
  onChangeLesson,
  onChangeSettings,
  onBack,
}: EditorScreenProps) => {
  const t = useTranslation();
  const [tabs, setTabs] = useState<EditorTab[]>(() => restoreTabs(project, routeFile));
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
    void soundPlayer.play('ideOpen');
  }, []);

  useEffect(() => {
    latestProject.current = project;
    latestTabs.current = tabs;
  }, [project, tabs]);

  // There is no saving by hand: what is typed reaches the project after a short pause, or when leaving.
  const saveOpenTabs = useCallback(() => {
    const dirtyTabs = latestTabs.current.filter(isDirty);

    if (dirtyTabs.length === 0) {
      return;
    }

    const storedTabs = new Map(dirtyTabs.map((tab) => [tab.file, tab.text]));
    const markSaved = (tab: EditorTab): EditorTab => {
      const text = storedTabs.get(tab.file);

      return text === undefined ? tab : { ...tab, savedText: text };
    };
    const files = { ...latestProject.current.files };

    for (const tab of dirtyTabs) {
      files[tab.file] = toStoredText(tab);
    }

    latestTabs.current = latestTabs.current.map(markSaved);
    setTabs((current) => current.map(markSaved));
    clearDrafts(latestProject.current.id);
    onSaveProject({ ...latestProject.current, files });
  }, [onSaveProject]);

  useEffect(() => {
    const timer = setTimeout(saveOpenTabs, AUTOSAVE_MILLISECONDS);

    return () => {
      clearTimeout(timer);
    };
  }, [saveOpenTabs, tabs]);

  useEffect(() => {
    window.addEventListener('pagehide', saveOpenTabs);

    return () => {
      window.removeEventListener('pagehide', saveOpenTabs);
      saveOpenTabs();
    };
  }, [saveOpenTabs]);

  const importableScripts = useMemo(
    () => Object.fromEntries(Object.entries(project.files).filter(([path]) => isScript(path) && path !== activeFile)),
    [activeFile, project.files],
  );
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
        void soundPlayer.play('run');
        runner.resume(mode);
      } else if (!isRunning) {
        void soundPlayer.play('run');
        setMobilePanel('output');
        runner.start({ file: activeFile, files: currentFiles(), locale, mode, breakpoints: project.breakpoints });
      }
    },
    [activeFile, currentFiles, hasBreakpoints, isRunning, locale, project.breakpoints, runner],
  );

  useEffect(() => {
    if (runner.failure !== null) {
      void soundPlayer.play('error');
    }
  }, [runner.failure]);

  const stopProgram = useCallback(() => {
    void soundPlayer.play('stop');
    soundPlayer.stopTones();
    runner.stop();
  }, [runner]);

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

  const relocateNode = useCallback(
    (node: TreeNode, target: string, order: string[]) => {
      const moved = (path: string): string => movePath(path, node.path, target);
      const moveKeys = <Value,>(entries: Record<string, Value>): Record<string, Value> =>
        Object.fromEntries(Object.entries(entries).map(([path, value]) => [moved(path), value]));
      const files = moveKeys(project.files);
      const source = parentFolder(node.path);

      // A folder only exists through what is inside it, so the one left empty needs its marker.
      if (source !== null && !Object.keys(files).some((path) => isInsideFolder(path, source))) {
        files[folderMarkerPath(source)] = '';
      }

      onSaveProject({ ...project, files, breakpoints: moveKeys(project.breakpoints), order });
      setTabs((current) => current.map((tab) => moveTab(tab, moved(tab.file))));

      if (moved(activeFile) !== activeFile) {
        onSelectFile(moved(activeFile));
      }
    },
    [activeFile, onSaveProject, onSelectFile, project],
  );

  const renameNode = useCallback(
    (node: TreeNode, target: string) => {
      relocateNode(
        node,
        target,
        (project.order ?? []).map((path) => movePath(path, node.path, target)),
      );
    },
    [project.order, relocateNode],
  );

  const moveNode = useCallback(
    (node: TreeNode, { target, order }: PlannedMove) => {
      void soundPlayer.play('move');
      relocateNode(node, target, order);
    },
    [relocateNode],
  );

  const downloadNode = useCallback(
    (node: TreeNode) => {
      const files = currentFiles();

      if (node.kind === 'file') {
        downloadFile(node.name, files[node.path] ?? '');
      } else {
        downloadProject({ name: node.name, files: filesOfFolder(files, node.path) });
      }
    },
    [currentFiles],
  );

  const openLessonCode = useCallback(
    (lessonId: string, code: string) => {
      const source = addScriptVersion(code);
      const paths = Object.keys(project.files);
      const existing = paths.find((path) => project.files[path] === source);
      const path = existing ?? provisionalName(lessonId, SCRIPT_EXTENSION, paths, null);

      if (existing === undefined) {
        onSaveProject({ ...project, files: { ...project.files, [path]: source } });
      }

      openFile(path, source);
      setMobilePanel('code');
    },
    [onSaveProject, openFile, project],
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
      void soundPlayer.play('breakpoint');
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

      if (FUNCTION_KEYS.includes(event.key) || (isControl && ['s', 'n'].includes(key))) {
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
      } else if (isControl && key === 's') {
        saveOpenTabs();
      } else if (isControl && key === 'n') {
        newTab();
      }
    };

    window.addEventListener('keydown', handleKey, true);

    return () => {
      window.removeEventListener('keydown', handleKey, true);
    };
  }, [cursor.line, newTab, runOrResume, saveOpenTabs, toggleBreakpoint, toggleFullScreen]);

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

  const runLabel = runner.status === 'paused' ? t('Continue') : t('Run');

  const lessonHref = (lessonId: string, section: string | null): string =>
    routeToHash({ name: 'project', projectId: project.id, file: activeFile, lesson: { lessonId, section } });

  return (
    <div className="editor-screen">
      {routeLesson === undefined ? null : (
        <LessonsDialog
          lessonId={routeLesson.lessonId}
          section={routeLesson.section}
          readLessons={settings.readLessons}
          lessonHref={lessonHref}
          onMarkRead={(id) => {
            if (!settings.readLessons.includes(id)) {
              onChangeSettings({ readLessons: [...settings.readLessons, id] });
            }
          }}
          onOpenCode={openLessonCode}
          onClose={() => {
            onSelectFile(activeFile);
          }}
        />
      )}
      <header className="toolbar">
        <button
          type="button"
          className="aero-button"
          aria-label={t('Back to projects')}
          title={t('Back to projects')}
          onClick={onBack}>
          <BackIcon />
        </button>
        <div className="toolbar-actions">
          <button
            type="button"
            className="aero-button aero-button-run"
            aria-label={runLabel}
            title={`${runLabel} (Ctrl+Enter)`}
            disabled={isRunning && runner.status !== 'paused'}
            onClick={() => {
              runOrResume('run');
            }}>
            <PlayIcon />
          </button>
          <button
            type="button"
            className="aero-button aero-button-stop"
            aria-label={t('Stop')}
            title={t('Stop')}
            disabled={!isRunning}
            onClick={stopProgram}>
            <StopIcon />
          </button>
        </div>
        <IdeMenuBar
          settings={settings}
          locale={locale}
          isRunning={isRunning}
          onNewTab={newTab}
          onFormat={() => {
            void soundPlayer.play('format');
            updateActiveText(formatCode(activeTab.text));
          }}
          onRun={runOrResume}
          onStop={stopProgram}
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
          onOpenLessons={() => {
            onChangeLesson(activeFile, { lessonId: null, section: null });
          }}
        />
      </header>

      <nav className="tab-bar" aria-label={t('Virtual files of this project')}>
        {tabs.map((tab) => (
          <div key={tab.file} className={tab.file === activeFile ? 'tab tab-active' : 'tab'}>
            <button
              type="button"
              data-sound="tab"
              aria-current={tab.file === activeFile ? 'page' : undefined}
              onClick={() => {
                onSelectFile(tab.file);
              }}>
              <span data-fixed-text>{tab.file}</span>
            </button>
            <button
              type="button"
              className="tab-close"
              data-sound="modalClose"
              aria-label={t('Close tab {name}', { name: tab.file })}
              onClick={() => {
                saveOpenTabs();
                closeTab(tab.file);
              }}>
              ×
            </button>
          </div>
        ))}
        <label className="suggestions-toggle" title={t('Press Tab to accept the gray text')}>
          <input
            type="checkbox"
            checked={settings.suggestions}
            onChange={(event) => {
              // Played here: by the time the click reaches the document, the state has already changed.
              void soundPlayer.play(event.target.checked ? 'suggestionsOn' : 'suggestionsOff');
              onChangeSettings({ suggestions: event.target.checked });
            }}
          />
          {t('Smart suggestions')}
        </label>
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
          <CloseButton
            onClick={() => {
              setArchiveNotice(null);
            }}
          />
        </div>
      )}

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
          projectName={project.name}
          paths={Object.keys(project.files)}
          order={project.order}
          activeFile={activeFile}
          onRenameProject={(name) => {
            onSaveProject({ ...project, name });
          }}
          onOpen={(path) => {
            openFile(path, project.files[path] ?? '');
            setMobilePanel('code');
          }}
          onCreateFile={createFile}
          onCreateFolder={createFolder}
          onDelete={(node) => {
            setDialog({ kind: 'delete-node', node });
          }}
          onRename={renameNode}
          onMove={moveNode}
          onDownload={downloadNode}
          canRename={!isRunning}
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
          codeFont={settings.codeFont}
          suggestions={settings.suggestions}
          locale={locale}
          scripts={importableScripts}
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
                <CloseButton onClick={runner.dismissFailure} />
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

      {dialog?.kind === 'delete-node' ? (
        <Modal
          openSound="alert"
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
              data-sound="delete"
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
    </div>
  );
};
