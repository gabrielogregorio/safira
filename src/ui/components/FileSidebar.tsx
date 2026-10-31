import * as ContextMenu from '@radix-ui/react-context-menu';
import type { ReactNode } from 'react';
import { useEffect, useRef, useState } from 'react';
import { useTranslation } from '@/i18n/i18n';
import type { FolderNode, TreeNode } from '@/projects/fileTree';
import { buildFileTree, extensionStart, isPathTaken, provisionalName, renameTarget } from '@/projects/fileTree';
import { NewFileIcon, NewFolderIcon, ProjectBadge } from './AeroIcons';
import type { SoundName } from '@/ui/sound/sounds';
import { soundPlayer } from '@/ui/sound/sounds';
import { ProjectNameField } from './ProjectNameField';

interface FileSidebarProps {
  projectName: string;
  paths: string[];
  activeFile: string;
  onRenameProject: (name: string) => void;
  onOpen: (path: string) => void;
  onCreateFile: (folder: string | null, name: string) => void;
  onCreateFolder: (folder: string | null, name: string) => void;
  onDelete: (node: TreeNode) => void;
  onRename: (node: TreeNode, path: string) => void;
  canRename: boolean;
}

interface Draft {
  kind: 'file' | 'folder';
  folder: string | null;
}

interface TreeActions {
  paths: string[];
  activeFile: string;
  draft: Draft | null;
  onOpen: (path: string) => void;
  onStartDraft: (draft: Draft) => void;
  onFinishDraft: (draft: Draft, name: string | null) => void;
  onDelete: (node: TreeNode) => void;
  renaming: string | null;
  canRename: boolean;
  onStartRename: (path: string) => void;
  onFinishRename: (node: TreeNode, name: string | null) => void;
}

interface TreeListProps extends TreeActions {
  nodes: TreeNode[];
  folder: string | null;
}

interface DraftRowProps {
  draft: Draft;
  paths: string[];
  onFinish: (draft: Draft, name: string | null) => void;
}

interface RowMenuProps {
  items: { label: string; onSelect: () => void; disabled?: boolean; sound?: SoundName }[];
  children: ReactNode;
}

interface NameInputProps {
  label: string;
  value: string;
  selectionEnd: number;
  isAllowed?: (name: string) => boolean;
  onFinish: (name: string | null) => void;
}

interface RenameRowProps {
  node: TreeNode;
  paths: string[];
  onFinish: (node: TreeNode, name: string | null) => void;
}

const FILE_EXTENSION = '.safira';
const PRESS_SETTLE_MILLISECONDS = 30;

const RowMenu = ({ items, children }: RowMenuProps) => (
  <ContextMenu.Root modal={false}>
    <ContextMenu.Trigger asChild>{children}</ContextMenu.Trigger>
    <ContextMenu.Portal>
      <ContextMenu.Content
        className="menubar-content"
        collisionPadding={8}
        onCloseAutoFocus={(event) => {
          event.preventDefault();
        }}>
        {items.map((item) => (
          <ContextMenu.Item
            key={item.label}
            className="menubar-item"
            disabled={item.disabled}
            data-sound={item.sound}
            onSelect={item.onSelect}>
            {item.label}
          </ContextMenu.Item>
        ))}
      </ContextMenu.Content>
    </ContextMenu.Portal>
  </ContextMenu.Root>
);

