import { resolveColor } from './colors';
import type { Expression, Statement, StatementKind, Value } from './ast';
import type { Locale } from './messages';
import { translateMessage } from './messages';
import { parse } from './parser';
import {
  capitalize,
  floorModulo,
  formatValue,
  isTruthy,
  sliceBackward,
  sliceForward,
  typeNameOf,
  valuesAreEqual,
} from './values';
import { readScriptVersion } from './version';
import type { VirtualFileSystem } from './virtualFileSystem';
import { importCandidates, withSafiraExtension } from './virtualFileSystem';

const DEFAULT_TONE_SECONDS = 0.5;

export type Effect =
  | { type: 'step'; file: string; line: number }
  | { type: 'output'; inline: boolean; text: string; color: string }
  | { type: 'clear' }
  | { type: 'input' }
  | { type: 'sleep'; milliseconds: number }
  | { type: 'tone'; frequency: number; milliseconds: number }
  | { type: 'files' };

export type Execution<Result> = Generator<Effect, Result, string | undefined>;

type Signal = 'normal' | 'break' | 'continue' | 'return' | 'halt';

interface FunctionDefinition {
  parameters: string[] | null;
  body: Statement[];
  file: string;
}

export interface VariableSnapshot {
  name: string;
  value: string;
  type: string;
}

export interface InterpreterOptions {
  files: VirtualFileSystem;
  locale: Locale;
  random?: (minimum: number, maximum: number) => number;
}

const MAXIMUM_CALL_DEPTH = 400;
const MILLISECONDS_PER_SECOND = 1000;
const ESCAPED_NEWLINE = /\\n/g;

const EXAMPLE_BY_STATEMENT: Partial<Record<StatementKind, string>> = {
  print: '02',
  assign: '01',
  if: '04',
  while: '05',
  repeat: '06',
  wait: '07',
  increment: '09',
  functionDeclaration: '10',
  fileCreate: '11',
  fileDelete: '11',
  fileAppend: '11',
  fileOverwrite: '11',
  import: '12',
  break: '14',
  continue: '13',
  halt: '15',
  listDeclare: '16',
  listDeclareSized: '16',
  listSet: '16',
  listInsert: '16',
  listRemove: '16',
  forEach: '17',
  forRange: '20',
  try: '21',
};

export class SafiraError extends Error {
  public file = '';
  public line = 0;
  public example: string | null = null;
}

const randomInteger = (minimum: number, maximum: number): number =>
  minimum + Math.floor(Math.random() * (maximum - minimum + 1));

const expandNewlines = (text: string): string => text.replace(ESCAPED_NEWLINE, '\n');

export class Interpreter {
  private readonly variables = new Map<string, Value>();
  private readonly functions = new Map<string, FunctionDefinition>();
  private readonly files: VirtualFileSystem;
  private readonly locale: Locale;
  private readonly random: (minimum: number, maximum: number) => number;
  private currentFile = '';
  private callDepth = 0;
  private returnValue: Value = null;
  private lastColor = '';

  public constructor(options: InterpreterOptions) {
    this.files = options.files;
    this.locale = options.locale;
    this.random = options.random ?? randomInteger;
  }

  public *run(file: string): Execution<void> {
    const source = this.files.read(file) ?? '';
    yield* this.runSource(file, source);
  }

  public getVariables(): VariableSnapshot[] {
    return [...this.variables].map(([name, value]) => ({
      name,
      value: formatValue(value),
      type: typeNameOf(value),
    }));
  }

  private *runSource(file: string, source: string): Execution<Signal> {
    const previousFile = this.currentFile;
    this.currentFile = file;
    const signal = yield* this.runBlock(parse(readScriptVersion(source).body));
    this.currentFile = previousFile;

    return signal;
  }

  private fail(key: string, ...values: (string | number)[]): never {
    throw new SafiraError(translateMessage(this.locale, key, ...values));
  }

