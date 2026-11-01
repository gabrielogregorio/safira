# Semáforo

## Semáforo

`limpiar la pantalla` borra lo mostrado, y `repetir 2 veces {` repite.

Haz un semáforo que se repite 2 veces: muestra `Alto` por 4 segundos, `Sigue` por 4 segundos y `Atención` por 2 segundos, limpiando la pantalla entre ellos.

```safira
# Escribe aquí.
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
