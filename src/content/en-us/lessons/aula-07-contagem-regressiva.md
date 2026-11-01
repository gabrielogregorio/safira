# Countdown

## Countdown

```safira
show "Ready..."

# Waits 1 second before going on.
wait 1 second
show "Go!"
```

## Challenge: Countdown

```safira
# Challenge: Show 3, 2 and 1, with a wait between them.
# At the end, show Fire!

```

```solution
show 3
wait 1 second
show 2
wait 1 second
show 1
wait 1 second
show "Fire!"
```

```check
{"uses": ["wait"], "hint": "Put wait 1 second between the show lines.", "cases": [{"shows": ["3", "2", "1", "Fire"]}]}
```