  private failWithDetail(key: string, detail: string): never {
    throw new SafiraError(`${translateMessage(this.locale, key)} ${detail}`.trim());
  }

  private *runBlock(statements: Statement[]): Execution<Signal> {
    for (const statement of statements) {
      const signal = yield* this.runStatement(statement);

      if (signal !== 'normal') {
        return signal;
      }
    }

    return 'normal';
  }

  private *runStatement(statement: Statement): Execution<Signal> {
    yield { type: 'step', file: this.currentFile, line: statement.line };

    try {
      return yield* this.execute(statement);
    } catch (error) {
      if (error instanceof SafiraError && error.line === 0) {
        error.file = this.currentFile;
        error.line = statement.line;
        error.example = EXAMPLE_BY_STATEMENT[statement.kind] ?? null;
      }

      throw error;
    }
  }

  private *execute(statement: Statement): Execution<Signal> {
    switch (statement.kind) {
      case 'print':
        yield* this.executePrint(statement.value, statement.inline);

        return 'normal';
      case 'assign':
        this.variables.set(statement.name, yield* this.evaluate(statement.value));

        return 'normal';
      case 'if':
        return yield* this.executeIf(statement);
      case 'while':
        return yield* this.executeWhile(statement.condition, statement.body);
      case 'repeat':
        return yield* this.executeRepeat(statement.count, statement.body);
      case 'forRange':
        return yield* this.executeForRange(statement);
      case 'forEach':
        return yield* this.executeForEach(statement);
      case 'functionDeclaration':
        this.functions.set(statement.name, {
          parameters: statement.parameters,
          body: statement.body,
          file: this.currentFile,
        });

        return 'normal';
      case 'expression':
        yield* this.evaluate(statement.value);

        return this.pendingHalt ? 'halt' : 'normal';
      case 'return':
        this.returnValue = statement.value === null ? '' : yield* this.evaluate(statement.value);

        return 'return';
      case 'break':
        return 'break';
      case 'continue':
        return 'continue';
      case 'halt':
        return 'halt';
      case 'clear':
        yield { type: 'clear' };

        return 'normal';
      case 'tone':
        yield* this.executeTone(statement);

        return 'normal';
      case 'wait':
        yield* this.executeWait(statement.amount, statement.unit);

        return 'normal';
      case 'import':
        return yield* this.executeImport(statement.name);
      case 'try':
        return yield* this.executeTry(statement);
      case 'invalid':
        return this.failWithDetail(statement.messageKey, statement.detail);
      default:
        yield* this.executeData(statement);

        return 'normal';
    }
  }

  private pendingHalt = false;

  private *executeData(statement: Statement): Execution<void> {
    switch (statement.kind) {
      case 'fileCreate':
        yield* this.executeFileCreate(statement.path);
        break;
      case 'fileDelete':
        yield* this.executeFileDelete(statement.path);
        break;
      case 'fileAppend':
        yield* this.executeFileWrite(statement.text, statement.path, 'append');
        break;
      case 'fileOverwrite':
        yield* this.executeFileWrite(statement.text, statement.path, 'overwrite');
        break;
      case 'listDeclare':
        yield* this.executeListDeclare(statement.name, statement.values);
        break;
      case 'listDeclareSized':
        yield* this.executeListDeclareSized(statement.name, statement.size);
        break;
      case 'listSet':
        yield* this.executeListSet(statement.name, statement.index, statement.value);
        break;
      case 'listInsert':
        yield* this.executeListInsert(statement.name, statement.value, statement.position);
        break;
      case 'listRemove':
        yield* this.executeListRemove(statement.name, statement.value);
        break;
      case 'increment':
        yield* this.executeIncrement(statement.name, statement.amount, statement.sign);
        break;
      case 'replaceText':
        yield* this.executeReplaceText(statement.name, statement.search, statement.replacement);
        break;
      default:
        break;
    }
  }

