# Diario

## Diario

```safira
# Crea el archivo y escribe en él.
crea el archivo "a.txt"
sobrescribir "hola" al archivo "a.txt"

# Lee el archivo.
texto = lea el archivo "a.txt"
muestra texto
```

## Desafío: Diario

```safira
# Desafío: Crea diario.
# txt, escribe Hoy aprendi Safira en él, lee el archivo y
# muestra el texto.

```

```solution
crea el archivo "diario.txt"
sobrescribir "Hoy aprendi Safira" al archivo "diario.txt"

texto = lea el archivo "diario.txt"
muestra texto
```

```check
{"uses": ["fileCreate", "fileAppend|fileOverwrite", "fileRead"], "hint": "Crea, sobrescribe, lee y muestra.", "cases": [{"shows": ["Hoy aprendi Safira"]}]}
```
