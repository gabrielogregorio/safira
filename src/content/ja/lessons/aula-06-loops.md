# くり返し

コンピューターはくり返しに疲れません。何回かだけ伝えましょう。

## repeat

`repeat` は、頼んだ回数だけブロックを動かします。

```safira
repeat 3 times {
    print "こんにちは!"
}
```

## 数える

`for each` が数えてくれて、変数は1回ごとに変わります。

```safira
for each number from 1 to 5 {
    print number
}
```

## while

`while` は、条件が正しくなくなるまでくり返します。終わるには 0 を入力します。

```safira
number = 1

while number is different from 0 {
    print "終わるには 0 を入力してください:"
    number = the number that the user enters
}

print "おしまい!"
```

## チャレンジ: 2のだん

2のだんを10まで表示しましょう。2、4、6、と続きます。くり返しを使います。

```safira
# 1から10まで数えて、その数の2倍を表示してください。

```

```solution
for each number from 1 to 10 {
    print number * 2
}
```

```check
{ "uses": ["repeat|while|forRange"], "hint": "for each number from 1 to 10 { ... } を使って、print number * 2 としましょう。", "cases": [{ "shows": ["2", "4", "6", "8", "10", "12", "14", "16", "18", "20"] }] }
```
