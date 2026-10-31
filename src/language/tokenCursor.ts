import type { CommandKey } from './phrases';
import { getPhrases } from './phrases';
import type { Token } from './tokenizer';

export class ParseFailure extends Error {}

export class TokenCursor {
  protected position = 0;

  public constructor(protected readonly tokens: Token[]) {}

  protected get current(): Token {
    return this.tokenAt(this.position);
  }

  protected tokenAt(index: number): Token {
    const lastToken = this.tokens[this.tokens.length - 1];

    return this.tokens[index] ?? lastToken;
  }

  protected advance(): Token {
    const token = this.current;
    this.position += 1;

    return token;
  }

  protected fail(): never {
    throw new ParseFailure();
  }

  protected isSymbol(text: string): boolean {
    return this.current.kind === 'symbol' && this.current.text === text;
  }

  protected acceptSymbol(text: string): boolean {
    if (this.isSymbol(text)) {
      this.position += 1;

      return true;
    }

    return false;
  }

  protected expectSymbol(text: string): void {
    if (!this.acceptSymbol(text)) {
      this.fail();
    }
  }

  private phraseLengthAt(words: string[], index: number): boolean {
    return words.every((word, offset) => {
      const token = this.tokenAt(index + offset);

      return token.kind === 'word' && token.normalized === word;
    });
  }

  protected peekPhrase(key: CommandKey): string[] | null {
    return getPhrases(key).find((words) => this.phraseLengthAt(words, this.position)) ?? null;
  }

  protected acceptPhrase(key: CommandKey): string[] | null {
    const words = this.peekPhrase(key);

    if (words !== null) {
      this.position += words.length;
    }

    return words;
  }

  protected expectPhrase(key: CommandKey): string[] {
    return this.acceptPhrase(key) ?? this.fail();
  }

  protected expectName(): string {
    if (this.current.kind !== 'word') {
      this.fail();
    }

    return this.advance().text;
  }

  protected isStatementEndAt(index: number): boolean {
    const token = this.tokenAt(index);
    const isBlockSymbol = token.kind === 'symbol' && (token.text === '{' || token.text === '}');

    return token.kind === 'newline' || token.kind === 'end' || isBlockSymbol;
  }

  protected isStatementEnd(): boolean {
    return this.isStatementEndAt(this.position);
  }

  protected skipNewlines(): void {
    while (this.current.kind === 'newline') {
      this.position += 1;
    }
  }

  protected attempt<Result>(action: () => Result): Result | null {
    const saved = this.position;

    try {
      return action();
    } catch (error) {
      if (error instanceof ParseFailure) {
        this.position = saved;

        return null;
      }

      throw error;
    }
  }
}
