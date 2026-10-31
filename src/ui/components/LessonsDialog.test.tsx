import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { lessonsOf } from '@/content/content';
import { LessonsDialog } from './LessonsDialog';

const tutorials = lessonsOf('en-us');

const setup = (lessonId: string | null = null, readLessons: string[] = []) => {
  const actions = { onMarkRead: vi.fn(), onOpenCode: vi.fn(), onClose: vi.fn() };
  render(
    <LessonsDialog
      lessonId={lessonId}
      section={null}
      readLessons={readLessons}
      lessonHref={(id, section) => `#/${id}/${section ?? ''}`}
      {...actions}
    />,
  );

  return actions;
};

describe('LessonsDialog', () => {
  it('starts on the first lesson when none is chosen or the address is unknown', () => {
    setup('nao-existe');

    expect(screen.getByRole('heading', { name: tutorials[0].title })).toBeInTheDocument();
    expect(screen.queryByRole('link', { name: 'Previous' })).not.toBeInTheDocument();
  });

  it('shows the chosen lesson and its neighbors', () => {
    setup(tutorials[1].id);

    expect(screen.getByRole('heading', { name: tutorials[1].title })).toBeInTheDocument();
    expect(screen.getByRole('link', { name: 'Previous' })).toHaveAttribute('href', `#/${tutorials[0].id}/`);
    expect(screen.getByRole('link', { name: 'Next' })).toHaveAttribute('href', `#/${tutorials[2].id}/`);
  });

  it('marks what was read and shows it', async () => {
    const { onMarkRead } = setup(tutorials[1].id, [tutorials[0].id]);

    expect(screen.getByRole('link', { name: `${tutorials[0].title} (Read)` })).toBeInTheDocument();

    await userEvent.click(screen.getByRole('link', { name: 'Next' }));

    expect(onMarkRead).toHaveBeenCalledWith(tutorials[1].id);
  });

  it('hands over the code with its lesson', async () => {
    const { onOpenCode } = setup('aula-02-exibicao');
    await userEvent.click(screen.getAllByRole('button', { name: 'Open in the IDE' })[0]);

    expect(onOpenCode).toHaveBeenCalledExactlyOnceWith('aula-02-exibicao', expect.stringContaining('print'));
  });

  it('closes like any modal', async () => {
    const { onClose } = setup();
    await userEvent.keyboard('{Escape}');

    expect(onClose).toHaveBeenCalled();
  });
});
