# Mostrar na tela

O `mostre` não escreve só texto. Ele também faz contas e usa cores.

## Texto e números

Texto fica entre aspas. Número fica sem aspas, e o computador faz a conta para você.

```safira
mostre "Dois mais dois é:"
mostre 2 + 2
mostre 10 * 3
```

## Cores

Coloque `na cor` depois do texto. Vale o nome da cor ou um código como `#ff1122`.

```safira
mostre "Azul" na cor azul
mostre "Roxo" na cor roxo
mostre "Vermelho" na cor #ff1122
```

## Desafio: a conta

Mostre o resultado de `25 * 4`. Deixe o computador fazer a conta, sem escrever o resultado.

```safira
# Mostre aqui o resultado de 25 * 4.

```

```solution
mostre 25 * 4
```

```check
{ "uses": ["print"], "hint": "Sem aspas, o computador faz a conta: mostre 25 * 4", "cases": [{ "shows": ["100"] }] }
```
