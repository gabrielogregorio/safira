# Lists

A list holds many values in a single variable.

## Create a list

Positions start at 1.

```safira
list of fruits receive "grape", "apple", "mango"

print fruits
print list of fruits in position 1
print the size of the list of fruits
```

## Add and remove

A list can grow and shrink while the program runs.

```safira
list of fruits receive "grape", "apple"

add "mango" at the end of the list of fruits
remove "grape" from the list of fruits

print fruits
```

## Go through all the items

`scroll through` runs the block once for each item.

```safira
list of fruits receive "grape", "apple", "mango"

scroll through the list of fruits assigning in fruit {
    print "I like " + fruit
}
```

## Challenge: shopping list

Create the list `groceries` with `rice` and `beans`. Add `milk` at the end and show each item on its own line.

```safira
# Create the list here.

# Add the milk here.

# Show each item here.

```

```solution
list of groceries receive "rice", "beans"

add "milk" at the end of the list of groceries

scroll through the list of groceries assigning in item {
    print item
}
```

```check
{ "uses": ["listDeclare", "listInsert", "forEach"], "hint": "Use list of ... receive, add ... at the end of the list of ... and scroll through the list of ...", "cases": [{ "shows": ["rice", "beans", "milk"] }] }
```
