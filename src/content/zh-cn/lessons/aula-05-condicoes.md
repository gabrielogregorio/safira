# 条件

用 `if`，程序就能选择做什么。

## 如果

只有当条件为真时，`{` 和 `}` 之间的代码才会运行。把 20 改成 10，再运行一次。

```safira
age = 20

if age is greater than 17 then {
    print "可以开车"
}
```

## 否则

`else` 是相反的路：条件为假时运行。

```safira
grade = 4

if grade is greater than or equal to 6 then {
    print "及格"
} else {
    print "不及格"
}
```

## 比较

你可以用 `is equal to`、`is different from`、`is greater than` 和 `is less than`。

```safira
password = "safira"

if password is equal to "safira" then {
    print "请进"
}
```

## 挑战：偶数还是奇数

请用户输入一个数字。如果它除以 2 的余数是 0，就显示 `偶数`。否则显示 `奇数`。

符号 `%` 得到除法的余数：`7 % 2` 是 1。

```safira
print "请输入一个数字："
number = the number that the user enters

# 在这里写 if。

```

```solution
print "请输入一个数字："
number = the number that the user enters

if number % 2 is equal to 0 then {
    print "偶数"
} else {
    print "奇数"
}
```

```check
{ "uses": ["if"], "hint": "这样比较：if number % 2 is equal to 0 then { ... } else { ... }", "cases": [{ "inputs": ["4"], "shows": ["偶数"], "hides": ["奇数"] }, { "inputs": ["7"], "shows": ["奇数"], "hides": ["偶数"] }] }
```
