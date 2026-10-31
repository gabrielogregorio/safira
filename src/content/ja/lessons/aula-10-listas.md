# リスト

リストは、たくさんの値を1つの変数に入れておけます。

## リストを作る

位置は1から始まります。

```safira
list of fruits receive "ぶどう", "りんご", "マンゴー"

print fruits
print list of fruits in position 1
print the size of the list of fruits
```

## 追加と削除

`add` で最後に追加し、`remove` で取り除きます。

```safira
list of fruits receive "ぶどう", "りんご"

add "マンゴー" at the end of the list of fruits
remove "ぶどう" from the list of fruits

print fruits
```

## すべての項目を見る

`scroll through` で、1つずつ順番に見ていきます。

```safira
list of fruits receive "ぶどう", "りんご", "マンゴー"

scroll through the list of fruits assigning in fruit {
    print fruit + "が好きです"
}
```

## チャレンジ: 買い物リスト

`shopping` というリストに `お米` と `豆` を入れます。最後に `牛乳` を追加して、項目を1行ずつ表示しましょう。

```safira
# ここでリストを作ってください。

# ここで牛乳を追加してください。

# ここで項目を1つずつ表示してください。

```

```solution
list of shopping receive "お米", "豆"

add "牛乳" at the end of the list of shopping

scroll through the list of shopping assigning in item {
    print item
}
```

```check
{ "uses": ["listDeclare", "listInsert", "forEach"], "hint": "list of ... receive、add ... at the end of the list of ...、scroll through the list of ... を使いましょう。", "cases": [{ "shows": ["お米", "豆", "牛乳"] }] }
```
