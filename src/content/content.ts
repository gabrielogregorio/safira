const exampleModules = import.meta.glob<string>('./examples/*.safira', {
  eager: true,
  query: '?raw',
  import: 'default',
});
const tutorialModules = import.meta.glob<string>('./tutorials/*.md', { eager: true, query: '?raw', import: 'default' });

export interface ContentEntry {
  id: string;
  title: string;
  text: string;
}

const EXTENSION_OR_FOLDER = /^.*\/|\.[a-z]+$/g;

const toId = (path: string): string => path.replace(EXTENSION_OR_FOLDER, '');

const ACCENTED_WORDS: Record<string, string> = {
  apresentacao: 'apresentação',
  exibicao: 'exibição',
  variaveis: 'variáveis',
  condicoes: 'condições',
  condicao: 'condição',
  funcoes: 'funções',
  numero: 'número',
  numeros: 'números',
  aleatorio: 'aleatório',
  ordenacao: 'ordenação',
  relatorio: 'relatório',
  agua: 'água',
  pascoa: 'páscoa',
};

const toTitle = (id: string): string => {
  const words = id
    .replace(/^(aula-|programa-)?(\d+-)?/, '')
    .split(/[-_]/)
    .map((word) => ACCENTED_WORDS[word] ?? word)
    .join(' ');

  return words.charAt(0).toUpperCase() + words.slice(1);
};

const TITLE_EMOJIS: Record<string, string> = {
  'programa-apresentacao': '💎',
  'programa-armazena-numeros': '🧮',
  'programa-cadastra': '📝',
  'programa-guarda-pessoas': '👥',
  'programa-maior-menor': '🔼',
  'programa-natal': '🎄',
  'programa-novo-ano': '🎆',
  'programa-ordenacao': '🔢',
  'programa-pascoa': '🐰',
  'programa-relatorio-agua': '💧',
  'programa-semana': '📅',
  'programa-sinal': '🚦',
  'programa-tinta': '🎨',
};

const withEmoji = (id: string, title: string): string => {
  const emoji = TITLE_EMOJIS[id];

  return emoji === undefined ? title : `${emoji} ${title}`;
};

const toEntries = (modules: Record<string, string>): ContentEntry[] =>
  Object.entries(modules)
    .map(([path, text]) => ({ id: toId(path), title: withEmoji(toId(path), toTitle(toId(path))), text }))
    .sort((first, second) => first.id.localeCompare(second.id));

export const examples = toEntries(exampleModules);

export const tutorials = toEntries(tutorialModules);

export const findExampleByPrefix = (prefix: string): ContentEntry | undefined =>
  examples.find((example) => example.id.startsWith(`${prefix}-`));
