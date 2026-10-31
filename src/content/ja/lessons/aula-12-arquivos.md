# ファイル

ファイルは情報をしまっておけます。プログラムが作ったものは、プロジェクトのファイルバーに表示されます。

## 作って書く

実行したあと、ファイルバーを見てみましょう。

```safira
create the file "note.txt"
add "パンを買う" to the file "note.txt"
```

## 読む

`read the file` で、ファイルの中の文字を読めます。

```safira
create the file "grade.txt"
overwrite "100点" to the file "grade.txt"

text = read the file "grade.txt"
print text
```

## 確認して消す

`delete the file` で消して、`does not exist` で、なくなったことを確かめます。

```safira
create the file "old.txt"
delete the file "old.txt"

if the file "old.txt" does not exist then {
    print "ファイルが消えました"
}
```

## チャレンジ: 日記

`diary.txt` というファイルを作り、`今日はサフィラを学びました` と書き込みます。そのファイルを読んで、文字を表示しましょう。

```safira
# ファイルを作って、書いて、読んで、表示してください。

```

```solution
create the file "diary.txt"
overwrite "今日はサフィラを学びました" to the file "diary.txt"

text = read the file "diary.txt"
print text
```

```check
{ "uses": ["fileCreate", "fileAppend|fileOverwrite", "fileRead"], "hint": "create the file、overwrite ... to the file、read the file を使いましょう。", "cases": [{ "shows": ["今日はサフィラを学びました"] }] }
```
