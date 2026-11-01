# Diário

## Diário

```safira
# Cria um arquivo e escreve nele.
crie o arquivo "a.txt"
sobrescreva "oi" no arquivo "a.txt"

# Lê o que foi escrito e mostra na tela.
texto = leia o arquivo "a.txt"
mostre texto
```

## Desafio: Diário

```safira
# Desafio: Crie o arquivo diario.
# txt e escreva nele Hoje aprendi Safira.
# Depois leia o arquivo e mostre o que está escrito.

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
