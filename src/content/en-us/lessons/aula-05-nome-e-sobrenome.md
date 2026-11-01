# First and last name

## First and last name

This asks for a text: `name = what the user types`.

```safira
name = what the user types
show "Hello, " + name
```

## Challenge: First and last name

Ask for the first name, ask for the last name and show both together, with a space between them.

```safira
# Write here.
```

```solution
name = what the user types
lastName = what the user types
show name + " " + lastName
```

```check
{"uses": ["input"], "hint": "Join with a space: name + \" \" + lastName", "cases": [{"inputs": ["Ana", "Lima"], "shows": ["Ana Lima"]}]}
```
