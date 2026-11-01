# 日记

## 日记

`创建文件 "a.txt"` 创建。`覆盖 "你好" 到文件 "a.txt"` 写入。`读取文件 "a.txt"` 读出文字。

创建 `日记.txt`,写入 `今天我学了Safira`,读取文件并显示文字。

```safira
# 在这里写。
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
