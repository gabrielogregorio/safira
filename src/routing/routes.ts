export interface LessonPlace {
  lessonId: string | null;
  section: string | null;
}

export type Route =
  | { name: 'home' }
  | { name: 'new'; exampleId: string | null }
  | { name: 'aquarium' }
  | { name: 'globe' }
  | { name: 'project'; projectId: string; file: string | null; lesson?: LessonPlace };

const LESSONS_SEGMENT = 'lessons';

const decodeSegment = (segment: string): string | null => {
  try {
    return decodeURIComponent(segment);
  } catch {
    return null;
  }
};

export const parseRoute = (hash: string): Route => {
  const segments = hash.replace(/^#\/?/, '').split('/').filter(Boolean).map(decodeSegment);
  const [screen, first = null, second = null, third = null, lessonId = null, section = null] = segments;

  if (segments.includes(null)) {
    return { name: 'home' };
  }

  if (screen === 'new') {
    return { name: 'new', exampleId: first };
  }

  if (screen === 'aquarium' || screen === 'globe') {
    return { name: screen };
  }

  if (screen === 'projects' && first !== null) {
    const place = { name: 'project', projectId: first, file: second } as const;

    return third === LESSONS_SEGMENT ? { ...place, lesson: { lessonId, section } } : place;
  }

  return { name: 'home' };
};

const buildHash = (segments: (string | null)[]): string =>
  `#/${segments
    .filter((segment) => segment !== null)
    .map(encodeURIComponent)
    .join('/')}`;

export const routeToHash = (route: Route): string => {
  switch (route.name) {
    case 'home':
      return '#/';
    case 'new':
      return buildHash(['new', route.exampleId]);
    case 'aquarium':
    case 'globe':
      return buildHash([route.name]);
    case 'project':
      return buildHash([
        'projects',
        route.projectId,
        route.file,
        ...(route.lesson === undefined ? [] : [LESSONS_SEGMENT, route.lesson.lessonId, route.lesson.section]),
      ]);
  }
};
