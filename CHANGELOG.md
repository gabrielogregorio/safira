# Changelog

## 0.9.0

Safira was rewritten from Python and Tkinter to a web IDE in TypeScript.

### Added

- Accessibility modes for protanopia, deuteranopia, tritanopia, achromatopsia, low vision, light sensitivity, and epilepsy and dizziness, tested with axe and with simulated color vision.
- The gear beside the Safira name opens the accessibility modes, each with a short explanation.
- The globe on the home screen loses its fish when the aquarium is empty.
- Lesson mode inside the IDE: a switch beside Smart suggestions swaps the tabs for a lesson bar, each step opens as a script, a run gives the check, and challenges are tested with hidden answers, so the next step only opens after a correct run. Hints, the solution and a way to start over are one click away.
- Examples and lessons in English, Portuguese, Spanish, Simplified Chinese and Japanese, rewritten for people who never programmed.
- Commands for lists, files and counting in English and Spanish, such as `for each x from 1 to 5` and `add "x" at the end of the list of fruits`.
- Commands in Simplified Chinese and Japanese, such as `如果 n 大于 5 那么 {` and `もし n 大なり 5 なら {`. Words are separated by spaces. A number can touch its unit, as in `1秒`, and the punctuation of those keyboards works.
- A command matrix in `src/language/matrix`: every statement, phrase, ordered pair, nesting, value and comparison runs in each language, about 60 thousand programs.
- Home screen to create projects from a blank file or from 34 examples.
- Virtual files per project, including `importe` and every file command.
- Hidden language version on the first line of each script, with an alert only when it is not supported.
- Variables panel, line by line execution and breakpoints in a Web Worker.
- Programs can be stopped at any time, including infinite loops.
- `Ctrl+Enter` runs the program, and running stops at breakpoints.
- Clickable breakpoint dots beside every line. A dot on a comment or an empty line stops at the next command.
- Inline suggestions in gray, accepted with Tab or a touch, for commands, whole lines and names in the file, with a checkbox above the editor.
- Variables inspector, always visible, with search and types, each one explained on hover.
- Top menu with Radix, navigable by keyboard and touch.
- Frutiger Aero look, with animated theme and language icons that cycle on each click. In the IDE, theme, language and sound live in the Interface menu.
- Colors by name, `#331`, `#ff1122` or `0xff1122`, after or before the text, and `mostra` beside `mostre` and `mostrar`.
- `importe` takes quoted paths, with or without `.safira`, beside the file or from the root, with suggestions from the project files. Function calls are suggested with their parameters, also from imported files.
- Notes, with `toque C por 1s`, `play D# by 0.1` or a list like `toque C2#, D2, Ré, R, Sol por 1s`, where `R` is a rest.
- Commands on the same line after conditions and loops, as in `se x entao mostre "a" senao mostre "b"`.
- Addresses for every screen, lesson, lesson section, project and file, with the browser back button.
- Click a project name to rename it in place: Enter or a click outside saves, Escape cancels. In the IDE the name sits on top of the file sidebar.
- Files and folders are renamed from the right click. Tabs, breakpoints and unsaved text follow, and a name in use is refused. Dragging moves them into folders and changes their order. The right click also downloads a file as it is, or a folder as a `.zip`.
- File sidebar with folders in each project. New items appear in the tree with a selected provisional name, and a right click offers delete, new file and new folder.
- Everything saves itself while typing, in the browser, with no save button and no question when leaving.
- Import and export of projects as `.zip`, into a new project or the open one, also by dropping the file on the home screen.
- Deploy to GitHub Pages on merge, and a preview environment for each pull request.
- Lessons in real markdown, inside the IDE under Help, with colored code and a button that opens each example as a file of the project.
- Resizable panels, by mouse and keyboard, kept between sessions.
- Time passes in the scenery while the page is open: the climates complete a cycle in 12 hours, with the sun, the moon and the stars moving, and choosing a theme is a jump in time. A reload returns to the chosen theme.
- Recorded sounds for clicks, passing over menus, changing tabs, opening a project and the IDE, renaming, the delete alert, closing, breakpoints, run and stop, formatting, weather changes, new files and folders, the suggestions switch, typing, accepting a suggestion, importing, changing language, passing over any button, searching variables, program errors, the program input field, exporting, moving items and dragging a selection, which plays while the mouse is pressed, with a switch to turn them off.
- Each language lands with a sound of its region, and each sky with its own weather sound.
- The home screen has an animated glass globe with water, a fish, bubbles and a sprout.
- Clicking the globe grows it into a full screen aquarium, also at `#/aquarium`, and the globe alone is at `#/globe`, so either can be a wallpaper. Both follow the sky. The 24 fish belong to this browser: they chase food, get fat and hungrier until they pop like a bubble, each with a color of its own, slowly slim down, run when clicked, and a very big one eats smaller ones for good. Clicks feed them, the right button feeds more, both buttons feed a lot, each wheel tick while holding drops one piece, and every popped bubble makes each drop 1.5 times bigger until the aquarium closes. Bubbles pop, plants shake, and holding or dragging moves the water, with a sea sound under it all.
- The browser console invites whoever opens it to the repository.
- Language changes rewrite the letters of the interface, and themes change in the scenery itself. Names people chose and the Safira name stay still.
- Interface and error messages in Simplified Chinese and Japanese.
- The example programs were ported to the new language and now carry emojis, so their author line names Gabriel Gregorio, who ported them.
- Recorded interface sounds for clicks, switches, opening, creating, deleting and modals, from Kenney's CC0 Interface Sounds pack, with a speaker switch beside theme and language.
- Opening a project switches the IDE on like an old screen, and opening a file wipes the editor with a glass sheen.
- Glossy icon buttons for new file, new folder, back, close, run and stop, following the theme.
- Istok Web as the interface font and JetBrains Mono for code, both bundled, with a menu switch for the code font.
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
