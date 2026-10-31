# Show on screen

`print` does not only write text. It also does math and uses colors.

## Text and numbers

Text goes between quotes. A number has no quotes, and the computer does the math for you.

```safira
print "Two plus two is:"
print 2 + 2
print 10 * 3
```

## All on the same line

With `print on this line`, the next thing keeps going on the same line.

```safira
print on this line "Good "
print on this line "morning!"
```

## Colors

Put `in color` after the text. You can use a color name or a code like `#ff1122`.

```safira
print "Blue" in color blue
print "Purple" in color purple
print "Red" in color #ff1122
```

## Challenge: the math

Show the result of `25 * 4`. Let the computer do the math, without typing the result.

```safira
# Show the result of 25 * 4 here.

```

```solution
print 25 * 4
```

```check
{ "uses": ["print"], "hint": "Without quotes, the computer does the math: print 25 * 4", "cases": [{ "shows": ["100"] }] }
```
