# Shopping list

## Shopping list

```safira
# Creates the list.
list of fruits receive "grape", "pear"

# Adds at the end.
add "kiwi" at the end of the list of fruits

# Goes through all the items.
scroll through the list of fruits assigning in item {
    show item
}
```

## Challenge: Shopping list

```safira
# Challenge: Create the list shopping with rice and beans,
# add milk at the end and show each item.

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
