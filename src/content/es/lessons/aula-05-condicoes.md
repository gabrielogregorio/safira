# Condiciones

Con el `si`, el programa elige qué hacer.

## Si

El bloque entre `{` y `}` solo se ejecuta cuando la condición es verdadera. Cambia el 20 por 10 y ejecuta de nuevo.

```safira
edad = 20

si edad es mayor que 17 entonces {
    muestra "Puede conducir"
}
```

## Si no

El `si no` es el camino contrario: se ejecuta cuando la condición es falsa.

```safira
nota = 4

si nota es mayor o igual a 6 entonces {
    muestra "Aprobó"
} si no {
    muestra "Reprobó"
}
```

## Comparar

Puedes usar `es igual a`, `es diferente de`, `es mayor que` y `es menor que`.

```safira
clave = "safira"

si clave es igual a "safira" entonces {
    muestra "Puede entrar"
}
```

## Desafío: par o impar

Pide un número. Si el resto de la división por 2 es 0, muestra `par`. Si no, muestra `impar`.

El signo `%` da el resto de la división: `7 % 2` es 1.

```safira
muestra "Escribe un número:"
numero = el número que ingresa el usuario

# Escribe el si aquí.

```

```solution
muestra "Escribe un número:"
numero = el número que ingresa el usuario

si numero % 2 es igual a 0 entonces {
    muestra "par"
} si no {
    muestra "impar"
}
```

```check
{ "uses": ["if"], "hint": "Compara con: si numero % 2 es igual a 0 entonces { ... } si no { ... }", "cases": [{ "inputs": ["4"], "shows": ["par"], "hides": ["impar"] }, { "inputs": ["7"], "shows": ["impar"], "hides": ["par"] }] }
```
