# Lista de compras

## Lista de compras

```safira
# Cria uma lista com duas frutas.
lista de frutas recebe "uva", "pera"

# Coloca mais uma fruta no final.
adicione "kiwi" no final da lista de frutas

# Mostra cada fruta, uma por linha.
percorra a lista de frutas atribuindo em item {
    mostre item
}
```

## Desafio: Lista de compras

```safira
# Desafio: Crie uma lista chamada compras com arroz e
# feijão.
# Coloque leite no final.
# Mostre cada item.

```

```solution
lista de compras recebe "arroz", "feijão"
adicione "leite" no final da lista de compras

percorra a lista de compras atribuindo em item {
    mostre item
}
```

```check
{"uses": ["listDeclare", "listInsert", "forEach"], "hint": "Crie, adicione e percorra a lista.", "cases": [{"shows": ["arroz", "feijão", "leite"]}]}
```
