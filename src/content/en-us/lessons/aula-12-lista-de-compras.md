# Shopping list

## Shopping list

`list of fruits receive "grape", "pear"` creates a list. `add "kiwi" at the end of the list of fruits` grows it. `scroll through the list of fruits assigning in item {` goes through all of it.

```safira
list of fruits receive "grape", "pear"
add "kiwi" at the end of the list of fruits

scroll through the list of fruits assigning in item {
    show item
}
```

## Challenge: Shopping list

Create the list `shopping` with `rice` and `beans`, add `milk` at the end and show each item.

```safira
# Write here.
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
