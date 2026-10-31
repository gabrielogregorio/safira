# Tiempo y sonido

Un programa también puede esperar y tocar notas.

## Esperar

`esperar` hace una pausa antes del siguiente comando.

```safira
muestra "Preparados..."
esperar 1 segundo
muestra "¡Ya!"
```

## Tocar una nota

`tocar` toca una nota. Vale `C`, `D`, `E` o `Do`, `Re`, `Mi`.

```safira
tocar Do por 0.5s
tocar Mi por 0.5s
tocar Sol por 1s
```

## Desafío: cuenta regresiva

Muestra 3, 2, 1, con una espera entre los números, y después muestra `¡Fuego!`.

```safira
# Muestra 3, espera, muestra 2, espera, muestra 1, espera.

# Al final, muestra ¡Fuego!

```

```solution
muestra 3
esperar 1 segundo
muestra 2
esperar 1 segundo
muestra 1
esperar 1 segundo
muestra "¡Fuego!"
```

```check
{ "uses": ["wait"], "hint": "Pon esperar 1 segundo entre los muestra.", "cases": [{ "shows": ["3", "2", "1", "Fuego"] }] }
```
