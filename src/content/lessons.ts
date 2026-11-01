import type { LessonCheck } from '@/lessons/lessonCheck';

export interface LessonStep {
  title: string;
  text: string;
  code: string;
  solution: string | null;
  check: LessonCheck | null;
}

export interface Lesson {
  id: string;
  title: string;
  steps: LessonStep[];
}

const FENCE = /```(safira|solution|check)\n([\s\S]*?)```\n?/g;
const TITLE = /^# (.+)$/m;

const readFence = (section: string, name: string): string | null => {
  const fence = [...section.matchAll(FENCE)].find((match) => match[1] === name);

  return fence === undefined ? null : fence[2].trimEnd();
};

const parseStep = (section: string): LessonStep => {
  const [title, ...lines] = section.split('\n');
  const body = lines.join('\n');
  const check = readFence(body, 'check');

  return {
    title: title.trim(),
    text: body.replace(FENCE, '').trim(),
    code: readFence(body, 'safira') ?? '',
    solution: readFence(body, 'solution'),
    check: check === null ? null : (JSON.parse(check) as LessonCheck),
  };
};

export const parseLesson = (id: string, source: string): Lesson => {
  const [head, ...sections] = source.split(/^## /m);

  return {
    id,
    title: TITLE.exec(head)?.[1].trim() ?? id,
    steps: sections.map(parseStep),
  };
};
