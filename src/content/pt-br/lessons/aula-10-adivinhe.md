# Adivinhe

## Adivinhe

```safira
# Sorteia um número: 1 ou 2.
dado = um número aleatório entre 1 e 2

# Se saiu 1, mostra Cara. Se não, mostra Coroa.
se dado for igual a 1 então {
    mostre "Cara"
} senão {
    mostre "Coroa"
}
```

## Desafio: Adivinhe

```safira
# Desafio: Sorteie um número de 1 a 3 e guarde em segredo.
# Peça um número.
# Se for igual, mostre Acertou.
# Se não, mostre Errou.

```

```solution
segredo = um número aleatório entre 1 e 3
palpite = o número que o usuário digitar

se palpite for igual a segredo então {
    mostre "Acertou"
} senão {
    mostre "Errou"
}
```

```check
{"uses": ["random", "if"], "hint": "Sorteie, peça o palpite e compare com o se.", "cases": [{"inputs": ["9"], "shows": ["Errou"], "hides": ["Acertou"]}]}
```
