import * as ContextMenu from '@radix-ui/react-context-menu';
import type { DragEvent, KeyboardEvent as ReactKeyboardEvent, MouseEvent, ReactNode } from 'react';
import { useEffect, useRef, useState } from 'react';
import type { Translate } from '@/i18n/i18n';
import { useTranslation } from '@/i18n/i18n';
import type { DropPlace, FolderNode, MoveDirection, PlannedMove, TreeNode } from '@/projects/fileTree';
import {
  buildFileTree,
  extensionStart,
  isPathTaken,
  moveDestinations,
  planMove,
  planStep,
  provisionalName,
  renameTarget,
} from '@/projects/fileTree';
import { Modal } from './Modal';
import { NewFileIcon, NewFolderIcon, ProjectBadge, TreeFileIcon, TreeFolderIcon } from './AeroIcons';
import type { SoundName } from '@/ui/sound/sounds';
import { soundPlayer } from '@/ui/sound/sounds';
import { ProjectNameField } from './ProjectNameField';

interface FileSidebarProps {
  projectName: string;
  paths: string[];
  order?: string[];
  activeFile: string;
  onRenameProject: (name: string) => void;
  onOpen: (path: string) => void;
  onCreateFile: (folder: string | null, name: string) => void;
  onCreateFolder: (folder: string | null, name: string) => void;
  onDelete: (node: TreeNode) => void;
  onRename: (node: TreeNode, path: string) => void;
  onDownload: (node: TreeNode) => void;
  onMove: (node: TreeNode, plan: PlannedMove) => void;
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
  onDownload: (node: TreeNode) => void;
  onStep: (node: TreeNode, direction: MoveDirection) => void;
  canStep: (node: TreeNode, direction: MoveDirection) => boolean;
  onStartMove: (node: TreeNode) => void;
  renaming: string | null;
  canRename: boolean;
  onStartRename: (path: string) => void;
  onFinishRename: (node: TreeNode, name: string | null) => void;
  dragProps: (node: TreeNode) => DragProps;
}

