# Show on screen

`show` does not only write text. It also does math and uses colors.

## Text and numbers

Text goes between quotes. A number has no quotes, and the computer does the math for you.

```safira
show "Two plus two is:"
show 2 + 2
show 10 * 3
```

## Colors

Put `in color` after the text. You can use a color name or a code like `#ff1122`.

```safira
show "Blue" in color blue
show "Purple" in color purple
show "Red" in color #ff1122
```

## Challenge: the math

Show the result of `25 * 4`. Let the computer do the math, without typing the result.

```safira
# Show the result of 25 * 4 here.

```

```solution
show 25 * 4
```

```check
{ "uses": ["print"], "hint": "Without quotes, the computer does the math: show 25 * 4", "cases": [{ "shows": ["100"] }] }
```
