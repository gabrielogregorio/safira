<div align="center">

# Safira

A programming language in natural language for first-time programmers, with a web IDE.

[**See it live »**](https://gabrielogregorio.github.io/safira/)

![TypeScript](https://img.shields.io/badge/TypeScript-6-3178c6)
![React](https://img.shields.io/badge/React-19-61dafb)
![Vite](https://img.shields.io/badge/Vite-8-646cff)
![Vitest](https://img.shields.io/badge/Vitest-5-6e9f18)
![Playwright](https://img.shields.io/badge/Playwright-1.62-2ead33)
![License](https://img.shields.io/badge/license-MIT-blue)

</div>

[![Safira switching to English, then running a program with a variable and a color](docs/demo.gif)](https://gabrielogregorio.github.io/safira/)

## About

Safira accepts commands the way a person talks. The same script can mix Portuguese, English, Spanish, Chinese and Japanese:

```
idade recebe 18
if idade is greater than 17 { mostre "Maior de idade" }
repeat 2 vezes { show "Oi" }
```

Everything runs in the browser, in a Web Worker. There is no server, and programs have no access to the disk: each
project has its own virtual files, which is where `crie o arquivo`, `leia o arquivo`, `importe` and saving work.

Click the dot beside a line to set a breakpoint: running stops there, and the variables inspector shows the values. On a
phone the IDE splits into Code, Output and Variables panels.

The interface, lessons and examples come in English, Portuguese, Spanish, Simplified Chinese and Japanese. Turn on Lesson mode in the Help menu for a very short tutorial with Professor Cat. He only teaches it once.

Every screen has an address: `#/new/16-listas`, `#/projects/<id>/dados%2Fnotas.txt`. Projects move between browsers as `.zip` files, which can be dropped on the home screen, and work saves itself while typing
so that it comes back after a crash or a power cut.

Every script keeps its language version on a hidden first line (`#safira 0.9`). The IDE only mentions it when the version
is not supported. A script without that line is treated as version 0.38, the last Python release.

## Set up on a new PC

1. Install [nvm](https://github.com/nvm-sh/nvm), then Node 24: `nvm install 24 && nvm use 24`
2. Clone the repository and enter it
3. Enable pnpm and install: `corepack enable && pnpm install`
4. Install the test browser: `pnpm exec playwright install --with-deps chromium`
5. Check everything: `pnpm run check:all`

Projects live in the browser `localStorage`, so they are not in the repository. Use the `.zip` export to move them
between PCs.

## Available scripts

| Script | What it does |
|---|---|
| `pnpm run dev` | Development server |
| `Ctrl+Enter` in the IDE | Runs the program, stopping at the red dots |
| `pnpm run build` | Type check and production build in `build/` |
| `pnpm run preview` | Serves the build on port 5556 |
| `pnpm run lint` / `pnpm run format` | ESLint and TypeScript / Prettier |
| `pnpm run unit` / `pnpm run unit:coverage` | Unit tests, with or without the coverage gate |
| `pnpm run e2e` | Playwright with axe, against the build |
| `pnpm run e2e:resources` | Memory and CPU in real use and idle, with `pnpm run preview` running. Memory fails the check, CPU is reported |
| `pnpm run e2e:lighthouse` | Lighthouse floors, with `pnpm run preview` running |
| `pnpm run check:all` | Format, lint, coverage, build and E2E |

## Tests

- `src/language/legacyGolden.json` holds outputs recorded from the original Python interpreter. It is the compatibility
  contract: a whole number is the only accepted difference (`3` instead of `3.0`).
- Each layer has its own tests beside the code: tokenizer, parser, interpreter, runner, projects and interface.
- `e2e/` runs the real worker, with axe in the three themes and layout checks from 320 to 1440 pixels.

## CI/CD

GitHub Actions runs lint, audit, unit tests with a coverage gate, E2E, the memory gate and CodeQL. Merging a `release/X.Y.Z`
branch into `main` creates the tag and the release; any other merge only deploys. Actions are pinned by commit hash.

| Address | What it is | Workflow |
|---|---|---|
| `https://<owner>.github.io/<repository>/` | The site, published on each merge into `main` | `deploy.yml` |
| `https://<owner>.github.io/<repository>/preview/<branch>/` | The site of a pull request, linked on it | `deploy-preview.yml` |

Both publish to the `gh-pages` branch through `.github/actions/publish-pages`, which GitHub Pages must be set to serve.
Assets use relative paths and routes use the hash, so one build works at any address.

## Language

| Layer | Folder | Role |
|---|---|---|
| Tokenizer | `src/language/tokenizer.ts` | Words, numbers, strings, comments |
| Phrases | `src/language/commands.json` | Every command in every language, and its syntax color |
| Parser | `src/language/parser.ts`, `expressionParser.ts` | Syntax tree. An unknown line only fails when it runs, so `tente` can catch it |
| Interpreter | `src/language/interpreter.ts` | A generator that pauses for input, waiting and breakpoints |
| Versions | `src/language/version.ts` | The hidden line and `SUPPORTED_VERSIONS` |

## License

MIT, see [LICENSE](LICENSE). The bundled Istok Web and JetBrains Mono fonts are under the SIL Open Font License 1.1, and the interface sounds are from Kenney's Interface Sounds pack, under CC0. The Brazilian language sound plays the opening of Asa Branca, by Luiz Gonzaga and Humberto Teixeira (1947), which is not in the public domain and is not covered by the MIT license.
