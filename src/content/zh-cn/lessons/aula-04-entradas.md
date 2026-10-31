# 询问用户

程序会和使用它的人聊天，就更有意思了。

## 读取文字

`what the user types` 会让程序停下来等待。在输出面板的输入框里打字，然后按回车。

```safira
print "你叫什么名字？"
name = what the user types

print "你好，" + name
```

## 读取数字

想用输入的内容做计算，就要请用户输入数字。

```safira
print "请输入一个数字："
number = the number that the user enters

double = number * 2
print "它的两倍是 " + double
```

## 挑战：三倍

请用户输入一个数字，然后显示它的三倍。

```safira
# 请用户输入一个数字。

# 显示这个数字乘以 3。

```

```solution
print "请输入一个数字："
number = the number that the user enters

print number * 3
```

```check
{ "uses": ["input"], "hint": "用 number = the number that the user enters，然后 print number * 3。", "cases": [{ "inputs": ["4"], "shows": ["12"] }, { "inputs": ["10"], "shows": ["30"] }] }
```
