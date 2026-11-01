import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { lessonsOf } from '@/content/content';
import { stepKey } from '@/lessons/lessonPlace';
import type { LessonPlace } from '@/settings/settings';
import { LessonPager } from './LessonPager';

const lessons = lessonsOf('en-us');
const PAGE_SIZE = 6;
const allStepsOf = (index: number) =>
  lessons[index].steps.map((_step, step) => stepKey({ lessonId: lessons[index].id, step }));

const setup = (place: LessonPlace, progress: string[] = []) => {
  const onOpen = vi.fn();
  render(<LessonPager lessons={lessons} place={place} progress={progress} onOpen={onOpen} />);

  return onOpen;
};

const numbers = () =>
  screen
    .getAllByRole('button')
    .map((button) => button.textContent)
    .filter((text) => /\d/.test(text));

describe('LessonPager', () => {
  it('shows only one page of lessons', () => {
    setup({ lessonId: lessons[0].id, step: 0 });

    expect(numbers()).toEqual(['1', '2', '3', '4', '5', '6']);
  });

  it('starts on the page of the current lesson', () => {
    setup({ lessonId: lessons[PAGE_SIZE + 1].id, step: 0 });

    expect(numbers()).toEqual(['7', '8', '9', '10', '11', '12']);
    expect(screen.getByRole('button', { name: `Lesson 8: ${lessons[7].title}` })).toHaveAttribute(
      'aria-current',
      'true',
    );
  });

  it('turns the pages up to the last lesson and back', async () => {
    setup({ lessonId: lessons[0].id, step: 0 });
    const next = screen.getByRole('button', { name: 'Next lessons' });
    const previous = screen.getByRole('button', { name: 'Previous lessons' });

    expect(previous).toBeDisabled();

    await userEvent.click(next);
    await userEvent.click(next);

    expect(numbers()).toEqual(['13', '14']);
    expect(next).toBeDisabled();

    await userEvent.click(previous);

    expect(numbers()).toEqual(['7', '8', '9', '10', '11', '12']);
  });

  it('opens a lesson where it stopped', async () => {
    const onOpen = setup({ lessonId: lessons[0].id, step: 0 }, [stepKey({ lessonId: lessons[1].id, step: 0 })]);
    await userEvent.click(screen.getByRole('button', { name: `Lesson 2: ${lessons[1].title}` }));

    expect(onOpen).toHaveBeenCalledExactlyOnceWith({ lessonId: lessons[1].id, step: 1 });
  });

  it('marks a finished lesson in its name, not only in its color', () => {
    setup({ lessonId: lessons[0].id, step: 0 }, allStepsOf(1));

    expect(screen.getByRole('button', { name: `Lesson 2: ${lessons[1].title} (done)` })).toHaveClass(
      'lesson-page-done',
    );
  });

  it('survives a saved place that no longer exists', () => {
    setup({ lessonId: 'gone', step: 0 });

    expect(numbers()).toEqual(['1', '2', '3', '4', '5', '6']);
  });
});