  private *executePrint(value: Expression | null, inline: boolean): Execution<void> {
    this.lastColor = '';
    const result = value === null ? '' : yield* this.evaluate(value);
    const color = this.lastColor;
    this.lastColor = '';
    yield { type: 'output', inline, text: expandNewlines(formatValue(result)), color };
  }

  private *executeIf(statement: Statement & { kind: 'if' }): Execution<Signal> {
    for (const branch of statement.branches) {
      if (isTruthy(yield* this.evaluate(branch.condition))) {
        return yield* this.runBlock(branch.body);
      }
    }

    return statement.otherwise === null ? 'normal' : yield* this.runBlock(statement.otherwise);
  }

  private *runLoopBody(body: Statement[]): Execution<Signal | 'exit'> {
    const signal = yield* this.runBlock(body);

    if (signal === 'break') {
      return 'exit';
    }

    return signal === 'continue' ? 'normal' : signal;
  }

  private *executeWhile(condition: Expression, body: Statement[]): Execution<Signal> {
    while (isTruthy(yield* this.evaluate(condition))) {
      const signal = yield* this.runLoopBody(body);

      if (signal === 'exit') {
        return 'normal';
      }

      if (signal !== 'normal') {
        return signal;
      }
    }

    return 'normal';
  }

  private *executeRepeat(count: Expression, body: Statement[]): Execution<Signal> {
    const times = this.toInteger(yield* this.evaluate(count));

    for (let round = 0; round < times; round += 1) {
      const signal = yield* this.runLoopBody(body);

      if (signal === 'exit') {
        return 'normal';
      }

      if (signal !== 'normal') {
        return signal;
      }
    }

    return 'normal';
  }

  private *executeForRange(statement: Statement & { kind: 'forRange' }): Execution<Signal> {
    const start = this.toInteger(yield* this.evaluate(statement.start));
    const end = this.toInteger(yield* this.evaluate(statement.end));
    const direction = start > end ? -1 : 1;

    for (let value = start; direction * value <= direction * end; value += direction) {
      this.variables.set(statement.name, value);
      const signal = yield* this.runLoopBody(statement.body);

      if (signal === 'exit') {
        return 'normal';
      }

      if (signal !== 'normal') {
        return signal;
      }
    }

    return 'normal';
  }

  private *executeForEach(statement: Statement & { kind: 'forEach' }): Execution<Signal> {
    const iterable = yield* this.evaluate(statement.iterable);

    if (typeof iterable !== 'string' && !Array.isArray(iterable)) {
      return this.fail('variavel_nao_numerica', formatValue(iterable));
    }

    for (const item of [...iterable]) {
      this.variables.set(statement.name, item);
      const signal = yield* this.runLoopBody(statement.body);

      if (signal === 'exit') {
        return 'normal';
      }

      if (signal !== 'normal') {
        return signal;
      }
    }

    return 'normal';
  }

  private *executeWait(amount: Expression, unit: 'seconds' | 'milliseconds'): Execution<void> {
    const value = yield* this.evaluate(amount);

    if (typeof value !== 'number') {
      this.fail('wait_not_numeric');
    }

    yield { type: 'sleep', milliseconds: unit === 'seconds' ? value * MILLISECONDS_PER_SECOND : value };
  }

  private *executeTone(statement: Statement & { kind: 'tone' }): Execution<void> {
    const value = statement.amount === null ? DEFAULT_TONE_SECONDS : yield* this.evaluate(statement.amount);

    if (typeof value !== 'number') {
      this.fail('wait_not_numeric');
    }

    const milliseconds = statement.unit === 'seconds' ? value * MILLISECONDS_PER_SECOND : value;

    for (const frequency of statement.frequencies) {
      yield { type: 'tone', frequency, milliseconds };
    }
  }

