import { parseLesson } from './lessons';

const SOURCE = `# Título

Introdução.

## Olhe

Aperte.

\`\`\`safira
mostre 1

\`\`\`

## Desafio

Faça.

\`\`\`safira
# aqui
\`\`\`

\`\`\`solution
mostre 2
\`\`\`

\`\`\`check
{ "hint": "Dica", "cases": [{ "shows": ["2"] }] }
\`\`\`
`;

describe('parseLesson', () => {
  const lesson = parseLesson('aula-01', SOURCE);

  it('reads the title and steps', () => {
    expect(lesson.title).toBe('Título');
    expect(lesson.steps.map((step) => step.title)).toEqual(['Olhe', 'Desafio']);
  });

  it('keeps the code apart from the explanation', () => {
    expect(lesson.steps[0]).toMatchObject({ text: 'Aperte.', code: 'mostre 1', solution: null, check: null });
  });

  it('reads the solution and check of a challenge', () => {
    expect(lesson.steps[1]).toMatchObject({
      solution: 'mostre 2',
      check: { hint: 'Dica', cases: [{ shows: ['2'] }] },
    });
  });

  it('leaves answers out of the document', () => {
    expect(lesson.text).toContain('Introdução.');
    expect(lesson.text).toContain('# aqui');
    expect(lesson.text).not.toContain('mostre 2');
    expect(lesson.text).not.toContain('Dica');
  });
});
