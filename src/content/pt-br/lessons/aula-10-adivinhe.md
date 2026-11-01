# Adivinhe

## Adivinhe

```safira
# Sorteia um número.
dado = um número aleatório entre 1 e 2

# O se escolhe o caminho.
se dado for igual a 1 então {
    mostre "Cara"
} senão {
    mostre "Coroa"
}
```

## Desafio: Adivinhe

```safira
# Desafio: Sorteie um número em segredo, peça um número e
# mostre Acertou se for igual ou Errou se não for.

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
