# Conditions

With `if`, the program chooses what to do.

## If

The block between `{` and `}` only runs when the condition is true. Change the 20 to 10 and run it again.

```safira
age = 20

if age is greater than 17 then {
    print "You can drive"
}
```

## Else

The `else` is the opposite path: it runs when the condition is false.

```safira
grade = 4

if grade is greater than or equal to 6 then {
    print "Passed"
} else {
    print "Failed"
}
```

## Compare

You can use `is equal to`, `is different from`, `is greater than` and `is less than`.

```safira
password = "safira"

if password is equal to "safira" then {
    print "Come in"
}
```

## Challenge: even or odd

Ask for a number. If the remainder of dividing by 2 is 0, show `even`. Otherwise, show `odd`.

The `%` sign gives the remainder of a division: `7 % 2` is 1.

```safira
print "Type a number:"
number = the number that the user enters

# Write the if here.

```

```solution
print "Type a number:"
number = the number that the user enters

if number % 2 is equal to 0 then {
    print "even"
} else {
    print "odd"
}
```

```check
{ "uses": ["if"], "hint": "Compare with: if number % 2 is equal to 0 then { ... } else { ... }", "cases": [{ "inputs": ["4"], "shows": ["even"], "hides": ["odd"] }, { "inputs": ["7"], "shows": ["odd"], "hides": ["even"] }] }
```
