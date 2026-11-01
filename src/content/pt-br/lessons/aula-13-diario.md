# Diário

## Diário

`crie o arquivo "a.txt"` cria. `sobrescreva "oi" no arquivo "a.txt"` escreve. `leia o arquivo "a.txt"` traz o texto.

Crie `diario.txt`, escreva `Hoje aprendi Safira` nele, leia o arquivo e mostre o texto.

```safira
# Escreva aqui.
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
