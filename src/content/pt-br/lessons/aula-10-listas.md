# Listas

Uma lista guarda vários valores em uma variável só.

## Criar uma lista

As posições começam em 1.

```safira
lista de frutas recebe "uva", "maçã", "manga"

mostre frutas
mostre lista de frutas na posição 1
mostre o tamanho da lista de frutas
```

## Adicionar e remover

Uma lista pode crescer e diminuir enquanto o programa roda.

```safira
lista de frutas recebe "uva", "maçã"

adicione "manga" no final da lista de frutas
remova "uva" da lista de frutas

mostre frutas
```

## Passar por todos os itens

`percorra` faz o bloco rodar uma vez para cada item.

```safira
lista de frutas recebe "uva", "maçã", "manga"

percorra a lista de frutas atribuindo em fruta {
    mostre "Eu gosto de " + fruta
}
```

## Desafio: lista de compras

Crie a lista `compras` com `arroz` e `feijão`. Adicione `leite` no final e mostre cada item em uma linha.

```safira
# Crie a lista aqui.

# Adicione o leite aqui.

# Mostre cada item aqui.

```

```solution
lista de compras recebe "arroz", "feijão"

adicione "leite" no final da lista de compras

percorra a lista de compras atribuindo em item {
    mostre item
}
```

```check
{ "uses": ["listDeclare", "listInsert", "forEach"], "hint": "Use lista de ... recebe, adicione ... no final da lista de ... e percorra a lista de ...", "cases": [{ "shows": ["arroz", "feijão", "leite"] }] }
```
