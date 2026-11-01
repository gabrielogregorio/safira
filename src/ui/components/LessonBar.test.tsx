import { fireEvent, render, screen, within } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { lessonsOf } from '@/content/content';
import { stepKey } from '@/lessons/lessonPlace';
import type { LessonPlace } from '@/settings/settings';
import { LessonBar } from './LessonBar';

const lessons = lessonsOf('en-us');
const firstLesson = lessons[0];
const lessonId = firstLesson.id;
const allOfFirstLesson = firstLesson.steps.map((_step, step) => stepKey({ lessonId, step }));

const setup = (place: LessonPlace, progress: string[] = allOfFirstLesson) => {
  const onOpen = vi.fn();
  render(<LessonBar lessons={lessons} place={place} progress={progress} onOpen={onOpen} />);

  return onOpen;
};

describe('LessonBar', () => {
  it('goes back one step', async () => {
    const onOpen = setup({ lessonId, step: 1 });
    await userEvent.click(screen.getByRole('button', { name: 'Previous step' }));

    expect(onOpen).toHaveBeenCalledExactlyOnceWith({ lessonId, step: 0 });
  });

  it('goes forward one step when the current one is done', async () => {
    const onOpen = setup({ lessonId, step: 0 });
    await userEvent.click(screen.getByRole('button', { name: 'Next step' }));

    expect(onOpen).toHaveBeenCalledExactlyOnceWith({ lessonId, step: 1 });
  });

  it('jumps to a step from its dot', async () => {
    const onOpen = setup({ lessonId, step: 0 });
    const title = firstLesson.steps[1].title;
    await userEvent.click(screen.getByRole('button', { name: `Step 2: ${title} (done)` }));

    expect(onOpen).toHaveBeenCalledExactlyOnceWith({ lessonId, step: 1 });
  });

  it('ignores a choice that is not a lesson', () => {
    const onOpen = setup({ lessonId, step: 0 });
    fireEvent.change(screen.getByRole('combobox', { name: 'Choose a lesson' }), { target: { value: 'nothing' } });

    expect(onOpen).not.toHaveBeenCalled();
  });

  it('shows no steps for a lesson that no longer exists', () => {
    setup({ lessonId: 'gone', step: 0 });

    expect(within(screen.getByRole('list', { name: 'Lesson steps' })).queryAllByRole('button')).toEqual([]);
    expect(screen.getByRole('button', { name: 'Previous step' })).toBeDisabled();
    expect(screen.getByRole('button', { name: 'Next step' })).toBeDisabled();
  });
});
