# Sortear

Jogos precisam de sorte, e o computador sabe sortear números.

## Jogar o dado

Execute várias vezes: o número muda.

```safira
dado = um número aleatório entre 1 e 6

mostre "Saiu " + dado
```

## Sorte e condição

Juntando o sorteio com o `se`, o programa decide sozinho.

```safira
moeda = um número aleatório entre 1 e 2

se moeda for igual a 1 então {
    mostre "Cara"
} senão {
    mostre "Coroa"
}
```

## Desafio: adivinhe

Sorteie um número entre 1 e 3 e guarde em `segredo`. Peça um número. Se for igual, mostre `Acertou`. Senão, mostre `Errou`.

```safira
# Sorteie o segredo aqui.

mostre "Adivinhe um número de 1 a 3:"
palpite = o número que o usuário digitar

# Compare o palpite com o segredo aqui.

```

```solution
segredo = um número aleatório entre 1 e 3

mostre "Adivinhe um número de 1 a 3:"
palpite = o número que o usuário digitar

se palpite for igual a segredo então {
    mostre "Acertou"
} senão {
    mostre "Errou"
}
```

```check
{ "uses": ["random", "if"], "hint": "Use segredo = um número aleatório entre 1 e 3 e compare com o se.", "cases": [{ "inputs": ["9"], "shows": ["Errou"], "hides": ["Acertou"] }] }
```
