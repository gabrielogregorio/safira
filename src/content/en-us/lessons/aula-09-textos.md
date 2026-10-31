# Play with texts

You can change the way a text looks and go through it letter by letter.

## Upper and lower case

A text can become all big, all small, or just with the first letter big.

```safira
name = "ana maria"

print name in upper case
print name in lower case
print name in capitalized
```

## Letter by letter

`scroll through` visits each letter, one at a time.

```safira
word = "Sun"

scroll through word assigning in letter {
    print letter
}
```

## Challenge: shout

Ask for a text and show that text all in upper case.

```safira
print "Type a word:"
word = what the user types

# Show the word in upper case here.

```

```solution
print "Type a word:"
word = what the user types

print word in upper case
```

```check
{ "uses": ["case"], "exact": true, "hint": "Write: print word in upper case", "cases": [{ "inputs": ["safira"], "shows": ["SAFIRA"] }] }
```
