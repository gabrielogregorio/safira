# Shopping list

## Shopping list

```safira
# Creates a list with two fruits.
list of fruits receive "grape", "pear"

# Puts one more fruit at the end.
add "kiwi" at the end of the list of fruits

# Shows each fruit, one per line.
scroll through the list of fruits assigning in item {
    show item
}
```

## Challenge: Shopping list

```safira
# Challenge: Create a list called shopping with rice and
# beans.
# Put milk at the end.
# Show each item.

```

```solution
list of shopping receive "rice", "beans"
add "milk" at the end of the list of shopping

scroll through the list of shopping assigning in item {
    show item
}
```

```check
{"uses": ["listDeclare", "listInsert", "forEach"], "hint": "Create, add and go through the list.", "cases": [{"shows": ["rice", "beans", "milk"]}]}
```
