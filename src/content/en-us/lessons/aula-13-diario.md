# Diary

## Diary

```safira
# Creates the file and writes in it.
create the file "a.txt"
overwrite "hi" to the file "a.txt"

# Reads the file.
text = read the file "a.txt"
show text
```

## Challenge: Diary

```safira
# Challenge: Create diary.
# txt, write Today I learned Safira in it, read the file
# and show the text.

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
