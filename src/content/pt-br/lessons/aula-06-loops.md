# Repetições

O computador não se cansa de repetir. Você só diz quantas vezes.

## Repita

`repita` roda o bloco o número de vezes que você pedir.

```safira
repita 3 vezes {
    mostre "Olá!"
}
```

## Contar

`para cada` conta para você, e a variável muda em cada volta.

```safira
para cada numero de 1 até 5 {
    mostre numero
}
```

## Enquanto

`enquanto` repete até a condição ficar falsa. Digite 0 para sair.

```safira
numero = 1

enquanto numero for diferente de 0 {
    mostre "Digite 0 para sair:"
    numero = o número que o usuário digitar
}

mostre "Fim!"
```

## Desafio: tabuada do 2

Mostre a tabuada do 2 até o 10: 2, 4, 6 e assim por diante. Use uma repetição.

```safira
# Conte de 1 até 10 e mostre o número vezes 2.

```

```solution
para cada numero de 1 até 10 {
    mostre numero * 2
}
```

```check
{ "uses": ["repeat|while|forRange"], "hint": "Use para cada numero de 1 até 10 { ... } e mostre numero * 2.", "cases": [{ "shows": ["2", "4", "6", "8", "10", "12", "14", "16", "18", "20"] }] }
```
