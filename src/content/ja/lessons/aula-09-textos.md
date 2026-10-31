# 文字をあつかう

文字の形を変えたり、1文字ずつ見たりできます。

## 大文字と小文字

文字は、すべて大文字、すべて小文字、最初だけ大文字にできます。

```safira
name = "ana maria"

print name in upper case
print name in lower case
print name in capitalized
```

## 1文字ずつ

`scroll through` は、1文字ずつ順番に見ていきます。

```safira
word = "Sun"

scroll through word assigning in letter {
    print letter
}
```

## チャレンジ: さけぶ

文字を1つ聞いて、その文字をすべて大文字で表示しましょう。

```safira
print "英語の単語を入力してください:"
word = what the user types

# ここで word を大文字で表示してください。

```

```solution
print "英語の単語を入力してください:"
word = what the user types

print word in upper case
```

```check
{ "uses": ["case"], "exact": true, "hint": "print word in upper case と書きましょう。", "cases": [{ "inputs": ["safira"], "shows": ["SAFIRA"] }] }
```
