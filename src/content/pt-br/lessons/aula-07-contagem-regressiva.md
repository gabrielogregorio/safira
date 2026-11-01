# Contagem regressiva

## Contagem regressiva

`espere 1 segundo` faz uma pausa.

```safira
mostre "Preparar..."
espere 1 segundo
mostre "Já!"
```

## Desafio: Contagem regressiva

Mostre 3, 2 e 1, com uma espera entre eles, e depois mostre `Fogo!`.

```safira
# Escreva aqui.
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
{"uses": ["wait"], "hint": "Coloque espere 1 segundo entre os mostre.", "cases": [{"shows": ["3", "2", "1", "Fogo"]}]}
```
