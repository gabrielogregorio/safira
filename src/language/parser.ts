import type { ConditionalBranch, Expression, Statement, StatementBody } from './ast';
import { ExpressionParser } from './expressionParser';
import type { CommandKey } from './phrases';
import { ParseFailure } from './tokenCursor';
import { tokenize } from './tokenizer';

const ASSIGNMENT_SYMBOLS = ['=', ':=', '<-'];

type StatementRule = () => StatementBody;

export class Parser extends ExpressionParser {
  private readonly sourceLines: string[];
  private inlineDepth = 0;

  private readonly rules: StatementRule[] = [
    () => this.parseSimple('limpatela', { kind: 'clear' }),
    () => this.parseReturn(),
    () => this.parsePrint('mostreNessa', true),
    () => this.parsePrint('mostre', false),
    () => this.parseSimple('continue', { kind: 'continue' }),
    () => this.parseSimple('pare', { kind: 'break' }),
    () => this.parseSimple('interrompa', { kind: 'halt' }),
    () => this.parseWhile(),
    () => this.parseRepeat(),
    () => this.parseForRange(),
    () => this.parseWait(),
    () => this.parseImport(),
    () => this.parseOrphanBlock('se_der_erro', 'precisa_def_tente_p_der_erro'),
    () => this.parseOrphanBlock('senao_der_erro', 'precisa_def_tente_p_n_der_erro'),
    () => this.parseOrphanBlock('em_qualquer_caso', 'precisa_def_tente_p_n_der_erro'),
    () => this.parseTry(),
    () => this.parseFileCreate(),
    () => this.parseFileDelete(),
    () => this.parseFileWrite('adicione_texto_arquivo', 'adicione_texto_arquivo_sub', 'fileAppend'),
    () => this.parseFileWrite('sobrescreva_texto_arquivo', 'sobrescreva_texto_arquivo_sub', 'fileOverwrite'),
    () => this.parseOrphanElse('se_nao_se'),
    () => this.parseOrphanElse('se_nao'),
    () => this.parseIf(),
    () => this.parseAssignment(),
    () => this.parseIncrement('incremente', 1),
    () => this.parseIncrement('decremente', -1),
    () => this.parseReplaceText(),
    () => this.parseListInsertAt(),
    () => this.parseListInsertEdge('addItensListaInternoFinal', 'end'),
    () => this.parseListInsertEdge('addItensListaInternoInicio', 'start'),
    () => this.parseListInsertEdge('addItensListaInterno', 'end'),
    () => this.parseListRemove(),
    () => this.parseListSet(),
    () => this.parseListSized(),
    () => this.parseListDeclare(),
    () => this.parseForEach(),
    () => this.parseFunction(),
    () => ({ kind: 'expression', value: this.parseValue() }),
  ];

  public constructor(source: string) {
    super(tokenize(source).tokens);
    this.sourceLines = source.split('\n');
  }

  public parseProgram(): Statement[] {
    const statements: Statement[] = [];

    for (;;) {
      this.skipNewlines();

      if (this.current.kind === 'end') {
        return statements;
      }

      statements.push(this.parseStatement());
    }
  }

  private parseStatement(): Statement {
    const line = this.current.line;

    if (this.acceptSymbol('}')) {
      return { kind: 'invalid', messageKey: 'nao_abriu_chave', detail: '', line };
    }

    const saved = this.position;

    for (const rule of this.rules) {
      const body = this.attempt(() => {
        const statement = rule();

        const isBeforeElse = this.inlineDepth > 0 && this.peekPhrase('se_nao') !== null;

        if (!this.isStatementEnd() && !this.endsWithBlock() && !isBeforeElse) {
          this.fail();
        }

        return statement;
      });

      if (body !== null) {
        return { ...body, line };
      }

      this.position = saved;
    }

    this.skipInvalidStatement();

    return {
      kind: 'invalid',
      messageKey: 'comando_desconhecido',
      detail: `'${(this.sourceLines[line - 1] ?? '').trim()}'`,
      line,
    };
  }

  private endsWithBlock(): boolean {
    return this.tokenAt(this.position - 1).text === '}';
  }

  private skipInvalidStatement(): void {
    while (this.current.kind !== 'newline' && this.current.kind !== 'end' && !this.isSymbol('}')) {
      if (this.isSymbol('{')) {
        this.parseBlock();

        return;
      }

      this.advance();
    }
  }

  private parseBlock(): Statement[] {
    this.skipNewlines();
    this.expectSymbol('{');
    const statements: Statement[] = [];

    for (;;) {
      this.skipNewlines();

      if (this.acceptSymbol('}')) {
        return statements;
      }

      if (this.current.kind === 'end') {
        statements.push({ kind: 'invalid', messageKey: 'nao_fechou_chave', detail: '', line: this.current.line });

        return statements;
      }

      statements.push(this.parseStatement());
    }
  }

