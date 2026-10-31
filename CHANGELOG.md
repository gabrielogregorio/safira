# Changelog

## 1.0.0-alpha.0

Safira was rewritten from Python and Tkinter to a web IDE in TypeScript.

### Added

- Home screen to create projects from a blank file or from 35 examples.
- Virtual files per project, including `importe` and every file command.
- Hidden language version on the first line of each script, with an alert only when it is not supported.
- Variables panel, line by line execution and breakpoints in a Web Worker.
- Programs can be stopped at any time, including infinite loops.

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
