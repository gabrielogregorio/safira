# Tempo e som

Um programa também pode esperar e tocar notas.

## Esperar

`espere` faz uma pausa antes do próximo comando.

```safira
mostre "Preparar..."
espere 1 segundo
mostre "Já!"
```

## Tocar uma nota

`toque` toca uma nota. Vale `C`, `D`, `E` ou `Do`, `Re`, `Mi`.

```safira
toque Do por 0.5s
toque Mi por 0.5s
toque Sol por 1s
```

## Desafio: contagem regressiva

Mostre 3, 2, 1, com uma espera entre os números, e depois mostre `Fogo!`.

```safira
# Mostre 3, espere, mostre 2, espere, mostre 1, espere.

# No final, mostre Fogo!

```

```solution
mostre 3
espere 1 segundo
mostre 2
espere 1 segundo
mostre 1
espere 1 segundo
mostre "Fogo!"
```

```check
{ "uses": ["wait"], "hint": "Coloque espere 1 segundo entre os mostre.", "cases": [{ "shows": ["3", "2", "1", "Fogo"] }] }
```
