import type { BinaryOperator, CaseMode, Expression, Value } from './ast';
import type { CommandKey } from './phrases';
import { isContinuationWord } from './phrases';
import { TokenCursor } from './tokenCursor';

type OperatorRule = [BinaryOperator, CommandKey | null, string | null];

const COMPARISON_RULES: OperatorRule[] = [
  ['lessOrEqual', 'logico_menor_igual', '<='],
  ['greaterOrEqual', 'logico_maior_igual', '>='],
  ['notEqual', 'logico_diferente', '!='],
  ['equal', 'logico_igual', '=='],
  ['greater', 'logico_maior', '>'],
  ['less', 'logico_menor', '<'],
];
const ADDITIVE_RULES: OperatorRule[] = [
  ['add', 'matematica_add', '+'],
  ['subtract', 'matematica_sub', '-'],
];
const MULTIPLICATIVE_RULES: OperatorRule[] = [
  ['multiply', 'matematica_mult', '*'],
  ['divide', 'matematica_div', '/'],
];
const CASE_RULES: [CaseMode, CommandKey][] = [
  ['upper', 'to_upper'],
  ['lower', 'to_lower'],
  ['capitalize', 'to_captalize'],
];
const NUMERIC_INPUT_WORDS = ['numerica', 'numeric', 'number', 'numero'];

export class ExpressionParser extends TokenCursor {
  private acceptOperator(rules: OperatorRule[]): BinaryOperator | null {
    for (const [operator, phraseKey, symbol] of rules) {
      if ((symbol !== null && this.acceptSymbol(symbol)) || (phraseKey !== null && this.acceptPhrase(phraseKey))) {
        return operator;
      }
    }

    return null;
  }

  private parseLeftAssociative(rules: OperatorRule[], parseOperand: () => Expression): Expression {
    let left = parseOperand();

    for (;;) {
      const operator = this.acceptOperator(rules);

      if (operator === null) {
        return left;
      }

      left = { kind: 'binary', operator, left, right: parseOperand() };
    }
  }

  protected parseValue(): Expression {
    let value = this.parseFormatted();

    for (;;) {
      const withCase = this.parseCaseSuffix(value);

      if (withCase !== null) {
        value = withCase;
      } else if (this.acceptPhrase('na_cor')) {
        value = { kind: 'colored', value, color: this.parseCondition() };
      } else {
        return value;
      }
    }
  }

  private parseCaseSuffix(value: Expression): Expression | null {
    const rule = CASE_RULES.find(([, key]) => this.acceptPhrase(key));

    return rule === undefined ? null : { kind: 'case', mode: rule[0], value };
  }

  private parseFormatted(): Expression {
    const template = this.parseCondition();

    if (this.acceptPhrase('formatar_textos') || this.acceptSymbol('%')) {
      return { kind: 'format', template, values: this.parseValueList() };
    }

    return template;
  }

  protected parseValueList(): Expression[] {
    const values: Expression[] = [];

    do {
      const value = this.parseCondition();
      values.push(this.parseCaseSuffix(value) ?? value);
    } while (this.acceptSymbol(','));

    return values;
  }

  protected parseCondition(): Expression {
    return this.parseLeftAssociative([['or', 'logico_ou', '||']], () =>
      this.parseLeftAssociative([['and', 'logico_e', '&&']], () => this.parseComparison()),
    );
  }

  private parseComparison(): Expression {
    return this.parseLeftAssociative(COMPARISON_RULES, () => this.parseAdditive());
  }

  protected parseAdditive(): Expression {
    return this.parseLeftAssociative(ADDITIVE_RULES, () => this.parseMultiplicative());
  }

  private parseMultiplicative(): Expression {
    let left = this.parseUnary();

    for (;;) {
      const operator = this.acceptOperator(MULTIPLICATIVE_RULES);
      const isFormatMarker = left.kind === 'literal' && typeof left.value === 'string';

      if (operator !== null) {
        left = { kind: 'binary', operator, left, right: this.parseUnary() };
      } else if (this.isSymbol('%') && !isFormatMarker) {
        this.advance();
        left = { kind: 'binary', operator: 'modulo', left, right: this.parseUnary() };
      } else {
        return left;
      }
    }
  }

  private parseUnary(): Expression {
    if (this.acceptSymbol('-')) {
      return { kind: 'negate', operand: this.parseUnary() };
    }

    if (this.acceptSymbol('+')) {
      return this.parseUnary();
    }

    return this.parsePower();
  }

  private parsePower(): Expression {
    const left = this.parseConcatenation();

    if (this.acceptSymbol('**') || this.acceptPhrase('matematica_elev')) {
      return { kind: 'binary', operator: 'power', left, right: this.parseUnary() };
    }

    return left;
  }

  private isAdjacentText(previous: Expression): boolean {
    if (this.current.kind === 'string') {
      return true;
    }

    const previousIsText = previous.kind === 'literal' && typeof previous.value === 'string';

    if (!previousIsText || this.current.kind !== 'word') {
      return false;
    }

    const isShortNameAtLineEnd = this.current.text.length === 1 && this.isStatementEndAt(this.position + 1);

    return isShortNameAtLineEnd || !isContinuationWord(this.current.normalized);
  }

