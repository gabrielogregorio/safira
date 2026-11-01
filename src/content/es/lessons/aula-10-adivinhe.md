# Adivina

## Adivina

```safira
# Sortea un número: 1 o 2.
dado = un número aleatorio entre 1 y 2

# Si sale 1, muestra Cara. Si no, muestra Cruz.
si dado es igual a 1 entonces {
    muestra "Cara"
} si no {
    muestra "Cruz"
}
```

## Desafío: Adivina

```safira
# Desafío: Sortea un número del 1 al 3 y guárdalo en
# secreto.
# Pide un número.
# Si es igual, muestra Acertaste.
# Si no, muestra Fallaste.

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
