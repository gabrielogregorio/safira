/** `[key]` is a command word, written once here and filled by the dictionary of each language. */
export interface Scenario {
  name: string;
  code: string;
  output: string[];
  inputs?: string[];
}

export type Statement = Scenario;

/** Each one stands alone, so they can be chained and nested in any order. */
export const STATEMENTS: Statement[] = [
  { name: 'print text', code: '[mostre] "oi"', output: ['oi'] },
  { name: 'print number', code: '[mostre] 7', output: ['7'] },
  { name: 'print decimal', code: '[mostre] 2.5', output: ['2.5'] },
  { name: 'print empty', code: '[mostre] ""', output: [''] },
  { name: 'print on one line', code: '[mostreNessa] "a"\n[mostreNessa] "b"\n[mostre] ""', output: ['ab'] },
  { name: 'print in color', code: '[mostre] "c" [na_cor] [azul]', output: ['c'] },
  { name: 'print in hex color', code: '[mostre] "c" [na_cor] #ff1122', output: ['c'] },
  { name: 'print color first', code: '[mostre] [na_cor] #331 "c"', output: ['c'] },
  { name: 'print joined', code: '[mostre] "a" + "b"', output: ['ab'] },
  { name: 'print text and number', code: '[mostre] "a" + 1', output: ['a1'] },
  { name: 'print filled', code: '[mostre] "a % b" [formatar_textos] 1', output: ['a 1 b'] },
  { name: 'print filled twice', code: '[mostre] "% e %" [formatar_textos] 1, 2', output: ['1 e 2'] },
  { name: 'assign with symbol', code: 'v = 3\n[mostre] v', output: ['3'] },
  { name: 'assign with word', code: 'v [declara_variaveis] 3\n[mostre] v', output: ['3'] },
  { name: 'assign text', code: 'v = "t"\n[mostre] v', output: ['t'] },
  { name: 'assign from itself', code: 'v = 1\nv = v + 1\n[mostre] v', output: ['2'] },
  { name: 'assign true', code: 'v = [logico_true]\n[mostre] v', output: ['True'] },
  { name: 'assign false', code: 'v = [logico_false]\n[mostre] v', output: ['False'] },
  { name: 'text input', code: 'v = [digitado]\n[mostre] v', inputs: ['7'], output: ['7'] },
  { name: 'save the answer', code: '[guarde_resposta] v\n[mostre] v', inputs: ['7'], output: ['7'] },
  { name: 'number input', code: 'v = [digitadoNumero]\n[mostre] v + 1', inputs: ['4'], output: ['5'] },
  { name: 'if true', code: '[se] 1 [logico_igual] 1 [se_final] {\n  [mostre] "s"\n}', output: ['s'] },
  { name: 'if false', code: '[se] 1 [logico_igual] 2 [se_final] {\n  [mostre] "s"\n}\n[mostre] "f"', output: ['f'] },
  {
    name: 'if else',
    code: '[se] 1 [logico_igual] 2 [se_final] {\n  [mostre] "s"\n} [se_nao] {\n  [mostre] "n"\n}',
    output: ['n'],
  },
  {
    name: 'if else if',
    code: '[se] 1 [logico_igual] 2 [se_final] {\n  [mostre] "a"\n} [se_nao_se] 1 [logico_igual] 1 [se_final] {\n  [mostre] "b"\n} [se_nao] {\n  [mostre] "c"\n}',
    output: ['b'],
  },
  { name: 'if inline', code: '[se] 1 [logico_igual] 1 [se_final] [mostre] "i"', output: ['i'] },
  {
    name: 'if inline else',
    code: '[se] 1 [logico_igual] 2 [se_final] [mostre] "i" [se_nao] [mostre] "j"',
    output: ['j'],
  },
  { name: 'repeat', code: '[repita] 2 [repitaVezes] {\n  [mostre] "r"\n}', output: ['r', 'r'] },
  { name: 'repeat zero', code: '[repita] 0 [repitaVezes] {\n  [mostre] "r"\n}\n[mostre] "z"', output: ['z'] },
  {
    name: 'while',
    code: 'c = 0\n[enquanto] c [logico_menor] 2 {\n  [mostre] c\n  c = c + 1\n}',
    output: ['0', '1'],
  },
  {
    name: 'while with end word',
    code: 'c = 0\n[enquanto] c [logico_menor] 1 [enquanto_final] {\n  [mostre] c\n  c = c + 1\n}',
    output: ['0'],
  },
  {
    name: 'count up',
    code: '[para_cada] k [para_cada_de] 1 [para_cada_ate] 3 {\n  [mostre] k\n}',
    output: ['1', '2', '3'],
  },
  {
    name: 'count down',
    code: '[para_cada] k [para_cada_de] 2 [para_cada_ate] 1 {\n  [mostre] k\n}',
    output: ['2', '1'],
  },
  {
    name: 'each item',
    code: '[declaraListas] l [recebeDeclaraListas] "a", "b"\n[percorra_items] l [percorra_items_lista_sub] i {\n  [mostre] i\n}',
    output: ['a', 'b'],
  },
  {
    name: 'each letter',
    code: 't = "ab"\n[percorra_items] t [percorra_items_lista_sub] i {\n  [mostre] i\n}',
    output: ['a', 'b'],
  },
  {
    name: 'break',
    code: '[para_cada] k [para_cada_de] 1 [para_cada_ate] 3 {\n  [se] k [logico_igual] 2 [se_final] {\n    [pare]\n  }\n  [mostre] k\n}',
    output: ['1'],
  },
  {
    name: 'continue',
    code: '[para_cada] k [para_cada_de] 1 [para_cada_ate] 3 {\n  [se] k [logico_igual] 2 [se_final] {\n    [continue]\n  }\n  [mostre] k\n}',
    output: ['1', '3'],
  },
  { name: 'wait seconds', code: '[aguarde] 0 [esperaEmSegundos]\n[mostre] "w"', output: ['w'] },
  { name: 'wait milliseconds', code: '[aguarde] 1 [esperaEmMs]\n[mostre] "w"', output: ['w'] },
  { name: 'tone', code: '[toque] C [toque_por] 1 [esperaEmSegundos]\n[mostre] "t"', output: ['t'] },
  { name: 'tone list', code: '[toque] C, D [toque_por] 1 [esperaEmMs]\n[mostre] "t"', output: ['t'] },
  { name: 'random', code: 'v = [aleatorio] 2 [aleatorioEntre] 3\n[mostre] v [logico_maior] 1', output: ['True'] },
  { name: 'upper', code: 't = "ab"\n[mostre] t [to_upper]', output: ['AB'] },
  { name: 'lower', code: 't = "AB"\n[mostre] t [to_lower]', output: ['ab'] },
  { name: 'capitalize', code: 't = "ab"\n[mostre] t [to_captalize]', output: ['Ab'] },
  { name: 'type', code: '[mostre] [tipo_variavel] 1', output: ['float'] },
  {
    name: 'replace',
    code: 't = "aba"\n[substitua] "b" [substitua_por] "c" [substitua_na_variavel] t\n[mostre] t',
    output: ['aca'],
  },
  { name: 'increase', code: 'n = 1\n[incremente] 2 [incremente_decremente] n\n[mostre] n', output: ['3'] },
  { name: 'decrease', code: 'n = 3\n[decremente] 2 [incremente_decremente] n\n[mostre] n', output: ['1'] },
  { name: 'function', code: '[funcoes] f1 {\n  [mostre] "h"\n}\nf1()', output: ['h'] },
  { name: 'function argument', code: '[funcoes] f2(p) {\n  [mostre] p\n}\nf2(5)', output: ['5'] },
  { name: 'function arguments', code: '[funcoes] f3(p, q) {\n  [mostre] p + q\n}\nf3(1, 2)', output: ['3'] },
  { name: 'function return', code: '[funcoes] f4(p) {\n  [retorne] p * 2\n}\n[mostre] f4(2)', output: ['4'] },
  {
    name: 'function with words',
    code: '[funcoes] f5 [recebeParametros] p, q {\n  [mostre] p + q\n}\nf5 [passandoParametros] 1, 2',
    output: ['3'],
  },
  {
    name: 'function return text',
    code: '[funcoes] f6 {\n  [retorne] "x"\n}\nv = f6()\n[mostre] v',
    output: ['x'],
  },
  { name: 'list', code: '[declaraListas] l [recebeDeclaraListas] 1, 2\n[mostre] l', output: ['[1, 2]'] },
  { name: 'list with symbol', code: '[declaraListas] l = 1, 2\n[mostre] l', output: ['[1, 2]'] },
  {
    name: 'list item',
    code: '[declaraListas] l [recebeDeclaraListas] "a", "b"\n[mostre] [declaraListas] l [listaNaPosicao] 2',
    output: ['b'],
  },
  {
    name: 'list change',
    code: '[declaraListas] l [recebeDeclaraListas] 1, 2\n[declaraListas] l [listaNaPosicao] 1 = 9\n[mostre] l',
    output: ['[9, 2]'],
  },
  {
    name: 'list change with word',
    code: '[declaraListas] l [recebeDeclaraListas] 1, 2\n[declaraListas] l [listaNaPosicao] 1 [recebeDeclaraListas] 9\n[mostre] l',
    output: ['[9, 2]'],
  },
  {
    name: 'list sized',
    code: '[declaraListas] l [listaCom] 2 [listaPosicoesCom]\n[mostre] [tamanho_da_lista] l',
    output: ['2'],
  },
  {
    name: 'list end',
    code: '[declaraListas] l [recebeDeclaraListas] 1\n[adicionarItensListas] 2 [addItensListaInternoFinal] l\n[mostre] l',
    output: ['[1, 2]'],
  },
  {
    name: 'list start',
    code: '[declaraListas] l [recebeDeclaraListas] 1\n[adicionarItensListas] 2 [addItensListaInternoInicio] l\n[mostre] l',
    output: ['[2, 1]'],
  },
  {
    name: 'list add',
    code: '[declaraListas] l [recebeDeclaraListas] 1\n[adicionarItensListas] 2 [addItensListaInterno] l\n[mostre] l',
    output: ['[1, 2]'],
  },
  {
    name: 'list position',
    code: '[declaraListas] l [recebeDeclaraListas] 1, 3\n[adicionarItensListas] 2 [listaNaPosicao] 2 [addItensListaInternoPosicaoFinaliza] l\n[mostre] l',
    output: ['[1, 2, 3]'],
  },
  {
    name: 'list remove',
    code: '[declaraListas] l [recebeDeclaraListas] 1, 2\n[remover_itens_listas] 1 [remover_itens_listas_interno] l\n[mostre] l',
    output: ['[2]'],
  },
  {
    name: 'list has',
    code: '[declaraListas] l [recebeDeclaraListas] 1, 2\n[se] [tiver_lista] 1 [tiver_interno_lista] l [se_final] {\n  [mostre] "y"\n}',
    output: ['y'],
  },
  {
    name: 'file write and read',
    code: '[crie_arquivo] "a.txt"\n[adicione_texto_arquivo] "x" [adicione_texto_arquivo_sub] "a.txt"\n[mostre] [leia_arquivo] "a.txt"',
    output: ['x'],
  },
  {
    name: 'file overwrite',
    code: '[crie_arquivo] "b.txt"\n[sobrescreva_texto_arquivo] "y" [sobrescreva_texto_arquivo_sub] "b.txt"\n[mostre] [leia_arquivo] "b.txt"',
    output: ['y'],
  },
  {
    name: 'file exists',
    code: '[crie_arquivo] "c.txt"\n[se] [arquivo_existe] "c.txt" [arquivo_existe_sub_existe] [se_final] {\n  [mostre] "e"\n}',
    output: ['e'],
  },
  {
    name: 'file missing',
    code: '[se] [arquivo_existe] "nada.txt" [arquivo_existe_nao_sub_existe] [se_final] {\n  [mostre] "n"\n}',
    output: ['n'],
  },
  {
    name: 'file delete',
    code: '[crie_arquivo] "d.txt"\n[delete_arquivo] "d.txt"\n[se] [arquivo_existe] "d.txt" [arquivo_existe_nao_sub_existe] [se_final] {\n  [mostre] "g"\n}',
    output: ['g'],
  },
  {
    name: 'import',
    code: '[crie_arquivo] "m.safira"\n[sobrescreva_texto_arquivo] "w = 8" [sobrescreva_texto_arquivo_sub] "m.safira"\n[importe] "m"\n[mostre] w',
    output: ['8'],
  },
  {
    name: 'try without error',
    code: '[tente] {\n  [mostre] "a"\n} [se_der_erro] {\n  [mostre] "b"\n}',
    output: ['a'],
  },
  {
    name: 'try with error',
    code: '[tente] {\n  [mostre] semvalor\n} [se_der_erro] {\n  [mostre] "b"\n}',
    output: ['b'],
  },
  {
    name: 'try all parts',
    code: '[tente] {\n  [mostre] "a"\n} [se_der_erro] {\n  [mostre] "b"\n} [senao_der_erro] {\n  [mostre] "c"\n} [em_qualquer_caso] {\n  [mostre] "d"\n}',
    output: ['a', 'c', 'd'],
  },
  { name: 'do nothing', code: '[nao_faca_nada]\n[mostre] "n"', output: ['n'] },
  {
    name: 'do nothing in a branch',
    code: '[se] 1 [logico_igual] 1 [se_final] {\n  [nao_faca_nada]\n} [se_nao] {\n  [mostre] "s"\n}\n[mostre] "f"',
    output: ['f'],
  },
  {
    name: 'do nothing inline',
    code: '[se] 1 [logico_igual] 1 [se_final] [nao_faca_nada] [se_nao] [mostre] "s"',
    output: [],
  },
  {
    name: 'key not pressed',
    code: '[se] [tecla_apertar] Enter [se_final] {\n  [mostre] "k"\n}\n[mostre] "n"',
    output: ['n'],
  },
  {
    name: 'key not held',
    code: '[se] [tecla_segurar] Shift+Enter {\n  [mostre] "k"\n} [se_nao] {\n  [mostre] "h"\n}',
    output: ['h'],
  },
  {
    name: 'key not released',
    code: '[ao_tecla] [tecla_soltar] ArrowUp {\n  [mostre] "k"\n}\n[mostre] "s"',
    output: ['s'],
  },
  {
    name: 'repeat forever',
    code: 'c = 0\n[repita_sempre] {\n  c = c + 1\n  [se] c [logico_igual] 3 [se_final] [pare]\n}\n[mostre] c',
    output: ['3'],
  },
  { name: 'repeat forever inline', code: '[repita_sempre] [pare]\n[mostre] "s"', output: ['s'] },
  { name: 'comment', code: '# nada\n[mostre] "x" # fim', output: ['x'] },
];

