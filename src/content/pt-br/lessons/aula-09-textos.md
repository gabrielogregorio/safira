# Mexer com textos

Dá para mudar o jeito de um texto e olhar letra por letra.

## Maiúsculas e minúsculas

Um texto pode ficar todo grande, todo pequeno ou só com a primeira letra grande.

```safira
nome = "ana maria"

mostre nome em maiusculo
mostre nome em minusculo
mostre nome captalizado
```

## Letra por letra

`percorra` passa por cada letra, uma de cada vez.

```safira
palavra = "Sol"

percorra palavra atribuindo em letra {
    mostre letra
}
```

## Desafio: gritar

Peça um texto e mostre esse texto todo em maiúsculas.

```safira
mostre "Digite uma palavra:"
palavra = o que o usuário digitar

# Mostre a palavra em maiúsculas aqui.

```

```solution
mostre "Digite uma palavra:"
palavra = o que o usuário digitar

mostre palavra em maiusculo
```

```check
{ "uses": ["case"], "exact": true, "hint": "Escreva: mostre palavra em maiusculo", "cases": [{ "inputs": ["safira"], "shows": ["SAFIRA"] }] }
```
