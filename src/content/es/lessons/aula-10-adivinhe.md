# Adivina

## Adivina

`un número aleatorio entre 1 y 3` sortea, y `si a es igual a b entonces {` compara. Después viene `} si no {`.

```safira
dado = un número aleatorio entre 1 y 2

si dado es igual a 1 entonces {
    muestra "Cara"
} si no {
    muestra "Cruz"
}
```

## Desafío: Adivina

Sortea un número en `secreto`, pide un número y muestra `Acertaste` si es igual o `Fallaste` si no.

```safira
# Escribe aquí.
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
