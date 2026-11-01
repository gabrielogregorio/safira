# Contagem regressiva

## Contagem regressiva

```safira
mostre "Preparar..."

# espere faz uma pausa.
espere 1 segundo
mostre "Já!"
```

## Desafio: Contagem regressiva

```safira
# Desafio: Mostre 3, 2 e 1, com uma espera entre eles, e
# depois mostre Fogo!
# .

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
