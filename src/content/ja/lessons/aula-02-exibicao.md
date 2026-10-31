# 画面に表示する

`print` は文字を出すだけではありません。計算をしたり、色をつけたりもできます。

## 文字と数

文字は引用符で囲みます。数は囲みません。計算はコンピューターがしてくれます。

```safira
print "2たす2は:"
print 2 + 2
print 10 * 3
```

## 同じ行に表示する

`print on this line` を使うと、次の表示が同じ行に続きます。

```safira
print on this line "おは"
print on this line "よう!"
```

## 色

文字のあとに `in color` を付けます。色の名前や、`#ff1122` のようなコードが使えます。

```safira
print "青" in color blue
print "紫" in color purple
print "赤" in color #ff1122
```

## チャレンジ: 計算

`25 * 4` の結果を表示しましょう。答えを書かずに、コンピューターに計算させます。

```safira
# ここに 25 * 4 の結果を表示してください。

```

```solution
print 25 * 4
```

```check
{ "uses": ["print"], "hint": "引用符をつけなければ、コンピューターが計算します: print 25 * 4", "cases": [{ "shows": ["100"] }] }
```
