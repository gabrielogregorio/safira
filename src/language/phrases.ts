import commands from './commands.json';
import { removeAccents } from './tokenizer';

export type CommandKey = keyof typeof commands;

export interface CommandDefinition {
  color: string;
  phrases: string[];
}

const definitions: Record<string, CommandDefinition> = commands;

const toWords = (phrase: string): string[] => removeAccents(phrase).split(' ').filter(Boolean);

const phraseWordsByKey = new Map<string, string[][]>(
  Object.entries(definitions).map(([key, definition]) => [key, definition.phrases.map(toWords)]),
);

export const getPhrases = (key: CommandKey): string[][] => phraseWordsByKey.get(key) ?? [];

export const getAllCommands = (): [string, CommandDefinition][] => Object.entries(definitions);

const CONTINUATION_KEYS: CommandKey[] = [
  'adicione_texto_arquivo_sub',
  'sobrescreva_texto_arquivo_sub',
  'addItensListaInterno',
  'addItensListaInternoInicio',
  'addItensListaInternoFinal',
  'remover_itens_listas_interno',
  'tiver_interno_lista',
  'incremente_decremente',
  'listaNaPosicao',
  'listaCom',
  'listaPosicoesCom',
  'na_cor',
  'formatar_textos',
  'substitua_por',
  'substitua_na_variavel',
  'percorra_items_lista_sub',
  'passandoParametros',
  'repitaVezes',
  'esperaEm',
  'se_final',
  'enquanto_final',
  'to_upper',
  'to_lower',
  'to_captalize',
  'aleatorioEntre',
  'arquivo_existe_sub_existe',
  'arquivo_existe_nao_sub_existe',
  'logico_e',
  'logico_ou',
  'logico_igual',
  'logico_diferente',
  'logico_maior',
  'logico_menor',
  'logico_maior_igual',
  'logico_menor_igual',
  'matematica_add',
  'matematica_sub',
  'matematica_mult',
  'matematica_div',
  'matematica_elev',
  'para_cada_de',
  'para_cada_ate',
  'percorrer_lst_str_a_cada_subum',
  'se_nao',
];

const continuationWords = new Set(
  CONTINUATION_KEYS.flatMap((key) => getPhrases(key).flatMap((words) => words.slice(0, 1))),
);

export const isContinuationWord = (word: string): boolean => continuationWords.has(word);
