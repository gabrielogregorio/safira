# Semáforo

## Semáforo

```safira
# Repete tudo 2 vezes.
# Apaga a tela, mostra um texto e espera.
repita 2 vezes {
    limpe a tela
    mostre "Olá"
    espere 1 segundo

    limpe a tela
    mostre "Tchau"
    espere 1 segundo
}
```

## Desafio: Semáforo

```safira
# Desafio: Faça um semáforo que repete 2 vezes.
# Mostre Pare por 4 segundos, Siga por 4 segundos e
# Atenção por 2 segundos.
# Apague a tela entre eles.

```

```solution
repita 2 vezes {
    limpe a tela
    mostre "🔴 Pare"
    espere 4 segundos

    limpe a tela
    mostre "🟢 Siga"
    espere 4 segundos

    limpe a tela
    mostre "🟠 Atenção"
    espere 2 segundos
}
```

```check
{"uses": ["repeat|while|forRange", "wait", "clear"], "hint": "Dentro do repita: limpe a tela, mostre e espere, três vezes.", "cases": [{"shows": ["Pare", "Siga", "Atenção"]}]}
```
