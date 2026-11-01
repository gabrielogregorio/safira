# 日记

## 日记

```safira
# 创建一个文件并写入文字。
创建文件 "a.txt"
覆盖 "你好" 到文件 "a.txt"

# 读出写入的文字并显示。
内容 = 读取文件 "a.txt"
显示 内容
```

## 挑战:日记

```safira
# 挑战:创建文件 日记.
# txt,写入 今天我学了Safira。
# 然后读取文件,显示里面的文字。

```

```solution
创建文件 "日记.txt"
覆盖 "今天我学了Safira" 到文件 "日记.txt"

内容 = 读取文件 "日记.txt"
显示 内容
```

```check
{"uses": ["fileCreate", "fileAppend|fileOverwrite", "fileRead"], "hint": "创建、覆盖、读取、显示。", "cases": [{"shows": ["今天我学了Safira"]}]}
```
