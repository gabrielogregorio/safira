export type Route =
  | { name: 'home' }
  | { name: 'new'; exampleId: string | null }
  | { name: 'lessons'; lessonId: string | null; section: string | null }
  | { name: 'project'; projectId: string; file: string | null };

const decodeSegment = (segment: string): string | null => {
  try {
    return decodeURIComponent(segment);
  } catch {
    return null;
  }
};

export const parseRoute = (hash: string): Route => {
  const segments = hash.replace(/^#\/?/, '').split('/').filter(Boolean).map(decodeSegment);
  const [screen, first = null, second = null] = segments;

  if (segments.includes(null)) {
    return { name: 'home' };
  }

  if (screen === 'new') {
    return { name: 'new', exampleId: first };
  }

  if (screen === 'lessons') {
    return { name: 'lessons', lessonId: first, section: second };
  }

  if (screen === 'projects' && first !== null) {
    return { name: 'project', projectId: first, file: second };
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
    case 'lessons':
      return buildHash(['lessons', route.lessonId, route.section]);
    case 'project':
      return buildHash(['projects', route.projectId, route.file]);
  }
};
