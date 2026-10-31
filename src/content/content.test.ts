import { parse } from '@/language/parser';
import { readScriptVersion } from '@/language/version';
import { examples, findExampleByPrefix, tutorials } from './content';

describe('bundled content', () => {
  it('ships every example and tutorial', () => {
    expect(examples).toHaveLength(35);
    expect(tutorials).toHaveLength(12);
  });

  it('builds readable titles', () => {
    expect(examples[0]).toMatchObject({ id: '01-variaveis', title: 'Variáveis' });
    expect(tutorials[0]).toMatchObject({ id: 'aula-01-apresentacao', title: 'Apresentação' });
  });

  it.each(examples.map((example) => [example.id, example.text] as const))('%s declares its version', (_id, text) => {
    expect(readScriptVersion(text)).toMatchObject({ version: '1.0', isDeclared: true });
  });

  it.each(
    examples.filter((example) => !example.id.startsWith('21')).map((example) => [example.id, example.text] as const),
  )('%s has no invalid line', (_id, text) => {
    expect(parse(readScriptVersion(text).body).map((statement) => statement.kind)).not.toContain('invalid');
  });

  it.each(tutorials.map((tutorial) => [tutorial.id, tutorial.text] as const))(
    '%s only teaches valid code',
    (_id, text) => {
      const snippets = text.split('```').filter((_part, index) => index % 2 === 1);
      const invalid = snippets.flatMap((snippet) =>
        parse(snippet)
          .filter((statement) => statement.kind === 'invalid')
          .map((statement) => (statement.kind === 'invalid' ? statement.detail : '')),
      );

      expect(invalid).toEqual([]);
    },
  );

  it('finds the example that explains a command', () => {
    expect(findExampleByPrefix('16')?.id).toBe('16-listas');
    expect(findExampleByPrefix('99')).toBeUndefined();
  });
});
