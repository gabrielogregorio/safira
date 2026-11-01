# Adivina

## Adivina

```safira
# Sortea un número.
dado = un número aleatorio entre 1 y 2

# El si elige el camino.
si dado es igual a 1 entonces {
    muestra "Cara"
} si no {
    muestra "Cruz"
}
```

## Desafío: Adivina

```safira
# Desafío: Sortea un número en secreto, pide un número y
# muestra Acertaste si es igual o Fallaste si no.

```

```solution
secreto = un número aleatorio entre 1 y 3
intento = el número que ingresa el usuario

si intento es igual a secreto entonces {
    muestra "Acertaste"
} si no {
    muestra "Fallaste"
}
```

```check
{"uses": ["random", "if"], "hint": "Sortea, pide el intento y compara con si.", "cases": [{"inputs": ["9"], "shows": ["Fallaste"], "hides": ["Acertaste"]}]}
```
