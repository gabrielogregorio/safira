# Diario

## Diario

`crea el archivo "a.txt"` crea. `sobrescribir "hola" al archivo "a.txt"` escribe. `lea el archivo "a.txt"` trae el texto.

Crea `diario.txt`, escribe `Hoy aprendi Safira` en él, lee el archivo y muestra el texto.

```safira
# Escribe aquí.
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
