# 条件

`if` を使うと、プログラムが何をするか選べます。

## if

`{` と `}` の間のブロックは、条件が正しいときだけ動きます。20を10に変えて、もう一度実行してみましょう。

```safira
age = 20

if age is greater than 17 then {
    print "運転できます"
}
```

## else

`else` は反対の道です。条件が正しくないときに動きます。

```safira
score = 4

if score is greater than or equal to 6 then {
    print "合格"
} else {
    print "不合格"
}
```

## 比べる

`is equal to`、`is different from`、`is greater than`、`is less than` が使えます。

```safira
password = "safira"

if password is equal to "safira" then {
    print "入ってください"
}
```

## チャレンジ: 偶数か奇数か

数を1つ聞きます。2で割った余りが0なら `偶数`、そうでなければ `奇数` と表示しましょう。

`%` は割り算の余りです。`7 % 2` は1になります。

```safira
print "数を入力してください:"
number = the number that the user enters

# ここに if を書いてください。

```

```solution
print "数を入力してください:"
number = the number that the user enters

if number % 2 is equal to 0 then {
    print "偶数"
} else {
    print "奇数"
}
```

```check
{ "uses": ["if"], "hint": "if number % 2 is equal to 0 then { ... } else { ... } で比べましょう。", "cases": [{ "inputs": ["4"], "shows": ["偶数"], "hides": ["奇数"] }, { "inputs": ["7"], "shows": ["奇数"], "hides": ["偶数"] }] }
```
