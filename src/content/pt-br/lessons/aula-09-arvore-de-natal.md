# Árvore piscando

## Árvore piscando

Sua árvore já está pronta aqui. Para piscar, troque as luzes por ⚫ em uma segunda árvore.

Faça a árvore piscar 3 vezes: use `repita`, `limpe a tela` e `espere 1 segundo`, mostrando a árvore acesa e depois apagada.

```safira
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
