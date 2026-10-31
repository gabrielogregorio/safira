# 列表

列表可以在一个变量里装很多个值。

## 创建列表

位置从 1 开始数。

```safira
list of fruits receive "葡萄", "苹果", "芒果"

print fruits
print list of fruits in position 1
print the size of the list of fruits
```

## 添加和删除

用 `add` 在末尾加一个项目，用 `remove` 删掉一个项目。

```safira
list of fruits receive "葡萄", "苹果"

add "芒果" at the end of the list of fruits
remove "葡萄" from the list of fruits

print fruits
```

## 走过所有项目

`scroll through` 会一个一个地走过列表里的每个项目。

```safira
list of fruits receive "葡萄", "苹果", "芒果"

scroll through the list of fruits assigning in fruit {
    print "我喜欢" + fruit
}
```

## 挑战：购物清单

创建列表 `groceries`，里面有 `米饭` 和 `豆子`。在末尾添加 `牛奶`，然后每个项目显示一行。

```safira
# 在这里创建列表。

# 在这里添加牛奶。

# 在这里显示每个项目。

```

```solution
list of groceries receive "米饭", "豆子"

add "牛奶" at the end of the list of groceries

scroll through the list of groceries assigning in item {
    print item
}
```

```check
{ "uses": ["listDeclare", "listInsert", "forEach"], "hint": "用 list of ... receive、add ... at the end of the list of ... 和 scroll through the list of ...", "cases": [{ "shows": ["米饭", "豆子", "牛奶"] }] }
```
