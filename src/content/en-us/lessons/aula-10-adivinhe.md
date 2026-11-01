# Guess

## Guess

`a random number between 1 and 3` draws a number, and `if a is equal to b then {` compares. Then comes `} else {`.

Draw a number into `secret`, ask for a number and show `Right` if it matches or `Wrong` if not.

```safira
# Write here.
```

```solution
secret = a random number between 1 and 3
guess = the number that the user enters

if guess is equal to secret then {
    show "Right"
} else {
    show "Wrong"
}
```

```check
{"uses": ["random", "if"], "hint": "Draw, ask for the guess and compare with if.", "cases": [{"inputs": ["9"], "shows": ["Wrong"], "hides": ["Right"]}]}
```
