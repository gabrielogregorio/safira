# Files

Files keep information. Everything the program creates shows up in the project's files bar.

## Create and write

Look at the files bar after you run.

```safira
create the file "note.txt"
add "Buy bread" to the file "note.txt"
```

## Read

`read the file` brings the text back into a variable. `overwrite` replaces all the text in the file.

```safira
create the file "grade.txt"
overwrite "Grade 10" to the file "grade.txt"

text = read the file "grade.txt"
print text
```

## Check and delete

You can ask whether a file exists and delete what you no longer need.

```safira
create the file "old.txt"
delete the file "old.txt"

if the file "old.txt" does not exist then {
    print "The file is gone"
}
```

## Challenge: diary

Create the file `diary.txt`, write `Today I learned Safira` in it, read the file and show the text.

```safira
# Create the file, write, read and show.

```

```solution
create the file "diary.txt"
overwrite "Today I learned Safira" to the file "diary.txt"

text = read the file "diary.txt"
print text
```

```check
{ "uses": ["fileCreate", "fileAppend|fileOverwrite", "fileRead"], "hint": "Use create the file, overwrite ... to the file and read the file.", "cases": [{ "shows": ["Today I learned Safira"] }] }
```
