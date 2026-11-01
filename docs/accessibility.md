# Accessibility

The target is WCAG 2.1 AA.

## Tools

- axe runs in E2E on the home screen, the editor and lesson mode, in the three themes, and on the home screen and the editor in every vision mode with each theme.
- `src/settings/vision.test.ts` measures every palette: WCAG contrast against the editor background, and distance between code groups as each kind of color blindness sees them, simulated with the Machado 2009 matrices.
- Lighthouse has a floor of 95 for accessibility.
- `eslint-plugin-jsx-a11y` runs in lint, and every `button` declares its `type`.
- Layout is tested from 320 to 1440 pixels, with no horizontal scroll.

## Vision modes

Interface > Accessibility, or the gear beside the Safira name on the home screen, which opens a modal with the modes. The theme still chooses the colors: each mode has versions for the light and for the dark surfaces, and syntax colors cannot be picked by hand.

| Mode | For | What changes |
|---|---|---|
| Protanopia, Deuteranopia | Weak or no red, weak or no green | Own syntax colors, Run in blue, Stop in orange, error and warning in orange and blue |
| Tritanopia | Weak or no blue | Own syntax colors, warnings in teal |
| Achromatopsia | No color at all | Grays with underline, bold and italic to tell code apart, Run and Stop told apart by icon and lightness |
| Low vision | Cataract, glaucoma, macular degeneration | Solid black or white surfaces, 7:1 text, no scenery, no text shadow |
| Light sensitivity | Migraine, photophobia | Dim warm surfaces in every theme, muted colors, darkened scenery |
| Epilepsy and dizziness | Seizures triggered by motion, vestibular conditions | The same effect as the reduced motion preference, without changing the system |

Color modes also mark code with weight, slant and underline, so color is never the only signal.

## What works

- Every action is reachable by keyboard, with the shortcuts listed in the menus.
- Landmarks, a skip link and a visible focus ring.
- The terminal is a live region, so a screen reader announces what programs print.
- Modals take the focus and close with Escape.
- The top menu follows the menu bar pattern: arrows move between and inside menus, Escape returns to the trigger.
- Theme and language are buttons that cycle on each click, and each one says the current choice in its name.
- Panel dividers are separators that work with the arrow keys.
- Language, theme and globe animations are skipped with the reduced motion preference, and the rewritten letters are not announced.
- On a phone, touch targets have at least 44 pixels.

## Known limits

- Colors chosen by a program with `mostre na cor`, the aquarium and the flags in the language button stay as they are in every mode.
- The simulation is a model. No person with each condition has checked these palettes yet.
- In the editor, Tab indents, so leaving it needs Shift+Tab or the skip link.
- The breakpoint dots work by mouse and touch. By keyboard, use F10 on the line.
- Neither NVDA nor Orca were tested by hand yet.
