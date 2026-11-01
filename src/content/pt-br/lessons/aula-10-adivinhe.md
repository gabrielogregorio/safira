# Adivinhe

## Adivinhe

`um número aleatório entre 1 e 3` sorteia, e `se a for igual a b então {` compara. Depois vem `} senão {`.

Sorteie um número em `segredo`, peça um número e mostre `Acertou` se for igual ou `Errou` se não for.

```safira
# Escreva aqui.
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
