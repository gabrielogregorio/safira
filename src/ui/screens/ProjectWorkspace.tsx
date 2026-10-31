import type { ComponentProps } from 'react';
import { useProjectHistory } from '@/ui/hooks/useProjectHistory';
import { EditorScreen } from './EditorScreen';

type ProjectWorkspaceProps = Omit<ComponentProps<typeof EditorScreen>, 'history'>;

// The editor starts again on every jump in time, and this part stays to remember where it is.
export const ProjectWorkspace = ({ project, onSaveProject, ...editorProps }: ProjectWorkspaceProps) => {
  const history = useProjectHistory(project, onSaveProject);

  return (
    <EditorScreen
      key={history.generation}
      {...editorProps}
      project={history.shownProject}
      history={history}
      onSaveProject={history.saveProject}
    />
  );
};