  private *executeImport(name: string): Execution<Signal> {
    const found = importCandidates(this.currentFile, name).find((path) => this.files.exists(path));
    const source = found === undefined ? null : this.files.read(found);

    if (found === undefined || source === null) {
      const file = withSafiraExtension(name);
      this.fail('erro_abrir_biblioteca', file, translateMessage(this.locale, 'arquivo_nao_existe', file));
    }

    const signal = yield* this.runSource(found, source);

    return signal === 'halt' ? 'halt' : 'normal';
  }

  private *executeTry(statement: Statement & { kind: 'try' }): Execution<Signal> {
    let failed = false;
    let signal: Signal = 'normal';

    try {
      signal = yield* this.runBlock(statement.body);
    } catch (error) {
      if (!(error instanceof SafiraError)) {
        throw error;
      }

      failed = true;
    }

    if (signal !== 'normal') {
      return signal;
    }

    const clause = failed ? statement.onError : statement.onSuccess;
    const clauseSignal = clause === null ? 'normal' : yield* this.runBlock(clause);

    if (clauseSignal !== 'normal') {
      return clauseSignal;
    }

    return statement.always === null ? 'normal' : yield* this.runBlock(statement.always);
  }

  private *evaluatePath(path: Expression): Execution<string> {
    const value = yield* this.evaluate(path);
    const text = formatValue(value);

    if (text === '') {
      this.fail('precisa_nome_arquivo');
    }

    return text;
  }

  private *executeFileCreate(path: Expression): Execution<void> {
    const file = yield* this.evaluatePath(path);

    if (!this.files.exists(file)) {
      this.files.write(file, '');
      yield { type: 'files' };
    }
  }

  private *executeFileDelete(path: Expression): Execution<void> {
    const file = yield* this.evaluatePath(path);

    if (!this.files.delete(file)) {
      this.fail('arquivo_nao_existe', file);
    }

    yield { type: 'files' };
  }

  private *executeFileWrite(text: Expression, path: Expression, mode: 'append' | 'overwrite'): Execution<void> {
    const file = yield* this.evaluatePath(path);
    const content = expandNewlines(formatValue(yield* this.evaluate(text)));

    if (!this.files.exists(file)) {
      this.fail('arquivo_nao_existe', file);
    }

    if (mode === 'append') {
      this.files.append(file, content);
    } else {
      this.files.write(file, content);
    }

    yield { type: 'files' };
  }

  private *evaluateAll(values: Expression[]): Execution<Value[]> {
    const results: Value[] = [];

    for (const value of values) {
      results.push(yield* this.evaluate(value));
    }

    return results;
  }

  private *executeListDeclare(name: string, values: Expression[]): Execution<void> {
    this.variables.set(name, yield* this.evaluateAll(values));
  }

  private *executeListDeclareSized(name: string, size: Expression): Execution<void> {
    const length = this.toInteger(yield* this.evaluate(size));
    this.variables.set(name, new Array<Value>(length).fill(''));
  }

  private getList(name: string): Value[] {
    const value = this.getVariable(name);

    if (!Array.isArray(value)) {
      return this.failWithDetail('nao_e_lista', name);
    }

    return value;
  }

  private getVariable(name: string): Value {
    const value = this.variables.get(name);

    if (value === undefined) {
      return this.failWithDetail('voce_precisa_definir_variavel', `'${name}'`);
    }

    return value;
  }

  private toInteger(value: Value): number {
    if (typeof value !== 'number') {
      return this.fail('variavel_nao_numerica', formatValue(value));
    }

    return Math.trunc(value);
  }

  private checkPosition(position: number, limit: number): void {
    if (position < 1) {
      this.fail('posicao_menor_limite_lista');
    }

    if (position > limit) {
      this.fail('posicao_maior_limite_lista');
    }
  }

  private *executeListSet(name: string, index: Expression, value: Expression): Execution<void> {
    const list = this.getList(name);
    const position = this.toInteger(yield* this.evaluate(index));
    this.checkPosition(position, list.length);
    list[position - 1] = yield* this.evaluate(value);
  }

