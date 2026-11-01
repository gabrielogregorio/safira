# Color and sound

## Color and sound

```safira
# Shows a text in blue.
show "Hello!" in color blue

# Plays the note C, which is Do, for half a second.
# Turn the sound on to hear it.
play C for 500ms
```

## Challenge: Color and sound

```safira
# Challenge: Show Congratulations in green.
# Then play the notes C, E and G for 300ms.

```

```solution
show "Congratulations" in color green
play C, E, G for 300ms
```

```check
{"uses": ["colored", "tone"], "hint": "show \"Congratulations\" in color green, then play C, E, G for 300ms", "cases": [{"shows": ["Congratulations"]}]}
```
