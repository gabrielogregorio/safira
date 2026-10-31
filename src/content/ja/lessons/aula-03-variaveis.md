# 変数

変数は、名前がついた小さな箱です。あとで使うために値を入れておけます。

## 値をしまう

`=` で箱に値を入れます。あとは名前を書くだけで使えます。

```safira
name = "Ana"
age = 20

print name
print age
```

## 変数を見る

実行したあと、変数パネルを見てみましょう。変数の名前、値、種類が表示されます。

1歩ずつ見たいときは、実行メニューを開いて「1行ずつ実行」を選びます。

```safira
points = 10
points = points + 5

print points
```

## 文字と変数をつなぐ

`+` で、文字と変数をつないで1つの文にできます。

```safira
name = "Ana"
age = 20

print "わたしの名前は" + name + "です"
print "年は" + age + "歳です"
```

## チャレンジ: あなたの町

`city` という変数に `Lima` を入れて、文字と変数をつなげて `Limaに住んでいます` と表示しましょう。

```safira
# ここで変数を作ってください。

# ここで文を表示してください。

```

```solution
city = "Lima"
print city + "に住んでいます"
```

```check
{ "uses": ["assign", "variable"], "hint": "city = \"Lima\" で変数を作り、+ でつなぎましょう。", "cases": [{ "shows": ["Limaに住んでいます"] }] }
```