const NameInput = ({ label, value, selectionEnd, isAllowed = () => true, onFinish }: NameInputProps) => {
  const t = useTranslation();
  const input = useRef<HTMLInputElement>(null);
  const isFinished = useRef(false);
  const isPressing = useRef(false);
  const latestOnFinish = useRef(onFinish);
  const [isRejected, setIsRejected] = useState(false);

  useEffect(() => {
    latestOnFinish.current = onFinish;
  }, [onFinish]);

  useEffect(() => {
    input.current?.focus();
    input.current?.setSelectionRange(0, selectionEnd);

    const notePress = (): void => {
      isPressing.current = true;
    };

    const noteRelease = (): void => {
      isPressing.current = false;
    };

    document.addEventListener('pointerdown', notePress, true);
    document.addEventListener('pointerup', noteRelease, true);

    return () => {
      document.removeEventListener('pointerdown', notePress, true);
      document.removeEventListener('pointerup', noteRelease, true);
    };
  }, [selectionEnd]);

  const finish = (name: string | null): void => {
    if (!isFinished.current) {
      isFinished.current = true;
      latestOnFinish.current(name);
    }
  };

  // Finishing moves the rows of the tree. In the middle of a press, that would take the click away from what was pressed.
  const finishAfterPress = (name: string | null): void => {
    const finishNow = (): void => {
      finish(name);
    };

    if (isPressing.current) {
      document.addEventListener('click', finishNow, { once: true });
      document.addEventListener(
        'pointerup',
        () => {
          setTimeout(finishNow, PRESS_SETTLE_MILLISECONDS);
        },
        { once: true },
      );
    } else {
      finishNow();
    }
  };

  const typedName = (): string => input.current?.value.trim() || value;

  return (
    <div className="tree-name-field">
      <div className="tree-row tree-row-active">
        <input
          ref={input}
          className="tree-input"
          aria-label={label}
          aria-invalid={isRejected}
          defaultValue={value}
          spellCheck={false}
          onChange={() => {
            setIsRejected(false);
          }}
          onBlur={() => {
            finishAfterPress(isAllowed(typedName()) ? typedName() : null);
          }}
          onKeyDown={(event) => {
            if (event.key === 'Enter' && isAllowed(typedName())) {
              finish(typedName());
            } else if (event.key === 'Enter') {
              setIsRejected(true);
            } else if (event.key === 'Escape') {
              finish(null);
            }
          }}
        />
      </div>
      {isRejected ? (
        <p className="tree-input-error" role="alert">
          {t('This name is invalid or already in use')}
        </p>
      ) : null}
    </div>
  );
};

const DraftRow = ({ draft, paths, onFinish }: DraftRowProps) => {
  const t = useTranslation();
  const isFile = draft.kind === 'file';
  const [provisional] = useState(() =>
    isFile
      ? provisionalName(t('new-file'), FILE_EXTENSION, paths, draft.folder)
      : provisionalName(t('new-folder'), '', paths, draft.folder),
  );

  return (
    <li>
      <NameInput
        label={isFile ? t('File name') : t('Folder name')}
        value={provisional}
        selectionEnd={provisional.length}
        onFinish={(name) => {
          onFinish(draft, name);
        }}
      />
    </li>
  );
};

const RenameRow = ({ node, paths, onFinish }: RenameRowProps) => {
  const t = useTranslation();
  const isFile = node.kind === 'file';

  return (
    <NameInput
      label={isFile ? t('File name') : t('Folder name')}
      value={node.name}
      selectionEnd={isFile ? extensionStart(node.name) : node.name.length}
      isAllowed={(name) => {
        const target = renameTarget(node, name);

        return target !== null && (target === node.path || !isPathTaken(paths, target));
      }}
      onFinish={(name) => {
        onFinish(node, name);
      }}
    />
  );
};

const FolderRow = ({ node, ...actions }: TreeActions & { node: FolderNode }) => {
  const t = useTranslation();
  const [isClosed, setIsClosed] = useState(false);
  const isOpen = !isClosed || actions.draft?.folder === node.path;

  return (
    <li>
      <RowMenu
        items={[
          {
            label: t('New file'),
            sound: 'fileCreate',
            onSelect: () => {
              actions.onStartDraft({ kind: 'file', folder: node.path });
            },
          },
          {
            label: t('New folder'),
            sound: 'folderCreate',
            onSelect: () => {
              actions.onStartDraft({ kind: 'folder', folder: node.path });
            },
          },
          {
            label: t('Rename'),
            sound: 'renameStart',
            disabled: !actions.canRename,
            onSelect: () => {
              actions.onStartRename(node.path);
            },
          },
          {
            label: t('Delete'),
            onSelect: () => {
              actions.onDelete(node);
            },
          },
        ]}>
        {actions.renaming === node.path ? (
          <RenameRow node={node} paths={actions.paths} onFinish={actions.onFinishRename} />
        ) : (
          <div className="tree-row">
            <button
              type="button"
              className="tree-name"
              aria-expanded={isOpen}
              onClick={() => {
                setIsClosed(isOpen);
              }}>
              <span aria-hidden="true">{isOpen ? '▾' : '▸'} </span>
              <span data-fixed-text>{node.name}</span>
            </button>
          </div>
        )}
      </RowMenu>
      {isOpen ? <TreeList nodes={node.children} folder={node.path} {...actions} /> : null}
    </li>
  );
};

