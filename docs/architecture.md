# Architecture

Safira runs only in the browser. There is no server, and programs never reach the disk, the network or browser storage.

## Layers

| Layer | Folder | Role |
|---|---|---|
| Language | `src/language` | Tokenizer, phrase table, parser, interpreter, formatter, highlighting, versions, virtual files |
| Runtime | `src/runtime` | `RunnerSession` drives the interpreter inside a Web Worker and talks by messages |
| Projects | `src/projects` | Project storage, drafts, file tree, zip archives |
| Routing | `src/routing` | Hash addresses for every screen |
| Interface | `src/ui` | React screens and components |
| Content | `src/content/<locale>` | Examples (`.safira`) and lessons (`.md`), one folder per language, with the same file names |
| Lessons | `src/lessons` | `lessonCheck.ts` tests a program with hidden answers, in its own Web Worker. `lessonPlace.ts` maps steps to files and progress |
| Settings and i18n | `src/settings`, `src/i18n` | Theme, font, panel sizes, dictionaries for en, pt-BR, es, zh-CN and ja |
| Sound | `src/ui/sound` | Player on Web Audio with short recorded files from Kenney (CC0). A click plays what `data-sound` names on the element, or the plain click. Run, stop, breakpoints and renames call the player directly, because they also come from the keyboard |
| Sky | `src/ui/sky` | The clock of the scenery. `settings.theme` is only the starting point: `useSkyClock` gives the phase, and the shown theme comes from it. Nothing about elapsed time is saved |
| Suggestions | `src/language/completion.ts`, `src/ui/components/ghostText.ts` | Pure suggestion logic, and the CodeMirror ghost text that paints it without touching the document |
| Aquarium | `src/ui/aquarium` | Pure simulation in `aquariumWorld.ts`, canvas drawing in `aquariumRenderer.ts`, fish kept in `aquariumStore.ts` |
| Globe | `src/ui/components/AeroOrb.tsx` | The animated picture of the home screen, in SVG and CSS, so it costs almost nothing |

`src/language` has no dependency on React or the DOM. The interface only reaches it through `src/runtime`, except for
pure helpers such as highlighting and formatting.

## How a program runs

1. `EditorScreen` sends the project files to `useRunner`, which starts `runner.worker.ts`.
2. `Interpreter` is a generator. It yields effects: `step`, `output`, `clear`, `input`, `sleep`, `files`.
3. `driveExecution` handles each effect. Input, waits and breakpoints are awaited, so nothing blocks.
4. `RunnerSession` batches output and posts events back. Stop terminates the worker.

## Language rules

- The parser never fails: an unknown line becomes an `invalid` statement that fails when it runs, so `tente` can catch it.
- Rule order in `parser.ts` is part of the language.
- All words live in `commands.json`, and every language is always active, so a script can mix them. A command with many phrases has a short `shown` list, used by suggestions and by Available commands, while the parser accepts every phrase.
- Variables are global, including function parameters.
- `#safira X` on line 1 is hidden by the editor. `SUPPORTED_VERSIONS` lists what this version runs, and a script without
  the line counts as `0.38`. The alert only appears for an unsupported version.
- `legacyGolden.json` holds outputs recorded from the Python interpreter, which is gone. Never regenerate it.

## Command matrix

`src/language/matrix` runs the language by combination, with one test file per language. `scenarios.ts` holds each program once, with markers like `[mostre]`, and `dialects.ts` fills them. The expected output is written by hand, and every language must also produce the same syntax tree as Portuguese.

| Block | What runs |
|---|---|
| Commands | Every statement alone |
| Phrases | Every statement with every phrase of each of its commands, from any language |
| Pairs | Every statement after every other |
| Nesting | Every statement in every block, and blocks two and three levels deep |
| Values | Every kind of value in every place that takes one |
| Comparisons | Every operator, word and symbol, with lower, equal and greater values |
| Formatter | Formatting never changes what a program means |
| Mixed | Words of different languages on one line and across lines |

A new command goes in `scenarios.ts` and in all five dictionaries. It runs with `pnpm run unit:matrix`, inside `check:all` and CI.

## Lessons

The course is 14 very short lessons, each with a program to run and then a challenge, started from Help. After the last one the cat leaves and `settings.catLeft` removes lesson mode for good; clearing the browser is the only reset. A lesson is one Markdown file, read by `parseLesson`. The `# title` names it, and each `## section` is a step with one `safira` fence, whose comments carry the explanation. A step with `solution` and `check` fences is a challenge. Lesson mode shows it step by step.

```json
{ "uses": ["repeat|while"], "exact": false, "hint": "Shown after a failure", "cases": [{ "inputs": ["4"], "shows": ["8"], "hides": ["9"] }] }
```

