# Ask the user

A program is more fun when it talks to whoever is using it.

## Read a text

`what the user types` stops the program and waits. Type in the field of the output panel and press Enter.

```safira
show "What is your name?"
name = what the user types

show "Hello, " + name
```

## Read a number

To do math with what was typed, ask for a number.

```safira
show "Type a number:"
number = the number that the user enters

double = number * 2
show "The double is " + double
```

## Challenge: the triple

Ask for a number and show its triple.

```safira
# Ask the user for a number.

# Show the number times 3.

```

```solution
show "Type a number:"
number = the number that the user enters

show number * 3
```

```check
{ "uses": ["input"], "hint": "Use number = the number that the user enters and then show number * 3.", "cases": [{ "inputs": ["4"], "shows": ["12"] }, { "inputs": ["10"], "shows": ["30"] }] }
```
