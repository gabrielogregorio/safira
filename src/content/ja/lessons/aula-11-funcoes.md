# 関数

関数は、名前がついたコードのかたまりです。1回書けば、何回でも使えます。

## 作って呼ぶ

関数を作っただけでは何も動きません。名前を呼んだときに動きます。

```safira
function hello {
    print "こんにちは!"
    print "お元気ですか?"
}

hello()
hello()
```

## 値を渡す

関数は、値を受け取ってそれを使えます。

```safira
function greet(name) {
    print "こんにちは、" + name
}

greet("Ana")
greet("Bia")
```

## 結果を返す

`return` は、呼んだ場所に結果を渡します。

```safira
function double(number) {
    return number * 2
}

print double(4)
```

## チャレンジ: 足し算

2つの数を受け取って、その合計を返す `add` という関数を作りましょう。そのあと `add(2, 3)` を表示します。

```safira
# ここで関数を作ってください。

# ここで add(2, 3) を表示してください。

```

```solution
function add(a, b) {
    return a + b
}

print add(2, 3)
```

```check
{ "uses": ["functionDeclaration", "return", "call"], "hint": "function add(a, b) { で始めて、return a + b を使いましょう。", "cases": [{ "shows": ["5"] }] }
```
