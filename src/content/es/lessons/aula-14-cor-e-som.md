# Color y sonido

## Color y sonido

```safira
# Muestra un texto en azul.
muestra "¡Hola!" en color azul

# Toca la nota C, que es Do, durante medio segundo.
# Activa el sonido para oírla.
tocar C por 500ms
```

## Desafío: Color y sonido

```safira
# Desafío: Muestra Felicidades en color verde.
# Después toca las notas C, E y G por 300ms.

```

```solution
muestra "Felicidades" en color verde
tocar C, E, G por 300ms
```

```check
{"uses": ["colored", "tone"], "hint": "muestra \"Felicidades\" en color verde y después tocar C, E, G por 300ms", "cases": [{"shows": ["Felicidades"]}]}
```
