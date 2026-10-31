# Sortear

Los juegos necesitan suerte, y el computador sabe sortear números.

## Tirar el dado

Ejecuta varias veces: el número cambia.

```safira
dado = un número aleatorio entre 1 y 6

muestra "Salió " + dado
```

## Suerte y condición

Al juntar el sorteo con el `si`, el programa decide solo.

```safira
moneda = un número aleatorio entre 1 y 2

si moneda es igual a 1 entonces {
    muestra "Cara"
} si no {
    muestra "Sello"
}
```

## Desafío: adivina

Sortea un número entre 1 y 3 y guárdalo en `secreto`. Pide un número. Si es igual, muestra `Acertaste`. Si no, muestra `Fallaste`.

```safira
# Sortea el secreto aquí.

muestra "Adivina un número del 1 al 3:"
intento = el número que ingresa el usuario

# Compara el intento con el secreto aquí.

```

```solution
secreto = un número aleatorio entre 1 y 3

muestra "Adivina un número del 1 al 3:"
intento = el número que ingresa el usuario

si intento es igual a secreto entonces {
    muestra "Acertaste"
} si no {
    muestra "Fallaste"
}
```

```check
{ "uses": ["random", "if"], "hint": "Usa secreto = un número aleatorio entre 1 y 3 y compara con el si.", "cases": [{ "inputs": ["9"], "shows": ["Fallaste"], "hides": ["Acertaste"] }] }
```