/** A program that ends everything or clears the screen cannot be chained like the others. */
export const CLOSING_STATEMENTS: Scenario[] = [
  { name: 'halt', code: '[mostre] "a"\n[interrompa]\n[mostre] "b"', output: ['a'] },
  { name: 'clear', code: '[mostre] "a"\n[limpatela]\n[mostre] "b"', output: ['b'] },
];

export interface ValueCase {
  name: string;
  setup?: string;
  value: string;
  shown: string;
}

export const VALUES: ValueCase[] = [
  { name: 'integer', value: '12', shown: '12' },
  { name: 'decimal', value: '1.5', shown: '1.5' },
  { name: 'negative', value: '-3', shown: '-3' },
  { name: 'text', value: '"t x"', shown: 't x' },
  { name: 'text with accent', value: '"ação"', shown: 'ação' },
  { name: 'text with number', value: '"a1"', shown: 'a1' },
  { name: 'emoji', value: '"🎉"', shown: '🎉' },
  { name: 'Chinese text', value: '"你好"', shown: '你好' },
  { name: 'Japanese text', value: '"こんにちは"', shown: 'こんにちは' },
  { name: 'true', value: '[logico_true]', shown: 'True' },
  { name: 'false', value: '[logico_false]', shown: 'False' },
  { name: 'variable', setup: 'o1 = 9', value: 'o1', shown: '9' },
  { name: 'sum', value: '2 + 3', shown: '5' },
  { name: 'subtraction', value: '2 - 3', shown: '-1' },
  { name: 'product', value: '2 * 3', shown: '6' },
  { name: 'division', value: '6 / 3', shown: '2' },
  { name: 'remainder', value: '7 % 3', shown: '1' },
  { name: 'power', value: '2 ** 3', shown: '8' },
  { name: 'precedence', value: '2 + 3 * 4', shown: '14' },
  { name: 'parentheses', value: '(2 + 3) * 4', shown: '20' },
  { name: 'word sum', value: '2 [matematica_add] 3', shown: '5' },
  { name: 'word subtraction', value: '5 [matematica_sub] 3', shown: '2' },
  { name: 'word product', value: '2 [matematica_mult] 3', shown: '6' },
  { name: 'word division', value: '6 [matematica_div] 3', shown: '2' },
  { name: 'word power', value: '2 [matematica_elev] 3', shown: '8' },
  { name: 'joined', value: '"a" + "b"', shown: 'ab' },
  { name: 'upper', setup: 'o2 = "ab"', value: 'o2 [to_upper]', shown: 'AB' },
  { name: 'lower', setup: 'o3 = "AB"', value: 'o3 [to_lower]', shown: 'ab' },
  {
    name: 'list item',
    setup: '[declaraListas] o4 [recebeDeclaraListas] 5, 6',
    value: '[declaraListas] o4 [listaNaPosicao] 2',
    shown: '6',
  },
  {
    name: 'list size',
    setup: '[declaraListas] o5 [recebeDeclaraListas] 5, 6',
    value: '[tamanho_da_lista] o5',
    shown: '2',
  },
  { name: 'function result', setup: '[funcoes] o6 {\n  [retorne] 4\n}', value: 'o6()', shown: '4' },
  { name: 'function with argument', setup: '[funcoes] o7(p) {\n  [retorne] p + 1\n}', value: 'o7(1)', shown: '2' },
  { name: 'comparison', value: '1 [logico_menor] 2', shown: 'True' },
];

