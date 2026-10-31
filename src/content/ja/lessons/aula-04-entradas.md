# ユーザーに質問する

使っている人と話せると、プログラムはもっと楽しくなります。

## 文字を読み取る

`what the user types` で、プログラムは止まって待ちます。出力パネルの入力欄に書いて、Enter を押しましょう。

```safira
print "お名前は何ですか?"
name = what the user types

print "こんにちは、" + name
```

## 数を読み取る

入力されたもので計算したいときは、数を頼みます。

```safira
print "数を入力してください:"
number = the number that the user enters

double = number * 2
print "2倍は " + double
```

## チャレンジ: 3倍

数を1つ聞いて、その3倍を表示しましょう。

```safira
# ユーザーに数を聞いてください。

# その数の3倍を表示してください。

```

```solution
print "数を入力してください:"
number = the number that the user enters

print number * 3
```

```check
{ "uses": ["input"], "hint": "number = the number that the user enters と書いてから、print number * 3 としましょう。", "cases": [{ "inputs": ["4"], "shows": ["12"] }, { "inputs": ["10"], "shows": ["30"] }] }
```
