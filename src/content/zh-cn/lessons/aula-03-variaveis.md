# 变量

变量就像一个有名字的小盒子。它保存一个值，留着以后使用。

## 保存一个值

`=` 把值放进小盒子里。之后只要用它的名字就行了。

```safira
name = "小安"
age = 20

print name
print age
```

## 看看变量

运行之后，看一下“变量”面板：它会显示每个变量的名字、值和类型。

想一步一步地看吗？打开“运行”菜单，选择“逐行运行”。

```safira
points = 10
points = points + 5

print points
```

## 把文字和变量连起来

`+` 可以把文字和变量连成一句话。

```safira
name = "小安"
age = 20

print "我的名字是" + name
print "我今年" + age + "岁"
```

## 挑战：你的城市

创建一个叫 `city` 的变量，值为 `Lima`，然后显示这句话 `我住在Lima`，用 `+` 把文字和变量连起来。

```safira
# 在这里创建变量。

# 在这里显示这句话。

```

```solution
city = "Lima"
print "我住在" + city
```

```check
{ "uses": ["assign", "variable"], "hint": "用 city = \"Lima\" 创建变量，再用 + 连起来。", "cases": [{ "shows": ["我住在Lima"] }] }
```
