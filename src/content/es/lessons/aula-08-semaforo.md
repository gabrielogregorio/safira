# Semáforo

## Semáforo

```safira
# Repite todo 2 veces.
# Borra la pantalla, muestra un texto y espera.
repetir 2 veces {
    limpiar la pantalla
    muestra "Hola"
    esperar 1 segundo

    limpiar la pantalla
    muestra "Adios"
    esperar 1 segundo
}
```

## Desafío: Semáforo

```safira
# Desafío: Haz un semáforo que se repite 2 veces.
# Muestra Alto por 4 segundos, Sigue por 4 segundos y
# Atención por 2 segundos.
# Borra la pantalla entre ellos.

```

```solution
repetir 2 veces {
    limpiar la pantalla
    muestra "🔴 Alto"
    esperar 4 segundos

    limpiar la pantalla
    muestra "🟢 Sigue"
    esperar 4 segundos

    limpiar la pantalla
    muestra "🟠 Atención"
    esperar 2 segundos
}
```

```check
{"uses": ["repeat|while|forRange", "wait", "clear"], "hint": "Dentro de repetir: limpia, muestra y espera, tres veces.", "cases": [{"shows": ["Alto", "Sigue", "Atención"]}]}
```