  private parseBody(): Statement[] {
    if (this.current.kind === 'newline' || this.isSymbol('{')) {
      return this.parseBlock();
    }

    if (this.isStatementEnd()) {
      this.fail();
    }

    this.inlineDepth += 1;
    const statement = this.parseStatement();
    this.inlineDepth -= 1;

    return [statement];
  }

  private peekAfterNewlines<Result>(action: () => Result | null): Result | null {
    const saved = this.position;
    this.skipNewlines();
    const result = this.attempt(action);

    if (result === null) {
      this.position = saved;
    }

    return result;
  }

  private parseSimple(key: CommandKey, body: StatementBody): StatementBody {
    this.expectPhrase(key);

    return body;
  }

  private parseReturn(): StatementBody {
    this.expectPhrase('retorne');

    return { kind: 'return', value: this.isStatementEnd() ? null : this.parseValue() };
  }

  private parsePrint(key: CommandKey, inline: boolean): StatementBody {
    this.expectPhrase(key);

    if (this.isStatementEnd()) {
      return { kind: 'print', inline, value: null };
    }

    return { kind: 'print', inline, value: this.attempt(() => this.parseColorFirst()) ?? this.parseValue() };
  }

  private parseWhile(): StatementBody {
    this.expectPhrase('enquanto');
    const condition = this.parseCondition();
    this.acceptPhrase('enquanto_final');

    return { kind: 'while', condition, body: this.parseBody() };
  }

  private parseRepeat(): StatementBody {
    this.expectPhrase('repita');
    const count = this.parseAdditive();
    this.expectPhrase('repitaVezes');

    return { kind: 'repeat', count, body: this.parseBody() };
  }

  private parseForRange(): StatementBody {
    this.expectPhrase('para_cada');
    const name = this.expectName();
    this.expectPhrase('para_cada_de');
    const start = this.parseAdditive();
    this.expectPhrase('para_cada_ate');
    const end = this.parseAdditive();

    return { kind: 'forRange', name, start, end, body: this.parseBody() };
  }

  private parseForEach(): StatementBody {
    this.expectPhrase('percorra_items');
    const iterable = this.parseValue();
    this.expectPhrase('percorra_items_lista_sub');
    const name = this.expectName();

    return { kind: 'forEach', iterable, name, body: this.parseBody() };
  }

  private parseWait(): StatementBody {
    this.expectPhrase('aguarde');
    const amount = this.parseAdditive();

    if (this.acceptPhrase('esperaEmMs')) {
      return { kind: 'wait', amount, unit: 'milliseconds' };
    }

    this.expectPhrase('esperaEmSegundos');

    return { kind: 'wait', amount, unit: 'seconds' };
  }

  private parseImport(): StatementBody {
    this.expectPhrase('importe');
    const parts: string[] = [];

    while (!this.isStatementEnd()) {
      parts.push(this.advance().text);
    }

    if (parts.length === 0) {
      this.fail();
    }

    return { kind: 'import', name: parts.join('').replace(/^"|"$/g, '') };
  }

  private parseOrphanBlock(key: CommandKey, messageKey: string): StatementBody {
    this.expectPhrase(key);
    this.parseBlock();

    return { kind: 'invalid', messageKey, detail: '' };
  }

  private parseOrphanElse(key: CommandKey): StatementBody {
    this.expectPhrase(key);

    if (key === 'se_nao_se') {
      this.parseCondition();
      this.acceptPhrase('se_final');
    }

    this.parseBody();

    return { kind: 'invalid', messageKey: 'precisa_def_p_cond_senao', detail: '' };
  }

  private parseClause(key: CommandKey): Statement[] | null {
    return this.peekAfterNewlines(() => {
      this.expectPhrase(key);

      return this.parseBody();
    });
  }

  private parseTry(): StatementBody {
    this.expectPhrase('tente');
    const body = this.parseBlock();
    const onError = this.parseClause('se_der_erro');
    const onSuccess = this.parseClause('senao_der_erro');
    const always = this.parseClause('em_qualquer_caso');

    return { kind: 'try', body, onError, onSuccess, always };
  }

  private parseIf(): StatementBody {
    this.expectPhrase('se');
    const branches = [this.parseBranch()];

    for (;;) {
      const branch = this.peekAfterNewlines(() => {
        this.expectPhrase('se_nao_se');

        return this.parseBranch();
      });

      if (branch === null) {
        return { kind: 'if', branches, otherwise: this.parseClauseElse() };
      }

      branches.push(branch);
    }
  }

  private parseClauseElse(): Statement[] | null {
    if (this.peekAfterNewlines(() => this.peekPhrase('senao_der_erro')) !== null) {
      return null;
    }

    return this.parseClause('se_nao');
  }

  private parseBranch(): ConditionalBranch {
    const condition = this.parseCondition();
    this.acceptPhrase('se_final');

    return { condition, body: this.parseBody() };
  }