/** `{}` is the value. Each one must show it, and only it. */
export const CONSUMERS: { name: string; code: string }[] = [
  { name: 'print', code: '[mostre] {}' },
  { name: 'print with parentheses', code: '[mostre] ({})' },
  { name: 'print on one line', code: '[mostreNessa] {}\n[mostre] ""' },
  { name: 'print in color', code: '[mostre] {} [na_cor] [azul]' },
  { name: 'assign', code: 'u = {}\n[mostre] u' },
  { name: 'assign with word', code: 'u [declara_variaveis] {}\n[mostre] u' },
  { name: 'fill', code: '[mostre] "%" [formatar_textos] {}' },
  {
    name: 'list',
    code: '[declaraListas] u1 [recebeDeclaraListas] {}, 0\n[mostre] [declaraListas] u1 [listaNaPosicao] 1',
  },
  { name: 'argument', code: '[funcoes] u2(p) {\n  [mostre] p\n}\nu2({})' },
  { name: 'return', code: '[funcoes] u3 {\n  [retorne] {}\n}\n[mostre] u3()' },
  { name: 'inside if', code: '[se] 1 [logico_igual] 1 [se_final] {\n  [mostre] {}\n}' },
  {
    name: 'file',
    code: '[crie_arquivo] "v.txt"\n[sobrescreva_texto_arquivo] {} [sobrescreva_texto_arquivo_sub] "v.txt"\n[mostre] [leia_arquivo] "v.txt"',
  },
];

