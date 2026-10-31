# Functions

A function is a named block of code. You write it once and use it as many times as you want.

## Create and call

Creating the function does not run anything. It only runs when you call its name.

```safira
function hello {
    print "Hello!"
    print "How are you?"
}

hello()
hello()
```

## Pass a value

A function can receive values to work with.

```safira
function greet(name) {
    print "Hello, " + name
}

greet("Ana")
greet("Bia")
```

## Give back a result

`return` hands a result to whoever called.

```safira
function double(number) {
    return number * 2
}

print double(4)
```

## Challenge: sum

Create the function `add_up`, which receives two numbers and returns their sum. Then show `add_up(2, 3)`.

```safira
# Create the function here.

# Show add_up(2, 3) here.

```

```solution
function add_up(a, b) {
    return a + b
}

print add_up(2, 3)
```

```check
{ "uses": ["functionDeclaration", "return", "call"], "hint": "Start with function add_up(a, b) { and use return a + b.", "cases": [{ "shows": ["5"] }] }
```