  private parseFileCreate(): StatementBody {
    this.expectPhrase('crie_arquivo');

    return { kind: 'fileCreate', path: this.parseAdditive() };
  }

  private parseFileDelete(): StatementBody {
    this.expectPhrase('delete_arquivo');

    return { kind: 'fileDelete', path: this.parseAdditive() };
  }

  private parseFileWrite(key: CommandKey, separator: CommandKey, kind: 'fileAppend' | 'fileOverwrite'): StatementBody {
    this.expectPhrase(key);
    const text = this.parseValue();
    this.expectPhrase(separator);
    const path = this.parseAdditive();
    this.acceptPhrase('sobrescreva_texto_arquivo_sub_sub');

    return { kind, text, path };
  }

  private acceptAssignment(): boolean {
    if (ASSIGNMENT_SYMBOLS.some((symbol) => this.acceptSymbol(symbol))) {
      return true;
    }

    return this.acceptPhrase('declara_variaveis') !== null;
  }

  private parseAssignment(): StatementBody {
    const name = this.expectName();

    if (!this.acceptAssignment()) {
      this.fail();
    }

    return { kind: 'assign', name, value: this.parseValue() };
  }

  private parseIncrement(key: CommandKey, sign: 1 | -1): StatementBody {
    this.expectPhrase(key);
    const amount = this.parseAdditive();
    this.expectPhrase('incremente_decremente');

    return { kind: 'increment', name: this.expectName(), amount, sign };
  }

  private parseReplaceText(): StatementBody {
    this.expectPhrase('substitua');
    const search = this.parseAdditive();
    this.expectPhrase('substitua_por');
    const replacement = this.parseAdditive();
    this.expectPhrase('substitua_na_variavel');

    return { kind: 'replaceText', name: this.expectName(), search, replacement };
  }

  private parseListInsertAt(): StatementBody {
    this.expectPhrase('adicionarItensListas');
    const value = this.parseAdditive();
    this.expectPhrase('listaNaPosicao');
    const position = this.parseAdditive();
    this.expectPhrase('addItensListaInternoPosicaoFinaliza');

    return { kind: 'listInsert', name: this.expectName(), value, position };
  }

  private parseListInsertEdge(separator: CommandKey, position: 'start' | 'end'): StatementBody {
    this.expectPhrase('adicionarItensListas');
    const value = this.parseAdditive();
    this.expectPhrase(separator);

    return { kind: 'listInsert', name: this.expectName(), value, position };
  }

  private parseListRemove(): StatementBody {
    this.expectPhrase('remover_itens_listas');
    const value = this.parseAdditive();
    this.expectPhrase('remover_itens_listas_interno');

    return { kind: 'listRemove', name: this.expectName(), value };
  }

  private parseListSet(): StatementBody {
    this.expectPhrase('declaraListas');
    const name = this.expectName();
    this.expectPhrase('listaNaPosicao');
    const index = this.parseAdditive();

    if (!this.acceptAssignment() && this.acceptPhrase('recebeDeclaraListas') === null) {
      this.fail();
    }

    return { kind: 'listSet', name, index, value: this.parseValue() };
  }

  private parseListSized(): StatementBody {
    this.expectPhrase('declaraListas');
    const name = this.expectName();
    this.expectPhrase('listaCom');
    const size = this.parseAdditive();
    this.expectPhrase('listaPosicoesCom');

    return { kind: 'listDeclareSized', name, size };
  }

  private parseListDeclare(): StatementBody {
    this.expectPhrase('declaraListas');
    const name = this.expectName();

    if (this.acceptPhrase('recebeDeclaraListas') === null && !this.acceptAssignment()) {
      this.fail();
    }

    return { kind: 'listDeclare', name, values: this.parseValueList() };
  }

  private parseParameterList(): string[] {
    const parameters = [this.expectName()];

    while (this.acceptSymbol(',')) {
      parameters.push(this.expectName());
    }

    return parameters;
  }

  private parseFunction(): StatementBody {
    this.expectPhrase('funcoes');
    const name = this.expectName();
    let parameters: string[] | null = null;

    if (this.acceptSymbol('(')) {
      parameters = this.isSymbol(')') ? null : this.parseParameterList();
      this.expectSymbol(')');
      this.acceptSymbol(':');
    } else if (this.acceptPhrase('recebeParametros')) {
      parameters = this.parseParameterList();
    }

    return { kind: 'functionDeclaration', name, parameters, body: this.parseBlock() };
  }
}

export const parse = (source: string): Statement[] => {
  try {
    return new Parser(source).parseProgram();
  } catch (error) {
    if (error instanceof ParseFailure) {
      return [{ kind: 'invalid', messageKey: 'comando_desconhecido', detail: '', line: 1 }];
    }

    throw error;
  }
};

export type { Expression };
