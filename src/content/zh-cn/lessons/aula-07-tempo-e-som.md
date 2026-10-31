# 时间和声音

程序还可以等待，也可以演奏音符。

## 等待

`wait` 会在下一条命令之前暂停一下。

```safira
print "准备……"
wait 1 second
print "开始！"
```

## 演奏一个音符

`play` 演奏一个音符。可以用 `C`、`D`、`E`，也可以用 `Do`、`Re`、`Mi`。

```safira
play Do for 0.5s
play Mi for 0.5s
play Sol for 1s
```

## 挑战：倒计时

显示 3、2、1，数字之间要等待，最后显示 `开火！`。

```safira
# 显示 3，等待，显示 2，等待，显示 1，等待。

# 最后，显示 开火！

```

```solution
print 3
wait 1 second
print 2
wait 1 second
print 1
wait 1 second
print "开火！"
```

```check
{ "uses": ["wait"], "hint": "在每个 print 之间加上 wait 1 second。", "cases": [{ "shows": ["3", "2", "1", "开火"] }] }
```
