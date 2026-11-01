# Lista de compras

## Lista de compras

```safira
# Cria a lista.
lista de frutas recebe "uva", "pera"

# Adiciona no final.
adicione "kiwi" no final da lista de frutas

# Passa por todos os itens.
percorra a lista de frutas atribuindo em item {
    mostre item
}
```

## Desafio: Lista de compras

```safira
# Desafio: Crie a lista compras com arroz e feijão,
# adicione leite no final e mostre cada item.

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
