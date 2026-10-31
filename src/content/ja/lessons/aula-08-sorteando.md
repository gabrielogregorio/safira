# ランダムに選ぶ

ゲームには運が必要です。コンピューターは数をランダムに選べます。

## サイコロをふる

何回か実行してみましょう。数が変わります。

```safira
dice = a random number between 1 and 6

print "出た数は " + dice
```

## 運と条件

ランダムな数と `if` を組み合わせると、プログラムが自分で決めます。

```safira
coin = a random number between 1 and 2

if coin is equal to 1 then {
    print "表"
} else {
    print "裏"
}
```

## チャレンジ: 当てよう

1から3の数をランダムに選んで、`secret` に入れます。数を1つ聞いて、同じなら `当たり`、違うなら `はずれ` と表示しましょう。

```safira
# ここで secret を選んでください。

print "1から3の数を当ててください:"
guess = the number that the user enters

# ここで guess と secret を比べてください。

```

```solution
secret = a random number between 1 and 3

print "1から3の数を当ててください:"
guess = the number that the user enters

if guess is equal to secret then {
    print "当たり"
} else {
    print "はずれ"
}
```

```check
{ "uses": ["random", "if"], "hint": "secret = a random number between 1 and 3 と書いて、if で比べましょう。", "cases": [{ "inputs": ["9"], "shows": ["はずれ"], "hides": ["当たり"] }] }
```
