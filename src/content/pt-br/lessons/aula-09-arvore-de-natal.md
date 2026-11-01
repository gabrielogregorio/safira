# Árvore piscando

## Árvore piscando

```safira
# Faz a estrela piscar: apaga a tela, mostra e espera.
repita 2 vezes {
    limpe a tela
    mostre "⭐"
    espere 1 segundo

    limpe a tela
    mostre "🌟"
    espere 1 segundo
}
```

## Desafio: Árvore piscando

```safira
# Desafio: Faça a árvore piscar
# 3 vezes.
# Mostre a árvore acesa, espere,
# apague a tela e mostre a
# árvore com as luzes em ⚫.

mostre "    ⭐"
mostre "   🎄🎄"
mostre "  🎄🔴🎄"
mostre " 🎄🟡🎄🔵"
mostre "    🟫"
mostre "🎅 Feliz Natal!"
```

```solution
repita 3 vezes {
    limpe a tela
    mostre "    ⭐"
    mostre "   🎄🎄"
    mostre "  🎄🔴🎄"
    mostre " 🎄🟡🎄🔵"
    mostre "    🟫"
    mostre "🎅 Feliz Natal!"
    espere 1 segundo

    limpe a tela
    mostre "    ⭐"
    mostre "   🎄🎄"
    mostre "  🎄⚫🎄"
    mostre " 🎄⚫🎄⚫"
    mostre "    🟫"
    mostre "🎅 Feliz Natal!"
    espere 1 segundo
}
```

```check
{"uses": ["repeat|while|forRange", "wait", "clear"], "hint": "Coloque as duas árvores dentro do repita, cada uma com limpe a tela e espere.", "cases": [{"shows": ["Feliz Natal", "Feliz Natal"]}]}
```
