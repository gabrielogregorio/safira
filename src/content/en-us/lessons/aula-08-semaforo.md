# Traffic light

## Traffic light

`clear` wipes what was shown, and `repeat 2 times {` repeats.

Make a traffic light that repeats 2 times: show `Stop` for 4 seconds, `Go` for 4 seconds and `Caution` for 2 seconds, clearing the screen between them.

```safira
# Write here.
```

```solution
repeat 2 times {
    clear
    show "🔴 Stop"
    wait 4 seconds

    clear
    show "🟢 Go"
    wait 4 seconds

    clear
    show "🟠 Caution"
    wait 2 seconds
}
```

```check
{"uses": ["repeat|while|forRange", "wait", "clear"], "hint": "Inside repeat: clear, show and wait, three times.", "cases": [{"shows": ["Stop", "Go", "Caution"]}]}
```
