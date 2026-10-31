# Safira

Web IDE and interpreter for Safira, a language in natural language. Runs only in the browser. See `README.md` for
setup and scripts.

## Security model

- User programs never reach `eval`, `Function` or the DOM. They run in `src/runtime/runner.worker.ts`.
- Program text is rendered as text in React. Print colors go through `style`, never through HTML.
- Programs only see `VirtualFileSystem`. There is no file, network or storage access from the language.

## Conventions

- Code, comments, docs and commits in English. Interface text goes through `t()`, with `pt-br` and `es` entries.
- Language words live in `src/language/commands.json`, never hardcoded in the parser.
- Parser rule order in `parser.ts` is part of the language: a rule moved up changes what programs mean.
- Full names, no magic numbers, blank line before `return`, `if` always with braces, `+= 1` instead of `++`.

Architecture, storage keys, addresses and known gaps: `docs/architecture.md`.

## Paid traps

- An unknown line must not fail at parse time, because `tente` must catch it. The parser emits an `invalid` statement.
- `legacyGolden.json` was recorded from the Python interpreter, which is gone. Do not regenerate it. A difference there
  is a compatibility break, or an intentional fix that belongs in `interpreter.test.ts` and in the changelog.
- Variables are global, functions included. Parameters overwrite globals. This is existing behavior that scripts rely on.
- `a`, `e`, `o` are both phrases and valid names. `isAdjacentText` in `expressionParser.ts` handles the conflict.
- Scripts that drive the browser must fix the locale to `en-US`: the interface follows the browser language.
- `mostre` examples named `Continue` and `Pare` collide with button names in tests. Keep action labels distinct.
- Breakpoints snap to the next command in `snapBreakpoints`, because comments never produce a step.
- In Playwright, wait for the focus to enter a Radix menu before pressing arrows, or the key moves the trigger.
- `textScramble.ts` writes in text nodes owned by React and must end with the exact final text.
- Radix marks everything behind a modal as `aria-hidden`, so that attribute cannot be used to skip text.
- `Modal` closes by unmounting, so the closing animation plays on a clone left in `document.body`.
- Empty folders are a `.keep` file in `Project.files`. Lists shown to the user go through `visibleFiles`.
- Waiting for animations in Playwright needs `allSettled`: a removed element rejects `finished`.
- A new language version must be added to `SUPPORTED_VERSIONS` while it can still run the older ones.
