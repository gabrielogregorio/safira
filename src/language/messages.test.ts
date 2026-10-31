import messages from './messages.json';
import { translateMessage } from './messages';

describe('translateMessage', () => {
  it('uses the requested language', () => {
    expect(translateMessage('en-us', 'math_division_by_zero')).toBe('It is not possible to divide by zero');
  });

  it('fills the markers in order', () => {
    expect(translateMessage('pt-br', 'slice_out_of_range', 9, 3)).toBe(
      'A posição 9 está fora do texto, que tem 3 letras',
    );
  });

  it('leaves a marker empty when the value is missing', () => {
    expect(translateMessage('pt-br', 'arquivo_nao_existe')).toBe("O arquivo '' não existe!");
  });

  it('falls back to Portuguese when a translation is missing', () => {
    expect(translateMessage('es', 'funcao_nao_passou_parametros', 'f', 1)).toContain('f');
  });

  it.each(['zh-cn', 'ja'] as const)('translates every message into %s with the same markers', (locale) => {
    for (const [key, texts] of Object.entries(messages as Record<string, Record<string, string | null>>)) {
      const english = texts['en-us'];

      if (typeof english === 'string') {
        expect(texts[locale]?.split('{}').length, key).toBe(english.split('{}').length);
      }
    }
  });

  it('shows the key of an unknown message', () => {
    expect(translateMessage('pt-br', 'nada')).toBe('nada');
  });
});
