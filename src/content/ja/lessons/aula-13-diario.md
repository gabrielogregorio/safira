# 日記

## 日記

```safira
# ファイルを作って文字を書きます。
ファイル作成 "a.txt"
上書き "やあ" ファイルへ "a.txt"

# 書いた文字を読んで表示します。
内容 = ファイル読み込み "a.txt"
表示 内容
```

## チャレンジ: 日記

```safira
# チャレンジ: ファイル 日記.
# txt を作り、今日Safiraを学びました と書きます。
# それから読んで表示しましょう。

```

```solution
ファイル作成 "日記.txt"
上書き "今日Safiraを学びました" ファイルへ "日記.txt"

内容 = ファイル読み込み "日記.txt"
表示 内容
```

```check
{"uses": ["fileCreate", "fileAppend|fileOverwrite", "fileRead"], "hint": "作成、上書き、読み込み、表示です。", "cases": [{"shows": ["今日Safiraを学びました"]}]}
```
