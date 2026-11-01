# Árbol parpadeante

## Árbol parpadeante

```safira
# Hace parpadear la estrella: borra, muestra y espera.
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

```safira
# Desafío: Haz que el árbol
# parpadee 3 veces.
# Muestra el árbol encendido,
# espera, borra la pantalla y
# muestra el árbol con las luces
# en ⚫.

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
