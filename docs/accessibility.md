# Accessibility

The target is WCAG 2.1 AA.

## Tools

- axe runs in E2E on the home, editor and lessons screens, in the three themes.
- Lighthouse has a floor of 95 for accessibility.
- `eslint-plugin-jsx-a11y` runs in lint, and every `button` declares its `type`.
- Layout is tested from 320 to 1440 pixels, with no horizontal scroll.

## What works

- Every action is reachable by keyboard, with the shortcuts listed in the menus.
- Landmarks, a skip link and a visible focus ring.
- The terminal is a live region, so a screen reader announces what programs print.
- Modals take the focus and close with Escape.

## Known limits

- In the editor, Tab indents, so leaving it needs Shift+Tab or the skip link.
- Clicking the gutter sets a breakpoint with the mouse. By keyboard, use F10 on the line.
- Neither NVDA nor Orca were tested by hand yet.
