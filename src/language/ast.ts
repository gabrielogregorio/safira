import type { KeyMode } from './keys';

export type Value = number | string | boolean | Value[] | null;

export type BinaryOperator =
  | 'add'
  | 'subtract'
  | 'multiply'
  | 'divide'
  | 'modulo'
  | 'power'
  | 'equal'
  | 'notEqual'
  | 'less'
  | 'lessOrEqual'
  | 'greater'
  | 'greaterOrEqual'
  | 'and'
  | 'or';

export type CaseMode = 'upper' | 'lower' | 'capitalize';

export type Expression =
  | { kind: 'literal'; value: Value }
  | { kind: 'variable'; name: string }
  | { kind: 'binary'; operator: BinaryOperator; left: Expression; right: Expression }
  | { kind: 'negate'; operand: Expression }
  | { kind: 'concat'; parts: Expression[] }
  | { kind: 'format'; template: Expression; values: Expression[] }
  | { kind: 'colored'; value: Expression; color: Expression }
  | { kind: 'case'; mode: CaseMode; value: Expression }
  | { kind: 'call'; name: string; values: Expression[] }
  | { kind: 'listValue'; name: string }
  | { kind: 'listGet'; name: string; index: Expression }
  | { kind: 'listHas'; name: string; value: Expression }
  | { kind: 'listSize'; name: string }
  | { kind: 'typeOf'; value: Expression }
  | { kind: 'input'; numeric: boolean; variableName: string | null }
  | { kind: 'random'; minimum: Expression; maximum: Expression }
  | { kind: 'fileRead'; path: Expression }
  | { kind: 'fileExists'; path: Expression; negated: boolean }
  | { kind: 'keyState'; mode: KeyMode; parts: KeyPart[] }
  | { kind: 'slice'; name: string; start: Expression; end: Expression; step: Expression | null };

/** A word is a key name, unless a variable with text has that name when the program runs. */
export type KeyPart = { kind: 'name'; text: string } | { kind: 'value'; value: Expression };

export interface ConditionalBranch {
  condition: Expression;
  body: Statement[];
}

export type StatementBody =
  | { kind: 'print'; value: Expression | null; inline: boolean }
  | { kind: 'assign'; name: string; value: Expression }
  | { kind: 'if'; branches: ConditionalBranch[]; otherwise: Statement[] | null }
  | { kind: 'while'; condition: Expression; body: Statement[] }
  | { kind: 'repeat'; count: Expression; body: Statement[] }
  | { kind: 'forRange'; name: string; start: Expression; end: Expression; body: Statement[] }
  | { kind: 'forEach'; iterable: Expression; name: string; body: Statement[] }
  | { kind: 'functionDeclaration'; name: string; parameters: string[] | null; body: Statement[] }
  | { kind: 'expression'; value: Expression }
  | { kind: 'return'; value: Expression | null }
  | { kind: 'break' }
  | { kind: 'continue' }
  | { kind: 'halt' }
  | { kind: 'noop' }
  | { kind: 'clear' }
  | { kind: 'wait'; amount: Expression; unit: 'seconds' | 'milliseconds' }
  | { kind: 'tone'; frequencies: number[]; amount: Expression | null; unit: 'seconds' | 'milliseconds' }
  | { kind: 'import'; name: string }
  | {
      kind: 'try';
      body: Statement[];
      onError: Statement[] | null;
      onSuccess: Statement[] | null;
      always: Statement[] | null;
    }
  | { kind: 'fileCreate'; path: Expression }
  | { kind: 'fileDelete'; path: Expression }
  | { kind: 'fileAppend'; text: Expression; path: Expression }
  | { kind: 'fileOverwrite'; text: Expression; path: Expression }
  | { kind: 'listDeclare'; name: string; values: Expression[] }
  | { kind: 'listDeclareSized'; name: string; size: Expression }
  | { kind: 'listSet'; name: string; index: Expression; value: Expression }
  | { kind: 'listInsert'; name: string; value: Expression; position: Expression | 'start' | 'end' }
  | { kind: 'listRemove'; name: string; value: Expression }
  | { kind: 'increment'; name: string; amount: Expression; sign: 1 | -1 }
  | { kind: 'replaceText'; name: string; search: Expression; replacement: Expression }
  | { kind: 'invalid'; messageKey: string; detail: string };

export type Statement = StatementBody & { line: number };

export type StatementKind = StatementBody['kind'];
