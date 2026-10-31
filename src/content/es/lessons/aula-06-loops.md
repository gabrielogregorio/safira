# Repeticiones

El computador no se cansa de repetir. Tú solo dices cuántas veces.

## Repetir

`repetir` ejecuta el bloque tantas veces como pidas.

```safira
repetir 3 veces {
    muestra "¡Hola!"
}
```

## Contar

`para cada` cuenta por ti, y la variable cambia en cada vuelta.

```safira
para cada numero desde 1 hasta 5 {
    muestra numero
}
```

## Mientras

`mientras` repite hasta que la condición se vuelve falsa. Escribe 0 para salir.

```safira
numero = 1

mientras numero es diferente de 0 {
    muestra "Escribe 0 para salir:"
    numero = el número que ingresa el usuario
}

muestra "¡Fin!"
```

## Desafío: tabla del 2

Muestra la tabla del 2 hasta el 10: 2, 4, 6 y así sucesivamente. Usa una repetición.

```safira
# Cuenta de 1 hasta 10 y muestra el número por 2.

```

```solution
para cada numero desde 1 hasta 10 {
    muestra numero * 2
}
```

```check
{ "uses": ["repeat|while|forRange"], "hint": "Usa para cada numero desde 1 hasta 10 { ... } y muestra numero * 2.", "cases": [{ "shows": ["2", "4", "6", "8", "10", "12", "14", "16", "18", "20"] }] }
```