interface DragProps {
  draggable: boolean;
  'data-drop'?: DropPlace;
  onDragStart: (event: DragEvent) => void;
  onDragEnd: () => void;
  onDragOver: (event: DragEvent) => void;
  onDrop: (event: DragEvent) => void;
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

interface RowMenuItem {
  label: string;
  onSelect: () => void;
  disabled?: boolean;
  sound?: SoundName;
  shortcut?: string;
}

interface RowMenuProps {
  items: RowMenuItem[];
  children: ReactNode;
}

interface MoveChoicesProps {
  node: TreeNode;
  paths: string[];
  order: string[];
  onChoose: (plan: PlannedMove) => void;
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
const MOVE_SHORTCUTS = 'Alt+ArrowUp Alt+ArrowDown Alt+M';
const FOLDER_EDGE = 0.25;
const FILE_MIDDLE = 0.5;

const dropPlaceAt = (event: DragEvent, node: TreeNode): DropPlace => {
  const { top, height } = event.currentTarget.getBoundingClientRect();
  const position = (event.clientY - top) / height;
  const edge = node.kind === 'folder' ? FOLDER_EDGE : FILE_MIDDLE;

  if (position < edge) {
    return 'before';
  }

  return position > 1 - edge ? 'after' : 'inside';
};

// The menu of a row lives on its context menu event, so this button asks for it the way a right click does.
const isTouchScreen = (): boolean =>
  typeof window.matchMedia === 'function' && window.matchMedia('(pointer: coarse)').matches;

const openRowMenu = (event: MouseEvent<HTMLButtonElement>): void => {
  const { left, bottom } = event.currentTarget.getBoundingClientRect();
  event.currentTarget.dispatchEvent(
    new window.MouseEvent('contextmenu', { bubbles: true, cancelable: true, clientX: left, clientY: bottom }),
  );
};

const RowMenuButton = ({ name }: { name: string }) => {
  const t = useTranslation();
  const label = t('More actions for {name}', { name });

  return (
    <button type="button" className="tree-more" aria-label={label} title={label} onClick={openRowMenu}>
      ⋮
    </button>
  );
};

const RowMenu = ({ items, children }: RowMenuProps) => {
  const isOpen = useRef(false);

  return (
    <ContextMenu.Root
      modal={false}
      onOpenChange={(open) => {
        isOpen.current = open;
      }}>
      <ContextMenu.Trigger
        asChild
        onClickCapture={(event) => {
          // Lifting the finger after a long press clicks the row, which would open the file and hide the menu.
          if (isOpen.current) {
            event.preventDefault();
            event.stopPropagation();
          }
        }}>
        {children}
      </ContextMenu.Trigger>
      <ContextMenu.Portal>
        <ContextMenu.Content
          className="menubar-content"
          collisionPadding={8}
          onCloseAutoFocus={(event) => {
            event.preventDefault();
          }}
          onFocusOutside={(event) => {
            // Lifting the finger focuses the row, and a touch outside still closes the menu.
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
              {item.shortcut === undefined ? null : <span className="menubar-shortcut">{item.shortcut}</span>}
            </ContextMenu.Item>
          ))}
        </ContextMenu.Content>
      </ContextMenu.Portal>
    </ContextMenu.Root>
  );
};

const moveItems = (t: Translate, actions: TreeActions, node: TreeNode): RowMenuItem[] => [
  {
    label: t('Move up'),
    shortcut: 'Alt+↑',
    disabled: !actions.canStep(node, 'up'),
    onSelect: () => {
      actions.onStep(node, 'up');
    },
  },
  {
    label: t('Move down'),
    shortcut: 'Alt+↓',
    disabled: !actions.canStep(node, 'down'),
    onSelect: () => {
      actions.onStep(node, 'down');
    },
  },
  {
    label: t('Move to...'),
    shortcut: 'Alt+M',
    disabled: !actions.canRename,
    onSelect: () => {
      actions.onStartMove(node);
    },
  },
];

const moveKeys =
  (actions: TreeActions, node: TreeNode) =>
  (event: ReactKeyboardEvent): void => {
    if (!event.altKey || !actions.canRename) {
      return;
    }

    if (event.key === 'ArrowUp' || event.key === 'ArrowDown') {
      event.preventDefault();
      actions.onStep(node, event.key === 'ArrowUp' ? 'up' : 'down');
    } else if (event.key.toLowerCase() === 'm') {
      event.preventDefault();
      actions.onStartMove(node);
    }
  };

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
          ...moveItems(t, actions, node),
          {
            label: t('Download'),
            sound: 'export',
            onSelect: () => {
              actions.onDownload(node);
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
          <div className="tree-row" {...actions.dragProps(node)}>
            <button
              type="button"
              className="tree-name"
              aria-expanded={isOpen}
              aria-keyshortcuts={MOVE_SHORTCUTS}
              data-tree-path={node.path}
              onKeyDown={moveKeys(actions, node)}
              onClick={() => {
                setIsClosed(isOpen);
              }}>
              <span className="tree-arrow" aria-hidden="true">
                {isOpen ? '▾' : '▸'}
              </span>
              <TreeFolderIcon isOpen={isOpen} />
              <span className="tree-label" data-fixed-text>
                {node.name}
              </span>
            </button>
            <RowMenuButton name={node.name} />
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
                ...moveItems(t, actions, node),
                {
                  label: t('Download'),
                  sound: 'export',
                  onSelect: () => {
                    actions.onDownload(node);
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
                <div
                  className={node.path === actions.activeFile ? 'tree-row tree-row-active' : 'tree-row'}
                  {...actions.dragProps(node)}>
                  <button
                    type="button"
                    className="tree-name"
                    data-sound="tab"
                    aria-current={node.path === actions.activeFile ? 'page' : undefined}
                    aria-keyshortcuts={MOVE_SHORTCUTS}
                    data-tree-path={node.path}
                    onKeyDown={moveKeys(actions, node)}
                    onClick={() => {
                      actions.onOpen(node.path);
                    }}>
                    <TreeFileIcon isScript={node.name.endsWith(FILE_EXTENSION)} />
                    <span className="tree-label" data-fixed-text>
                      {node.name}
                    </span>
                  </button>
                  <RowMenuButton name={node.name} />
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

const MoveChoices = ({ node, paths, order, onChoose }: MoveChoicesProps) => {
  const t = useTranslation();
  const destinations = moveDestinations(paths, order, node);

  if (destinations.length === 0) {
    return <p>{t('There is no folder to move this to.')}</p>;
  }

  return (
    <ul className="move-choices">
      {destinations.map(({ folder, plan }) => (
        <li key={folder?.path ?? ''}>
          <button
            type="button"
            className="button"
            data-fixed-text={folder === null ? undefined : true}
            onClick={() => {
              onChoose(plan);
            }}>
            {folder === null ? t('Project root') : folder.path}
          </button>
        </li>
      ))}
    </ul>
  );
};

export const FileSidebar = ({
  projectName,
  paths,
  order = [],
  activeFile,
  onRenameProject,
  onOpen,
  onCreateFile,
  onCreateFolder,
  onDelete,
  onRename,
  onDownload,
  onMove,
  canRename,
}: FileSidebarProps) => {
  const t = useTranslation();
  const [draft, setDraft] = useState<Draft | null>(null);
  const [renaming, setRenaming] = useState<string | null>(null);

  const [dragged, setDragged] = useState<TreeNode | null>(null);

  // F2 renames what is selected, as in a file manager. The selection is the open file, wherever the focus is.
  useEffect(() => {
    const renameSelected = (event: KeyboardEvent): void => {
      if (event.key === 'F2' && canRename) {
        event.preventDefault();
        void soundPlayer.play('renameStart');
        setRenaming(activeFile);
      }
    };

    window.addEventListener('keydown', renameSelected);

    return () => {
      window.removeEventListener('keydown', renameSelected);
    };
  }, [activeFile, canRename]);

  const [dropTarget, setDropTarget] = useState<{ path: string; place: DropPlace } | null>(null);
  const [moving, setMoving] = useState<TreeNode | null>(null);
  const [movedMessage, setMovedMessage] = useState('');
  const sidebar = useRef<HTMLElement>(null);
  const focusAfterMove = useRef<string | null>(null);

  // After the modal gives the focus back, so the moved item keeps it even under a new path.
  useEffect(() => {
    const path = focusAfterMove.current;

    if (path === null) {
      return undefined;
    }

    focusAfterMove.current = null;
    const timer = setTimeout(() => {
      sidebar.current?.querySelector<HTMLElement>(`[data-tree-path="${CSS.escape(path)}"]`)?.focus();
    });

    return () => {
      clearTimeout(timer);
    };
  }, [paths, order]);

  const moveWithKeyboard = (node: TreeNode, plan: PlannedMove): void => {
    focusAfterMove.current = plan.target;
    setMovedMessage(t('Moved: {name}', { name: node.name }));
    onMove(node, plan);
  };

  const step = (node: TreeNode, direction: MoveDirection): void => {
    const plan = planStep(paths, order, node, direction);

    if (plan !== null) {
      moveWithKeyboard(node, plan);
    }
  };

  const endDrag = (): void => {
    setDragged(null);
    setDropTarget(null);
  };

  const finishDrop = (event: DragEvent, plan: PlannedMove | null): void => {
    event.preventDefault();
    event.stopPropagation();

    if (dragged !== null && plan !== null) {
      onMove(dragged, plan);
    }

    endDrag();
  };

  const planDrop = (anchor: TreeNode | null, place: DropPlace): PlannedMove | null =>
    dragged === null ? null : planMove(paths, order, dragged, anchor, place);

  const dragProps = (node: TreeNode): DragProps => ({
    // On a touch screen, holding a draggable row starts a drag, which cancels the long press of the menu.
    draggable: canRename && !isTouchScreen(),
    'data-drop': dropTarget?.path === node.path ? dropTarget.place : undefined,
    onDragStart: (event) => {
      event.stopPropagation();
      event.dataTransfer.effectAllowed = 'move';
      event.dataTransfer.setData('text/plain', node.path);
      setDragged(node);
    },
    onDragEnd: endDrag,
    onDragOver: (event) => {
      const place = dropPlaceAt(event, node);

      event.stopPropagation();

      if (planDrop(node, place) === null) {
        setDropTarget(null);
      } else {
        event.preventDefault();
        setDropTarget({ path: node.path, place });
      }
    },
    onDrop: (event) => {
      finishDrop(event, planDrop(node, dropPlaceAt(event, node)));
    },
  });

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
    <nav
      ref={sidebar}
      className="file-sidebar"
      aria-label={t('Files')}
      onDragOver={(event) => {
        setDropTarget(null);

        if (planDrop(null, 'inside') !== null) {
          event.preventDefault();
        }
      }}
      onDrop={(event) => {
        finishDrop(event, planDrop(null, 'inside'));
      }}>
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
        nodes={buildFileTree(paths, order)}
        folder={null}
        paths={paths}
        activeFile={activeFile}
        draft={draft}
        onOpen={onOpen}
        onStartDraft={setDraft}
        onFinishDraft={finishDraft}
        onDelete={onDelete}
        onDownload={onDownload}
        onStep={step}
        canStep={(node, direction) => canRename && planStep(paths, order, node, direction) !== null}
        onStartMove={setMoving}
        renaming={renaming}
        canRename={canRename}
        onStartRename={setRenaming}
        onFinishRename={finishRename}
        dragProps={dragProps}
      />
      <p className="visually-hidden" role="status">
        {movedMessage}
      </p>
      {moving === null ? null : (
        <Modal
          title={t('Move {name} to', { name: moving.name })}
          onClose={() => {
            setMoving(null);
          }}>
          <MoveChoices
            node={moving}
            paths={paths}
            order={order}
            onChoose={(plan) => {
              setMoving(null);
              moveWithKeyboard(moving, plan);
            }}
          />
        </Modal>
      )}
    </nav>
  );
};
