# Ask the user

A program is more fun when it talks to whoever is using it.

## Read a text

`what the user types` stops the program and waits. Type in the field of the output panel and press Enter.

```safira
print "What is your name?"
name = what the user types

print "Hello, " + name
```

## Read a number

To do math with what was typed, ask for a number.

```safira
print "Type a number:"
number = the number that the user enters

double = number * 2
print "The double is " + double
```

## Challenge: the triple

Ask for a number and show its triple.

```safira
# Ask the user for a number.

# Show the number times 3.

```

```solution
print "Type a number:"
number = the number that the user enters

print number * 3
```

```check
{ "uses": ["input"], "hint": "Use number = the number that the user enters and then print number * 3.", "cases": [{ "inputs": ["4"], "shows": ["12"] }, { "inputs": ["10"], "shows": ["30"] }] }
```
