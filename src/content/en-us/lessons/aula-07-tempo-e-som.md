# Time and sound

A program can also wait and play notes.

## Wait

`wait` takes a pause before the next command.

```safira
print "Ready..."
wait 1 second
print "Go!"
```

## Play a note

`play` plays a note. You can use `C`, `D`, `E` or `Do`, `Re`, `Mi`.

```safira
play Do for 0.5s
play Mi for 0.5s
play Sol for 1s
```

## Challenge: countdown

Show 3, 2, 1, with a wait between the numbers, and then show `Fire!`.

```safira
# Show 3, wait, show 2, wait, show 1, wait.

# At the end, show Fire!

```

```solution
print 3
wait 1 second
print 2
wait 1 second
print 1
wait 1 second
print "Fire!"
```

```check
{ "uses": ["wait"], "hint": "Put wait 1 second between the prints.", "cases": [{ "shows": ["3", "2", "1", "Fire"] }] }
```
