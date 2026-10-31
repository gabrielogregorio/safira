# Loops

The computer never gets tired of repeating. You just say how many times.

## Repeat

`repeat` runs the block as many times as you ask.

```safira
repeat 3 times {
    print "Hello!"
}
```

## Count

`for each` counts for you, and the variable changes on each round.

```safira
for each number from 1 to 5 {
    print number
}
```

## While

`while` repeats until the condition becomes false. Type 0 to leave.

```safira
number = 1

while number is different from 0 {
    print "Type 0 to leave:"
    number = the number that the user enters
}

print "The end!"
```

## Challenge: the 2 times table

Show the 2 times table up to 10: 2, 4, 6 and so on. Use a loop.

```safira
# Count from 1 to 10 and show the number times 2.

```

```solution
for each number from 1 to 10 {
    print number * 2
}
```

```check
{ "uses": ["repeat|while|forRange"], "hint": "Use for each number from 1 to 10 { ... } and print number * 2.", "cases": [{ "shows": ["2", "4", "6", "8", "10", "12", "14", "16", "18", "20"] }] }
```