- `uses` lists syntax kinds from `ast.ts`, and `a|b` accepts either.
- `shows` must appear in order and `hides` must not appear. Case, accents and punctuation are forgiven unless `exact` is set.
- A run that ends without an error gives the check on a plain step. On a challenge, `useLessonMode` runs `checkProgram` over the files of that run, and gives up on endless programs after 200,000 steps or 4 seconds.
- Each step is a real file, `aulas/03-sua-cidade-1.safira`, so saving, breakpoints and the inspector work as usual. The folder name is translated, so each language keeps its own scripts. Progress lives in the settings as `lesson:step` and survives a change of language.
- The code teaches, in its comments, and `ProfessorCat` only points: scenes `intro`, `read`, `play`, `write`, `input`, `result`, `farewell`. He stays inside the code field and never covers the output, travels between heights with a small random change in speed and arrival, and the angle of the arm is computed from there to the target of the scene. The pose comes from the state: `wave`, `point`, `thumbs`, `facepalm`. He is the only guide.
- `Next` stays locked until the step is done, but the lesson list is free, so nobody gets stuck.
- `content.test.ts` proves, for every language, that each solution passes its check, that the starting code fails it, and that every example runs.

## Browser storage

| Key | Content |
|---|---|
| `safira.projects.v1` | Projects with files, breakpoints and the order chosen in the sidebar. A `.zip` does not carry the order |
| `safira.aquarium.v1` | The fish of this browser and their weight. Clearing it is the only way to bring eaten fish back |
| `safira.settings.v1` | Language, chosen theme, vision mode, fonts, sound, suggestions, panel sizes, lesson mode, place, progress and whether the cat left |

`storageKey` builds these names. A preview shares the origin of the site, so under `/preview/<branch>/` the prefix becomes `safira-preview.<branch>.` and a change there never touches the data of the site, Delete everything included. The site keeps `safira.`, so nothing needs a migration.

An empty folder is a `.keep` file in `Project.files`. Screens hide it with `visibleFiles` and `buildFileTree`.

## Addresses

| Address | Screen |
|---|---|
| `#/` | Home |
| `#/new`, `#/new/<example>` | New project, with an example already chosen |
| `#/aquarium`, `#/globe` | Aquarium and globe, full screen, meant to work as a wallpaper |
| `#/projects/<id>/<file>` | Project and file, with the file URL encoded |
| `#/projects/<id>/aulas%2F03-sua-cidade-1.safira` | A step of lesson mode is a file, so it has an address like any other |

## Interface decisions

- Syntax colors follow the theme and the vision mode only. `applyVision` in `src/settings/vision.ts` writes them, with the interface tokens of the mode, as inline variables on `html`, so they win over the theme rules and leave no trace when the mode ends.
- There is no saving by hand. Open tabs reach the project 300 ms after typing stops, on `pagehide` and when leaving. Ctrl+S only forces it.
- `importe` looks beside the importing file first, then from the root, with or without `.safira`.
- Notes travel from the worker as `tone` events, and `soundPlayer.tone` plays them. A rest only waits.
- Each sound is named in `sounds.ts`. A click plays `data-sound`, text fields share a focus and a typing sound, and any clickable element has a hover sound. `data-sound="none"` silences the click of a button whose result has its own sound and arrives after a route change, as the plain click cannot step aside in time.

- The look is Frutiger Aero: glass panels, glossy buttons, sky, water and aurora, with no external images.
- `SceneBackdrop` keeps the three scenes mounted and cross fades them, so a theme changes in the background.
- A language change runs `scrambleDocument`, which rewrites the letters into the new text. Code, terminal and variables
  are left alone.
- Modals use Radix Dialog. The closing animation plays on a clone, because a modal closes by unmounting.
- On a phone the IDE splits into Files, Code, Output and Variables panels, and dividers are hidden.

## Deleting everything

Settings > Delete everything removes every key of this copy from both storages, then `snapAway` in `src/ui/snapEffect.ts` turns the screen to dust and black. A flag in `sessionStorage` survives the reload, and the small script in `index.html` reads it before the first paint, so the reset screen stays black for 2 seconds, fades in over 5 and gets the pointer back 4 seconds into the fade.

## Running on the local network

`vite --host 0.0.0.0` serves the page by the address of the machine. A page opened that way is not a secure context, so `crypto.randomUUID` does not exist there. `createId` in `projectStore.ts` falls back to `getRandomValues`.

## Known gaps

- `tokenize` grows faster than the size of the source: 40 thousand `(` take about 8 seconds. Only an absurd program feels it, and Stop works.
- Lighthouse is not in `tests.yml`.
- Content in the five languages loads at once, which costs bundle size. Loading only the active language should help.
- With the page idle, the headless test browser used about one CPU core. It was not measured on a normal machine.
- Chinese and Japanese commands need spaces between words, because nothing segments those languages. The whole-line and phrase suggestions there are short.
- Japanese commands come before their values, as in `もし n 大なり 5 なら`, because the grammar has one order for every language.
- `print` and `display` keep the line open, because `legacyGolden.json` records that. English content uses `show`, which ends the line.
- A `.zip` does not carry the order chosen in the sidebar.
- `R` in a note list is a rest. That was a decision, not something asked for.
- `localStorage` does not promise a disk write at the moment of a power cut, so the last seconds can be lost.
- The Brazilian language sound plays the opening of Asa Branca (1947), which is not in the public domain. Replace it if the rights become a problem.
- No manual screen reader pass was done.