const TreeList = ({ nodes, folder, ...actions }: TreeListProps) => {
  const t = useTranslation();

  return (
    <ul className="tree-list">
      {nodes.map((node) =>
        node.kind === 'folder' ? (
          <FolderRow key={node.path} node={node} {...actions} />
        ) : (
          <li key={node.path}>
            <RowMenu
              items={[
                {
                  label: t('Rename'),
                  sound: 'renameStart',
                  disabled: !actions.canRename,
                  onSelect: () => {
                    actions.onStartRename(node.path);
                  },
                },
                {
                  label: t('Delete'),
                  onSelect: () => {
                    actions.onDelete(node);
                  },
                },
              ]}>
              {actions.renaming === node.path ? (
                <RenameRow node={node} paths={actions.paths} onFinish={actions.onFinishRename} />
              ) : (
                <div className={node.path === actions.activeFile ? 'tree-row tree-row-active' : 'tree-row'}>
                  <button
                    type="button"
                    className="tree-name"
                    data-sound="tab"
                    aria-current={node.path === actions.activeFile ? 'page' : undefined}
                    onClick={() => {
                      actions.onOpen(node.path);
                    }}>
                    <span data-fixed-text>{node.name}</span>
                  </button>
                </div>
              )}
            </RowMenu>
          </li>
        ),
      )}
      {actions.draft?.folder === folder ? (
        <DraftRow draft={actions.draft} paths={actions.paths} onFinish={actions.onFinishDraft} />
      ) : null}
    </ul>
  );
};

export const FileSidebar = ({
  projectName,
  paths,
  activeFile,
  onRenameProject,
  onOpen,
  onCreateFile,
  onCreateFolder,
  onDelete,
  onRename,
  canRename,
}: FileSidebarProps) => {
  const t = useTranslation();
  const [draft, setDraft] = useState<Draft | null>(null);
  const [renaming, setRenaming] = useState<string | null>(null);

  const finishRename = (node: TreeNode, name: string | null): void => {
    setRenaming(null);
    const target = name === null ? null : renameTarget(node, name);

    if (target !== null && target !== node.path) {
      void soundPlayer.play('rename');
      onRename(node, target);
    }
  };

  const finishDraft = (finished: Draft, name: string | null): void => {
    setDraft(null);

    if (name !== null) {
      (finished.kind === 'file' ? onCreateFile : onCreateFolder)(finished.folder, name);
    }
  };

  return (
    <nav className="file-sidebar" aria-label={t('Files')}>
      <h1 className="file-sidebar-project" data-fixed-text>
        <ProjectBadge />
        <ProjectNameField name={projectName} onRename={onRenameProject} />
      </h1>
      <header className="file-sidebar-header">
        <h2>{t('Files')}</h2>
        <div className="aero-group">
          <button
            type="button"
            className="aero-button"
            data-sound="fileCreate"
            aria-label={t('New file')}
            title={t('New file')}
            onClick={() => {
              setDraft({ kind: 'file', folder: null });
            }}>
            <NewFileIcon />
          </button>
          <button
            type="button"
            className="aero-button"
            data-sound="folderCreate"
            aria-label={t('New folder')}
            title={t('New folder')}
            onClick={() => {
              setDraft({ kind: 'folder', folder: null });
            }}>
            <NewFolderIcon />
          </button>
        </div>
      </header>
      <TreeList
        nodes={buildFileTree(paths)}
        folder={null}
        paths={paths}
        activeFile={activeFile}
        draft={draft}
        onOpen={onOpen}
        onStartDraft={setDraft}
        onFinishDraft={finishDraft}
        onDelete={onDelete}
        renaming={renaming}
        canRename={canRename}
        onStartRename={setRenaming}
        onFinishRename={finishRename}
      />
    </nav>
  );
};
