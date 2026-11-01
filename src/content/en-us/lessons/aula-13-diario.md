# Diary

## Diary

```safira
# Creates a file and writes in it.
create the file "a.txt"
overwrite "hi" to the file "a.txt"

# Reads what was written and shows it.
text = read the file "a.txt"
show text
```

## Challenge: Diary

```safira
# Challenge: Create the file diary.
# txt and write Today I learned Safira in it.
# Then read the file and show what is written.

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
