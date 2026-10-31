# 文件

文件用来保存信息。程序创建的所有东西，都会出现在项目的文件栏里。

## 创建和写入

运行之后，看一下文件栏。

```safira
create the file "note.txt"
add "买面包" to the file "note.txt"
```

## 读取

用 `read the file` 把文件里的内容读出来。

```safira
create the file "grade.txt"
overwrite "成绩 10" to the file "grade.txt"

text = read the file "grade.txt"
print text
```

## 检查和删除

用 `delete the file` 删除文件，再检查它是否还存在。

```safira
create the file "old.txt"
delete the file "old.txt"

if the file "old.txt" does not exist then {
    print "文件不见了"
}
```

## 挑战：日记

创建文件 `diary.txt`，在里面写入 `今天我学了Safira`，再读取这个文件并显示文字。

```safira
# 创建文件、写入、读取并显示。

```

```solution
create the file "diary.txt"
overwrite "今天我学了Safira" to the file "diary.txt"

text = read the file "diary.txt"
print text
```

```check
{ "uses": ["fileCreate", "fileAppend|fileOverwrite", "fileRead"], "hint": "用 create the file、overwrite ... to the file 和 read the file。", "cases": [{ "shows": ["今天我学了Safira"] }] }
```
