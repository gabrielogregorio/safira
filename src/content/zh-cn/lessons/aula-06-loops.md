# 重复

电脑重复做事从不觉得累。你只要告诉它做几次。

## repeat

`repeat` 会把代码块运行你指定的次数。

```safira
repeat 3 times {
    print "你好！"
}
```

## 数数

`for each` 帮你数数，变量每一圈都会变化。

```safira
for each number from 1 to 5 {
    print number
}
```

## while

`while` 会一直重复，直到条件变为假。输入 0 就退出。

```safira
number = 1

while number is different from 0 {
    print "输入 0 退出："
    number = the number that the user enters
}

print "结束！"
```

## 挑战：2 的乘法表

显示 2 的乘法表，一直到 10：2、4、6，依此类推。请使用重复。

```safira
# 从 1 数到 10，显示这个数字乘以 2。

```

```solution
for each number from 1 to 10 {
    print number * 2
}
```

```check
{ "uses": ["repeat|while|forRange"], "hint": "用 for each number from 1 to 10 { ... }，然后 print number * 2。", "cases": [{ "shows": ["2", "4", "6", "8", "10", "12", "14", "16", "18", "20"] }] }
```