  private *executeListInsert(name: string, value: Expression, position: Expression | 'start' | 'end'): Execution<void> {
    const list = this.getList(name);
    const item = yield* this.evaluate(value);

    if (position === 'start') {
      list.unshift(item);
    } else if (position === 'end') {
      list.push(item);
    } else {
      const index = this.toInteger(yield* this.evaluate(position));
      this.checkPosition(index, list.length + 1);
      list.splice(index - 1, 0, item);
    }
  }

  private *executeListRemove(name: string, value: Expression): Execution<void> {
    const list = this.getList(name);
    const item = yield* this.evaluate(value);
    const index = list.findIndex((candidate) => valuesAreEqual(candidate, item));

    if (index === -1) {
      this.failWithDetail('nao_esta_na_lista', `"${formatValue(item)}" "${name}"`);
    }

    list.splice(index, 1);
  }

  private *executeIncrement(name: string, amount: Expression, sign: 1 | -1): Execution<void> {
    const current = this.getVariable(name);
    const value = yield* this.evaluate(amount);

    if (typeof current !== 'number') {
      this.fail('variavel_nao_numerica', name);
    }

    if (typeof value !== 'number') {
      this.fail('variavel_nao_numerica', formatValue(value));
    }

    this.variables.set(name, current + sign * value);
  }

  private *executeReplaceText(name: string, search: Expression, replacement: Expression): Execution<void> {
    const current = this.getVariable(name);

    if (typeof current !== 'string') {
      this.fail('p_usar_substituicao_variavel');
    }

    const from = formatValue(yield* this.evaluate(search));
    const to = formatValue(yield* this.evaluate(replacement));
    this.variables.set(name, current.split(from).join(to));
  }

  private *evaluate(expression: Expression): Execution<Value> {
    switch (expression.kind) {
      case 'literal':
        return expression.value;
      case 'variable':
        return this.getVariable(expression.name);
      case 'binary':
        return yield* this.evaluateBinary(expression);
      case 'negate':
        return -this.toNumber(yield* this.evaluate(expression.operand));
      case 'concat':
        return (yield* this.evaluateAll(expression.parts)).map(formatValue).join('');
      case 'format':
        return yield* this.evaluateFormat(expression.template, expression.values);
      case 'colored':
        return yield* this.evaluateColored(expression.value, expression.color);
      case 'case':
        return yield* this.evaluateCase(expression);
      case 'call':
        return yield* this.evaluateCall(expression.name, expression.values);
      case 'listValue':
        return this.getList(expression.name);
      case 'listGet':
        return yield* this.evaluateListGet(expression.name, expression.index);
      case 'listHas': {
        const item = yield* this.evaluate(expression.value);

        return this.getList(expression.name).some((candidate) => valuesAreEqual(candidate, item));
      }
      case 'listSize':
        return this.getList(expression.name).length;
      case 'typeOf':
        return typeNameOf(yield* this.evaluate(expression.value));
      case 'input':
        return yield* this.evaluateInput(expression.numeric, expression.variableName);
      case 'random':
        return yield* this.evaluateRandom(expression.minimum, expression.maximum);
      case 'fileRead':
        return yield* this.evaluateFileRead(expression.path);
      case 'fileExists':
        return (yield* this.evaluateFileExists(expression.path)) !== expression.negated;
      case 'slice':
        return yield* this.evaluateSlice(expression);
    }
  }

  private toNumber(value: Value): number {
    if (typeof value === 'boolean') {
      return Number(value);
    }

    if (typeof value !== 'number') {
      return this.failWithDetail('nao_possivel_fazer_conta', `|${formatValue(value)}|`);
    }

    return value;
  }

