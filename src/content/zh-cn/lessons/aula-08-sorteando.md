# 随机

游戏需要运气，电脑会随机抽数字。

## 掷骰子

多运行几次：数字会变。

```safira
dice = a random number between 1 and 6

print "掷出了 " + dice
```

## 运气和条件

把随机数和 `if` 结合起来，程序就能自己做决定。

```safira
coin = a random number between 1 and 2

if coin is equal to 1 then {
    print "正面"
} else {
    print "反面"
}
```

## 挑战：猜一猜

随机抽一个 1 到 3 之间的数字，保存在 `secret` 里。请用户输入一个数字。如果相等，就显示 `猜对了`。否则显示 `猜错了`。

```safira
# 在这里随机抽出 secret。

print "猜一个 1 到 3 的数字："
guess = the number that the user enters

# 在这里比较 guess 和 secret。

```

```solution
secret = a random number between 1 and 3

print "猜一个 1 到 3 的数字："
guess = the number that the user enters

if guess is equal to secret then {
    print "猜对了"
} else {
    print "猜错了"
}
```

```check
{ "uses": ["random", "if"], "hint": "用 secret = a random number between 1 and 3，再用 if 比较。", "cases": [{ "inputs": ["9"], "shows": ["猜错了"], "hides": ["猜对了"] }] }
```
