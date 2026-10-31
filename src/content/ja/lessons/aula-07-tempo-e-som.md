# 時間と音

プログラムは、待ったり音を鳴らしたりもできます。

## 待つ

`wait` は、次のコマンドの前に少し止まります。

```safira
print "よーい..."
wait 1 second
print "スタート!"
```

## 音を鳴らす

`play` は音を鳴らします。`C`、`D`、`E` や `Do`、`Re`、`Mi` が使えます。

```safira
play Do for 0.5s
play Mi for 0.5s
play Sol for 1s
```

## チャレンジ: カウントダウン

3、2、1と、数の間に待ち時間を入れて表示し、最後に `発射!` と表示しましょう。

```safira
# 3を表示して、待って、2を表示して、待って、1を表示して、待ちます。

# 最後に 発射! と表示してください。

```

```solution
print 3
wait 1 second
print 2
wait 1 second
print 1
wait 1 second
print "発射!"
```

```check
{ "uses": ["wait"], "hint": "print の間に wait 1 second を入れましょう。", "cases": [{ "shows": ["3", "2", "1", "発射"] }] }
```
