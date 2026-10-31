# Variables

A variable is a little box with a name. It holds a value for you to use later.

## Keep a value

The `=` puts the value in the box. After that, just use the name.

```safira
name = "Ana"
age = 20

print name
print age
```

## See the variables

After you run, look at the Variables panel: it shows the name, the value and the type of each one.

Want to see it step by step? Open the Run menu and choose Run line by line.

```safira
points = 10
points = points + 5

print points
```

## Join text and a variable

The `+` joins texts and variables into a single sentence.

```safira
name = "Ana"
age = 20

print "My name is " + name
print "I am " + age + " years old"
```

## Challenge: your city

Create a variable called `city` with the value `Lima` and show the sentence `I live in Lima`, joining the text with the variable.

```safira
# Create the variable here.

# Show the sentence here.

```

```solution
city = "Lima"
print "I live in " + city
```

```check
{ "uses": ["assign", "variable"], "hint": "Create the variable with city = \"Lima\" and use + to join.", "cases": [{ "shows": ["I live in Lima"] }] }
```
