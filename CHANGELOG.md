# Changelog

## 0.9.0

Safira was rewritten from Python and Tkinter to a web IDE in TypeScript.

### Added

- Home screen to create projects from a blank file or from 35 examples.
- Virtual files per project, including `importe` and every file command.
- Hidden language version on the first line of each script, with an alert only when it is not supported.
- Variables panel, line by line execution and breakpoints in a Web Worker.
- Programs can be stopped at any time, including infinite loops.
- `Ctrl+Enter` runs the program, and running stops at breakpoints.
- Clickable breakpoint dots beside every line. A dot on a comment or an empty line stops at the next command.
- Inline suggestions in gray, accepted with Tab or a touch, for commands, whole lines and names in the file, with a checkbox above the editor.
- Variables inspector, always visible, with search and types.
- Top menu with Radix, navigable by keyboard and touch.
- Frutiger Aero look, with animated theme and language icons that cycle on each click. In the IDE, theme, language and sound live in the Interface menu.
- Colors by name, `#331`, `#ff1122` or `0xff1122`, after or before the text, and `mostra` beside `mostre` and `mostrar`.
- Commands on the same line after conditions and loops, as in `se x entao mostre "a" senao mostre "b"`.
- Addresses for every screen, lesson, lesson section, project and file, with the browser back button.
- Click a project name to rename it in place: Enter or a click outside saves, Escape cancels. In the IDE the name sits on top of the file sidebar.
- Files and folders are renamed from the right click. Tabs, breakpoints and unsaved text follow, and a name in use is refused.
- File sidebar with folders in each project. New items appear in the tree with a selected provisional name, and a right click offers delete, new file and new folder.
- Unsaved work is kept while typing and recovered after a crash or a power cut.
- Import and export of projects as `.zip`, into a new project or the open one, also by dropping the file on the home screen.
- Deploy to GitHub Pages on merge, and a preview environment for each pull request.
- Lessons in real markdown, inside the IDE under Help, with colored code and a button that opens each example as a file of the project.
- Resizable panels, by mouse and keyboard, kept between sessions.
- Time passes in the scenery while the page is open: the climates complete a cycle in 12 hours, with the sun, the moon and the stars moving, and choosing a theme is a jump in time. A reload returns to the chosen theme.
- Recorded sounds for clicks, passing over menus, changing tabs, opening a project and the IDE, renaming, the delete alert, closing, breakpoints, run and stop, formatting, weather changes, new files and folders, the suggestions switch, typing, accepting a suggestion, importing, changing language, passing over any button, searching variables, program errors and dragging a selection, which lasts longer the more lines it covers, with a switch to turn them off.
- Language changes rewrite the letters of the interface, and themes change in the scenery itself. Names people chose and the Safira name stay still.
- Interface and error messages in Simplified Chinese and Japanese.
- The example programs were ported to the new language and now carry emojis, so their author line names Gabriel Gregorio, who ported them.
- Recorded interface sounds for clicks, switches, opening, creating, deleting and modals, from Kenney's CC0 Interface Sounds pack, with a speaker switch beside theme and language.
- Opening a project switches the IDE on like an old screen, and opening a file wipes the editor with a glass sheen.
- Glossy icon buttons for new file, new folder, back, close, run and stop, following the theme.
- Istok Web as the interface font and JetBrains Mono for code, both bundled, with a menu switch for the code font.
- A 3D sapphire as the logo, written directly in WebGL 2. It spins and points at the mouse, draws at 15 to 30 frames per second, rests when the window loses focus, stands still with the reduced motion preference and falls back to a flat logo without WebGL.
- Modals with an overlay, a retro opening and a closing animation, closing when clicking outside.
- Confirmation before deleting a project or a file.
- Styled mouse cursor and scrollbars.
- Phone layout with Files, Code, Output and Variables panels and 44 pixel touch targets.

### Changed

- Whole numbers print as `3`, not `3.0`.
- Commands accept accents, as in `função` and `senão`.

### Fixed

- `;` inside a string no longer breaks the program, and `;` now separates commands.
- `\n` no longer cuts the printed text.
- Parentheses work in conditions.
- Functions can call themselves.
- `senao` runs after a false `se`, even when an earlier `se` was true.
- `substitua` really replaces the text.
- A division by zero has its own message.
- `x[2:2]` returns the second letter.
- Python code can no longer run through `eval`.

### Removed

- Automatic updates, access logs and the Python application.
- Access to real files: there is no way to read or write the disk.
