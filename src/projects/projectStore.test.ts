import { createProject, loadProjects, MAIN_FILE, removeProject, saveProjects, upsertProject } from './projectStore';

describe('projectStore', () => {
  beforeEach(() => {
    localStorage.clear();
  });

  it('creates a project with a versioned main file', () => {
    expect(createProject('Novo')).toMatchObject({ name: 'Novo', files: { [MAIN_FILE]: '#safira 0.9\n' } });
  });

  it('keeps the projects between sessions', () => {
    const project = createProject('Novo');
    saveProjects([project]);

    expect(loadProjects()).toEqual([project]);
  });

  it('returns an empty list when nothing was saved', () => {
    expect(loadProjects()).toEqual([]);
  });

  it('survives corrupted storage', () => {
    localStorage.setItem('safira.projects.v1', '{quebrado');

    expect(loadProjects()).toEqual([]);
  });

  it('drops entries that are not projects', () => {
    localStorage.setItem('safira.projects.v1', JSON.stringify([{ nada: 1 }]));

    expect(loadProjects()).toEqual([]);
  });

  it('reports when the browser refuses to save', () => {
    vi.spyOn(Storage.prototype, 'setItem').mockImplementationOnce(() => {
      throw new Error('full');
    });

    expect(saveProjects([])).toBe(false);
  });

  it('puts the changed project first and replaces the old copy', () => {
    const first = createProject('A');
    const second = createProject('B');
    const result = upsertProject([first, second], { ...second, name: 'C' });

    expect(result.map((project) => project.name)).toEqual(['C', 'A']);
  });

  it('removes a project by id', () => {
    const project = createProject('A');

    expect(removeProject([project], project.id)).toEqual([]);
  });
});
