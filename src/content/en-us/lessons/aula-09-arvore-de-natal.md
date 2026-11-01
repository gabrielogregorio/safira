# Blinking tree

## Blinking tree

`clear` and `wait` make anything blink.

```safira
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

Make the tree blink 3 times: use `repeat`, `clear` and `wait 1 second`, showing the tree on and then off.

```safira
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
