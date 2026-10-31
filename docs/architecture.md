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
| Content | `src/content` | Examples (`.safira`) and lessons (`.md`) |
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
- All words live in `commands.json`, and every language is always active, so a script can mix them.
- Variables are global, including function parameters.
- `#safira X` on line 1 is hidden by the editor. `SUPPORTED_VERSIONS` lists what this version runs, and a script without
  the line counts as `0.38`. The alert only appears for an unsupported version.
- `legacyGolden.json` holds outputs recorded from the Python interpreter, which is gone. Never regenerate it.

## Browser storage

| Key | Content |
|---|---|
| `safira.projects.v1` | Projects with files, breakpoints and the order chosen in the sidebar. A `.zip` does not carry the order |
| `safira.drafts.v1` | Read once, to bring in unsaved text from older versions |
| `safira.aquarium.v1` | The fish of this browser and their weight. Clearing it is the only way to bring eaten fish back |
| `safira.settings.v1` | Language, chosen theme, vision mode, fonts, sound, suggestions, panel sizes, read lessons |

An empty folder is a `.keep` file in `Project.files`. Screens hide it with `visibleFiles` and `buildFileTree`.

## Addresses

| Address | Screen |
|---|---|
| `#/` | Home |
| `#/new`, `#/new/<example>` | New project, with an example already chosen |
| `#/aquarium`, `#/globe` | Aquarium and globe, full screen, meant to work as a wallpaper |
| `#/projects/<id>/<file>` | Project and file, with the file URL encoded |
| `#/projects/<id>/<file>/lessons/<lesson>/<section>` | Lessons open over that project, reached from Help |

## Interface decisions

- Syntax colors follow the theme and the vision mode only. `applyVision` in `src/settings/vision.ts` writes them, with the interface tokens of the mode, as inline variables on `html`, so they win over the theme rules and leave no trace when the mode ends.
- There is no saving by hand. Open tabs reach the project 300 ms after typing stops, on `pagehide` and when leaving. Ctrl+S only forces it.
- `importe` looks beside the importing file first, then from the root, with or without `.safira`.
- Notes travel from the worker as `tone` events, and `soundPlayer.tone` plays them. A rest only waits.
- Each sound is named in `sounds.ts`. A click plays `data-sound`, text fields share a focus and a typing sound, and any clickable element has a hover sound.

- The look is Frutiger Aero: glass panels, glossy buttons, sky, water and aurora, with no external images.
- `SceneBackdrop` keeps the three scenes mounted and cross fades them, so a theme changes in the background.
- A language change runs `scrambleDocument`, which rewrites the letters into the new text. Code, terminal and variables
  are left alone.
- Modals use Radix Dialog. The closing animation plays on a clone, because a modal closes by unmounting.
- On a phone the IDE splits into Files, Code, Output and Variables panels, and dividers are hidden.

## Known gaps

- The full test run is behind the code: unit and E2E were last complete before the autosave, aquarium and sound work.
- Coverage is 92%, with thresholds at 90/83/87/90. The goal is 100%.
- Lighthouse is not in `tests.yml`, and the deploy workflows have not run on GitHub yet.
- The bundle has about 906 kB. Loading the lessons on demand should remove the markdown packages from it.
- Examples and lessons exist only in Brazilian Portuguese, and suggestions in Chinese and Japanese use the English list.
- Previews are not removed from `gh-pages` when a pull request closes.
- A `.zip` does not carry the order chosen in the sidebar, and dragging has no keyboard or touch alternative.
- `R` in a note list is a rest. That was a decision, not something asked for.
- `localStorage` does not promise a disk write at the moment of a power cut, so the last seconds can be lost.
- The Brazilian language sound plays the opening of Asa Branca (1947), which is not in the public domain. Replace it if the rights become a problem.
- The README needs a GIF, and no manual screen reader pass was done.
