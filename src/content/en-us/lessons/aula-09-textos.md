# Play with texts

You can change the way a text looks and go through it letter by letter.

## Upper and lower case

A text can become all big, all small, or just with the first letter big.

```safira
name = "ana maria"

show name in upper case
show name in lower case
show name in capitalized
```

## Letter by letter

`scroll through` visits each letter, one at a time.

```safira
word = "Sun"

scroll through word assigning in letter {
    show letter
}
```

## Challenge: shout

Ask for a text and show that text all in upper case.

```safira
show "Type a word:"
word = what the user types

# Show the word in upper case here.

```

```solution
show "Type a word:"
word = what the user types

show word in upper case
```

```check
{ "uses": ["case"], "exact": true, "hint": "Write: show word in upper case", "cases": [{ "inputs": ["safira"], "shows": ["SAFIRA"] }] }
```
