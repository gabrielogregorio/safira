# Blinking tree

## Blinking tree

```safira
# Makes the star blink: clears, shows and waits.
repeat 2 times {
    clear
    show "⭐"
    wait 1 second

    clear
    show "🌟"
    wait 1 second
}
```

## Challenge: Blinking tree

```safira
# Challenge: Make the tree blink
# 3 times.
# Show the tree lit, wait, clear
# the screen and show the tree
# with the lights as ⚫.

show "    ⭐"
show "   🎄🎄"
show "  🎄🔴🎄"
show " 🎄🟡🎄🔵"
show "    🟫"
show "🎅 Merry Christmas!"
```

```solution
repeat 3 times {
    clear
    show "    ⭐"
    show "   🎄🎄"
    show "  🎄🔴🎄"
    show " 🎄🟡🎄🔵"
    show "    🟫"
    show "🎅 Merry Christmas!"
    wait 1 second

    clear
    show "    ⭐"
    show "   🎄🎄"
    show "  🎄⚫🎄"
    show " 🎄⚫🎄⚫"
    show "    🟫"
    show "🎅 Merry Christmas!"
    wait 1 second
}
```

```check
{"uses": ["repeat|while|forRange", "wait", "clear"], "hint": "Put both trees inside repeat, each with clear and wait.", "cases": [{"shows": ["Merry Christmas", "Merry Christmas"]}]}
```
