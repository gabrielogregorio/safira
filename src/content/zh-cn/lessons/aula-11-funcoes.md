# 函数

函数是一段有名字的代码。你写一次，就可以用很多次。

## 创建和调用

创建函数不会运行任何东西。只有当你调用它的名字时，它才会运行。

```safira
function hello {
    print "你好！"
    print "还好吗？"
}

hello()
hello()
```

## 传入一个值

函数可以接收值，并用这些值来工作。

```safira
function greet(name) {
    print "你好，" + name
}

greet("小安")
greet("小美")
```

## 返回结果

`return` 把一个结果交给调用它的地方。

```safira
function double(number) {
    return number * 2
}

print double(4)
```

## 挑战：求和

创建函数 `add_up`，它接收两个数字，并返回它们的和。然后显示 `add_up(2, 3)`。

```safira
# 在这里创建函数。

# 在这里显示 add_up(2, 3)。

```

```solution
function add_up(a, b) {
    return a + b
}

print add_up(2, 3)
```

```check
{ "uses": ["functionDeclaration", "return", "call"], "hint": "以 function add_up(a, b) { 开头，再用 return a + b。", "cases": [{ "shows": ["5"] }] }
```
