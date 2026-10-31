import * as ContextMenu from '@radix-ui/react-context-menu';
import type { ReactNode } from 'react';
import { useEffect, useRef, useState } from 'react';
import { useTranslation } from '@/i18n/i18n';
import type { FolderNode, TreeNode } from '@/projects/fileTree';
import { buildFileTree, provisionalName } from '@/projects/fileTree';
import { NewFileIcon, NewFolderIcon } from './AeroIcons';

interface FileSidebarProps {
  paths: string[];
  activeFile: string;
  onOpen: (path: string) => void;
  onCreateFile: (folder: string | null, name: string) => void;
  onCreateFolder: (folder: string | null, name: string) => void;
  onDelete: (node: TreeNode) => void;
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
  items: { label: string; onSelect: () => void }[];
  children: ReactNode;
}

const FILE_EXTENSION = '.safira';

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
          <ContextMenu.Item key={item.label} className="menubar-item" onSelect={item.onSelect}>
            {item.label}
          </ContextMenu.Item>
        ))}
      </ContextMenu.Content>
    </ContextMenu.Portal>
  </ContextMenu.Root>
);

const DraftRow = ({ draft, paths, onFinish }: DraftRowProps) => {
  const t = useTranslation();
  const input = useRef<HTMLInputElement>(null);
  const isFinished = useRef(false);
  const isFile = draft.kind === 'file';
  const [provisional] = useState(() =>
    isFile
      ? provisionalName(t('new-file'), FILE_EXTENSION, paths, draft.folder)
      : provisionalName(t('new-folder'), '', paths, draft.folder),
  );

  useEffect(() => {
    input.current?.focus();
    input.current?.select();
  }, []);

  const finish = (name: string | null): void => {
    if (!isFinished.current) {
      isFinished.current = true;
      onFinish(draft, name);
    }
  };

  const keepTypedName = (): void => {
    finish(input.current?.value.trim() || provisional);
  };

  return (
    <li>
      <div className="tree-row tree-row-active">
        <input
          ref={input}
          className="tree-input"
          aria-label={isFile ? t('File name') : t('Folder name')}
          defaultValue={provisional}
          spellCheck={false}
          onBlur={keepTypedName}
          onKeyDown={(event) => {
            if (event.key === 'Enter') {
              keepTypedName();
            }

            if (event.key === 'Escape') {
              finish(null);
            }
          }}
        />
      </div>
    </li>
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
            onSelect: () => {
              actions.onStartDraft({ kind: 'file', folder: node.path });
            },
          },
          {
            label: t('New folder'),
            onSelect: () => {
              actions.onStartDraft({ kind: 'folder', folder: node.path });
            },
          },
          {
            label: t('Delete'),
            onSelect: () => {
              actions.onDelete(node);
            },
          },
        ]}>
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
                  label: t('Delete'),
                  onSelect: () => {
                    actions.onDelete(node);
                  },
                },
              ]}>
              <div className={node.path === actions.activeFile ? 'tree-row tree-row-active' : 'tree-row'}>
                <button
                  type="button"
                  className="tree-name"
                  data-sound="open"
                  aria-current={node.path === actions.activeFile ? 'page' : undefined}
                  onClick={() => {
                    actions.onOpen(node.path);
                  }}>
                  <span data-fixed-text>{node.name}</span>
                </button>
              </div>
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
  paths,
  activeFile,
  onOpen,
  onCreateFile,
  onCreateFolder,
  onDelete,
}: FileSidebarProps) => {
  const t = useTranslation();
  const [draft, setDraft] = useState<Draft | null>(null);

  const finishDraft = (finished: Draft, name: string | null): void => {
    setDraft(null);

    if (name !== null) {
      (finished.kind === 'file' ? onCreateFile : onCreateFolder)(finished.folder, name);
    }
  };

  return (
    <nav className="file-sidebar" aria-label={t('Files')}>
      <header className="file-sidebar-header">
        <h2>{t('Files')}</h2>
        <div className="aero-group">
          <button
            type="button"
            className="aero-button"
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
      />
    </nav>
  );
};
