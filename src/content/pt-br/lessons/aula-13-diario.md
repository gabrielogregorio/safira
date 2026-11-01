# Diário

## Diário

```safira
# Cria o arquivo e escreve nele.
crie o arquivo "a.txt"
sobrescreva "oi" no arquivo "a.txt"

# Lê o arquivo.
texto = leia o arquivo "a.txt"
mostre texto
```

## Desafio: Diário

```safira
# Desafio: Crie diario.
# txt, escreva Hoje aprendi Safira nele, leia o arquivo e
# mostre o texto.

```

```solution
crie o arquivo "diario.txt"
sobrescreva "Hoje aprendi Safira" no arquivo "diario.txt"

texto = leia o arquivo "diario.txt"
mostre texto
```

```check
{"uses": ["fileCreate", "fileAppend|fileOverwrite", "fileRead"], "hint": "Crie, sobrescreva, leia e mostre.", "cases": [{"shows": ["Hoje aprendi Safira"]}]}
```
