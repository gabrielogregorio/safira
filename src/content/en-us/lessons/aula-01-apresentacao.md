# Welcome to Safira

Safira is a programming language where you write almost the way you talk.

## Your first program

A program is a list of orders for the computer. This one has a single order: show a text on the screen.

Press ▶ Run and see the result next to it.

```safira
print "Hello, world!"
```

## One order after another

Safira reads from top to bottom, one line at a time. Each `print` writes on a new line.

```safira
print "First"
print "Second"
print "Third"
```

## Comments

A line that starts with `#` is a comment. It is a note for whoever reads the code, and the computer ignores it.

```safira
# This line does not show on the screen.
print "This one does!"
```

## Challenge: talk to me

Make the program show the text `Hello, Safira!`.

```safira
# Write your code below.

```

```solution
print "Hello, Safira!"
```

```check
{ "uses": ["print"], "hint": "Use the print command with the text between quotes.", "cases": [{ "shows": ["Hello, Safira!"] }] }
```
