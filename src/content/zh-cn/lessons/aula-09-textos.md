# 玩转文字

你可以改变文字的写法，也可以一个字母一个字母地看。

## 大写和小写

一段文字可以全部大写、全部小写，或者只有第一个字母大写。

```safira
name = "ana maria"

print name in upper case
print name in lower case
print name in capitalized
```

## 一个字母一个字母

`scroll through` 会一个一个地走过每个字母。

```safira
word = "Sol"

scroll through word assigning in letter {
    print letter
}
```

## 挑战：大喊

请用户输入一段文字，然后把它全部用大写显示出来。

```safira
print "请输入一个单词："
word = what the user types

# 在这里把单词用大写显示出来。

```

```solution
print "请输入一个单词："
word = what the user types

print word in upper case
```

```check
{ "uses": ["case"], "exact": true, "hint": "这样写：print word in upper case", "cases": [{ "inputs": ["safira"], "shows": ["SAFIRA"] }] }
```
