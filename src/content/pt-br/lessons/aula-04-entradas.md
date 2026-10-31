# Perguntar ao usuário

Um programa fica mais legal quando conversa com quem está usando.

## Ler um texto

`o que o usuário digitar` para o programa e espera. Digite no campo do painel de saída e aperte Enter.

```safira
mostre "Qual é o seu nome?"
nome = o que o usuário digitar

mostre "Olá, " + nome
```

## Ler um número

Para fazer conta com o que foi digitado, peça um número.

```safira
mostre "Digite um número:"
numero = o número que o usuário digitar

dobro = numero * 2
mostre "O dobro é " + dobro
```

## Desafio: o triplo

Peça um número e mostre o triplo dele.

```safira
# Peça um número ao usuário.

# Mostre o número vezes 3.

```

```solution
mostre "Digite um número:"
numero = o número que o usuário digitar

mostre numero * 3
```

```check
{ "uses": ["input"], "hint": "Use numero = o número que o usuário digitar e depois mostre numero * 3.", "cases": [{ "inputs": ["4"], "shows": ["12"] }, { "inputs": ["10"], "shows": ["30"] }] }
```
