# Diario

## Diario

```safira
# Crea un archivo y escribe en él.
crea el archivo "a.txt"
sobrescribir "hola" al archivo "a.txt"

# Lee lo escrito y lo muestra.
texto = lea el archivo "a.txt"
muestra texto
```

## Desafío: Diario

```safira
# Desafío: Crea el archivo diario.
# txt y escribe en él Hoy aprendi Safira.
# Después lee el archivo y muestra lo que dice.

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
