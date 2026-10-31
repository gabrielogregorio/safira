# Bem-vindo à Safira

A Safira é uma linguagem de programação em que você escreve quase como fala.

## Seu primeiro programa

Um programa é uma lista de ordens para o computador. Esta tem uma ordem só: mostrar um texto na tela.

Aperte ▶ Executar e veja o resultado ao lado.

```safira
mostre "Olá, mundo!"
```

## Uma ordem depois da outra

A Safira lê de cima para baixo, uma linha de cada vez. Cada `mostre` escreve em uma linha nova.

```safira
mostre "Primeiro"
mostre "Segundo"
mostre "Terceiro"
```

## Comentários

Uma linha que começa com `#` é um comentário. É um recado para quem lê o código, e o computador ignora.

```safira
# Esta linha não aparece na tela.
mostre "Esta aparece!"
```

## Desafio: fale comigo

Faça o programa mostrar o texto `Olá, Safira!`.

```safira
# Escreva o seu código aqui embaixo.

```

```solution
mostre "Olá, Safira!"
```

```check
{ "uses": ["print"], "hint": "Use o comando mostre com o texto entre aspas.", "cases": [{ "shows": ["Olá, Safira!"] }] }
```
