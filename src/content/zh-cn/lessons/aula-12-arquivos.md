# 文件

文件用来保存信息。程序创建的所有东西，都会出现在项目的文件栏里。

## 创建和写入

运行之后，看一下文件栏。

```safira
创建文件 "笔记.txt"
写入 "买面包" 到文件 "笔记.txt"
```

## 读取

用 `读取文件` 把文件里的内容读出来。

```safira
创建文件 "成绩.txt"
覆盖 "成绩 10" 到文件 "成绩.txt"

内容 = 读取文件 "成绩.txt"
显示 内容
```

## 检查和删除

用 `删除文件` 删除文件，再检查它是否还存在。

```safira
创建文件 "old.txt"
删除文件 "old.txt"

如果 文件 "old.txt" 不存在 那么 {
    显示 "文件不见了"
}
```

## 挑战：日记

创建文件 `diary.txt`，在里面写入 `今天我学了Safira`，再读取这个文件并显示文字。

```safira
# 创建文件、写入、读取并显示。

```

```solution
创建文件 "diary.txt"
覆盖 "今天我学了Safira" 到文件 "diary.txt"

内容 = 读取文件 "diary.txt"
显示 内容
```

```check
{ "uses": ["fileCreate", "fileAppend|fileOverwrite", "fileRead"], "hint": "用 创建文件、overwrite ... to the file 和 读取文件。", "cases": [{ "shows": ["今天我学了Safira"] }] }
```
