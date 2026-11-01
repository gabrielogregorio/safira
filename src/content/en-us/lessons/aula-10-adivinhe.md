# Guess

## Guess

```safira
# Draws a number: 1 or 2.
die = a random number between 1 and 2

# If it is 1, shows Heads. If not, shows Tails.
if die is equal to 1 then {
    show "Heads"
} else {
    show "Tails"
}
```

## Challenge: Guess

```safira
# Challenge: Draw a number from 1 to 3 and keep it in
# secret.
# Ask for a number.
# If it matches, show Right.
# If not, show Wrong.

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
