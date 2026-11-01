# Traffic light

## Traffic light

```safira
# repeat does it all again.
# clear wipes what was shown.
repeat 2 times {
    clear
    show "Hello"
    wait 1 second

    clear
    show "Bye"
    wait 1 second
}
```

## Challenge: Traffic light

```safira
# Challenge: Make a traffic light that repeats 2 times:
# show Stop for 4 seconds, Go for 4 seconds and Caution
# for 2 seconds, clearing the screen between them.

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