  private *evaluateBinary(expression: Expression & { kind: 'binary' }): Execution<Value> {
    const { operator } = expression;

    if (operator === 'and' || operator === 'or') {
      const left = yield* this.evaluate(expression.left);
      const shortCircuits = isTruthy(left) === (operator === 'or');

      return shortCircuits ? left : yield* this.evaluate(expression.right);
    }

    const left = yield* this.evaluate(expression.left);
    const right = yield* this.evaluate(expression.right);

    switch (operator) {
      case 'add':
        return this.add(left, right);
      case 'equal':
        return valuesAreEqual(left, right);
      case 'notEqual':
        return !valuesAreEqual(left, right);
      case 'less':
      case 'lessOrEqual':
      case 'greater':
      case 'greaterOrEqual':
        return this.compare(operator, left, right);
      default:
        return this.calculate(operator, this.toNumber(left), this.toNumber(right));
    }
  }

  private add(left: Value, right: Value): Value {
    if (typeof left === 'string' || typeof right === 'string') {
      return formatValue(left) + formatValue(right);
    }

    if (Array.isArray(left) && Array.isArray(right)) {
      return [...left, ...right];
    }

    return this.toNumber(left) + this.toNumber(right);
  }

  private compare(operator: 'less' | 'lessOrEqual' | 'greater' | 'greaterOrEqual', left: Value, right: Value): boolean {
    const bothText = typeof left === 'string' && typeof right === 'string';
    const bothNumeric = typeof left !== 'string' && typeof right !== 'string';

    if ((!bothText && !bothNumeric) || Array.isArray(left) || Array.isArray(right) || left === null || right === null) {
      this.failWithDetail('nao_possivel_fazer_condicao', `|${formatValue(left)} ${formatValue(right)}|`);
    }

    switch (operator) {
      case 'less':
        return left < right;
      case 'lessOrEqual':
        return left <= right;
      case 'greater':
        return left > right;
      default:
        return left >= right;
    }
  }

  private calculate(
    operator: 'subtract' | 'multiply' | 'divide' | 'modulo' | 'power',
    left: number,
    right: number,
  ): number {
    if ((operator === 'divide' || operator === 'modulo') && right === 0) {
      this.fail('math_division_by_zero');
    }

    switch (operator) {
      case 'subtract':
        return left - right;
      case 'multiply':
        return left * right;
      case 'divide':
        return left / right;
      case 'modulo':
        return floorModulo(left, right);
      default:
        return left ** right;
    }
  }

  private *evaluateFormat(template: Expression, values: Expression[]): Execution<Value> {
    const text = yield* this.evaluate(template);

    if (typeof text !== 'string') {
      return this.fail('format_needs_text');
    }

    const results = yield* this.evaluateAll(values);
    const pieces = text.split('%');

    if (pieces.length - 1 !== results.length) {
      return this.fail('format_args_mismatch', pieces.length - 1, results.length);
    }

    return pieces.map((piece, index) => piece + formatValue(results[index] ?? '')).join('');
  }

  private *evaluateColored(value: Expression, color: Expression): Execution<Value> {
    const result = yield* this.evaluate(value);
    this.lastColor = yield* this.evaluateColor(color);

    return result;
  }

  private *evaluateColor(color: Expression): Execution<string> {
    const namedColor = color.kind === 'variable' && !this.variables.has(color.name) ? resolveColor(color.name) : null;

    if (namedColor !== null) {
      return namedColor;
    }

    const text = formatValue(yield* this.evaluate(color));

    return resolveColor(text) ?? text;
  }

  private *evaluateCase(expression: Expression & { kind: 'case' }): Execution<Value> {
    const value = yield* this.evaluate(expression.value);

    if (typeof value !== 'string') {
      return this.fail('p_maiusc_minusc_cap_texto', expression.mode);
    }

    if (expression.mode === 'upper') {
      return value.toUpperCase();
    }

    return expression.mode === 'lower' ? value.toLowerCase() : capitalize(value);
  }

