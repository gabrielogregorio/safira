import { useState } from 'react';
import { useTranslation } from '@/i18n/i18n';
import type { FolderNode, TreeNode } from '@/projects/fileTree';
import { buildFileTree } from '@/projects/fileTree';

interface FileSidebarProps {
  paths: string[];
  activeFile: string;
  onOpen: (path: string) => void;
  onNewFile: (folder: string | null) => void;
  onNewFolder: (folder: string | null) => void;
  onDelete: (node: TreeNode) => void;
}

interface TreeListProps extends Omit<FileSidebarProps, 'paths'> {
  nodes: TreeNode[];
}

const FolderRow = ({ node, ...actions }: Omit<TreeListProps, 'nodes'> & { node: FolderNode }) => {
  const t = useTranslation();
  const [isOpen, setIsOpen] = useState(true);

  return (
    <li>
      <div className="tree-row">
        <button
          type="button"
          className="tree-name"
          aria-expanded={isOpen}
          onClick={() => {
            setIsOpen(!isOpen);
          }}>
          <span aria-hidden="true">{isOpen ? '▾' : '▸'} </span>
          {node.name}
        </button>
        <button
          type="button"
          className="tree-action"
          aria-label={t('New file in {name}', { name: node.name })}
          title={t('New file in {name}', { name: node.name })}
          onClick={() => {
            actions.onNewFile(node.path);
          }}>
          +
        </button>
        <button
          type="button"
          className="tree-action"
          aria-label={t('New folder in {name}', { name: node.name })}
          title={t('New folder in {name}', { name: node.name })}
          onClick={() => {
            actions.onNewFolder(node.path);
          }}>
          ⊞
        </button>
        <button
          type="button"
          className="tree-action"
          aria-label={t('Delete {name}', { name: node.name })}
          title={t('Delete {name}', { name: node.name })}
          onClick={() => {
            actions.onDelete(node);
          }}>
          ×
        </button>
      </div>
      {isOpen ? <TreeList nodes={node.children} {...actions} /> : null}
    </li>
  );
};

const TreeList = ({ nodes, ...actions }: TreeListProps) => {
  const t = useTranslation();

  return (
    <ul className="tree-list">
      {nodes.map((node) =>
        node.kind === 'folder' ? (
          <FolderRow key={node.path} node={node} {...actions} />
        ) : (
          <li key={node.path}>
            <div className={node.path === actions.activeFile ? 'tree-row tree-row-active' : 'tree-row'}>
              <button
                type="button"
                className="tree-name"
                aria-current={node.path === actions.activeFile ? 'page' : undefined}
                onClick={() => {
                  actions.onOpen(node.path);
                }}>
                {node.name}
              </button>
              <button
                type="button"
                className="tree-action"
                aria-label={t('Delete {name}', { name: node.name })}
                title={t('Delete {name}', { name: node.name })}
                onClick={() => {
                  actions.onDelete(node);
                }}>
                ×
              </button>
            </div>
          </li>
        ),
      )}
    </ul>
  );
};

export const FileSidebar = ({ paths, ...actions }: FileSidebarProps) => {
  const t = useTranslation();

  return (
    <nav className="file-sidebar" aria-label={t('Files')}>
      <header className="file-sidebar-header">
        <h2>{t('Files')}</h2>
        <button
          type="button"
          className="button button-small"
          onClick={() => {
            actions.onNewFile(null);
          }}>
          {t('New file')}
        </button>
        <button
          type="button"
          className="button button-small"
          onClick={() => {
            actions.onNewFolder(null);
          }}>
          {t('New folder')}
        </button>
      </header>
      <TreeList nodes={buildFileTree(paths)} {...actions} />
    </nav>
  );
};
