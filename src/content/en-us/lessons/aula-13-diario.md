# Diary

## Diary

`create the file "a.txt"` creates. `overwrite "hi" to the file "a.txt"` writes. `read the file "a.txt"` brings the text.

Create `diary.txt`, write `Today I learned Safira` in it, read the file and show the text.

```safira
# Write here.
```

```solution
create the file "diary.txt"
overwrite "Today I learned Safira" to the file "diary.txt"

text = read the file "diary.txt"
show text
```

```check
{"uses": ["fileCreate", "fileAppend|fileOverwrite", "fileRead"], "hint": "Create, overwrite, read and show.", "cases": [{"shows": ["Today I learned Safira"]}]}
```