  private bindParameters(name: string, definition: FunctionDefinition, values: Value[]): void {
    const parameters = definition.parameters ?? [];

    if (definition.parameters === null && values.length > 0) {
      this.fail('funcao_informou_mais_parametros', name);
    }

    if (values.length === 0 && parameters.length > 0) {
      this.fail('funcao_nao_passou_parametros', name, parameters.length);
    }

    if (parameters.length !== values.length) {
      this.fail('funcao_tem_parametros_divergentes', name, parameters.length, values.length);
    }

    parameters.forEach((parameter, index) => {
      this.variables.set(parameter, values[index] ?? null);
    });
  }

  private *evaluateCall(name: string, values: Expression[]): Execution<Value> {
    const definition = this.functions.get(name);

    if (definition === undefined) {
      return this.fail('funcao_nao_existe', name);
    }

    if (this.callDepth >= MAXIMUM_CALL_DEPTH) {
      return this.fail('recursion_limit');
    }

    this.bindParameters(name, definition, yield* this.evaluateAll(values));
    this.callDepth += 1;
    const previousFile = this.currentFile;
    this.currentFile = definition.file;
    const signal = yield* this.runBlock(definition.body);
    this.currentFile = previousFile;
    this.callDepth -= 1;

    if (signal === 'halt') {
      this.pendingHalt = true;
    }

    return signal === 'return' ? this.returnValue : '';
  }

  private *evaluateListGet(name: string, index: Expression): Execution<Value> {
    const position = this.toInteger(yield* this.evaluate(index));
    const list = this.getList(name);
    this.checkPosition(position, list.length);

    return list[position - 1] ?? null;
  }

  private *evaluateInput(numeric: boolean, variableName: string | null): Execution<Value> {
    if (variableName !== null && this.variables.has(variableName)) {
      return this.getVariable(variableName);
    }

    const typed = (yield { type: 'input' }) ?? '';

    if (!numeric) {
      return typed;
    }

    const value = Number(typed);

    if (typed.trim() === '' || Number.isNaN(value)) {
      return this.failWithDetail('digitou_caractere', `"${typed}"`);
    }

    return value;
  }

  private *evaluateRandom(minimum: Expression, maximum: Expression): Execution<Value> {
    const first = yield* this.evaluate(minimum);
    const second = yield* this.evaluate(maximum);

    if (typeof first !== 'number') {
      return this.fail('aleatorio_valor1_nao_numerico');
    }

    if (typeof second !== 'number') {
      return this.fail('aleatorio_valor2_nao_numerico');
    }

    const low = Math.trunc(first);
    const high = Math.trunc(second);

    if (low === high) {
      return this.fail('aleatorio_valor1_igual_valo2');
    }

    if (low > high) {
      return this.fail('aleatorio_valor1_maior_valo2');
    }

    return this.random(low, high);
  }

  private *evaluateFileRead(path: Expression): Execution<Value> {
    const file = yield* this.evaluatePath(path);

    return this.files.read(file) ?? this.fail('arquivo_nao_existe', file);
  }

  private *evaluateFileExists(path: Expression): Execution<boolean> {
    return this.files.exists(yield* this.evaluatePath(path));
  }

  private *evaluateSlice(expression: Expression & { kind: 'slice' }): Execution<Value> {
    const text = this.getVariable(expression.name);

    if (typeof text !== 'string') {
      return this.fail('slice_only_text');
    }

    const start = this.toInteger(yield* this.evaluate(expression.start));
    const end = this.toInteger(yield* this.evaluate(expression.end));
    const step = expression.step === null ? null : this.toInteger(yield* this.evaluate(expression.step));

    for (const position of [start, end]) {
      if (position < 1 || position > text.length) {
        this.fail('slice_out_of_range', position, text.length);
      }
    }

    return start > end ? sliceBackward(text, start, end, step) : sliceForward(text, start, end, step);
  }
}
