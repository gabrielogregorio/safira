# Changelog

## 1.0.0-alpha.0

Safira was rewritten from Python and Tkinter to a web IDE in TypeScript.

### Added

- Home screen to create projects from a blank file or from 35 examples.
- Virtual files per project, including `importe` and every file command.
- Hidden language version on the first line of each script, with an alert only when it is not supported.
- Variables panel, line by line execution and breakpoints in a Web Worker.
- Programs can be stopped at any time, including infinite loops.
- `Ctrl+Enter` runs the program, and running stops at breakpoints.
- Clickable breakpoint dots beside every line. A dot on a comment or an empty line stops at the next command.
- Variables inspector, always visible, with search and types.
- Top menu with Radix, navigable by keyboard and touch.
- Frutiger Aero look, with illustrated theme and language choices on every screen.
- Commands on the same line after conditions and loops, as in `se x entao mostre "a" senao mostre "b"`.
- Addresses for every screen, lesson, lesson section, project and file, with the browser back button.
- File sidebar with folders in each project.
- Unsaved work is kept while typing and recovered after a crash or a power cut.
- Import and export of projects as `.zip`, into a new project or the open one.
- Lessons in real markdown, with colored code and a button to open each example in the IDE.
- Resizable panels, by mouse and keyboard, kept between sessions.
- Language changes rewrite the letters of the interface, and themes change in the scenery itself.
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
