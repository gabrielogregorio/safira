# Condições

Com o `se`, o programa escolhe o que fazer.

## Se

O bloco entre `{` e `}` só roda quando a condição é verdadeira. Troque o 20 por 10 e execute de novo.

```safira
idade = 20

se idade for maior que 17 então {
    mostre "Pode dirigir"
}
```

## Senão

O `senão` é o caminho contrário: roda quando a condição é falsa.

```safira
nota = 4

se nota for maior ou igual a 6 então {
    mostre "Passou"
} senão {
    mostre "Reprovou"
}
```

## Comparar

Você pode usar `for igual a`, `for diferente de`, `for maior que` e `for menor que`.

```safira
senha = "safira"

se senha for igual a "safira" então {
    mostre "Pode entrar"
}
```

## Desafio: par ou ímpar

Peça um número. Se o resto da divisão por 2 for 0, mostre `par`. Senão, mostre `ímpar`.

O sinal `%` dá o resto da divisão: `7 % 2` é 1.

```safira
mostre "Digite um número:"
numero = o número que o usuário digitar

# Escreva o se aqui.

```

```solution
mostre "Digite um número:"
numero = o número que o usuário digitar

se numero % 2 for igual a 0 então {
    mostre "par"
} senão {
    mostre "ímpar"
}
```

```check
{ "uses": ["if"], "hint": "Compare com: se numero % 2 for igual a 0 então { ... } senão { ... }", "cases": [{ "inputs": ["4"], "shows": ["par"], "hides": ["ímpar"] }, { "inputs": ["7"], "shows": ["ímpar"], "hides": ["par"] }] }
```