/** `{}` is the body. */
export const BLOCKS: { name: string; code: string; times: number; setup?: string }[] = [
  { name: 'if', code: '[se] 1 [logico_igual] 1 [se_final] {\n{}\n}', times: 1 },
  { name: 'else', code: '[se] 1 [logico_igual] 2 [se_final] {\n  [mostre] "x"\n} [se_nao] {\n{}\n}', times: 1 },
  {
    name: 'else if',
    code: '[se] 1 [logico_igual] 2 [se_final] {\n  [mostre] "x"\n} [se_nao_se] 1 [logico_igual] 1 [se_final] {\n{}\n}',
    times: 1,
  },
  { name: 'repeat', code: '[repita] 2 [repitaVezes] {\n{}\n}', times: 2 },
  { name: 'count', code: '[para_cada] z1 [para_cada_de] 1 [para_cada_ate] 2 {\n{}\n}', times: 2 },
  { name: 'while', code: 'z2 = 0\n[enquanto] z2 [logico_menor] 2 {\n  z2 = z2 + 1\n{}\n}', times: 2 },
  {
    name: 'each',
    setup: '[declaraListas] z3 [recebeDeclaraListas] 1, 2',
    code: '[percorra_items] z3 [percorra_items_lista_sub] z4 {\n{}\n}',
    times: 2,
  },
  { name: 'function', code: '[funcoes] z5 {\n{}\n}\nz5()', times: 1 },
  { name: 'try', code: '[tente] {\n{}\n} [se_der_erro] {\n  [mostre] "x"\n}', times: 1 },
  { name: 'catch', code: '[tente] {\n  [mostre] semvalor\n} [se_der_erro] {\n{}\n}', times: 1 },
  { name: 'finally', code: '[tente] {\n  n1 = 1\n} [em_qualquer_caso] {\n{}\n}', times: 1 },
];

export const COMPARISONS: { key: string; results: [boolean, boolean, boolean] }[] = [
  { key: 'logico_igual', results: [false, true, false] },
  { key: 'logico_diferente', results: [true, false, true] },
  { key: 'logico_maior', results: [false, false, true] },
  { key: 'logico_menor', results: [true, false, false] },
  { key: 'logico_maior_igual', results: [false, true, true] },
  { key: 'logico_menor_igual', results: [true, true, false] },
];

export const SYMBOL_COMPARISONS: { symbol: string; results: [boolean, boolean, boolean] }[] = [
  { symbol: '==', results: [false, true, false] },
  { symbol: '!=', results: [true, false, true] },
  { symbol: '>', results: [false, false, true] },
  { symbol: '<', results: [true, false, false] },
  { symbol: '>=', results: [false, true, true] },
  { symbol: '<=', results: [true, true, false] },
];
