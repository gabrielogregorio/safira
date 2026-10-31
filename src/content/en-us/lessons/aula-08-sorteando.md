# Draw

Games need luck, and the computer knows how to draw numbers.

## Roll the die

Run it several times: the number changes.

```safira
die = a random number between 1 and 6

print "It was " + die
```

## Luck and conditions

Putting the draw together with `if`, the program decides by itself.

```safira
coin = a random number between 1 and 2

if coin is equal to 1 then {
    print "Heads"
} else {
    print "Tails"
}
```

## Challenge: guess

Draw a number between 1 and 3 and keep it in `secret`. Ask for a number. If it is equal, show `Correct`. Otherwise, show `Wrong`.

```safira
# Draw the secret here.

print "Guess a number from 1 to 3:"
guess = the number that the user enters

# Compare the guess with the secret here.

```

```solution
secret = a random number between 1 and 3

print "Guess a number from 1 to 3:"
guess = the number that the user enters

if guess is equal to secret then {
    print "Correct"
} else {
    print "Wrong"
}
```

```check
{ "uses": ["random", "if"], "hint": "Use secret = a random number between 1 and 3 and compare with the if.", "cases": [{ "inputs": ["9"], "shows": ["Wrong"], "hides": ["Correct"] }] }
```
