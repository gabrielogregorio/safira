# Árbol parpadeante

## Árbol parpadeante

`limpiar la pantalla` y `esperar` hacen parpadear cualquier cosa.

```safira
repetir 2 veces {
    limpiar la pantalla
    muestra "⭐"
    esperar 1 segundo

    limpiar la pantalla
    muestra "🌟"
    esperar 1 segundo
}
```

## Desafío: Árbol parpadeante

Haz que el árbol parpadee 3 veces: usa `repetir`, `limpiar la pantalla` y `esperar 1 segundo`, mostrando el árbol encendido y luego apagado.

```safira
muestra "    ⭐"
muestra "   🎄🎄"
muestra "  🎄🔴🎄"
muestra " 🎄🟡🎄🔵"
muestra "    🟫"
muestra "🎅 Feliz Navidad!"
```

```solution
repetir 3 veces {
    limpiar la pantalla
    muestra "    ⭐"
    muestra "   🎄🎄"
    muestra "  🎄🔴🎄"
    muestra " 🎄🟡🎄🔵"
    muestra "    🟫"
    muestra "🎅 Feliz Navidad!"
    esperar 1 segundo

    limpiar la pantalla
    muestra "    ⭐"
    muestra "   🎄🎄"
    muestra "  🎄⚫🎄"
    muestra " 🎄⚫🎄⚫"
    muestra "    🟫"
    muestra "🎅 Feliz Navidad!"
    esperar 1 segundo
}
```

```check
{"uses": ["repeat|while|forRange", "wait", "clear"], "hint": "Pon los dos árboles dentro de repetir, cada uno con limpiar la pantalla y esperar.", "cases": [{"shows": ["Feliz Navidad", "Feliz Navidad"]}]}
```