  private parseConcatenation(): Expression {
    const parts = [this.parsePrimary()];

    while (this.isAdjacentText(parts[parts.length - 1])) {
      parts.push(this.parsePrimary());
    }

    return parts.length === 1 ? (parts[0]) : { kind: 'concat', parts };
  }

  private parsePrimary(): Expression {
    const token = this.current;

    if (token.kind === 'number') {
      this.advance();

      return { kind: 'literal', value: Number(token.text) };
    }

    if (token.kind === 'string') {
      return this.parseString();
    }

    if (this.acceptSymbol('(')) {
      const inner = this.parseValue();
      this.expectSymbol(')');

      return inner;
    }

    if (token.kind !== 'word') {
      this.fail();
    }

    return this.parseCommandValue() ?? this.parseName();
  }

  private parseString(): Expression {
    const token = this.advance();

    if (!token.terminated) {
      this.fail();
    }

    const value: Value = token.text.slice(1, -1);

    return { kind: 'literal', value };
  }

  private parseCommandValue(): Expression | null {
    return (
      this.attempt(() => this.parseInput()) ??
      this.attempt(() => this.parseRandom()) ??
      this.attempt(() => this.parseListValue()) ??
      this.attempt(() => this.parseListHas()) ??
      this.attempt(() => this.parseListSize()) ??
      this.attempt(() => this.parseFileExists()) ??
      this.attempt(() => this.parseFileRead()) ??
      this.attempt(() => this.parseTypeOf()) ??
      this.parseBoolean()
    );
  }

  private parseInput(): Expression {
    const isSingleWord = this.peekPhrase('digitado')?.length === 1;
    const words = this.expectPhrase('digitado');
    const numeric = words.some((word) => NUMERIC_INPUT_WORDS.includes(word));

    return { kind: 'input', numeric, variableName: isSingleWord ? (words[0]) : null };
  }

  private parseRandom(): Expression {
    this.expectPhrase('aleatorio');
    const minimum = this.parseAdditive();
    this.expectPhrase('aleatorioEntre');

    return { kind: 'random', minimum, maximum: this.parseAdditive() };
  }

  private parseListValue(): Expression {
    this.expectPhrase('declaraListas');
    const name = this.expectName();

    if (this.acceptPhrase('listaNaPosicao')) {
      return { kind: 'listGet', name, index: this.parseAdditive() };
    }

    return { kind: 'listValue', name };
  }

  private parseListHas(): Expression {
    this.expectPhrase('tiver_lista');
    const value = this.parseAdditive();
    this.expectPhrase('tiver_interno_lista');

    return { kind: 'listHas', value, name: this.expectName() };
  }

  private parseListSize(): Expression {
    this.expectPhrase('tamanho_da_lista');

    return { kind: 'listSize', name: this.expectName() };
  }

  private parseFileExists(): Expression {
    if (this.acceptPhrase('arquivo_existe_completo')) {
      return { kind: 'fileExists', path: this.parseAdditive(), negated: false };
    }

    this.expectPhrase('arquivo_existe');
    const path = this.parseAdditive();

    if (this.acceptPhrase('arquivo_existe_nao_sub_existe')) {
      return { kind: 'fileExists', path, negated: true };
    }

    this.expectPhrase('arquivo_existe_sub_existe');

    return { kind: 'fileExists', path, negated: false };
  }

  private parseFileRead(): Expression {
    this.expectPhrase('leia_arquivo');

    return { kind: 'fileRead', path: this.parseAdditive() };
  }

  private parseTypeOf(): Expression {
    this.expectPhrase('tipo_variavel');

    return { kind: 'typeOf', value: this.parseAdditive() };
  }

  private parseBoolean(): Expression | null {
    if (this.acceptPhrase('logico_true')) {
      return { kind: 'literal', value: true };
    }

    if (this.acceptPhrase('logico_false')) {
      return { kind: 'literal', value: false };
    }

    return null;
  }

  private parseName(): Expression {
    const name = this.expectName();

    if (this.acceptSymbol('(')) {
      const values = this.isSymbol(')') ? [] : this.parseValueList();
      this.expectSymbol(')');

      return { kind: 'call', name, values };
    }

    if (this.acceptPhrase('passandoParametros')) {
      return { kind: 'call', name, values: this.parseValueList() };
    }

    return this.attempt(() => this.parseSlice(name)) ?? { kind: 'variable', name };
  }

  private parseSlice(name: string): Expression {
    const bracket = this.acceptSymbol('[');

    if (!bracket && !this.acceptPhrase('percorrer_lst_str_a_cada') && this.current.kind !== 'number') {
      this.fail();
    }

    const start = this.parseAdditive();

    if (!this.acceptSymbol(':')) {
      this.expectPhrase('percorrer_lst_str_a_cada_subum');
    }

    const end = this.parseAdditive();
    const hasStep = this.acceptSymbol(':') || this.acceptPhrase('percorrer_lst_str_a_cada_subdois') !== null;
    const step = hasStep ? this.parseAdditive() : null;

    if (bracket) {
      this.expectSymbol(']');
    }

    return { kind: 'slice', name, start, end, step };
  }
}
